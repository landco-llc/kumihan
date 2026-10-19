import importlib.util
from pathlib import Path
import unittest
from html.parser import HTMLParser
from urllib.parse import urlsplit
import posixpath
ROOT=Path(__file__).resolve().parents[2]
class SiteTests(unittest.TestCase):
 def test_twelve_pages_languages_downloads_and_alternates(self):
  path=ROOT/'tools/build_satzbild_site.py';self.assertTrue(path.exists(),'Satzbild site generator must exist')
  spec=importlib.util.spec_from_file_location('satzbild_site',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  outputs=m.outputs();self.assertEqual(len(outputs),12)
  for path,text in outputs.items():
   locale='ja' if '.ja.' in path else 'en' if '.en.' in path else 'de'
   self.assertIn(f'<html lang="{locale}">',text)
   for language in ('de','en','ja'):self.assertIn(f'hreflang="{language}"',text)
   self.assertNotIn('hreflang="es-419"',text)
   self.assertIn('KUMIHAN｜Satzbild',text);self.assertIn('<main',text)
   class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
     d=dict(attrs)
     for key in ('href','src'):
      value=d.get(key,'')
      if value and not urlsplit(value).scheme and not value.startswith(('/', '#')):
       target=posixpath.normpath(posixpath.join(posixpath.dirname(path),urlsplit(value).path))
       self_test.assertTrue(target in outputs or (ROOT/target).is_file(),(path,target))
      if value.startswith('/kumihan/'):
       target=value[len('/kumihan/'):].split('#')[0]
       if target:self_test.assertTrue(target in outputs or (ROOT/target).is_file(),(path,target))
   self_test=self;Links().feed(text)
   if path.startswith('docs/'):
    self.assertEqual(text.count('-v0.1.0.zip</a>'),5)
    self.assertIn('SHA256SUMS.txt',text)
