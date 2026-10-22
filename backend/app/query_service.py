# -*- coding: utf-8 -*-
"""查询编排（UC-03）：检索 → 关系判定 → 有效性解析 → 回答生成 → 持久化。

- 组装 SRS 3.2 的 QueryResult（含实际截止时间与运行配置，NFR-04）；
- 查询结果落库，供事后核查（UC-03 后置：保存可核查的查询结果）；
- gold（qa 表）全程不参与（SRS 3.1）。
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import Any
from uuid import uuid4

from .config import Settings, get_settings
from .database import Database
from .errors import NotFoundError
from .generation.answer import generate_answer
from .llm.client import LLMClient, get_llm_client
from .models import (
    AnswerResult,
    CandidateValidity,
    ConflictResolution,
    MemoryWithScore,
    QueryRequest,
    QueryResult,
    Relation,
)
from .reasoning import relations as relation_judge
from .reasoning.resolution import resolve_conflicts
from .reasoning.validity import resolve_validity
from .retrieval.retriever import Retriever


def _flatten_candidates(candidates: list[MemoryWithScore]) -> list[dict[str, Any]]:
    """MemoryWithScore → 规则/LLM 比较用的扁平字典。"""
    out = []
    for c in candidates:
        m = c.memory
        out.append({
            "memory_id": m.memory_id,
            "score": c.score,
            "content": m.content,
            "entity": m.entity,
            "attribute": m.attribute,
            "value": m.value,
            "session_time": m.session_time,
            "time_expression": m.time_expression,
            "event_time": m.event_time,
            "sources": [s.model_dump() for s in m.sources],
        })
    return out


def _collect_source_meta(
    db: Database,
    conversation_id: str,
    candidates: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """聚合冲突候选的来源轮次元数据（speaker / session_id / turn_no）。

    只查询涉及冲突的记忆，避免对全部候选发起逐条查询。
    """
    turn_ids: set[str] = set()
    for c in candidates:
        for s in c.get("sources", []):
            turn_ids.add(s["turn_id"])
    if not turn_ids:
        return {}

    placeholders = ",".join("?" for _ in turn_ids)
    rows = db.query(
        f"SELECT turn_id, session_id, speaker, turn_no FROM turns "
        f"WHERE conversation_id=? AND turn_id IN ({placeholders})",
        (conversation_id, *sorted(turn_ids)),
    )
    turn_info = {
        r["turn_id"]: {
            "session_id": r["session_id"],
            "speaker": r["speaker"],
            "turn_no": r["turn_no"],
        }
        for r in rows
    }

    meta: dict[str, list[dict[str, Any]]] = {}
    for c in candidates:
        entries = []
        for s in c.get("sources", []):
            info = turn_info.get(s["turn_id"])
            if info:
                entries.append(info)
        meta[c["memory_id"]] = entries
    return meta


def _apply_resolutions(
    validity_items: list[dict[str, Any]],
    resolutions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    """把消解结果回写到有效性：winner → effective，loser → historical。

    返回 (逐条有效性, effective_ids, conflict_ids)。未消解的冲突保持 conflict。
    """
    winners = {r["winner_memory_id"] for r in resolutions
               if r["resolution"] == "resolved" and r.get("winner_memory_id")}
    losers = {r["loser_memory_id"] for r in resolutions
              if r["resolution"] == "resolved" and r.get("loser_memory_id")}

    new_validity: list[dict[str, Any]] = []
    for item in validity_items:
        mid = item["memory_id"]
        if mid in winners:
            new_validity.append({
                "memory_id": mid,
                "status": "effective",
                "reason": "冲突消解后保留的一方，作为当前有效证据",
            })
        elif mid in losers:
            new_validity.append({
                "memory_id": mid,
                "status": "historical",
                "reason": "冲突消解中被判定为不可靠的一方，保留为历史证据",
            })
        else:
            new_validity.append(item)

    effective = [x["memory_id"] for x in new_validity if x["status"] == "effective"]
    conflict = [x["memory_id"] for x in new_validity if x["status"] == "conflict"]
    return new_validity, effective, conflict


def _resolution_note(resolutions: list[dict[str, Any]]) -> str | None:
    resolved = [r for r in resolutions if r["resolution"] == "resolved"]
    if not resolved:
        return None
    methods = {r["method"] for r in resolved}
    label = {
        "turn_order": "轮次自纠",
        "source_authority": "来源可信度",
        "evidence_count": "证据量",
    }
    names = "、".join(label[m] for m in sorted(methods) if m in label)
    return f"本次查询消解了 {len(resolved)} 条冲突（依据：{names}），已按当前有效记忆作答。"


def run_query(
    db: Database,
    req: QueryRequest,
    *,
    settings: Settings | None = None,
    client: LLMClient | None = None,
) -> QueryResult:
    s = settings or get_settings()
    llm = client or get_llm_client(s)
    retriever = Retriever(db)
    top_k = req.top_k or s.retrieval_default_top_k

    # 1. 检索（含 as_of 校验 / 截止过滤，FR-08 / BR-09）
    candidates, effective_cutoff, filtered_count = retriever.retrieve(
        req.conversation_id,
        req.question,
        as_of=req.as_of,
        top_k=top_k,
    )
    flat = _flatten_candidates(candidates)
    query_id = uuid4().hex[:12]

    # 2. 关系判定（FR-09）
    rel_items, used_relation_mode = relation_judge.judge_relations(
        req.question, flat, query_id, settings=s, client=llm,
    )

    # 3. 有效性解析（FR-10）
    validity_items, effective_ids, conflict_ids = resolve_validity(
        flat, rel_items, settings=s,
    )

    # 3.5 冲突消解（Bonus）：对 CONFLICT 尝试确定性消解，再回写有效性
    conflict_relations = [r for r in rel_items if r["type"] == "CONFLICT"]
    conflict_candidates = [c for c in flat if c["memory_id"] in set(conflict_ids)]
    source_meta = _collect_source_meta(db, req.conversation_id, conflict_candidates)
    resolution_items = resolve_conflicts(conflict_relations, flat, source_meta=source_meta)
    if resolution_items:
        validity_items, effective_ids, conflict_ids = _apply_resolutions(
            validity_items, resolution_items,
        )
    resolution_note = _resolution_note(resolution_items)

    effective_flat = [c for c in flat if c["memory_id"] in set(effective_ids)]
    conflict_flat = [c for c in flat if c["memory_id"] in set(conflict_ids)]

    # 4. 回答生成（FR-11）
    answer: AnswerResult = generate_answer(
        llm,
        req.question,
        candidates=flat,
        effective=effective_flat,
        conflict_memories=conflict_flat,
        conflict_relations=conflict_relations,
        settings=s,
        resolution_note=resolution_note,
    )

    result = QueryResult(
        query_id=query_id,
        conversation_id=req.conversation_id,
        question=req.question,
        as_of=req.as_of,
        effective_cutoff=effective_cutoff,
        top_k=top_k,
        candidates=candidates,
        relations=[Relation.model_validate(r) for r in rel_items],
        validity=[CandidateValidity.model_validate(v) for v in validity_items],
        effective_memory_ids=effective_ids,
        conflict_memory_ids=conflict_ids,
        conflict_resolutions=[ConflictResolution.model_validate(r) for r in resolution_items],
        answer=answer,
        run_config={
            "retrieval": "tfidf",
            "relation_mode_configured": s.relation_mode,
            "relation_mode_used": used_relation_mode,
            "llm_provider": s.llm_provider,
            "llm_model": s.llm_model,
            "prompt_versions": {
                "extract": s.extract_prompt_version,
                "relation": s.relation_prompt_version,
                "answer": s.answer_prompt_version,
            },
            "candidate_pool_after_cutoff": filtered_count,
        },
    )

    # 5. 持久化（UC-03 后置）
    with db.transaction():
        db.execute(
            "INSERT INTO query_results (query_id, conversation_id, question, as_of, created_at, result_json) "
            "VALUES (?,?,?,?,?,?)",
            (query_id, req.conversation_id, req.question, req.as_of,
             datetime.now().isoformat(timespec="seconds"),
             result.model_dump_json()),
        )
    return result


def get_query_result(db: Database, query_id: str) -> QueryResult:
    row = db.query_one(
        "SELECT result_json FROM query_results WHERE query_id=?", (query_id,))
    if row is None:
        raise NotFoundError(f"查询结果不存在：{query_id}")
    return QueryResult.model_validate(json.loads(row["result_json"]))
