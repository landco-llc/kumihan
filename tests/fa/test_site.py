import unittest
import json
import re
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[2]
class PageTests(unittest.TestCase):
    def test_all_localized_pages_and_alternates(self):
        for lang,suffix in (('fa',''),('en','.en'),('ja','.ja')):
            base='kumihan-fa'+suffix+'.html'
            names=[base]+['docs/install-kumihan-fa-'+host+suffix+'.html' for host in ('chatgpt','claude','gemini')]
            for name in names:
                with self.subTest(name=name):
                    source=(ROOT/name).read_text(encoding='utf-8')
                    self.assertIn('lang="'+lang+'"',source)
                    self.assertEqual(source.count('rel="canonical"'),1)
                    self.assertEqual(source.count('hreflang="x-default"'),1)
                    self.assertIn('KUMIHAN｜تراز',source)
                    self.assertNotIn('kumihan-fa.ar.html',source)
                    self.assertIn('hreflang="fa"',source)
                    self.assertIn('hreflang="en"',source)
                    self.assertIn('hreflang="ja"',source)
                    self.assertIn('v0.1.0',source)
                    if lang=='fa':
                        self.assertIn('dir="rtl"',source)
                        # Vazirmatn comes from this site's copy of the Google Fonts stylesheet.
                        sheets=re.findall(r'href="[^"]*(assets/fonts/google/[0-9a-f]+\.css)',source)
                        self.assertTrue(any('Vazirmatn' in (ROOT/s).read_text(encoding='utf-8') for s in sheets))
                    else:
                        self.assertIn('dir="ltr"',source)
    def test_site_uses_canonical_sections(self):
        p=(ROOT/'kumihan-fa.html').read_text()
        for name in ('hero','intro-strip','features','idea-band','skills-section','install-section','status-section','cta-section'):
            self.assertIn('class="'+name+'"',p)
        self.assertIn('/kumihan/assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png',p)
        self.assertIn('kumihan-fa.css',p)
    def test_host_bundle_names(self):
        for host in ('claude','gemini'):
            p=(ROOT/'docs'/('install-kumihan-fa-'+host+'.html')).read_text()
            self.assertIn('v0.1.0.zip',p)
            self.assertIn('SHA256SUMS',p)
        a=json.loads((ROOT/'plugins/kumihan-fa/downloads/MANIFEST.json').read_text())
        self.assertEqual(len(a['archives']),15)
        self.assertTrue(all(x['sha256'] for x in a['archives']))
if __name__=="__main__":
    unittest.main()
