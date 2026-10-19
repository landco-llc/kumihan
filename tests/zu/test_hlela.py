"""Hlela source and package validation; native host results remain untested."""
import hashlib,json,unittest,zipfile
from importlib.util import spec_from_file_location,module_from_spec
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/"plugins/kumihan-hlela"
s=spec_from_file_location("zu_checker",BASE/"runtime/checks.py");m=module_from_spec(s);s.loader.exec_module(m)
class Hlela(unittest.TestCase):
 def test_rules(self):
  rules=json.loads((BASE/"rules/catalog.json").read_text())
  fixtures=json.loads((BASE/"fixtures/acceptance.json").read_text())
  self.assertEqual(len(rules),24);self.assertEqual(len(fixtures),20)
  self.assertEqual({r["id"] for r in rules},{f"ZU-{i:02}" for i in range(1,25)})
  self.assertTrue(all(r["auto_fix"] is False and r["description_zu"] and r["description_en"] for r in rules))
 def test_skills(self):
  for slug in ("kumihan-hlela","kumihan-hlela-web","kumihan-hlela-documents","kumihan-hlela-review"):
   root=BASE/"skills"/slug
   for name in ("SKILL.md","agents/openai.yaml","assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png","rules/catalog.json","fixtures/acceptance.json","locales/zu-ZA.json","runtime/checks.py"):
    self.assertTrue((root/name).is_file(),str(root/name))
 def test_metadata(self):
  for name in ("plugin.json",".claude-plugin/plugin.json","gemini-extension.json"):
   x=json.loads((BASE/name).read_text())
   self.assertEqual(x["version"],"0.1.0")
   self.assertIn(" | ",x["description"])
   self.assertEqual(x.get("displayName",x.get("extensions",{}).get("com.openai",{}).get("interface",{}).get("displayName")),"KUMIHAN｜Hlela")
 def test_checker(self):
  raw=b"word-break:break-all; hyphens:auto"
  self.assertEqual(m.inspect(raw,"zu",raw)["preservation"],"passed")
  self.assertEqual(m.inspect(raw,"zu-ZA",b"changed")["preservation"],"failed")
  self.assertEqual(m.inspect(raw)["source_sha256"],hashlib.sha256(raw).hexdigest())
  self.assertEqual(m.inspect(raw)["rendering"],"not-checked")
  with self.assertRaises(ValueError):m.inspect(raw,"sw-TZ")
  self.assertIn("ZU-06",{f["rule_id"] for f in m.inspect(raw)["findings"]})
 def test_packages(self):
  root=BASE/"downloads";manifest=json.loads((root/"MANIFEST.json").read_text())
  self.assertEqual(len(manifest["packages"]),15)
  for item in manifest["packages"]:
   zpath=root/item["name"]
   self.assertTrue(zpath.name.endswith("-v0.1.0.zip"))
   self.assertEqual(hashlib.sha256(zpath.read_bytes()).hexdigest(),item["sha256"])
   with zipfile.ZipFile(zpath) as z:self.assertIsNone(z.testzip())
 def test_pages(self):
  for lang,suffix in (("zu",""),("en",".en"),("ja",".ja")):
   html=(ROOT/f"kumihan-zu{suffix}.html").read_text()
   self.assertIn(f'<html lang="{lang}">',html)
   self.assertIn("KUMIHAN｜Hlela",html)
   for host in ("chatgpt","claude","gemini"):
    body=(ROOT/f"docs/install-hlela-{host}{suffix}.html").read_text()
    self.assertIn("kumihan-hlela",body)
    self.assertIn("-v0.1.0.zip",body)
