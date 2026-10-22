"""English Measure release site admission: original preservation hashes remain immutable."""
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from en_measure_release_transition import admitted, RECORD, TAG  # noqa: E402
from check_seo_preservation import audit  # noqa: E402


class EnglishReleaseTransition(unittest.TestCase):
    def test_exact_whitelist_and_original_contract(self):
        record = json.loads((ROOT / RECORD).read_text(encoding="utf-8"))
        baseline = json.loads((ROOT / "tests/contracts/release-preservation.json").read_text(encoding="utf-8"))
        self.assertEqual(record["tag"], TAG)
        self.assertEqual(len(record["paths"]), 23)
        for name, row in record["paths"].items():
            self.assertTrue(name in ("README.md", "index.html") or
                            (name.startswith("top-") and name.endswith(".html")), name)
            self.assertEqual(baseline[row["family"]][name], row["before"])
            content = (ROOT / name).read_bytes()
            if row["family"] == "bodies":
                content = re.search(rb"<body\b[\s\S]*", content, re.I)[0]
            self.assertEqual(hashlib.sha256(content).hexdigest(), row["after"])
            self.assertTrue(admitted(ROOT, name, row["before"], content))
            self.assertFalse(admitted(ROOT, name, row["before"], content + b"tampered"))
        self.assertEqual(audit(), [])


if __name__ == "__main__":
    unittest.main()
