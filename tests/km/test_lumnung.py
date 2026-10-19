"""Lumnung Khmer release source, packaging and site checks (native host not checked)."""
import hashlib,json,unittest,zipfile
from importlib.util import spec_from_file_location,module_from_spec
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"plugins/kumihan-lumnung"
s=spec_from_file_location("km_checker",BASE/"runtime/checks.py")
checker=module_from_spec(s);s.loader.exec_module(checker)
SKILLS=("kumihan-lumnung","kumihan-lumnung-web","kumihan-lumnung-documents","kumihan-lumnung-review")
class Khmer(unittest.TestCase):
 def test_catalog(self):
  rules=json.loads((BASE/"rules/catalog.json").read_text(encoding="utf-8"))
  fixtures=json.loads((BASE/"fixtures/acceptance.json").read_text(encoding="utf-8"))
  self.assertEqual(len(rules),30);self.assertEqual(len(fixtures),24)
  self.assertEqual({r["id"] for r in rules},{f"KM-{i:02}" for i in range(1,31)})
  self.assertTrue(all(r["auto_fix"] is False and r["description_en"] and r["description_km"] for r in rules))
 def test_metadata(self):
  for rel in ("plugin.json",".claude-plugin/plugin.json",".codex-plugin/plugin.json","gemini-extension.json"):
   meta=json.loads((BASE/rel).read_text(encoding="utf-8"))
   self.assertEqual(meta["version"],"0.1.0")
   self.assertIn(" | ",meta["description"])
   self.assertEqual(meta.get("displayName",meta.get("extensions",{}).get("com.openai",{}).get("interface",{}).get("displayName")),"KUMIHAN｜លំនឹង")
  for slug in SKILLS:
   path=BASE/"skills"/slug
   for rel in ("SKILL.md","agents/openai.yaml","rules/catalog.json","fixtures/acceptance.json","runtime/checks.py","locales/km-KH.json","assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"):
    self.assertTrue((path/rel).is_file(),str(path/rel))
 def test_preservation(self):
  raw="ខ្មែរ សួស្តី".encode()
  self.assertEqual(checker.inspect(raw,"km",raw)["preservation"],"passed")
  self.assertEqual(checker.inspect(raw,"km-KH",b"changed")["preservation"],"failed")
  self.assertEqual(checker.inspect(raw)["coeng_count"],1)
  self.assertEqual(checker.inspect(b"word-break:break-all")["findings"][0]["rule_id"],"KM-09")
  with self.assertRaises(ValueError):checker.inspect(raw,"kh")
 def test_archives(self):
  manifest=json.loads((BASE/"downloads/MANIFEST.json").read_text(encoding="utf-8"))
  self.assertEqual(manifest["product"],"KUMIHAN｜លំនឹង")
  self.assertEqual(len(manifest["packages"]),15)
  for record in manifest["packages"]:
   file=BASE/"downloads"/record["name"]
   self.assertTrue(file.name.endswith("-v0.1.0.zip"))
   self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(),record["sha256"])
   with zipfile.ZipFile(file) as z:self.assertIsNone(z.testzip())
 def test_site(self):
  for lang,ending in (("km",""),("en",".en"),("ja",".ja")):
   page=(ROOT/f"kumihan-km{ending}.html").read_text(encoding="utf-8")
   self.assertIn(f'<html lang="{lang}">',page)
   self.assertIn("KUMIHAN｜លំនឹង",page)
   for host in ("chatgpt","claude","gemini"):
    guide=(ROOT/f"docs/install-lumnung-{host}{ending}.html").read_text(encoding="utf-8")
    self.assertIn("kumihan-lumnung",guide)
    self.assertIn("-v0.1.0.zip",guide)
  self.assertIn('lang="km"',(ROOT/"top-km.html").read_text(encoding="utf-8"))
