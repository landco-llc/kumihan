import importlib.util
from pathlib import Path
import unittest
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[2]
class SiteTests(unittest.TestCase):
 def test_twelve_pages_languages_downloads_and_alternates(self):
  path=ROOT/'tools/build_grafia_site.py';self.assertTrue(path.exists(),'Grafía site generator must exist')
  spec=importlib.util.spec_from_file_location('grafia_site',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  outputs=m.outputs();self.assertEqual(len(outputs),12)
  for path,text in outputs.items():
   locale='ja' if '.ja.' in path else 'en' if '.en.' in path else 'es'
   self.assertIn(f'<html lang="{locale}">',text)
   for language in ('es','en','ja'):self.assertIn(f'hreflang="{language}"',text)
   self.assertNotIn('hreflang="es-419"',text)
   self.assertIn('KUMIHAN｜Grafía',text);self.assertIn('<main',text)
   class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
     d=dict(attrs)
     for key in ('href','src'):
      value=d.get(key,'')
      if value.startswith('/kumihan/'):
       target=value[len('/kumihan/'):].split('#')[0]
       if target:self_test.assertTrue(target in outputs or (ROOT/target).is_file(),(path,target))
   self_test=self;Links().feed(text)
   if path.startswith('docs/'):
    self.assertEqual(text.count('-v0.1.0.zip</a>'),5)
    self.assertIn('SHA256SUMS.txt',text)
