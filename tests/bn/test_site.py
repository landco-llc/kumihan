"""Static checks for Bengali site and the 9 installation guides."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BRAND="KUMIHAN｜অক্ষরসজ্জা"
class SiteContract(unittest.TestCase):
 def test_main_pages(self):
  for code in ("bn","en","ja"):
   name="kumihan-bn"+("" if code=="bn" else "."+code)+".html"
   s=(ROOT/name).read_text("utf-8")
   self.assertIn(f'<html lang="{code}"',s)
   self.assertIn(BRAND,s)
   self.assertIn('assets/bn-site-overrides.css',s)
   self.assertIn('href="#install"',s)
   self.assertIn('rel="canonical"',s)
   self.assertIn('href="https://landco.co.jp/"',s)
   self.assertNotIn("Satzbild",s)
   self.assertNotIn("अक्षर-संगति",s)
 def test_all_guides(self):
  for host in ("chatgpt","claude","gemini"):
   for locale in ("bn","en","ja"):
    p=ROOT/"docs"/("install-kumihan-bn-"+host+("" if locale=="bn" else "."+locale)+".html")
    s=p.read_text("utf-8")
    self.assertIn('<html lang="'+locale+'"',s)
    self.assertIn(BRAND,s)
    self.assertIn("v0.1.0.zip",s)
    for anchor in ('id="format"','id="download"','id="steps"','id="test"','id="updates"','id="limits"'): self.assertIn(anchor,s)
 def test_archive_links(self):
  d=ROOT/"plugins/kumihan-bn/downloads"
  for page in ROOT.glob("kumihan-bn*.html"):
   s=page.read_text("utf-8")
   self.assertIn("docs/install-kumihan-bn-",s)
  for p in (ROOT/"docs").glob("install-kumihan-bn-*.html"):
   s=p.read_text("utf-8")
   import re
   for fn in re.findall(r"downloads/([\w-]+\.zip)",s):
    self.assertTrue((d/fn).is_file(),f"{p.name} -> {fn}")
if __name__=="__main__": unittest.main()
