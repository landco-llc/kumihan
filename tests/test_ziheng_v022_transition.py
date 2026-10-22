"""Exact Ziheng source admission without rebaselining older releases."""
import copy
import hashlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_seo_preservation import audit  # noqa: E402
from locale_resolver import resolve_context, resolve_rules  # noqa: E402
from ziheng_v022_transition import (  # noqa: E402
    BASELINE, BASELINE_SHA256, BASE_COMMIT, LOCALE_BASELINE,
    LOCALE_BASELINE_SHA256, PROTECTED_PATHS, RECORD, RECORD_SHA256, SITE_BODIES,
    admitted, admitted_locale, allowed,
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":")).encode("utf-8"))


def scoped_bytes(path, family):
    raw = (ROOT / path).read_bytes()
    if family == "bodies":
        raw = re.search(rb"<body\b[\s\S]*", raw, re.I)[0]
    return raw


def write_contract_root(root, record):
    """Only the admission contract and immutable baselines are needed here."""
    for path in (BASELINE, LOCALE_BASELINE):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / path).read_bytes())
    (root / RECORD).write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")


def overlay_file(root, relative_path, raw):
    """Copy one path; symlink siblings without mutating repository files."""
    original, current = ROOT, root
    parts = Path(relative_path).parts
    for part in parts:
        for child in original.iterdir():
            if child.name not in (part, ".git"):
                (current / child.name).symlink_to(child, target_is_directory=child.is_dir())
        original, current = original / part, current / part
        if part != parts[-1]:
            current.mkdir()
    current.write_bytes(raw)


