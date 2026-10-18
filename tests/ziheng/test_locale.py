"""Additive locale selection must never change historical Japanese policy sets."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))

class LocaleTests(unittest.TestCase):
    def setUp(self):
        import locale_resolver
        self.api = locale_resolver

    def test_locale_is_explicit_and_case_insensitive(self):
        for locale in ['zh-Hant-TW', 'ZH-hant-tw', 'zh-hant-HK', 'ja-JP']:
            c = self.api.resolve_context(locale, 'web-editorial')
            self.assertIn(c['locale'], ['zh-Hant-TW', 'zh-Hant-HK', 'ja-JP'])
            self.assertEqual(c['script'], 'Hant' if c['language']=='zh' else 'Jpan')
        for locale in ['zh', 'zh-Hant', 'zh-TW', 'zh-Hans-TW', 'zh-Hant-MO', 'en-US', 'ja', '../ja-JP', 'zh-Hant-TW-x-test', '']:
            with self.subTest(locale=locale), self.assertRaises(ValueError):
                self.api.resolve_context(locale, 'web-editorial')
        with self.assertRaises(ValueError): self.api.resolve_context('ja-JP', '../../unknown')

    def test_historical_japanese_fixture_exact_set(self):
        for p in (ROOT/'skills/kumihan/profiles').glob('*.json'):
            profile = json.loads(p.read_text())
            selected = self.api.resolve_rules(self.api.resolve_context('ja-JP', p.stem), ROOT)
            self.assertEqual([r['id'] for r in selected], profile['rule_ids'])
            self.assertTrue(all('title_ja' in r for r in selected))

if __name__ == '__main__': unittest.main()
