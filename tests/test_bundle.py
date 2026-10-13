"""Synthetic data-only bundle safety tests, independent of product sources."""
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import shutil
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile
from test_report import rule

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SKILLS = ("kumihan", "kumihan-web", "kumihan-documents", "kumihan-review")


def archive(path, version="0.1.0", additions=None):
    files = {}
    for skill in SKILLS:
        content = {"SKILL.md": b"# Synthetic workflow\nRead [guidance](references/guidance.md).\n",
                   "references/guidance.md": b"Original synthetic guidance.\n", "LICENSE": b"Synthetic fixture license.\n"}
        content.update({"schemas/" + path.name: path.read_bytes() for path in (ROOT / "schemas").glob("*.json")})
        schema = json.loads(content["schemas/rule.schema.json"])
        rules = []
        for identity in schema["$defs"]["rule_id"]["enum"]:
            value = rule(); value["id"] = identity; value["media"] = schema["$defs"]["media_profile"]["enum"]
            rules.append(value)
        content["rules/catalog.json"] = json.dumps(rules).encode()
        from test_catalog import registry
        content["sources/public-sources.json"] = json.dumps(registry(rules)).encode()
        for identity in schema["$defs"]["media_profile"]["enum"]:
            content[f"profiles/{identity}.json"] = json.dumps({"id": identity, "revision": 1,
                "title": "Synthetic profile", "description": "Original synthetic selection.",
                "rule_ids": [r["id"] for r in rules], "guidance": ["Observe supplied original text."]}).encode()
        inv = {"format": "kumihan-skill-1", "version": version,
               "files": {name: "sha256:" + hashlib.sha256(data).hexdigest() for name, data in content.items()}}
        content["inventory.json"] = json.dumps(inv, sort_keys=True).encode()
        files.update({f"{skill}/{name}": data for name, data in content.items()})
    files["bundle.json"] = json.dumps({"format": "kumihan-bundle-1", "version": version,
                                      "skills": list(SKILLS)}).encode()
    if additions:
        files.update(additions)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as out:
        for name, data in files.items():
            out.writestr(name, data)
    return path