class ZihengV022Transition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((ROOT / RECORD).read_text(encoding="utf-8"))
        cls.baseline = json.loads((ROOT / BASELINE).read_text(encoding="utf-8"))

    def test_frozen_contracts_and_exact_source_scope(self):
        self.assertEqual(sha((ROOT / RECORD).read_bytes()), RECORD_SHA256)
        self.assertEqual(sha((ROOT / BASELINE).read_bytes()), BASELINE_SHA256)
        self.assertEqual(sha((ROOT / LOCALE_BASELINE).read_bytes()), LOCALE_BASELINE_SHA256)
        frozen = {
            "tests/contracts/ja-v020-transition.json":
                "7384581911f63c36b01261d6b79040257ac98b3addfa607d2b30c53f7a2cfb76",
            "tests/contracts/en-measure-v010-transition.json":
                "142b6aea1ecd405a572ce3aaa9c60c362f6a5acde8565c44fc78f83a1595f7c4",
            "tests/contracts/multilingual-v010-release-transition.json":
                "9fdd16190a896f7b84455c0719cb14bd93313267bb8c419b85887ac18a365249",
        }
        for path, expected in frozen.items():
            self.assertEqual(sha((ROOT / path).read_bytes()), expected, path)
        self.assertEqual(self.record["base_commit"], BASE_COMMIT)
        self.assertEqual(len(PROTECTED_PATHS), 98)
        self.assertEqual(len(SITE_BODIES), 12)
        self.assertEqual(set(self.record["paths"]), PROTECTED_PATHS | SITE_BODIES)
        for path, row in self.record["paths"].items():
            with self.subTest(path=path):
                self.assertTrue(allowed(path, row["family"]))
                self.assertEqual(row["before"], self.baseline[row["family"]][path])
                self.assertRegex(row["preimage_sha256"], r"^[0-9a-f]{64}$")
                self.assertNotEqual(row["preimage_sha256"], row["after"])
                self.assertTrue(admitted(ROOT, path, row["before"],
                                         scoped_bytes(path, row["family"]), row["family"]))
        self.assertEqual(audit(), [])

    def test_readme_change_is_one_zh_source_version_cell(self):
        change = self.record["readme_change"]
        self.assertTrue(change["preimage_line"].startswith("| ZH-HANT |"))
        self.assertEqual(change["after_line"], change["preimage_line"].replace(
            "| v0.2.0 |", "| v0.2.2 |", 1))
        self.assertIn("Published **v0.2.0**", change["after_line"])
        raw = (ROOT / "README.md").read_bytes()
        previous = raw.replace(change["after_line"].encode(), change["preimage_line"].encode(), 1)
        self.assertEqual(sha(previous), self.record["paths"]["README.md"]["preimage_sha256"])

    def test_unknown_paths_hashes_and_families_are_rejected(self):
        for path, row in self.record["paths"].items():
            with self.subTest(path=path):
                raw = scoped_bytes(path, row["family"])
                self.assertFalse(admitted(ROOT, path, row["before"], raw + b"tampered", row["family"]))
                self.assertFalse(admitted(ROOT, path, "0" * 64, raw, row["family"]))
                wrong_family = "bodies" if row["family"] == "protected" else "protected"
                self.assertFalse(admitted(ROOT, path, row["before"], raw, wrong_family))
        for path in ("index.html", "top-en.html", "privacy.html", "LICENSE",
                     "plugins/kumihan-zilu/rules/catalog.json",
                     "plugins/kumihan-ziheng/unreviewed.json",
                     "plugins/kumihan-ziheng/downloads/history/0.2.0/MANIFEST.json",
                     "plugins/kumihan-ziheng/downloads/plugins/kumihan-ziheng-0.2.2.zip",
                     "plugins/kumihan-ziheng/../kumihan-zilu/README.md"):
            for family in ("protected", "bodies"):
                self.assertFalse(allowed(path, family), (path, family))
                self.assertFalse(admitted(ROOT, path, "0" * 64, b"candidate", family))

    def test_coordinated_artifact_and_contract_tampering_is_rejected(self):
        name = "plugins/kumihan-ziheng/rules/zh-hant.json"
        row = self.record["paths"][name]
        forged = scoped_bytes(name, row["family"]) + b"tampered"
        tampered = copy.deepcopy(self.record)
        tampered["paths"][name]["after"] = sha(forged)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_contract_root(root, tampered)
            self.assertFalse(admitted(root, name, row["before"], forged, row["family"]))

    def test_changed_preimage_is_rejected_even_with_valid_candidate(self):
        name = "README.md"
        row = self.record["paths"][name]
        tampered = copy.deepcopy(self.record)
        tampered["paths"][name]["preimage_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_contract_root(root, tampered)
            self.assertFalse(admitted(root, name, row["before"], (ROOT / name).read_bytes(), "protected"))

    def test_rebaselined_original_contract_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_contract_root(root, self.record)
            name = "README.md"
            row = self.record["paths"][name]
            self.assertTrue(admitted(root, name, row["before"], (ROOT / name).read_bytes(), "protected"))
            (root / BASELINE).write_bytes((root / BASELINE).read_bytes() + b" ")
            self.assertFalse(admitted(root, name, row["before"], (ROOT / name).read_bytes(), "protected"))

    def test_old_zip_remains_frozen_in_full_preservation_audit(self):
        name = next(path for path in self.baseline["protected"]
                    if path.startswith("plugins/kumihan-ziheng/") and path.endswith(".zip"))
        raw = (ROOT / name).read_bytes()
        before = self.baseline["protected"][name]
        self.assertEqual(sha(raw), before)
        self.assertFalse(admitted(ROOT, name, before, raw, "protected"))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            overlay_file(root, name, raw + b"tampered")
            self.assertIn(f"protected: main bytes changed: {name}", audit(root))

    def test_twelve_explicit_zh_profiles_and_six_unchanged_ja_profiles(self):
        baseline = json.loads((ROOT / LOCALE_BASELINE).read_bytes())
        counts = {True: 0, False: 0}
        for row in baseline["records"]:
            context = resolve_context(row["locale"], row["medium"])
            actual = digest(resolve_rules(context, ROOT))
            context_sha256 = digest(context)
            self.assertEqual(context_sha256, row["context_sha256"])
            is_zh = row["locale"] in ("zh-Hant-TW", "zh-Hant-HK")
            counts[is_zh] += 1
            accepted = admitted_locale(ROOT, row["locale"], row["medium"],
                                       row["rules_sha256"], context_sha256, actual)
            self.assertEqual(accepted, is_zh, row)
            if not is_zh:
                self.assertEqual(actual, row["rules_sha256"])
            else:
                captured = self.record["locale_profiles"][f"{row['locale']}|{row['medium']}"]
                self.assertEqual(captured["before"], row["rules_sha256"])
                self.assertEqual(captured["preimage_sha256"], row["rules_sha256"])
                self.assertEqual(captured["after"], actual)
                for before, context_hash, after in (
                        ("0" * 64, context_sha256, actual),
                        (row["rules_sha256"], "0" * 64, actual),
                        (row["rules_sha256"], context_sha256, "0" * 64)):
                    self.assertFalse(admitted_locale(ROOT, row["locale"], row["medium"],
                                                     before, context_hash, after))
        self.assertEqual(counts, {True: 12, False: 6})
        self.assertFalse(admitted_locale(ROOT, "zh-Hant", "web-ui", "0" * 64, "0" * 64, "0" * 64))
        self.assertFalse(admitted_locale(ROOT, "zh-Hant-TW", "unreviewed", "0" * 64, "0" * 64, "0" * 64))


if __name__ == "__main__":
    unittest.main()
