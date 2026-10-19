import json
import re
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import seo_metadata as seo

class MetadataTests(unittest.TestCase):
    def test_root_canonical(self):
        self.assertEqual(seo.canonical_url('index.html'), seo.CONFIG['site_url'])
        self.assertEqual(seo.canonical_url(seo.CONFIG['site_url'] + 'index.html'), seo.CONFIG['site_url'])

    def test_safe_json_and_actual_image(self):
        result = seo.render_metadata('</script><script>bad', 'A & B', 'zh-Hant-TW', seo.canonical_url('test.html'))
        data = json.loads(re.search(r'application/ld\+json">(.*?)</script>', result, re.S)[1])
        self.assertEqual(data['@graph'][-1]['name'], '</script><script>bad')
        self.assertNotIn('</script><script>bad', result)
        self.assertIn('content="1200"', result)
        self.assertIn('content="summary_large_image"', result)
        self.assertIn('content="zh_TW"', result)

    def test_idempotent_and_preserves_body(self):
        html = '<html lang="ar" dir="rtl"><head><title>عنوان</title><meta name="description" content="وصف"><link rel="canonical" href="https://landco-llc.github.io/kumihan/test.html"><meta property="og:title" content="old"></head><body>نص</body></html>'
        result = seo.enrich_html(html, 'test.html')
        self.assertEqual(result, seo.enrich_html(result, 'test.html'))
        self.assertIn('<body>نص</body>', result)
        self.assertEqual(result.count('property="og:title"'), 1)
        self.assertIn('dir="rtl"', result)

    def test_registry_groups_are_separate(self):
        html = '<html lang="fr"><head><title>T</title><meta name="description" content="D"></head></html>'
        product = seo.enrich_html(html, 'kumihan-fr.html')
        self.assertIn('kumihan-fr.en.html', product)
        self.assertNotIn('top-en.html', product)
        gateway = seo.enrich_html(html, 'top-fr.html')
        self.assertIn('top-ja.html', gateway)
        self.assertNotIn('top-en.html', gateway)
        self.assertNotIn('kumihan-fr.en.html', gateway)

    def test_unknown_pages_do_not_guess_translations(self):
        html = '<html lang="en"><head><title>T</title><meta name="description" content="D"></head></html>'
        self.assertNotIn('hreflang=', seo.enrich_html(html, 'docs/new-guide.html'))

if __name__ == '__main__':
    unittest.main()