class BundleTests(unittest.TestCase):
    def setUp(self):
        try:
            self.module = importlib.import_module("scripts.verify_bundle")
        except ImportError:
            self.fail("Frozen verify_bundle callable is not implemented")
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "fixture.zip"

    def test_valid_synthetic_bundle_and_version_binding(self):
        archive(self.path)
        self.assertEqual(self.module.verify_bundle(self.path, "0.1.0"), [])
        self.assertTrue(self.module.verify_bundle(self.path, "0.2.0"))
        self.assertTrue(self.module.verify_bundle(self.path, "../0.1.0"))

    def test_required_frozen_resources_are_checked_offline(self):
        archive(self.path)
        with zipfile.ZipFile(self.path) as bundle:
            files = {name.split("/", 1)[1]: bundle.read(name) for name in bundle.namelist() if name.startswith("kumihan/")}
        for resource in ["schemas/rule.schema.json", "profiles/web-ui.json", "rules/catalog.json", "sources/public-sources.json"]:
            changed = dict(files); del changed[resource]
            inv = json.loads(changed["inventory.json"]); del inv["files"][resource]
            changed["inventory.json"] = json.dumps(inv).encode()
            self.assertTrue(self.module.verify_skill_files(changed, "0.1.0"), resource)
        changed = dict(files); changed["schemas/rule.schema.json"] = b'{"$ref":"https://invalid.example/schema"}'
        inv = json.loads(changed["inventory.json"]); inv["files"]["schemas/rule.schema.json"] = "sha256:" + hashlib.sha256(changed["schemas/rule.schema.json"]).hexdigest()
        changed["inventory.json"] = json.dumps(inv).encode()
        self.assertTrue(self.module.verify_skill_files(changed, "0.1.0"))

    def test_damaged_compressed_member_returns_diagnostic(self):
        archive(self.path)
        with zipfile.ZipFile(self.path) as bundle:
            files = {name: bundle.read(name) for name in bundle.namelist()}
        with zipfile.ZipFile(self.path, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            for name, data in files.items(): bundle.writestr(name, data)
        with zipfile.ZipFile(self.path) as bundle:
            member = bundle.infolist()[0]
            offset = member.header_offset + 30 + len(member.filename.encode()) + len(member.extra)
        data = bytearray(self.path.read_bytes()); data[offset:offset + 6] = b"\xff" * 6
        self.path.write_bytes(data)
        self.assertTrue(self.module.verify_bundle(self.path, "0.1.0"))

    def test_unresolved_listed_sources_fail_even_with_fresh_inventory(self):
        archive(self.path)
        with zipfile.ZipFile(self.path) as bundle:
            files = {name.split("/", 1)[1]: bundle.read(name) for name in bundle.namelist() if name.startswith("kumihan/")}
        files["sources/public-sources.json"] = b'{"registry_version":"0.1.0","sources":[]}'
        inv = json.loads(files["inventory.json"])
        inv["files"]["sources/public-sources.json"] = "sha256:" + hashlib.sha256(files["sources/public-sources.json"]).hexdigest()
        files["inventory.json"] = json.dumps(inv).encode()
        self.assertTrue(self.module.verify_skill_files(files, "0.1.0"))

    def test_extra_resource_roles_and_unreachable_references_are_rejected(self):
        archive(self.path)
        with zipfile.ZipFile(self.path) as bundle:
            files = {name.split("/", 1)[1]: bundle.read(name) for name in bundle.namelist() if name.startswith("kumihan/")}
        for name in ["schemas/extra.schema.json", "rules/extra.json", "profiles/extra.json", "sources/extra.json", "references/unused.md"]:
            with self.subTest(name=name):
                changed = dict(files); changed[name] = b"{}"
                inv = json.loads(changed["inventory.json"]); inv["files"][name] = "sha256:" + hashlib.sha256(changed[name]).hexdigest()
                changed["inventory.json"] = json.dumps(inv).encode()
                self.assertTrue(self.module.verify_skill_files(changed, "0.1.0"))

    def test_path_escapes_case_collisions_unlisted_files_and_logs(self):
        for name in ["../outside", "/absolute", "C:/escape", "C:\\escape", "\\\\host\\share",
                     "kumihan/../other", "kumihan//x", "kumihan/SKILL.MD", "kumihan/raw.log",
                     "kumihan/private.txt", "kumihan/references/font.woff2"]:
            with self.subTest(name=name):
                archive(self.path, additions={name: b"synthetic"})
                self.assertTrue(self.module.verify_bundle(self.path, "0.1.0"))

    def test_duplicate_entries_symlinks_and_nonregular_members(self):
        for mode in [stat.S_IFLNK | 0o777, stat.S_IFIFO | 0o600]:
            archive(self.path)
            info = zipfile.ZipInfo("kumihan/link"); info.create_system = 3; info.external_attr = mode << 16
            with zipfile.ZipFile(self.path, "a") as out: out.writestr(info, b"../outside")
            self.assertTrue(self.module.verify_bundle(self.path, "0.1.0"))
        archive(self.path)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(self.path, "a") as out: out.writestr("kumihan/SKILL.md", b"duplicate")
        self.assertTrue(self.module.verify_bundle(self.path, "0.1.0"))

    def test_missing_stale_references_and_digest_mismatch(self):
        for content in [b"[missing](references/missing.md)", b"[escape](../../outside)",
                        b"[absolute](/etc/passwd)", b"[wrong case](references/Guidance.md)"]:
            archive(self.path, additions={"kumihan/SKILL.md": content})
            self.assertTrue(self.module.verify_bundle(self.path, "0.1.0"))
        archive(self.path, additions={"kumihan/inventory.json": b"{}"})
        self.assertTrue(self.module.verify_bundle(self.path, "0.1.0"))

    def test_bounded_inventory_and_compression(self):
        archive(self.path, additions={"kumihan/large.md": b"x" * (2 * 1024 * 1024 + 1)})
        self.assertTrue(self.module.verify_bundle(self.path, "0.1.0"))

    def test_reference_errors_with_recomputed_inventory_and_isolation(self):
        archive(self.path)
        with zipfile.ZipFile(self.path) as bundle:
            files = {name.split("/", 1)[1]: bundle.read(name) for name in bundle.namelist()
                     if name.startswith("kumihan/")}
        isolated = Path(self.tmp.name) / "unrelated" / "skill"
        for name, content in files.items():
            target = isolated / name; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(content)
        self.assertEqual(self.module.verify_skill_directory(isolated, "0.1.0"), [])
        for target in ["references/missing.md", "../../outside", "/etc/passwd", "C:\\escape", "references/Guidance.md"]:
            changed = dict(files); changed["SKILL.md"] = f"[local]({target})".encode()
            inv = json.loads(changed["inventory.json"])
            inv["files"]["SKILL.md"] = "sha256:" + hashlib.sha256(changed["SKILL.md"]).hexdigest()
            changed["inventory.json"] = json.dumps(inv).encode()
            self.assertIn("bundle: missing, stale or unsafe local reference",
                          self.module.verify_skill_files(changed, "0.1.0"))
        (isolated / "unlisted.md").write_text("Original synthetic extra.")
        self.assertTrue(self.module.verify_skill_directory(isolated, "0.1.0"))

    def test_listed_unsafe_files_and_content_are_not_executed(self):
        marker = Path(self.tmp.name) / "executed"
        archive(self.path, additions={"kumihan/references/run.py": f"open({str(marker)!r}, 'w').write('unsafe')".encode()})
        self.assertTrue(self.module.verify_bundle(self.path, "0.1.0"))
        self.assertFalse(marker.exists())
        archive(self.path)
        with zipfile.ZipFile(self.path) as bundle:
            files = {name.split("/", 1)[1]: bundle.read(name) for name in bundle.namelist() if name.startswith("kumihan/")}
        for name in ["references/raw.log", "references/raw-log.md", "references/transcript.json",
                     "references/maintainer-routing.md", "references/font.woff2", "references/run.py", "references/CON.md"]:
            changed = dict(files); changed[name] = b"synthetic"
            inv = json.loads(changed["inventory.json"]); inv["files"][name] = "sha256:" + hashlib.sha256(changed[name]).hexdigest()
            changed["inventory.json"] = json.dumps(inv).encode()
            self.assertTrue(self.module.verify_skill_files(changed, "0.1.0"))
        with zipfile.ZipFile(self.path, "w", compression=zipfile.ZIP_DEFLATED) as out:
            out.writestr("bomb.md", b"x" * (3 * 1024 * 1024))
        self.assertTrue(self.module.verify_bundle(self.path, "0.1.0"))
        self.path.write_bytes(b"not an archive")
        self.assertTrue(self.module.verify_bundle(self.path, "0.1.0"))
        self.path.unlink()
        self.assertTrue(self.module.verify_bundle(self.path, "0.1.0"))


class BuilderTests(unittest.TestCase):
    def setUp(self):
        try:
            self.module = importlib.import_module("scripts.build_skills")
        except ImportError:
            self.fail("Frozen build_skills callable is not implemented")
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "source"; self.root.mkdir()
        from test_catalog import complete_root
        complete_root(self.root)
        (self.root / "LICENSE").write_text("Original synthetic fixture license.\n")
        for skill in SKILLS:
            path = self.root / "skill-src" / skill / "references"
            path.mkdir(parents=True)
            (path.parent / "SKILL.md").write_text("# Synthetic workflow\nRead [guidance](references/guidance.md).\n")
            (path / "guidance.md").write_text("Original synthetic consumer guidance.\n")

    def test_public_builder_requires_complete_catalog_inputs(self):
        output = Path(self.tmp.name) / "blocked"
        (self.root / "tests/fixtures/priority-cases.json").unlink()
        with self.assertRaisesRegex(ValueError, "missing priority cases"):
            self.module.build_skills(self.root, output, "0.1.0", 1700000000)
        self.assertFalse(output.exists())

    def test_invalid_version_epoch_output_and_no_overwrite(self):
        output = Path(self.tmp.name) / "output"
        for version, epoch in [("../0.1.0", 1700000000), ("0.1.0+meta", 1700000000),
                               ("0.1.0", -1), ("0.1.0", True), ("0.1.0", 999999999999999)]:
            with self.subTest(version=version, epoch=epoch), self.assertRaises(ValueError):
                self.module.build_skills(self.root, output, version, epoch)
            self.assertFalse(output.exists())
        output.mkdir(); (output / "sentinel").write_text("Keep original.")
        with self.assertRaises(ValueError): self.module.build_skills(self.root, output, "0.1.0", 1700000000)
        self.assertEqual((output / "sentinel").read_text(), "Keep original.")
        with self.assertRaises(ValueError): self.module.build_skills(self.root, self.root / "skill-src/kumihan/inside", "0.1.0", 1700000000)

    def test_public_builder_supports_zero_epoch_and_new_dist_inside_root(self):
        archive_path = self.module.build_skills(self.root, self.root / "dist", "0.1.0", 0)
        with zipfile.ZipFile(archive_path) as bundle:
            self.assertEqual(bundle.infolist()[0].date_time, (1980, 1, 1, 0, 0, 0))
            provenance = json.loads(bundle.read("kumihan/references/provenance.json"))
            self.assertEqual(provenance["source_epoch"], 0)

    def test_unreferenced_source_and_restricted_control_data_are_rejected(self):
        extra = self.root / "skill-src/kumihan/references/unused.md"
        extra.write_text("Original synthetic unused prose.")
        with self.assertRaisesRegex(ValueError, "unreferenced"):
            self.module.build_skills(self.root, Path(self.tmp.name) / "unused", "0.1.0", 1700000000)
        extra.unlink()
        entry = self.root / "skill-src/kumihan/SKILL.md"
        entry.write_text("Read [guidance](references/guidance.md) and [context](references/context.json).\n")
        control = extra.with_name("context.json")
        control.write_text('{"approver_ref":"synthetic-principal","state":"current"}')
        with self.assertRaisesRegex(ValueError, "restricted"):
            self.module.build_skills(self.root, Path(self.tmp.name) / "control", "0.1.0", 1700000000)

    def test_public_builder_repeat_bytes_epoch_and_isolated_copy(self):
        # Exercise the frozen public callable using complete original fixtures.
        first = self.module.build_skills(self.root, Path(self.tmp.name) / "one", "0.1.0", 1700000000)
        second = self.module.build_skills(self.root, Path(self.tmp.name) / "two", "0.1.0", 1700000000)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        from scripts.verify_bundle import verify_bundle, verify_skill_directory
        self.assertEqual(verify_bundle(first, "0.1.0"), [])
        with zipfile.ZipFile(first) as bundle:
            self.assertEqual(bundle.namelist(), sorted(bundle.namelist()))
            for member in bundle.infolist():
                self.assertEqual(member.compress_type, zipfile.ZIP_STORED)
                self.assertEqual(member.date_time, (2023, 11, 14, 22, 13, 20))
            unrelated = Path(self.tmp.name) / "unrelated" / "single-skill"
            for name in bundle.namelist():
                if name.startswith("kumihan/"):
                    path = unrelated / name[len("kumihan/"):]
                    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(bundle.read(name))
        shutil.rmtree(self.root)
        self.assertEqual(verify_skill_directory(unrelated, "0.1.0"), [])

    def test_public_builder_rejects_symlinks_logs_unlisted_and_stale_references(self):
        entry = self.root / "skill-src/kumihan/SKILL.md"
        for content in ["[escape](../../outside)", "[missing](references/missing.md)", "<script src='remote'></script>"]:
            entry.write_text(content)
            output = Path(self.tmp.name) / "rejected"
            with self.assertRaises(ValueError):
                self.module.build_skills(self.root, output, "0.1.0", 1700000000)
            self.assertFalse(output.exists())
        entry.write_text("# Synthetic workflow\n")
        extra = entry.parent / "raw.log"; extra.write_text("Synthetic log.")
        with self.assertRaises(ValueError):
            self.module.build_skills(self.root, Path(self.tmp.name) / "log", "0.1.0", 1700000000)
        extra.unlink(); extra.symlink_to(entry)
        with self.assertRaises(ValueError):
            self.module.build_skills(self.root, Path(self.tmp.name) / "link", "0.1.0", 1700000000)


    def test_cli_verified_packaging_content_failures_are_exit_one(self):
        entry = self.root / "skill-src/kumihan/SKILL.md"
        for content in ["Read [missing](references/missing.md).", "Read [guidance](references/guidance.md). <script src='synthetic'></script>"]:
            entry.write_text(content)
            result = subprocess.run([sys.executable, str(ROOT / "scripts/build_skills.py"),
                "--root", str(self.root), "--output-dir", str(Path(self.tmp.name) / "rejected"),
                "--version", "0.1.0", "--source-epoch", "1700000000"], capture_output=True, text=True)
            with self.subTest(content=content):
                self.assertEqual(result.returncode, 1)
                self.assertEqual(json.loads(result.stdout)["status"], "failed")
                self.assertFalse((Path(self.tmp.name) / "rejected").exists())


class CliTests(unittest.TestCase):
    def test_invalid_arguments_emit_one_json_and_exit_two(self):
        for module, arguments in [("validate_catalog", []), ("validate_report", []),
                                  ("build_skills", ["--source-epoch", "not-an-integer"]),
                                  ("verify_bundle", [])]:
            with self.subTest(module=module):
                result = subprocess.run([sys.executable, str(ROOT / f"scripts/{module}.py"), *arguments], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stdout)["status"], "incomplete")
                self.assertNotIn("Traceback", result.stderr)

    def test_builder_verified_content_failure_is_exit_one(self):
        from test_catalog import structural_root
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "source"; root.mkdir()
            values = structural_root(root)
            (root / "rules/catalog.json").write_text(json.dumps(values + [values[0]]))
            result = subprocess.run([sys.executable, str(ROOT / "scripts/build_skills.py"),
                "--root", str(root), "--output-dir", str(Path(directory) / "output"),
                "--version", "0.1.0", "--source-epoch", "1700000000"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)["status"], "failed")

    def test_nonregular_archive_is_rejected_without_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "archive.fifo"; os.mkfifo(path)
            result = subprocess.run([sys.executable, str(ROOT / "scripts/verify_bundle.py"),
                "--archive", str(path), "--expected-version", "0.1.0"], capture_output=True, text=True, timeout=2)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["status"], "incomplete")


if __name__ == "__main__":
    unittest.main()
