"""Public URL contract and product identity; rendered behavior checked separately."""
import unittest
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
class SourceContract(unittest.TestCase):
 def test_twelve_pages_have_matching_locale_paths(self):
  for platform in [None,'chatgpt','claude','gemini']:
   group={}
   for loc,suffix,lang in [('ko','','ko-KR'),('en','.en','en'),('ja','.ja','ja')]:
    name=f'docs/install-ko-{platform}{suffix}.html' if platform else f'kumihan-ko{suffix}.html'
    with self.subTest(path=name):
     self.assertTrue((ROOT/name).is_file(),name)
     fm,body=(ROOT/name).read_text().split('---',2)[1:]
     meta=yaml.safe_load(fm)
     self.assertEqual(meta['lang'],lang)
     self.assertEqual(meta['layout'],'geuljjaim')
     self.assertEqual(meta['canonical_path'],'/'+name)
     self.assertIn('KUMIHAN｜글짜임',body)
     self.assertIn('v0.1.0',body)
     self.assertNotIn('drive.google.com',body)
     self.assertNotIn('<br',body)
     group[loc]=(meta,body)
   for meta,body in group.values():
    for loc,(other,_) in group.items(): self.assertEqual(meta[f'{loc}_path'],other['canonical_path'])
 def test_assets_are_local_and_no_font_palette(self):
  css=(ROOT/'assets/geuljjaim.css').read_text()
  self.assertIn('prefers-reduced-motion',css)
  self.assertIn(':focus-visible',css)
  self.assertNotIn('@import',css)
  self.assertNotIn('break-all',css)
