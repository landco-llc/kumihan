"""KUMIHAN｜Mizani v0.1.0 product smoke checks (no native-render claims)."""
import hashlib,json,unittest,zipfile
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"plugins/kumihan-mizani"
sp=spec_from_file_location("mizani_checker",BASE/"runtime/checks.py");m=module_from_spec(sp);sp.loader.exec_module(m)
class Mizani(unittest.TestCase):
 def test_rules_and_fixtures(self):
  rules=json.loads((BASE/"rules/catalog.json").read_text())
  tests=json.loads((BASE/"fixtures/acceptance.json").read_text())
  self.assertEqual(len(rules),24);self.assertEqual(len(tests),24)
  self.assertEqual({x["id"] for x in rules},{f"SW-{i:02}" for i in range(1,25)})
  self.assertTrue(all(x["auto_fix"] is False and x["description_sw"] and x["description_en"] for x in rules))
  self.assertTrue(all(x["status"]=="not-checked" for x in tests))
 def test_host_display_and_licenses(self):
  for rel in ("plugin.json",".claude-plugin/plugin.json","gemini-extension.json"):
   obj=json.loads((BASE/rel).read_text())
   self.assertEqual(obj["version"],"0.1.0")
   self.assertIn(" | ",obj["description"])
   self.assertEqual(obj.get("displayName",obj.get("extensions",{}).get("com.openai",{}).get("interface",{}).get("displayName")),"KUMIHAN｜Mizani")
  for suffix in ("","-web","-documents","-review"):
   d=BASE/"skills"/("kumihan-mizani"+suffix)
   for item in ("SKILL.md","agents/openai.yaml","rules/catalog.json","fixtures/acceptance.json","references/web.md","locales/sw-CD.json","assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"):
    self.assertTrue((d/item).is_file(),(d/item).as_posix())
 def test_readonly_and_unicode(self):
  raw="ng’ombe na ng'ombe; saa moja asubuhi".encode()
  self.assertEqual(m.inspect(raw,"sw-TZ",raw)["preservation"],"passed")
  self.assertEqual(m.inspect(raw,"sw-CD",b"modified")["preservation"],"failed")
  self.assertEqual(m.inspect(raw)["source_sha256"],hashlib.sha256(raw).hexdigest())
  self.assertEqual(m.inspect(raw)["rendering"],"not-checked")
  with self.assertRaises(ValueError):m.inspect(raw,"id-ID")
 def test_released_archives(self):
  root=BASE/"downloads";manifest=json.loads((root/"MANIFEST.json").read_text())
  self.assertEqual(len(manifest["packages"]),15)
  for row in manifest["packages"]:
   f=root/row["name"];self.assertTrue(f.name.endswith("-v0.1.0.zip"))
   self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(),row["sha256"])
   with zipfile.ZipFile(f) as z:
    self.assertIsNone(z.testzip());self.assertTrue(any(x.endswith("/SKILL.md") for x in z.namelist()))

 def test_landing_and_install_guides(self):
  from pathlib import Path
  import re
  root=Path(__file__).resolve().parents[2]
  for code,suffix in (("sw",""),("en",".en"),("ja",".ja")):
   path=root/f"kumihan-sw{suffix}.html"
   self.assertTrue(path.is_file(),path)
   html=path.read_text(encoding="utf-8")
   self.assertIn('KUMIHAN｜Mizani',html)
   self.assertIn(f'<html lang="{code}">',html)
   self.assertIn("assets/mizani-site.css",html)
   self.assertIn('lang="',html)
   self.assertNotIn("kumihan-laras",html)
   for host in ("chatgpt","claude","gemini"):
    path=root/f"docs/install-mizani-{host}{suffix}.html"
    self.assertTrue(path.is_file(),path)
    txt=path.read_text(encoding="utf-8")
    self.assertIn("kumihan-mizani",txt)
    self.assertIn("-v0.1.0.zip",txt)
