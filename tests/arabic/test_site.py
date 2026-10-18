"""Acceptance tests for generated Arabic product pages and acquisition paths."""
import importlib.util
import unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class Tags(HTMLParser):
    def __init__(self,text):
        super().__init__();self.tags=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
class Site(unittest.TestCase):
    def test_twelve_pages_language_navigation_and_real_host_assets(self):
        spec=importlib.util.spec_from_file_location('ar_site',ROOT/'tools/build_ar_site.py')
        self.assertTrue(spec and spec.loader and Path(spec.origin).exists(),'Arabic site generator is missing')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        out=m.outputs();self.assertEqual(len(out),12)
        sections=['hero','intro-strip','features','idea-band','skills-section','install-section','status-section','cta-section']
        for name,body in out.items():
            with self.subTest(page=name):
                self.assertEqual((ROOT/name).read_text(),body)
                t=Tags(body);html=next(a for tag,a in t.tags if tag=='html')
                self.assertEqual(html['dir'],'rtl' if html['lang']=='ar' else 'ltr')
                self.assertEqual({a['hreflang'] for tag,a in t.tags if tag=='link' and a.get('rel')=='alternate'},{'ar','en','ja','x-default'})
                self.assertTrue(any('kumihan-install.css' in a.get('href','') for tag,a in t.tags))
                if not name.startswith('docs/'):
                    classes=[a.get('class','').split()[0] for tag,a in t.tags if tag=='section']
                    self.assertEqual(classes,sections)
                else:
                    zips=[a['href'] for tag,a in t.tags if tag=='a' and a.get('href','').endswith('.zip')]
                    self.assertEqual(len(zips),5 if m.published() else 0)
                    self.assertEqual(len(set(zips)),len(zips))
                    for link in zips:
                        self.assertIn('/releases/download/kumihan-ar-v0.1.0/',link)
                        self.assertTrue((ROOT/'plugins/kumihan-ar/downloads'/link.rsplit('/',1)[1]).is_file())
                for tag,a in t.tags:
                    link=a.get('href','')
                    if link.startswith('/kumihan/') and not link.endswith('/'):
                        path=link.removeprefix('/kumihan/').split('#')[0]
                        if path:self.assertTrue((ROOT/path).is_file(),link)
