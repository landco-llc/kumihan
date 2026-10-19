import importlib.util
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "plugins" / "kumihan-lad"
SPEC = importlib.util.spec_from_file_location("lad_checks", P / "runtime" / "checks.py")
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)

class RussianRules(unittest.TestCase):
    def test_rule_count_and_sources(self):
        d=json.loads((P/"rules/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(d["product"],"KUMIHAN｜Лад")
        self.assertEqual(len(d["rules"]),48)
        self.assertEqual(len({r["id"] for r in d["rules"]}),48)
        self.assertTrue(all(r["auto_fix"] is False for r in d["rules"]))
        self.assertTrue(all(r["conditions_ja"] and r["guidance_ja"] for r in d["rules"]))
        self.assertEqual(sum(r["priority"]=="A" for r in d["rules"]),38)
    def test_proposed_fixtures_not_falsely_executed(self):
        d=json.loads((P/"tests/fixtures.json").read_text(encoding="utf-8"))
        self.assertEqual(len(d["fixtures"]),40)
        self.assertTrue(all(f["origin_status"]=="PROPOSED_NOT_RUN" for f in d["fixtures"]))
    def test_no_silent_unicode_normalization(self):
        raw="ёлка йод за́мок № 7 \u202f«Текст»".encode("utf-8")
        r=CHECK.inspect(raw,locale="ru-RU",candidate=raw)
        self.assertEqual(r["preservation"],"passed")
        self.assertEqual(r["source_sha256"],hashlib.sha256(raw).hexdigest())
        self.assertEqual(r["rendering"],"not-checked")
        self.assertEqual(r["native_host"],"not-checked")
        self.assertEqual(r["language_editor"],"not-checked")
        self.assertEqual(CHECK.inspect(raw,candidate=b"different")["preservation"],"failed")
    def test_look_alikes_and_nbsp_are_advisory(self):
        raw="Семён AВC №\u202f7 5%".encode("utf-8")
        res=CHECK.inspect(raw)
        ids={f["rule_id"] for f in res["findings"]}
        self.assertIn("RU-008",ids)
        self.assertIn("RU-025",ids)
        self.assertIn("RU-006",ids)
    def test_multiple_hosts_and_brand_metadata(self):
        for file in ("plugin.json",".codex-plugin/plugin.json",".claude-plugin/plugin.json","gemini-extension.json"):
            d=json.loads((P/file).read_text(encoding="utf-8"))
            self.assertEqual(d["version"],"0.1.0")
            self.assertEqual(d.get("displayName",d.get("extensions",{}).get("com.openai",{}).get("interface",{}).get("displayName")),"KUMIHAN｜Лад")
            self.assertIn("Русская",d["description"])
            self.assertIn("Russian",d["description"])
    def test_standalone_package_payloads(self):
        sys.path.insert(0,str(ROOT/"tools"))
        import build_lad
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)
            self.assertEqual(build_lad.build(output),15)
            manifest=json.loads((output/"MANIFEST.json").read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["packages"]),15)
            self.assertEqual(manifest["tag"],"kumihan-ru-v0.1.0")
            self.assertEqual(len(list(output.glob("*.zip"))),15)
            for item in manifest["packages"]:
                archive=output/item["name"]
                self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(),item["sha256"])
                with ZipFile(archive) as z:
                    names=z.namelist()
                    self.assertTrue(any(p.endswith("/SKILL.md") for p in names))
                    self.assertTrue(any(p.endswith("/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png") for p in names))
                    self.assertTrue(any(p.endswith("rules/catalog.json") for p in names))

if __name__=="__main__":unittest.main()
