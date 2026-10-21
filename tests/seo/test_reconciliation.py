"""Current-main regressions: aliases, shared cards, gateway groups and locales."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import seo_metadata as seo
import site_share
import build_gateways
from seo_inventory import Page

class ReconciliationTests(unittest.TestCase):
    def test_allowlisted_alias_without_description(self):
        source = build_gateways.redirect('index.html')
        result = seo.enrich_html(source, 'top-en.html')
        page = Page('top-en.html', result)
        self.assertTrue(page.noindex)
        self.assertEqual(page.canonical, seo.CONFIG['site_url'])
        self.assertEqual(source.split('<body>')[1], result.split('<body>')[1])
        self.assertEqual(result, seo.enrich_html(result, 'top-en.html'))

    def test_missing_description_is_not_an_alias(self):
        source = build_gateways.redirect('index.html')
        with self.assertRaises(ValueError): seo.enrich_html(source, 'other.html')
        with self.assertRaises(ValueError): seo.enrich_html(source.replace('noindex', 'index'), 'top-en.html')

    def test_shared_card_survives_mixed_quotes_and_repeated_enrichment(self):
        html = "<html lang='fa' dir='rtl'><head><title>آزمون</title><meta name='description' content='توضیح'><meta content='old' property='og:title'></head><body>نیم‌فاصله</body></html>"
        result = seo.enrich_html(html, 'fixture.html')
        page = Page('fixture.html', result)
        self.assertEqual(page.meta['og:description'], [site_share.description('fa', 'توضیح')])
        self.assertEqual(page.meta['og:image'], [site_share.IMAGE])
        self.assertEqual(page.meta['twitter:card'], ['summary_large_image'])
        self.assertEqual(page.meta['og:image:width'], ['1200'])
        self.assertEqual(len(page.meta['og:title']), 1)
        self.assertEqual(result, seo.enrich_html(result, 'fixture.html'))
        self.assertEqual(Page('fixture.html', site_share.apply(result)).meta['og:title'], ['آزمون'])

    def test_english_root_and_new_gateway_languages(self):
        source = '<html lang="en"><head><title>T</title><meta name="description" content="D"></head></html>'
        page = Page('index.html', seo.enrich_html(source, 'index.html'))
        alternates = dict(page.alternates)
        self.assertEqual(len(alternates), 29)
        self.assertEqual(alternates['en'], seo.CONFIG['site_url'])
        self.assertEqual(alternates['x-default'], seo.CONFIG['site_url'])
        for lang in ["fa", "km", "zu", "sw", "el", "nl", "ms", "tr", "he", "sa"]: self.assertIn(lang, alternates)

    def test_unknown_share_language_fails(self):
        with self.assertRaises(ValueError): site_share.description('xx', 'Unknown')

    def test_jekyll_data_covers_all_registered_languages(self):
        data = site_share.data()
        for lang in ['fa', 'km', 'zu', 'fr', 'sw', 'zh-Hant-TW', 'ko-KR']:
            self.assertEqual(data[lang]['locale'], site_share.locale(lang))

class PrivacyIntegrationTests(unittest.TestCase):
    def test_privacy_pages_use_shared_seo_and_disjoint_translations(self):
        import build_privacy
        for path, content in build_privacy.outputs().items():
            page = Page(path, content)
            if path == 'privacy-ja.html':
                self.assertTrue(page.noindex)
                self.assertEqual(page.canonical, seo.CONFIG['site_url'] + 'privacy.html')
                self.assertIn('privacy.html#ja', content)
                continue
            self.assertEqual(len(page.graphs), 1)
            self.assertEqual(set(dict(page.alternates)), {'en'})
            self.assertEqual(page.meta['og:url'], [page.canonical])
            self.assertEqual(content.count('class="privacy-language"'), 28)
            self.assertIn('privacy', content)

    def test_privacy_builder_is_checked_by_common_pipeline(self):
        from build_seo import commands
        self.assertTrue(any(Path(cmd[1]).name == 'build_privacy.py' for cmd in commands(True)))
