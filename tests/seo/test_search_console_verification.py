"""Search Console verification artifacts are not public SEO content pages."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import build_gateways
from seo_inventory import public_paths

FILE = 'google767fc14b71f44ff9.html'
TOKEN = '7TydORMgx59wB9YToKeA0BfSawBSKEpW1Ed7OZGnxaI'


class SearchConsoleVerification(unittest.TestCase):
    def test_exact_verification_file(self):
        self.assertEqual((ROOT / FILE).read_bytes(),
                         b'google-site-verification: google767fc14b71f44ff9.html')
        self.assertNotIn(FILE, [p.name for p in public_paths(ROOT)])

    def test_home_tag_is_generated_only_in_english_head(self):
        pages = build_gateways.outputs()
        self.assertEqual(pages['index.html'].count(TOKEN), 1)
        head, body = pages['index.html'].split('</head>', 1)
        self.assertIn('<meta name="google-site-verification" content="' + TOKEN + '" />', head)
        self.assertNotIn(TOKEN, body)
        for name, source in pages.items():
            if name != 'index.html':
                self.assertNotIn(TOKEN, source, name)

    def test_source_page_matches_generator(self):
        self.assertEqual((ROOT / 'index.html').read_text(encoding='utf-8'),
                         build_gateways.outputs()['index.html'])


if __name__ == '__main__':
    unittest.main()
