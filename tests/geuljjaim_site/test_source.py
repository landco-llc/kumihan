"""Public URL contract and product identity; rendered behavior checked separately."""
import unittest
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
class SourceContract(unittest.TestCase):
 def test_twelve_pages_have_matching_locale_paths(self):
  """3 Jekyll landings + 9 static guides from tools/build_install_guides.py."""
  import re
  site='https://landco-llc.github.io/kumihan'
  for platform in [None,'chatgpt','claude','gemini']:
   group={}
   for loc,suffix,lang in [('ko','','ko-KR'),('en','.en','en'),('ja','.ja','ja')]:
    name=f'docs/install-ko-{platform}{suffix}.html' if platform else f'kumihan-ko{suffix}.html'
    with self.subTest(path=name):
     self.assertTrue((ROOT/name).is_file(),name)
     src=(ROOT/name).read_text()
     if platform is None:
      fm,body=src.split('---',2)[1:]
      meta=yaml.safe_load(fm)
      self.assertEqual(meta['lang'],lang)
      self.assertEqual(meta['layout'],'geuljjaim-index')
      self.assertEqual(meta['canonical_path'],'/'+name)
      paths={l:meta[f'{l}_path'] for l in ('ko','en','ja')}
     else:
      self.assertFalse(src.startswith('---'),'guides are static HTML without front matter')
      body=src
      self.assertEqual(re.search(r'<html lang="([^"]+)"',src).group(1),lang)
      self.assertNotIn('dir="rtl"',src)
      self.assertEqual(re.findall(r'<link rel="canonical" href="([^"]+)"',src),[site+'/'+name])
      alternates=dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"',src))
      self.assertEqual(alternates.pop('x-default'),f'{site}/docs/install-ko-{platform}.html')
      code={'ko-KR':'ko','en':'en','ja':'ja'}
      self.assertEqual(set(alternates),set(code))
      paths={code[h]:u.removeprefix(site) for h,u in alternates.items()}
      switch=re.findall(r'<a href="([^"]+)" lang="([^"]+)" hreflang="[^"]+" data-language',src)
      self.assertEqual(switch,[(f'install-ko-{platform}{s}.html',l) for s,l in (('','ko-KR'),('.en','en'),('.ja','ja'))])
      self.assertIn('<a class="brand" href="../kumihan-ko'+suffix+'.html">KUMIHAN<span class="brand-sub" lang="ko-KR">｜글짜임</span></a>',src)
     self.assertIn('KUMIHAN｜글짜임',body)
     self.assertIn('v0.1.0',body)
     self.assertNotIn('drive.google.com',body)
     self.assertNotIn('<br',body)
     group[loc]=('/'+name,paths)
   for own,paths in group.values():
    self.assertEqual(paths,{loc:other for loc,(other,_) in group.items()},own)
 def test_landing_display_copy_avoids_sentence_punctuation(self):
  """KUMIHAN web-marketing display role; excludes regular body content."""
  import re
  import html
  for suffix in ('','.en','.ja'):
   name=f'kumihan-ko{suffix}.html'
   src=(ROOT/name).read_text()
   fm,body=src.split('---',2)[1:]
   meta=yaml.safe_load(fm)
   headings=[html.unescape(re.sub(r'<[^>]+>','',t)).strip() for t in re.findall(r'<h[12]\b[^>]*>(.*?)</h[12]>',body,re.S)]
   with self.subTest(page=name):
    self.assertEqual(len(headings),7)
    self.assertEqual(meta['title'],headings[0])
    for heading in headings:
     self.assertFalse(any(mark in heading for mark in ('、','。',',','.')),heading)
  for suffix in ('','.en','.ja'):
   s=(ROOT/f'kumihan-ko{suffix}.html').read_text()
   for token in ('hero-layout','intro-strip','feature-grid','idea-band','skills-grid','install-layout','status-box','cta-layout'):
    self.assertIn(token,s)
  design=(ROOT/'assets/geuljjaim-index.css').read_text()
  self.assertIn('.feature-grid',design)
  self.assertIn('.skill-card',design)
  layout=(ROOT/'_layouts/geuljjaim-index.html').read_text()
  self.assertIn("site.data.site_footer", layout)  # shared footer: KUMIHAN top and every edition

  self.assertIn('html[lang="ja"] body',design)
  self.assertIn('html[lang="ja"] .hero h1 .phrase',design)
  self.assertNotIn('@import',design)
  css=(ROOT/'assets/geuljjaim.css').read_text()
  self.assertIn('html[lang="ja"] body{line-break:strict}',css)
  self.assertIn('html[lang="ja"] .hero h1',css)
 def test_assets_are_local_and_no_font_palette(self):
  css=(ROOT/'assets/geuljjaim.css').read_text()
  self.assertIn('prefers-reduced-motion',css)
  self.assertIn(':focus-visible',css)
  self.assertNotIn('@import',css)
  self.assertNotIn('break-all',css)
