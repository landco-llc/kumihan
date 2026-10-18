"""Static contract checks; these do not claim browser/host rendering success."""
import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import unittest
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[2]
SPEC=importlib.util.spec_from_file_location('thai_site_builder',ROOT/'tools/build_th_site.py')
SITE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SITE)

class Document(HTMLParser):
 def __init__(self,text):
  super().__init__();self.elements=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.elements.append((tag,dict(attrs)))

class ThaiSiteContract(unittest.TestCase):
 def test_generated_output_current(self):
  subprocess.run([sys.executable,str(ROOT/'tools/build_th_site.py'),'--check'],check=True,capture_output=True)
 def test_all_localized_pages_and_links(self):
  pages=[SITE.home(l) for l in SITE.COPY]+[SITE.guide(h,l) for h in SITE.HOSTS for l in SITE.COPY]
  for path in pages:
   with self.subTest(path=path):
    text=(ROOT/path).read_text();doc=Document(text)
    expected=next(l for l in SITE.COPY if path==SITE.home(l) or any(path==SITE.guide(h,l) for h in SITE.HOSTS))
    self.assertEqual(next(a['lang'] for t,a in doc.elements if t=='html'),expected)
    canon=[a['href'] for t,a in doc.elements if t=='link' and a.get('rel')=='canonical']
    self.assertEqual(canon,[SITE.BASE+path])
    self.assertEqual({a['hreflang'] for t,a in doc.elements if t=='link' and a.get('rel')=='alternate'},{'th-TH','en','ja','x-default'})
    self.assertIn(SITE.NAME,text)
    ids={a['id'] for _,a in doc.elements if 'id' in a}
    for tag,a in doc.elements:
     if tag!='a' or 'href' not in a:continue
     url=urlparse(a['href'])
     if url.scheme:continue
     target=(ROOT/path).parent/url.path if url.path else ROOT/path
     self.assertTrue(target.is_file(),a['href'])
     if url.fragment:
      targetdoc=Document(target.read_text())
      self.assertIn(url.fragment,{a.get('id') for _,a in targetdoc.elements})
    self.assertIn('not-checked',text)
 def test_exact_assets_and_host_scope(self):
  for host in SITE.HOSTS:
   for lang in SITE.COPY:
    text=(ROOT/SITE.guide(host,lang)).read_text()
    suffix={'chatgpt':'','claude':'-Claude-skill','gemini':'-Gemini-Apps-skill'}[host]
    package={'chatgpt':'kumihan-th-plugin','claude':'kumihan-th-Claude-Code-plugin','gemini':'kumihan-th-Gemini-CLI-extension'}[host]
    for asset in [package+'-v0.1.0.zip']+[s+suffix+'-v0.1.0.zip' for s in SITE.SKILLS]:
     self.assertIn(asset,text)
    self.assertIn('SHA256SUMS.txt',text)
    self.assertIn('น้ำชา เก่ง ภาษาไทย',text)
    self.assertIn('data-copy="sample"',text)
    self.assertNotIn('v0.1.7',text)
 def test_no_destructive_typography_hacks(self):
  css=(ROOT/'assets/thai-site.css').read_text().replace(' ','')
  for rule in ['word-break:break-all','overflow:hidden','white-space:nowrap']:
   self.assertNotIn(rule,css)
  for lang in SITE.COPY:
   text=(ROOT/SITE.home(lang)).read_text()
   self.assertNotIn('\u200b',text);self.assertNotIn('\u2060',text)
   for host in SITE.HOSTS:self.assertIn('href="'+SITE.guide(host,lang)+'"',text)
 def test_hash_switch_uses_real_anchors(self):
  for lang in SITE.COPY:
   doc=Document((ROOT/SITE.home(lang)).read_text())
   links=[a for t,a in doc.elements if t=='a' and 'data-language' in a]
   self.assertEqual(len(links),3)
   self.assertEqual({a['href'] for a in links},{SITE.home(l) for l in SITE.COPY})
  self.assertIn("window.addEventListener('hashchange', preserveHash)",(ROOT/'assets/thai-site.js').read_text())

if __name__=='__main__':unittest.main()
