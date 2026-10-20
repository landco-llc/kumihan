#!/usr/bin/env python3
"""Static consistency only; neither a phrase analyzer nor a renderer."""
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "tests" / "contracts" / "ja-type-011-cases.json"
data = json.loads(path.read_text(encoding="utf-8"))
assert data["rule_proposal"] == "JA-TYPE-011"
assert data["state"] == "active-source-candidate-guidance-only"
ids = set()
for case in data["cases"]:
    assert case["id"] not in ids
    ids.add(case["id"])
    assert case["context"] and case["reason"] and case["text"]
    for field in ("preferred_lines", "less_preferred_lines", "rejected_when_preferred_fits", "fallback_lines"):
        if field not in case:
            continue
        groups = [case[field]] if field == "preferred_lines" else case[field]
        for lines in groups:
            assert lines and all(isinstance(s, str) and s for s in lines)
            assert "".join(lines) == case["text"], (case["id"], field)
main = next(c for c in data["cases"] if c["id"] == "JA-TYPE-011-P01")
assert main["preferred_lines"] == ["いつものAIツールから", "はじめよう"]
assert ["いつもの", "AIツールから", "はじめよう"] in main["less_preferred_lines"]
assert ["いつものAIツールか", "ら", "はじめよう"] in main["rejected_when_preferred_fits"]
print(f"PASS: {len(data['cases'])} spec fixtures are internally consistent (no rendered check)")
