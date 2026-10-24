"""Behavioral negative cases for the source-preserving regional review contract."""
import importlib.util
import json
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / 'plugins/kumihan-measure'
spec = importlib.util.spec_from_file_location('regional_semantics', PLUGIN / 'runtime/check_source.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class RegionalSemanticsTests(unittest.TestCase):
    def test_protected_spans_survive_every_permission(self):
        source = 'World Health Organization / AirAsia / "colour" / `organise()` / ID-colour-01 / $1,234.50 / te reo Māori / Green Tea（煎茶） / العربية'
        for locale in ('en', 'en-US', 'en-GB'):
            for permission in ('immutable', 'suggestions', 'rewrite-authorized'):
                with self.subTest(locale=locale, permission=permission):
                    report = checker.review_bytes(source.encode(), locale, text_permission=permission)
                    self.assertEqual(source, report['source'])
                    self.assertEqual('passed', report['source_integrity']['status'])
                    self.assertEqual([], report['annotations'])
                    self.assertEqual('not-checked', report['native_rendering'])
                    altered = source.replace('World Health Organization', 'World Health Organisation').encode()
                    self.assertEqual('failed', checker.review_bytes(source.encode(), locale, candidate=altered, text_permission=permission)['source_integrity']['status'])

    def test_regional_meanings_never_become_replacements(self):
        for source in ('We will table this motion.', 'Can we prepone the meeting?', 'Where is the CR?', 'Turn at the robot.', 'That is grand.', 'A takeaway from this report.'):
            for locale in ('en-US', 'en-GB'):
                report = checker.review_bytes(source.encode(), locale)
                notices = [d for d in report['diagnostics'] if d['code'] == 'regional-meaning-review']
                self.assertEqual(1, len(notices))
                self.assertEqual('needs-review', notices[0]['status'])
                self.assertEqual(source, report['source'])
                self.assertEqual([], report['annotations'])
        report = checker.review_bytes(b'A neutral sentence.', 'en-US')
        self.assertNotIn('regional-meaning-review', [d['code'] for d in report['diagnostics']])
        self.assertFalse(checker.review_bytes(b'table prepone', 'und')['guidance'])

    def test_ambiguous_date_and_value_changes_fail_closed(self):
        raw = b'03/04/2026 / USD 1,234.50 / 09:00 UTC'
        report = checker.review_bytes(raw, 'en-GB')
        self.assertEqual(raw.decode(), report['source'])
        self.assertEqual('needs-review', next(d for d in report['diagnostics'] if d['code'] == 'ambiguous-date')['status'])
        for candidate in (raw.replace(b'03/04', b'04/03'), raw.replace(b'USD', b'GBP'), raw.replace(b'1,234.50', b'1,234.00')):
            self.assertEqual('failed', checker.review_bytes(raw, 'en-US', candidate=candidate)['source_integrity']['status'])

    def test_house_style_keeps_organization_and_medium_context(self):
        for style in ('University of Oxford', 'OUP Music & Letters', 'Microsoft', 'SGDS UI'):
            report = checker.review_bytes(b'Organize Your Account', 'en-GB', medium='display', house_style=style)
            notice = next(d for d in report['diagnostics'] if d['code'] == 'house-style-scope-review')
            self.assertEqual(style, notice['evidence']['house_style'])
            self.assertEqual('display', notice['evidence']['medium'])
            self.assertEqual('needs-review', notice['status'])
            self.assertEqual('Organize Your Account', report['source'])
        self.assertNotIn('house-style-scope-review', [d['code'] for d in checker.review_bytes(b'Organize', 'en-GB')['diagnostics']])

    def test_new_rules_remain_advice_and_keep_existing_ids(self):
        rules = json.loads((PLUGIN / 'rules/catalog.json').read_text())
        self.assertEqual(51, len(rules))
        self.assertEqual(51, len({r['id'] for r in rules}))
        regional = [r for r in rules if r['id'].startswith('EN-REG-')]
        self.assertEqual(6, len(regional))
        self.assertTrue(all(r['status'] == 'guidance-only' and r['automatic_pass_allowed'] is False for r in regional))
        self.assertTrue(all(r['scope']['context_required'] for r in regional))


if __name__ == '__main__':
    unittest.main()
