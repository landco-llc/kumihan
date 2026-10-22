"""Exact composition of the separately reviewed ZiHeng and ZiLu source rows.

The original edition transitions stay frozen. This layer accepts only the
combined README and source-version facts, with both parent states recoverable.
It does not admit publication, product, archive, or HTML changes.
"""
import ast
import copy
import hashlib
import json
import re
from pathlib import Path

from ziheng_v022_transition import (
    BASELINE, BASELINE_SHA256, BASE_COMMIT,
    RECORD as SOURCE_RECORD, RECORD_SHA256 as SOURCE_RECORD_SHA256,
)

RECORD = "tests/contracts/ziheng-zilu-source-composition.json"
RECORD_SHA256 = "83c77758c6b48579bc3c38531ffca80ec88f4a36e3fb992eea6b8bbb7f83c7c7"
ZILU_TRANSITION = "tools/zilu_v012_transition.py"
FACTS = "assets/edition-versions.json"
STATES = {"base", "ziheng", "zilu", "combined"}
EDITION_CHANGES = {
    "zh-hant": ("0.2.0", "0.2.2"),
    "zh-hans": ("0.1.0", "0.1.2"),
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _readme_states(data):
    item = data["readme"]
    base = item["base_content"].encode("utf-8")
    if set(item["changes"]) != set(EDITION_CHANGES) or set(item["states"]) != STATES:
        raise ValueError("Unexpected README composition scope")
    changes = {}
    for edition, (old, new) in EDITION_CHANGES.items():
        change = item["changes"][edition]
        before, after = change["before"].encode("utf-8"), change["after"].encode("utf-8")
        label = b"| ZH-HANT |" if edition == "zh-hant" else b"| ZH-HANS |"
        if (not before.startswith(label) or base.count(before) != 1 or
                after != before.replace(("| v" + old + " |").encode(),
                                        ("| v" + new + " |").encode(), 1) or before == after):
            raise ValueError("README permits only each source-version cell")
        changes[edition] = (before, after)
    states = {"base": base}
    for state, editions in (("ziheng", ["zh-hant"]), ("zilu", ["zh-hans"]),
                            ("combined", ["zh-hant", "zh-hans"])):
        raw = base
        for edition in editions:
            raw = raw.replace(*changes[edition], 1)
        states[state] = raw
    for state, raw in states.items():
        if item["states"][state] != {"sha256": sha(raw), "git_blob": git_blob(raw)}:
            raise ValueError("README parent state changed")
    return states


def load_record(root):
    """Verify pinned parents independently of the currently displayed versions."""
    root = Path(root)
    try:
        raw = (root / RECORD).read_bytes()
        if sha(raw) != RECORD_SHA256:
            return None
        data = json.loads(raw)
        source_raw = (root / SOURCE_RECORD).read_bytes()
        baseline_raw = (root / BASELINE).read_bytes()
        # ZiLu may add later, separately reviewed body hashes. Retain its exact
        # original evidence here without freezing the unrelated active helper.
        zilu_raw = data["zilu_transition_preimage"].encode("utf-8")
        if (sha(source_raw) != SOURCE_RECORD_SHA256 or sha(baseline_raw) != BASELINE_SHA256 or
                sha(zilu_raw) != data["zilu_transition_sha256"] or
                data["schema_version"] != 1 or
                data["scope"] != "ziheng-v022-zilu-v012-source-composition" or
                data["base_commit"] != BASE_COMMIT or
                data["source_transition_sha256"] != SOURCE_RECORD_SHA256 or
                set(data["parents"]) != {"ziheng", "zilu"} or
                any(not re.fullmatch(r"[0-9a-f]{40}", value) for value in data["parents"].values())):
            return None
        source = json.loads(source_raw)
        baseline = json.loads(baseline_raw)
        states = _readme_states(data)
        expected_assignment = next(node for node in ast.parse(zilu_raw).body
                                   if isinstance(node, ast.Assign) and
                                   any(isinstance(target, ast.Name) and target.id == "EXPECTED"
                                       for target in node.targets))
        zilu_expected = ast.literal_eval(expected_assignment.value)
        change = source["readme_change"]
        if (data["readme"]["baseline_sha256"] != baseline["protected"]["README.md"] or
                data["readme"]["baseline_sha256"] != source["paths"]["README.md"]["before"] or
                sha(states["base"]) != source["paths"]["README.md"]["preimage_sha256"] or
                sha(states["ziheng"]) != source["paths"]["README.md"]["after"] or
                sha(states["zilu"]) != zilu_expected["README.md"] or
                data["readme"]["changes"]["zh-hant"] != {
                    "before": change["preimage_line"], "after": change["after_line"]} or
                set(data["facts"]["states"]) != STATES or
                any(not re.fullmatch(r"[0-9a-f]{64}", value)
                    for value in data["facts"]["states"].values())):
            return None
        return data
    except (OSError, ValueError, KeyError, TypeError, SyntaxError, StopIteration):
        return None


def readme_state(root, state):
    """Return a retained state, never a reconstructed live-page baseline."""
    if state not in STATES:
        raise ValueError("Unknown source state")
    data = load_record(root)
    if data is None:
        raise ValueError("Invalid source composition record")
    return _readme_states(data)[state]


def ziheng_source_bytes(root, path, family):
    """Keep the original ZiHeng source admission's positive fixture unchanged."""
    raw = readme_state(root, "ziheng") if path == "README.md" else (Path(root) / path).read_bytes()
    if family == "bodies":
        match = re.search(rb"<body\b[\s\S]*", raw, re.I)
        if match is None:
            raise ValueError("Missing HTML body")
        raw = match[0]
    return raw


def admitted(root, path, before, raw, family):
    if path != "README.md" or family != "protected":
        return False
    data = load_record(root)
    return (data is not None and before == data["readme"]["baseline_sha256"] and
            raw == _readme_states(data)["combined"])


def facts_match(root, raw):
    """Reverse just the two source-version fields and recover both exact parents."""
    data = load_record(root)
    if data is None:
        return False
    try:
        facts = json.loads(raw)
        if (sha(raw) != data["facts"]["states"]["combined"] or
                any(facts["editions"][edition]["source_version"] != versions[1]
                    for edition, versions in EDITION_CHANGES.items())):
            return False
        for state, retained in (("base", set()), ("ziheng", {"zh-hant"}),
                                ("zilu", {"zh-hans"}), ("combined", set(EDITION_CHANGES))):
            parent = copy.deepcopy(facts)
            for edition, versions in EDITION_CHANGES.items():
                parent["editions"][edition]["source_version"] = versions[edition in retained]
            if sha(json_bytes(parent)) != data["facts"]["states"][state]:
                return False
        return True
    except (ValueError, KeyError, TypeError):
        return False
