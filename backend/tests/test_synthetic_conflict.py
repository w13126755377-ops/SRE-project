# -*- coding: utf-8 -*-
"""合成受控用例：同一会话内同属性不同值 → CONFLICT（AT-12 / BR-05）。

该 fixture 不是 LoCoMo 真实数据，只用于验证规则和页面展示；
不得把它当作真实数据分布或评测结果。
"""
from __future__ import annotations

from pathlib import Path

from app.config import get_settings
from app.data.importer import import_dataset
from app.memory.builder import create_build_task, run_build_task
from app.models import QueryRequest
from app.query_service import run_query

FIXTURE = Path(__file__).parent / "fixtures" / "synthetic_conflict.json"
CONVERSATION_ID = "synthetic-conflict-01"


def test_synthetic_conflict_end_to_end(db):
    report = import_dataset(
        db,
        str(FIXTURE),
        dataset_version="synthetic",
        settings=get_settings(),
    )
    assert report.imported == [CONVERSATION_ID]

    status = create_build_task(db, CONVERSATION_ID)
    final = run_build_task(db, status.task_id)
    assert final.status == "completed"

    result = run_query(
        db,
        QueryRequest(
            conversation_id=CONVERSATION_ID,
            question="Alex DoorDash job",
            top_k=10,
        ),
        settings=get_settings(),
    )

    assert len(result.candidates) == 2
    assert [relation.type for relation in result.relations] == ["CONFLICT"]

    # 冲突已被「轮次自纠」消解：同一会话内更靠后的失业自述胜出
    assert len(result.conflict_resolutions) == 1
    resolution = result.conflict_resolutions[0]
    assert resolution.resolution == "resolved"
    assert resolution.method == "turn_order"
    assert resolution.winner_memory_id and resolution.loser_memory_id

    by_id = {c.memory.memory_id: c.memory for c in result.candidates}
    winner = by_id[resolution.winner_memory_id]
    loser = by_id[resolution.loser_memory_id]
    assert winner.value == "unemployed"
    assert loser.value == "DoorDash"

    # 消解后：冲突集合清空，有效性变为「一方有效 + 一方历史」，正常作答
    assert result.conflict_memory_ids == []
    assert {item.status for item in result.validity} == {"effective", "historical"}
    assert result.answer.status == "answered"
    assert "lost my job" in (result.answer.text or "")
    assert result.answer.resolution_note
