# -*- coding: utf-8 -*-
"""B5+ · 冲突消解（确定性规则优先，无 LLM 依赖，可独立单测）。

职责：在 CONFLICT 关系判定之后，为每一条冲突尝试找到可解释的消解依据，
决定「该信哪一方」。只在查询级生效，不回写原始 Memory（SRS 3.2）。

消解策略（按优先级，命中即返回）：
- turn_order       同一会话内，更靠后轮次的自述视为「自我更正」（"Actually…"），
                   后者为当前有效，前序自述标记为历史（BR-05 的补强）；
- source_authority 本人自述（speaker == entity）优先于他人转述/传闻；
- evidence_count   来源轮次更多的一方更可靠；
- none             均无依据 → 保留 unresolved，双方并存（BR-06 保守兜底）。

输入 candidate 为扁平字典（见 query_service._flatten_candidates）；
source_meta 为 memory_id → [{session_id, speaker, turn_no}]，由调用方从 turns 表
聚合后传入，本模块不依赖存储层。
"""
from __future__ import annotations

from typing import Any, Optional


def _unresolved(base: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        **base,
        "resolution": "unresolved",
        "winner_memory_id": None,
        "loser_memory_id": None,
        "method": "none",
        "reason": reason,
    }


def _speakers(source_meta: dict[str, list[dict]], memory_id: str) -> list[str]:
    return [m.get("speaker", "") for m in source_meta.get(memory_id, [])]


def _is_self(candidate: dict[str, Any], source_meta: dict[str, list[dict]]) -> bool:
    entity = (candidate.get("entity") or "").strip().lower()
    if not entity:
        return False
    return any(s.strip().lower() == entity for s in _speakers(source_meta, candidate["memory_id"]))


def _sessions(source_meta: dict[str, list[dict]], memory_id: str) -> dict[str, int]:
    """返回 {session_id: 该记忆在该会话内的最大 turn_no}。"""
    by_session: dict[str, int] = {}
    for m in source_meta.get(memory_id, []):
        sid = m.get("session_id")
        no = m.get("turn_no")
        if sid and no is not None:
            by_session[sid] = max(by_session.get(sid, 0), no)
    return by_session


def _turn_order(
    base: dict[str, Any],
    a: dict[str, Any],
    b: dict[str, Any],
    source_meta: dict[str, list[dict]],
) -> Optional[dict[str, Any]]:
    """同会话内更靠后轮次的自述 → 自我更正，后者胜。"""
    sessions_a = _sessions(source_meta, a["memory_id"])
    sessions_b = _sessions(source_meta, b["memory_id"])
    common = set(sessions_a) & set(sessions_b)
    if not common:
        return None
    latest_a = max(sessions_a[s] for s in common)
    latest_b = max(sessions_b[s] for s in common)
    if latest_a == latest_b:
        return None
    later, earlier = (a, b) if latest_a > latest_b else (b, a)
    later_no = max(latest_a, latest_b)
    earlier_no = min(latest_a, latest_b)
    # 仅当「更靠后」的一方是自述时，才视为自我更正
    if not _is_self(later, source_meta):
        return None
    loser = b if later is a else a
    winner_entity = (later.get("entity") or later["memory_id"])
    return {
        **base,
        "resolution": "resolved",
        "winner_memory_id": later["memory_id"],
        "loser_memory_id": loser["memory_id"],
        "method": "turn_order",
        "reason": (
            f"轮次自纠：同一会话内 {winner_entity} 在更靠后的轮次（turn_no {later_no}）"
            f"更正了此前（turn_no {earlier_no}）的陈述，判定后者为当前有效，"
            "前序陈述标记为历史"
        ),
    }


def _source_authority(
    base: dict[str, Any],
    a: dict[str, Any],
    b: dict[str, Any],
    source_meta: dict[str, list[dict]],
) -> Optional[dict[str, Any]]:
    """本人自述优先于他人转述/传闻。"""
    self_a = _is_self(a, source_meta)
    self_b = _is_self(b, source_meta)
    if self_a == self_b:
        return None
    winner, loser = (a, b) if self_a else (b, a)
    we = (winner.get("entity") or winner["memory_id"])
    le = (loser.get("entity") or loser["memory_id"])
    return {
        **base,
        "resolution": "resolved",
        "winner_memory_id": winner["memory_id"],
        "loser_memory_id": loser["memory_id"],
        "method": "source_authority",
        "reason": (
            f"来源可信度：{we} 的本人自述优先于关于 {le} 的他人转述/传闻，"
            "判定自述一方为当前有效，另一方标记为历史"
        ),
    }


def _evidence_count(
    base: dict[str, Any],
    a: dict[str, Any],
    b: dict[str, Any],
    source_meta: dict[str, list[dict]],
) -> Optional[dict[str, Any]]:
    """来源轮次更多的一方更可靠。"""
    n_a = len(source_meta.get(a["memory_id"], []))
    n_b = len(source_meta.get(b["memory_id"], []))
    if n_a == n_b:
        return None
    winner, loser = (a, b) if n_a > n_b else (b, a)
    return {
        **base,
        "resolution": "resolved",
        "winner_memory_id": winner["memory_id"],
        "loser_memory_id": loser["memory_id"],
        "method": "evidence_count",
        "reason": (
            f"证据数量：一方有 {max(n_a, n_b)} 个来源轮次，多于另一方"
            f"（{min(n_a, n_b)} 个），判定证据更充分的一方为当前有效"
        ),
    }


def resolve_conflicts(
    conflict_relations: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    *,
    source_meta: Optional[dict[str, list[dict]]] = None,
) -> list[dict[str, Any]]:
    """为每条 CONFLICT 返回消解结果（不含 Pydantic 包装，由调用方组装）。"""
    by_id = {c["memory_id"]: c for c in candidates}
    meta = source_meta or {}
    return [_resolve_one(rel, by_id, meta) for rel in conflict_relations]


def _resolve_one(
    rel: dict[str, Any],
    by_id: dict[str, dict[str, Any]],
    source_meta: dict[str, list[dict]],
) -> dict[str, Any]:
    base = {
        "relation_id": rel.get("relation_id", ""),
        "from_memory_id": rel["from_memory_id"],
        "to_memory_id": rel["to_memory_id"],
    }
    a = by_id.get(rel["from_memory_id"])
    b = by_id.get(rel["to_memory_id"])
    if a is None or b is None:
        return _unresolved(base, "冲突端点缺失，无法消解，保留双方证据")

    result = (
        _turn_order(base, a, b, source_meta)
        or _source_authority(base, a, b, source_meta)
        or _evidence_count(base, a, b, source_meta)
    )
    if result is not None:
        return result
    return _unresolved(
        base,
        "无充分消解依据（时间相同且来源可信度与证据量相当），保留双方证据待核查（BR-06）",
    )
