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
GSPEC=importlib.util.spec_from_file_location('install_guides_builder',ROOT/'tools/build_install_guides.py')
GUIDES=importlib.util.module_from_spec(GSPEC)
GSPEC.loader.exec_module(GUIDES)

NAME='KUMIHAN｜ดุลอักษร'
BASE='https://landco-llc.github.io/kumihan/'
DOWNLOAD='https://github.com/landco-llc/kumihan/releases/download/kumihan-th-v0.1.1/'
SKILLS=('kumihan-th','kumihan-th-web','kumihan-th-documents','kumihan-th-review')
def host_assets(host):
 suffix={'chatgpt':'','claude':'-Claude-skill','gemini':'-Gemini-Apps-skill'}[host]
 package={'chatgpt':'kumihan-th-plugin','claude':'kumihan-th-Claude-Code-plugin','gemini':'kumihan-th-Gemini-CLI-extension'}[host]
 return [package+'-v0.1.1.zip']+[s+suffix+'-v0.1.1.zip' for s in SKILLS]

class Document(HTMLParser):
 def __init__(self,text):
  super().__init__();self.elements=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.elements.append((tag,dict(attrs)))

class ThaiSiteContract(unittest.TestCase):
 def test_generated_output_current(self):
  subprocess.run([sys.executable,str(ROOT/'tools/build_th_site.py'),'--check'],check=True,capture_output=True)
 def check_local_links(self,path,doc):
  for tag,a in doc.elements:
   if tag!='a' or 'href' not in a:continue
   url=urlparse(a['href'])
   if url.scheme:continue
   target=(ROOT/path).parent/url.path if url.path else ROOT/path
   self.assertTrue(target.is_file(),a['href'])
   if url.fragment:
    targetdoc=Document(target.read_text())
    self.assertIn(url.fragment,{a.get('id') for _,a in targetdoc.elements})
 def test_all_localized_pages_and_links(self):
  for lang in SITE.COPY:
   path=SITE.home(lang)
   with self.subTest(path=path):
    text=(ROOT/path).read_text();doc=Document(text)
    self.assertEqual(next(a['lang'] for t,a in doc.elements if t=='html'),lang)
    canon=[a['href'] for t,a in doc.elements if t=='link' and a.get('rel')=='canonical']
    self.assertEqual(canon,[BASE+path])
    self.assertEqual({a['hreflang'] for t,a in doc.elements if t=='link' and a.get('rel')=='alternate'},{'th-TH','en','ja','x-default'})
    self.assertIn(NAME,text)
    self.check_local_links(path,doc)
    self.assertIn('not-checked',text)
  # Guides come from tools/build_install_guides.py: native lang = the landing's <html lang>.
  for host in SITE.HOSTS:
   for lang in SITE.COPY:
    path=SITE.guide(host,lang)
    with self.subTest(path=path):
     self.assertEqual(path,GUIDES.guide_path('th',host,lang))
     text=(ROOT/path).read_text();doc=Document(text)
     self.assertEqual(next(a['lang'] for t,a in doc.elements if t=='html'),lang)
     self.assertNotIn('dir',next(a for t,a in doc.elements if t=='html'))
     canon=[a['href'] for t,a in doc.elements if t=='link' and a.get('rel')=='canonical']
     self.assertEqual(canon,[BASE+path])
     alternates={a['hreflang']:a['href'] for t,a in doc.elements if t=='link' and a.get('rel')=='alternate'}
     self.assertEqual(alternates,{**{l:BASE+SITE.guide(host,l) for l in SITE.COPY},'x-default':BASE+SITE.guide(host,'th')})
     switch={a['href']:a['lang'] for t,a in doc.elements if t=='a' and 'data-language' in a}
     self.assertEqual(switch,{Path(SITE.guide(host,l)).name:l for l in SITE.COPY})
     self.assertIn('<a class="brand" href="../'+SITE.home(lang)+'">KUMIHAN<span class="brand-sub" lang="th">｜ดุลอักษร</span></a>',text)
     self.assertIn(NAME,text)
     self.check_local_links(path,doc)
 def test_exact_assets_and_host_scope(self):
  for host in SITE.HOSTS:
   for lang in SITE.COPY:
    text=(ROOT/SITE.guide(host,lang)).read_text()
    for asset in host_assets(host):
     self.assertIn('href="'+DOWNLOAD+asset+'"',text)
    self.assertIn('href="'+DOWNLOAD+'SHA256SUMS.txt"',text)
    self.assertNotIn('v0.1.7',text)
 def test_release_download_links_use_flat_asset_names(self):
  # GitHub Release assets are a flat namespace, unlike the repo source tree.
  # An extra plugins/, skills/, claude/, or gemini/ segment yields HTTP 404.
  import json
  manifest=json.loads((ROOT/'plugins/kumihan-th/downloads/MANIFEST.json').read_text())
  asset_names={item['release_asset'] for item in manifest['archives']}
  self.assertEqual(len(asset_names),15)
  facts=json.loads((ROOT/'assets/edition-versions.json').read_text())['editions']['th']
  self.assertEqual(facts['release_url'],DOWNLOAD.replace('/download/','/tag/').rstrip('/'))
  self.assertEqual({a['url'] for a in facts['verified_assets']},{DOWNLOAD+n for n in asset_names})
  for host in SITE.HOSTS:
   host_names=set(host_assets(host))
   self.assertEqual(len(host_names),5)
   self.assertTrue(host_names <= asset_names)
   for lang in SITE.COPY:
    with self.subTest(host=host,lang=lang):
     page=Document((ROOT/SITE.guide(host,lang)).read_text())
     links=[a['href'] for tag,a in page.elements
            if tag=='a' and a.get('href','').endswith('.zip')]
     self.assertEqual(len(links),5)
     self.assertEqual(set(links),{DOWNLOAD+name for name in host_names})
     self.assertTrue(all(urlparse(url).path.rsplit('/',1)[-1] in asset_names
                         for url in links))
 def test_no_destructive_typography_hacks(self):
  css=(ROOT/'assets/thai-site.css').read_text().replace(' ','')
  for rule in ['word-break:break-all','overflow:hidden','white-space:nowrap']:
   self.assertNotIn(rule,css)
  for lang in SITE.COPY:
   text=(ROOT/SITE.home(lang)).read_text()
   self.assertNotIn('\u200b',text);self.assertNotIn('\u2060',text)
   for host in SITE.HOSTS:self.assertIn('href="'+SITE.guide(host,lang)+'"',text)
 def test_japanese_landing_uses_canonical_index_structure(self):
  import re
  from html import unescape
  canonical=(ROOT/'_layouts/landing.html').read_text()
  japanese=(ROOT/'kumihan-th-ja.html').read_text()
  sections=lambda text: re.findall(r'<section class="([^"]+)"',text)
  self.assertEqual(sections(japanese),sections(canonical))
  for css_class in ('hero-layout','intro-layout','feature-grid','idea-layout',
                    'skills-grid','install-layout','status-box','cta-layout','kumihan-footer'):
   pattern=r'class="[^"]*\b'+re.escape(css_class)+r'\b[^"]*"'
   self.assertRegex(japanese,pattern)
   if css_class=='kumihan-footer':
    self.assertIn('site.data.site_footer',canonical)  # the layout renders the shared footer
   else:
    self.assertRegex(canonical,pattern)
  self.assertIn('KUMIHAN｜ดุลอักษร',japanese)
  self.assertIn('lang="ja"',japanese)
  self.assertIn('line-break: strict',japanese)
  self.assertIn('releases/tag/kumihan-th-v0.1.1',japanese)
  for match in re.finditer(r'<h([123])\b[^>]*>(.*?)</h\1>',japanese,re.S):
   visible=unescape(re.sub('<[^>]*>','',match.group(2)))
   self.assertNotRegex(visible,r'[、。]',msg=visible)
 def test_thai_landing_uses_canonical_index_without_forced_thai_breaks(self):
  import re
  canonical=(ROOT/'_layouts/landing.html').read_text()
  thai=(ROOT/'kumihan-th.html').read_text()
  sections=lambda text: re.findall(r'<section class="([^"]+)"',text)
  self.assertEqual(sections(thai),sections(canonical))
  for css_class in ('hero-layout','intro-layout','feature-grid','idea-layout',
                    'skills-grid','install-layout','status-box','cta-layout','kumihan-footer'):
   pattern=r'class="[^"]*\b'+re.escape(css_class)+r'\b[^"]*"'
   self.assertRegex(thai,pattern)
  self.assertIn('lang="th"',thai)
  self.assertIn('"Noto Sans Thai"',thai)
  self.assertIn('word-break: normal',thai)
  self.assertIn('.header-nav a { white-space: normal',thai)
  self.assertNotIn('word-break: break-all',thai)
  self.assertIn('href="docs/install-kumihan-th-claude.html"',thai)
  self.assertIn('href="docs/install-kumihan-th-gemini.html"',thai)
 def test_hash_switch_uses_real_anchors(self):
  for lang in SITE.COPY:
   doc=Document((ROOT/SITE.home(lang)).read_text())
   links=[a for t,a in doc.elements if t=='a' and 'data-language' in a]
   self.assertEqual(len(links),3)
   self.assertEqual({a['href'] for a in links},{SITE.home(l) for l in SITE.COPY})
  self.assertIn("window.addEventListener('hashchange', preserveHash)",(ROOT/'assets/thai-site.js').read_text())

if __name__=='__main__':unittest.main()
