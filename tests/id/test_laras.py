"""Laras v0.1.0 lightweight, evidence-bounded acceptance smoke tests."""
import hashlib, json, re, unittest, zipfile
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"plugins/kumihan-laras"
spec=spec_from_file_location("laras_check",BASE/"runtime/checks.py")
checker=module_from_spec(spec);spec.loader.exec_module(checker)
class Laras(unittest.TestCase):
 def test_rules_and_sources(self):
  rules=json.loads((BASE/"rules/catalog.json").read_text(encoding="utf-8"))
  sources=json.loads((BASE/"sources/public-sources.json").read_text(encoding="utf-8"))
  self.assertEqual(len(rules),34)
  self.assertEqual({x["id"] for x in rules},{f"ID-{i:02}" for i in range(1,35)})
  self.assertGreaterEqual(len(sources),60)
  self.assertTrue(all(x["description_id"] and x["description_en"] for x in rules))
  self.assertTrue(all(x["auto_fix"] is False for x in rules))
 def test_research_acceptance(self):
  cases=json.loads((BASE/"fixtures/acceptance.json").read_text(encoding="utf-8"))
  self.assertEqual({x["id"] for x in cases},{f"AT-{i:02}" for i in range(1,21)})
  self.assertEqual({x["status"] for x in cases},{"not-checked"})
 def test_metadata(self):
  for rel in ("plugin.json",".claude-plugin/plugin.json","gemini-extension.json"):
   d=json.loads((BASE/rel).read_text(encoding="utf-8"))
   self.assertEqual(d["name"],"kumihan-laras")
   self.assertEqual(d["version"],"0.1.0")
   self.assertIn(" | ",d["description"])
   self.assertEqual(d["displayName"] if rel!="plugin.json" else d["extensions"]["com.openai"]["interface"]["displayName"],"KUMIHAN｜Laras")
 def test_independent_skills(self):
  for suffix in ("","-web","-documents","-review"):
   d=BASE/"skills"/("kumihan-laras"+suffix)
   for rel in ("SKILL.md","agents/openai.yaml","rules/catalog.json","locales/id-ID.json","sources/public-sources.json","runtime/checks.py","LICENSE","assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"):
    self.assertTrue((d/rel).is_file(),str(d/rel))
 def test_readonly_and_utf8(self):
  text="disimpan di tempat kering · pilihan-pilihan · kami · Rp1.250.000 · 09:30 · ê".encode("utf-8")
  report=checker.inspect(text,"id-ID",candidate=text)
  self.assertEqual(report["preservation"],"passed")
  self.assertEqual(report["source_sha256"],hashlib.sha256(text).hexdigest())
  self.assertEqual(report["rendering"],"not-checked")
  self.assertGreaterEqual(len(report["findings"]),2)
  self.assertEqual(checker.inspect(text,"id",candidate=b"changed")["preservation"],"failed")
  with self.assertRaises(ValueError): checker.inspect(text,"ms-MY")
 def test_dont_overclaim_hyphenation(self):
  p=checker.inspect(b'word-break: break-all; hyphens: auto; lang="in"')
  found={x["rule_id"] for x in p["findings"]}
  self.assertIn("ID-32",found)
  self.assertIn("ID-31",found)
  self.assertEqual(p["native_host"],"not-checked")
 def test_archives(self):
  folder=BASE/"downloads"
  archives=list(folder.glob("*.zip"))
  self.assertEqual(len(archives),15)
  manifest=json.loads((folder/"MANIFEST.json").read_text())
  self.assertEqual(len(manifest["packages"]),15)
  for item in manifest["packages"]:
   self.assertIn("-v0.1.0.zip",item["name"])
   z=folder/item["name"]
   self.assertEqual(hashlib.sha256(z.read_bytes()).hexdigest(),item["sha256"])
   with zipfile.ZipFile(z) as f:
    self.assertIsNone(f.testzip())
    self.assertTrue(any(n.endswith("/SKILL.md") for n in f.namelist()))
 def test_site_and_guides(self):
  for suffix,lang in (("","id"),(".en","en"),(".ja","ja")):
   s=(ROOT/f"kumihan-id{suffix}.html").read_text(encoding="utf-8")
   self.assertIn("KUMIHAN｜Laras",s)
   self.assertIn(f'<html lang="{lang}">',s)
   self.assertIn('class="intro-strip"',s)
   self.assertIn('class="status-section"',s)
   self.assertNotIn("｜Compasso",s)
   for host in ("chatgpt","claude","gemini"):
    guide=(ROOT/f"docs/install-laras-{host}{suffix}.html").read_text(encoding="utf-8")
    self.assertIn("KUMIHAN",guide)
    self.assertIn('class="shell content-layout"',guide)
    self.assertNotIn("compasso",guide.lower())
if __name__=="__main__":unittest.main()
