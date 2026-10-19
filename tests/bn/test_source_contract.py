"""Bangla skill contract smoke tests. These are not browser or native-language tests."""
import importlib.util,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/"plugins"/"kumihan-bn"
spec=importlib.util.spec_from_file_location("bn_checks",SRC/"runtime"/"checks.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class SourceContract(unittest.TestCase):
 def test_original_same(self):
  raw="কি কো কৌ ক্ষ র‍্য ক্‌ষ অ্যা ড়".encode()
  result=mod.check(raw,raw)
  self.assertEqual(result["status"],"passed")
  self.assertEqual(result["rendering"],"not-checked")
 def test_normalization_not_preservation(self):
  a="ড়".encode()
  b="ড়".encode()
  r=mod.check(a,b)
  self.assertEqual(r["status"],"failed")
  self.assertTrue(r["derived_nfc_equal"])
 def test_joiner_difference(self):
  self.assertEqual(mod.check("র‍্য".encode(),"র্য".encode())["status"],"failed")
 def test_research_counts(self):
  self.assertEqual(len(json.loads((SRC/"rules/catalog.json").read_text())["rules"]),36)
  self.assertEqual(len(json.loads((SRC/"fixtures/qa.json").read_text())["cases"]),60)
 def test_standalone_references(self):
  for suffix in ("","-web","-documents","-review"):
   p=SRC/"skills"/("kumihan-bn"+suffix)
   self.assertTrue((p/"SKILL.md").exists())
   self.assertTrue((p/"references/workflow.md").exists())
   self.assertTrue((p/"assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png").exists())

if __name__=="__main__":unittest.main()
