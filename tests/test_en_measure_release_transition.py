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
from ziheng_v022_transition import admitted as ziheng_admitted  # noqa: E402
from ziheng_zilu_source_composition import admitted as composed_admitted  # noqa: E402
from zilu_v012_transition import EXPECTED, BODY_EXPECTED  # noqa: E402


class EnglishReleaseTransition(unittest.TestCase):
    def test_exact_whitelist_and_original_contract(self):
        record = json.loads((ROOT / RECORD).read_text(encoding="utf-8"))
        baseline = json.loads((ROOT / "tests/contracts/release-preservation.json").read_text(encoding="utf-8"))
        self.assertEqual(record["tag"], TAG)
        self.assertEqual(len(record["paths"]), 23)
        later = json.loads((ROOT / "tests/contracts/multilingual-v010-release-transition.json").read_text())["paths"]
        for name, row in record["paths"].items():
            self.assertTrue(name in ("README.md", "index.html") or
                            (name.startswith("top-") and name.endswith(".html")), name)
            self.assertEqual(baseline[row["family"]][name], row["before"])
            content = (ROOT / name).read_bytes()
            if row["family"] == "bodies":
                content = re.search(rb"<body\b[\s\S]*", content, re.I)[0]
            current_hash=hashlib.sha256(content).hexdigest()
            if not (composed_admitted(ROOT, name, row["before"], content, row["family"]) or
                    ziheng_admitted(ROOT, name, row["before"], content, row["family"])):
                zilu = EXPECTED if row["family"] == "protected" else BODY_EXPECTED
                self.assertEqual(current_hash, zilu.get(name, later.get(name, {}).get("after", row["after"])))
            if name not in later:
                self.assertTrue(admitted(ROOT, name, row["before"], content))
            else:
                self.assertEqual(later[name]["before"], row["before"])
            self.assertFalse(admitted(ROOT, name, row["before"], content + b"tampered"))
        self.assertEqual(audit(), [])


if __name__ == "__main__":
    unittest.main()
