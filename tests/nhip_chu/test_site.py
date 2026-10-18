from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
class SiteTests(unittest.TestCase):
 def test_pages(self):
  for lang,suffix in (("vi",""),("en",".en"),("ja",".ja")):
   page=(ROOT/f"kumihan-vi{suffix}.html").read_text(encoding="utf-8")
   self.assertIn(f'<html lang="{lang}">',page)
   self.assertIn("KUMIHAN｜Nhịp Chữ",page)
   self.assertIn("assets/nhip-chu-site.css",page)
   for other in ("kumihan-vi.html","kumihan-vi.en.html","kumihan-vi.ja.html"):self.assertIn(other,page)
   for host in ("chatgpt","claude","gemini"):
    path=ROOT/f"docs/install-nhip-chu-{host}{suffix}.html"
    s=path.read_text(encoding="utf-8")
    self.assertIn(f'<html lang="{lang}">',s)
    self.assertIn("SHA256SUMS.txt",s)
    self.assertIn("v0.1.0.zip",s)
    self.assertIn("../assets/kumihan-install.css",s)
 def test_design_policy(self):
  css=(ROOT/"assets/nhip-chu-site.css").read_text(encoding="utf-8")
  self.assertIn("word-break: normal",css)
  self.assertIn("line-height: 1.31",css)
  self.assertNotIn("word-break: break-all",css)
  self.assertIn("Vietnam", (ROOT/"kumihan-vi.en.html").read_text(encoding="utf-8"))
if __name__=="__main__": unittest.main()
