# -*- coding: utf-8 -*-
"""冲突消解确定性规则单元测试（Bonus：turn_order / source_authority / evidence_count）。"""
from __future__ import annotations

from app.reasoning.resolution import resolve_conflicts


def _cand(mid, entity, value, sources):
    return {
        "memory_id": mid,
        "score": 0.5,
        "content": f"content of {mid}",
        "entity": entity,
        "attribute": "occupation",
        "value": value,
        "session_time": "2024-03-01",
        "event_time": None,
        "time_expression": None,
        "sources": sources,
    }


def _rel(frm, to, rid="rel_1"):
    return {
        "relation_id": rid,
        "from_memory_id": frm,
        "to_memory_id": to,
        "type": "CONFLICT",
        "reason": "r",
        "evidence_memory_ids": [frm, to],
    }


def test_turn_order_self_correction():
    """同一会话内更靠后轮次的自述 → 自我更正，后者胜。"""
    cands = [
        _cand("a", "Alex", "DoorDash", [{"session_id": "1", "turn_id": "D1:2"}]),
        _cand("b", "Alex", "unemployed", [{"session_id": "1", "turn_id": "D1:4"}]),
    ]
    meta = {
        "a": [{"session_id": "1", "speaker": "Alex", "turn_no": 2}],
        "b": [{"session_id": "1", "speaker": "Alex", "turn_no": 4}],
    }
    res = resolve_conflicts([_rel("a", "b")], cands, source_meta=meta)
    assert res[0]["resolution"] == "resolved"
    assert res[0]["winner_memory_id"] == "b"
    assert res[0]["loser_memory_id"] == "a"
    assert res[0]["method"] == "turn_order"


def test_later_turn_not_self_no_turn_order():
    """更靠后的轮次若非自述（他人插话），不按自纠消解。"""
    cands = [
        _cand("a", "Alex", "DoorDash", [{"session_id": "1", "turn_id": "D1:2"}]),
        _cand("b", "Alex", "unemployed", [{"session_id": "1", "turn_id": "D1:4"}]),
    ]
    meta = {
        "a": [{"session_id": "1", "speaker": "Alex", "turn_no": 2}],
        "b": [{"session_id": "1", "speaker": "Jordan", "turn_no": 4}],  # 他人转述
    }
    res = resolve_conflicts([_rel("a", "b")], cands, source_meta=meta)
    # 不满足自纠（后者非自述），转为来源可信度：自述方 a 胜
    assert res[0]["resolution"] == "resolved"
    assert res[0]["winner_memory_id"] == "a"
    assert res[0]["method"] == "source_authority"


def test_source_authority_self_over_hearsay():
    """本人自述优先于他人转述。"""
    cands = [
        _cand("a", "Gina", "DoorDash", [{"session_id": "1", "turn_id": "D1:1"}]),
        _cand("b", "Gina", "store", [{"session_id": "2", "turn_id": "D2:1"}]),
    ]
    meta = {
        "a": [{"session_id": "1", "speaker": "Jon", "turn_no": 1}],    # 转述
        "b": [{"session_id": "2", "speaker": "Gina", "turn_no": 1}],   # 自述
    }
    res = resolve_conflicts([_rel("a", "b")], cands, source_meta=meta)
    assert res[0]["resolution"] == "resolved"
    assert res[0]["winner_memory_id"] == "b"
    assert res[0]["method"] == "source_authority"


def test_evidence_count_more_sources_wins():
    """来源轮次更多的一方更可靠。"""
    cands = [
        _cand("a", "Gina", "DoorDash", [{"session_id": "1", "turn_id": "D1:1"}]),
        _cand("b", "Gina", "store", [
            {"session_id": "2", "turn_id": "D2:1"},
            {"session_id": "3", "turn_id": "D3:1"},
        ]),
    ]
    meta = {
        "a": [{"session_id": "1", "speaker": "Gina", "turn_no": 1}],
        "b": [
            {"session_id": "2", "speaker": "Gina", "turn_no": 1},
            {"session_id": "3", "speaker": "Gina", "turn_no": 1},
        ],
    }
    res = resolve_conflicts([_rel("a", "b")], cands, source_meta=meta)
    assert res[0]["resolution"] == "resolved"
    assert res[0]["winner_memory_id"] == "b"
    assert res[0]["method"] == "evidence_count"


def test_no_basis_unresolved():
    """无消解依据 → unresolved，保留双方（BR-06）。"""
    cands = [
        _cand("a", "Gina", "25", [{"session_id": "1", "turn_id": "D1:1"}]),
        _cand("b", "Gina", "30", [{"session_id": "2", "turn_id": "D2:1"}]),
    ]
    meta = {
        "a": [{"session_id": "1", "speaker": "Gina", "turn_no": 1}],
        "b": [{"session_id": "2", "speaker": "Gina", "turn_no": 1}],
    }
    res = resolve_conflicts([_rel("a", "b")], cands, source_meta=meta)
    assert res[0]["resolution"] == "unresolved"
    assert res[0]["method"] == "none"
    assert res[0]["winner_memory_id"] is None
