"""Both source updates compose without rewriting either frozen admission."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from ziheng_v022_transition import admitted as source_admitted
from ziheng_zilu_source_composition import (
    BASELINE, FACTS, RECORD, RECORD_SHA256, SOURCE_RECORD, SOURCE_RECORD_SHA256,
    ZILU_TRANSITION, admitted, facts_match, json_bytes, load_record, readme_state,
    sha, ziheng_source_bytes,
)


def contract_root(root):
    for path in (BASELINE, SOURCE_RECORD, RECORD):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / path).read_bytes())


class ConcurrentChineseSourceComposition(unittest.TestCase):
    def test_pinned_readme_composition_retains_both_exact_parent_states(self):
        self.assertEqual(sha((ROOT / RECORD).read_bytes()), RECORD_SHA256)
        self.assertEqual(sha((ROOT / SOURCE_RECORD).read_bytes()), SOURCE_RECORD_SHA256)
        data = load_record(ROOT)
        self.assertIsNotNone(data)
        raw = (ROOT / "README.md").read_bytes()
        self.assertEqual(raw, readme_state(ROOT, "combined"))
        self.assertTrue(admitted(ROOT, "README.md", data["readme"]["baseline_sha256"], raw, "protected"))
        for edition, parent in (("zh-hans", "ziheng"), ("zh-hant", "zilu")):
            change = data["readme"]["changes"][edition]
            self.assertEqual(raw.replace(change["after"].encode(), change["before"].encode(), 1),
                             readme_state(ROOT, parent))

    def test_original_ziheng_admission_still_accepts_its_retained_source(self):
        data = json.loads((ROOT / SOURCE_RECORD).read_bytes())
        before = data["paths"]["README.md"]["before"]
        original = ziheng_source_bytes(ROOT, "README.md", "protected")
        self.assertTrue(source_admitted(ROOT, "README.md", before, original, "protected"))
        self.assertFalse(source_admitted(ROOT, "README.md", before,
                                         readme_state(ROOT, "combined"), "protected"))

    def test_facts_are_exactly_two_source_versions_without_publication_changes(self):
        raw = (ROOT / FACTS).read_bytes()
        self.assertTrue(facts_match(ROOT, raw))
        facts = json.loads(raw)
        for edition, key, value in (("zh-hans", "published_version", "0.1.2"),
                                    ("zh-hant", "published_version", "0.2.2"),
                                    ("ja", "source_version", "9.9.9")):
            forged = copy.deepcopy(facts)
            forged["editions"][edition][key] = value
            self.assertFalse(facts_match(ROOT, json_bytes(forged)))
        self.assertFalse(facts_match(ROOT, raw + b" "))

    def test_wrong_path_family_hash_or_original_baseline_is_rejected(self):
        data = load_record(ROOT)
        before = data["readme"]["baseline_sha256"]
        raw = readme_state(ROOT, "combined")
        self.assertFalse(admitted(ROOT, "README.md", "0" * 64, raw, "protected"))
        self.assertFalse(admitted(ROOT, "README.md", before, raw + b"tamper", "protected"))
        self.assertFalse(admitted(ROOT, "README.md", before, raw, "bodies"))
        for path in (FACTS, "index.html", "kumihan-zh-han.html", "kumihan-zh-cn.html",
                     "plugins/kumihan-ziheng/plugin.json", "plugins/kumihan-zilu/plugin.json",
                     "plugins/kumihan-ziheng/downloads/plugins/kumihan-ziheng-0.2.0.zip",
                     "plugins/kumihan-ziheng/downloads/plugins/kumihan-ziheng-0.2.2.zip"):
            self.assertFalse(admitted(ROOT, path, before, raw, "protected"), path)

    def test_pinned_inputs_and_coordinated_record_tampering_are_rejected(self):
        for path in (BASELINE, SOURCE_RECORD, RECORD):
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                contract_root(root)
                self.assertIsNotNone(load_record(root))
                target = root / path
                target.write_bytes(target.read_bytes() + b" ")
                self.assertIsNone(load_record(root))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contract_root(root)
            data = json.loads((root / RECORD).read_bytes())
            data["readme"]["base_content"] += "tampered"
            data["readme"]["states"]["combined"]["sha256"] = sha(b"forged")
            data["zilu_transition_preimage"] += "\n# changed retained evidence\n"
            data["zilu_transition_sha256"] = sha(data["zilu_transition_preimage"].encode())
            (root / RECORD).write_bytes(json_bytes(data))
            self.assertIsNone(load_record(root))

    def test_both_exact_historical_distributions_remain_available(self):
        import version_display
        for code, version, count in (("zh-hant", "0.2.0", 15),
                                     ("zh-hant", "0.1.0", 15),
                                     ("zh-hans", "0.1.0", 15)):
            with self.subTest(edition=code, version=version):
                self.assertEqual(len(version_display.source_archives(code, version)), count)


if __name__ == "__main__":
    unittest.main()
