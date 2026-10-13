"""Original synthetic report boundary cases; no external approval claims."""
import copy
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DIGEST = "sha256:" + "a" * 64


def report():
    return {"report_id": "synthetic-report", "artifact_ref": "artifact.txt",
            "artifact_digest": DIGEST, "ruleset_version": "0.1.0",
            "profile": "web-editorial", "checks": [{"rule_id": "CONTENT-001",
            "status": "passed", "method": "manual", "evidence_refs": ["observed.txt"],
            "scope": "whole", "reason": "Original synthetic observation."}],
            "environment": {"host": "synthetic", "tools": {}, "renderers": []},
            "limitations": ["Structural fixture only."], "content_change_summary": []}


def rule():
    return {"id": "CONTENT-001", "revision": 1, "title_ja": "合成確認",
            "requirement_en": "Compare supplied original text.", "kind": "project-policy",
            "strength": "must", "impact": "error", "media": ["web-editorial"],
            "source_refs": ["policy:synthetic"], "conditions": [],
            "verification": {"method": "manual", "coverage": "planned"},
            "fix_policy": {"mode": "review-only", "protected_content": [], "guidance": "Observe."},
            "exception_policy": {"allowed": True, "bounds": "One exact scope.", "approval_required": True},
            "case_ids": []}


class ReportTests(unittest.TestCase):
    def setUp(self):
        try:
            self.validate = importlib.import_module("scripts.validate_report").validate_report
        except ImportError:
            self.fail("Frozen validate_report callable is not implemented")

    def test_valid_structural_report_does_not_authenticate_evidence(self):
        value = report()
        original = copy.deepcopy(value)
        self.assertEqual(self.validate(value, [rule()]), [])
        self.assertEqual(value, original)

    def test_reject_invalid_shapes_without_coercion(self):
        changes = [("artifact_digest", None), ("extra", "unsafe"), ("ruleset_version", "0.1.0+meta")]
        for key, value in changes:
            with self.subTest(key=key):
                item = report(); item[key] = value
                self.assertTrue(self.validate(item, [rule()]))
        for status in [True, "PASS", "passed ", 1, None]:
            with self.subTest(status=status):
                item = report(); item["checks"][0]["status"] = status
                self.assertTrue(self.validate(item, [rule()]))
                self.assertIs(item["checks"][0]["status"], status)
        for item in [None, [], {}, {"checks": None}]:
            self.assertTrue(self.validate(item, [rule()]))

    def test_all_statuses_remain_distinct(self):
        for status in ["passed", "failed", "needs-review", "not-checked", "unsupported", "not-applicable", "waived"]:
            item = report(); item["checks"][0]["status"] = status
            if status == "waived":
                item["checks"][0]["waiver"] = {"approval_ref": "opaque", "scope": "whole",
                                              "reason": "Bounded synthetic exception.", "artifact_digest": DIGEST}
            self.assertEqual(self.validate(item, [rule()]), [])
            self.assertEqual(item["checks"][0]["status"], status)

    def test_pass_needs_nonblank_evidence_and_method(self):
        for evidence in [[], [" "], None]:
            item = report(); item["checks"][0]["evidence_refs"] = evidence
            self.assertTrue(self.validate(item, [rule()]))
        item = report(); del item["checks"][0]["method"]
        self.assertTrue(self.validate(item, [rule()]))

    def test_diagnostics_do_not_echo_untrusted_keys(self):
        item = report(); item["environment"]["tools"] = {"UNTRUSTED-CONTROL\n": 42}
        self.assertNotIn("UNTRUSTED-CONTROL", " ".join(self.validate(item, [rule()])))

    def test_unimplemented_static_pass_is_rejected(self):
        item = report(); item["checks"][0]["method"] = "static"
        catalog_rule = rule(); catalog_rule["verification"]["method"] = "static"
        self.assertTrue(self.validate(item, [catalog_rule]))

    def test_duplicate_keys_and_catalog_relationships(self):
        item = report(); item["checks"].append(copy.deepcopy(item["checks"][0]))
        self.assertTrue(self.validate(item, [rule()]))
        item["checks"][1]["scope"] = "section-2"
        self.assertEqual(self.validate(item, [rule()]), [])
        self.assertTrue(self.validate(report(), []))
        self.assertTrue(self.validate(report(), [rule(), rule()]))
        item = report(); item["checks"][0]["method"] = "static"
        self.assertTrue(self.validate(item, [rule()]))

    def test_wrong_artifact_scope_and_disallowed_waiver(self):
        item = report(); check = item["checks"][0]; check["status"] = "waived"
        check["waiver"] = {"approval_ref": "opaque", "scope": "whole", "reason": "Synthetic exception.", "artifact_digest": DIGEST}
        for key, value in [("scope", "elsewhere"), ("artifact_digest", "sha256:" + "b" * 64)]:
            bad = copy.deepcopy(item); bad["checks"][0]["waiver"][key] = value
            self.assertTrue(self.validate(bad, [rule()]))
        disallowed = rule(); disallowed["exception_policy"]["allowed"] = False
        self.assertTrue(self.validate(item, [disallowed]))
        check["status"] = "passed"
        self.assertTrue(self.validate(item, [rule()]))

    def test_local_evidence_missing_wrong_artifact_and_untrusted_waiver_fail_closed(self):
        from scripts.validate_report import local_evidence_errors
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); value = report()
            self.assertIn("report: missing or unsafe local artifact/evidence", local_evidence_errors(root, value))
            (root / "artifact.txt").write_bytes(b"Original synthetic target.\n")
            (root / "observed.txt").write_bytes(b"Original synthetic observation.\n")
            self.assertIn("report: local artifact digest mismatch", local_evidence_errors(root, value))
            value["artifact_digest"] = "sha256:" + hashlib.sha256((root / "artifact.txt").read_bytes()).hexdigest()
            self.assertIn("report: evidence relevance and observed method authentication unavailable", local_evidence_errors(root, value))
            value["checks"][0]["status"] = "waived"
            self.assertIn("report: trusted approval lookup/authority/time/latest-state context unavailable", local_evidence_errors(root, value))
            for path in ["../outside", "/etc/passwd", "C:\\escape", "\\\\host\\share"]:
                value["checks"][0]["evidence_refs"] = [path]
                self.assertIn("report: missing or unsafe local artifact/evidence", local_evidence_errors(root, value))
            (root / "alias").symlink_to(root / "observed.txt")
            value["checks"][0]["evidence_refs"] = ["alias"]
            self.assertIn("report: missing or unsafe local artifact/evidence", local_evidence_errors(root, value))

    def test_cli_complete_fixture_context_keeps_admission_limits_and_exits(self):
        from test_catalog import complete_root
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); complete_root(root)
            artifact = b"Original synthetic target.\n"
            (root / "artifact.txt").write_bytes(artifact)
            (root / "observed.txt").write_text("Original synthetic observation.\n")
            value = report(); value["artifact_digest"] = "sha256:" + hashlib.sha256(artifact).hexdigest()
            path = root / "report.json"
            for status, expected in [("not-checked", 0), ("failed", 1), ("passed", 2), ("waived", 2)]:
                value["checks"][0]["status"] = status
                if status == "waived":
                    value["checks"][0]["waiver"] = {"approval_ref": "synthetic-unverified", "scope": "whole", "reason": "Synthetic request.", "artifact_digest": value["artifact_digest"]}
                path.write_text(json.dumps(value))
                result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_report.py"), "--root", str(root), "--report", str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stdout)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(json.loads(path.read_text())["checks"][0]["status"], status)


if __name__ == "__main__":
    unittest.main()
