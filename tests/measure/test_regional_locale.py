"""Regional boundaries and source-preservation contract, without rendering claims."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / 'plugins/kumihan-measure'


def load(relative):
    return json.loads((PLUGIN / relative).read_text(encoding='utf-8'))


def checker():
    spec = importlib.util.spec_from_file_location('regional_locale_checker', PLUGIN / 'runtime/check_source.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RegionalLocaleTests(unittest.TestCase):
    def test_coverage_and_fallback_never_promote_advisory_regions(self):
        config = load('locales/supported.json')
        primary = {'en-US', 'en-GB', 'en-CA', 'en-AU', 'en-IN', 'en-SG'}
        advisory = {'en-NZ', 'en-IE', 'en-MY', 'en-PH', 'en-HK', 'en-ZA', 'en-NG', 'en-KE', 'en-GH', 'en-JM'}
        self.assertEqual(primary, set(config['coverage']['supported']))
        self.assertEqual(advisory, set(config['coverage']['advisory']))
        self.assertEqual({'en'} | primary | advisory, set(config['locales']))
        self.assertEqual(17, len(config['locales']))
        for tag in primary | advisory:
            row = load(f'locales/{tag}.json')
            self.assertEqual(tag, row['locale'])
            self.assertEqual('en', row['fallback'])
            self.assertEqual('supported' if tag in primary else 'advisory', row['coverage'])
            self.assertFalse(row['automatic_rewrite'])
            self.assertEqual('not-checked', row['native_rendering'])
            self.assertTrue(row['source_ids'])
            self.assertTrue(all(s.startswith('REG-S') for s in row['source_ids']))
        self.assertIsNone(load('locales/en.json')['fallback'])

    def test_locale_resolution_is_explicit_and_preserves_sensitive_source(self):
        runtime = checker()
        original = 'World Health Organization / AirAsia / Māori / Green Tea（煎茶） / العربية / 03/04/2026 / 12,34,567'.encode()
        for tag in load('locales/supported.json')['locales']:
            with self.subTest(locale=tag):
                result = runtime.review_bytes(original, tag.swapcase())
                self.assertEqual(tag, result['locale'])
                self.assertEqual(original, result['source'].encode())
                self.assertEqual('passed', result['source_integrity']['status'])
                self.assertEqual('not-checked', result['native_rendering'])
                changed = runtime.review_bytes(original, tag, candidate=original.replace('Māori'.encode(), b'Maori'))
                self.assertEqual('failed', changed['source_integrity']['status'])
        for tag in ['und', 'en-XX', 'fr-CA', 'en_US', '', None]:
            self.assertEqual('und', runtime.review_bytes(original, tag)['locale'])
        self.assertEqual('en', runtime.review_bytes(original, 'en')['locale'])

    def test_house_style_requires_organisation_and_matching_scope(self):
        config = load('profiles/house-styles.json')
        self.assertFalse(config['locale_alone_activates_house_style'])
        self.assertEqual('source-preservation-and-edit-permission', config['precedence'][0])
        profiles = {p['id']: p for p in config['profiles']}
        self.assertEqual('-ise', profiles['oxford-university']['conventions']['verb_suffix'])
        self.assertEqual('-ize', profiles['oup-music-and-letters']['conventions']['verb_suffix'])
        self.assertNotEqual(profiles['oxford-university']['scope'], profiles['oup-music-and-letters']['scope'])
        self.assertEqual('sentence case', profiles['microsoft']['conventions']['capitalisation'])
        self.assertEqual(['government-web-ui'], profiles['sgds-current']['scope'])
        self.assertEqual('Inter', profiles['sgds-current']['conventions']['font_example'])
        self.assertEqual('Lato', profiles['sgds-v1']['conventions']['font_example'])
        self.assertIn('centre', profiles['queens-university']['conventions']['spelling_examples'])
        self.assertIn('organize', profiles['queens-university']['conventions']['spelling_examples'])
        for row in profiles.values():
            self.assertFalse(row['automatic_rewrite'])
            self.assertEqual('explicit-house-style-and-matching-scope', row['activation'])
            self.assertTrue(row['version_or_date'])
        r = checker().review_bytes(b'Organize an event', 'en-GB', house_style='Unknown organisation')
        self.assertEqual('Unknown organisation', r['context']['house_style'])
        self.assertEqual('Organize an event', r['source'])


if __name__ == '__main__':
    unittest.main()
