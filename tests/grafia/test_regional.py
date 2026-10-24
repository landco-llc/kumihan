"""Executable boundaries are separate from native/editorial research acceptance."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'plugins/kumihan-grafia'


class RegionalBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('regional_checks', BASE / 'runtime/checks.py')
        cls.api = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.api)

    def test_region_never_selects_pronoun_currency_or_timezone(self):
        # A future country->pronoun/currency default must fail this test.
        for locale in ['es', 'es-ES', 'es-MX', 'es-AR', 'es-CO', 'es-CL', 'es-PE', 'es-419', 'es-US']:
            with self.subTest(locale=locale):
                result = self.api.review('Vos tenés tu libro; tú tenés; usted tiene. $ 1.234,50'.encode(), locale=locale)
                self.assertIsNone(result['context']['market'])
                self.assertIsNone(result['context']['currency'])
                self.assertIsNone(result['context']['timeZone'])
                self.assertEqual(result['context']['pronoun'], 'inherit')
                self.assertEqual(result['context']['verb_paradigm'], 'inherit')
                self.assertFalse(result['findings'])

    def test_regional_negative_cases_preserve_exact_bytes(self):
        matrix = json.loads((BASE / 'fixtures/regional-boundaries.json').read_bytes())
        for case in matrix['cases']:
            with self.subTest(case=case['id']):
                data = case['input'].encode('utf-8')
                result = self.api.review(data, locale=case['locale'])
                self.assertEqual(result['original_hash'], hashlib.sha256(data).hexdigest())
                self.assertEqual(result['preservation']['status'], 'passed')
                self.assertEqual({f['rule_id'] for f in result['findings']}, set(case['candidate_rule_ids']))
                self.assertTrue(all(f['status'] == 'needs-review' and f['edits_authorized'] is False for f in result['findings']))
                self.assertEqual(result['rendering'], 'not-checked')
                self.assertEqual(result['native_host'], 'not-checked')

    def test_canonical_equivalence_never_grants_edit_permission(self):
        for original, candidate in [('ñ', 'n\u0303'), ('á', 'a\u0301'), ('35\u00a0%', '35 %'), ('24\u202f°C', '24 °C'), ('1.º', '1.o')]:
            with self.subTest(original=original):
                result = self.api.review(original.encode(), candidate=candidate.encode())
                self.assertEqual(result['preservation']['status'], 'failed')


@unittest.skipUnless(shutil.which('node'), 'Node unavailable: formatter observation NOT_RUN')
class IntlBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = subprocess.run(['node', str(BASE / 'runtime/intl_probe.mjs')], capture_output=True, text=True)

    def test_probe_is_available(self):
        self.assertEqual(self.result.returncode, 0, self.result.stderr)

    def report(self):
        self.assertEqual(self.result.returncode, 0, self.result.stderr)
        return json.loads(self.result.stdout)

    def test_explicit_inputs_and_runtime_evidence(self):
        report = self.report()
        self.assertTrue({'node', 'icu', 'cldr'} <= report['versions'].keys())
        self.assertEqual(len(report['numbers']), 9)
        for row in report['numbers']:
            self.assertEqual(row['raw_decimal'], '1234567.89123')
            self.assertEqual(row['original_after_format'], row['raw_decimal'])
            self.assertEqual(row['resolved']['currency'], row['explicit_currency'])
            self.assertEqual(row['resolved']['minimumFractionDigits'], 2)
            self.assertEqual(row['resolved']['maximumFractionDigits'], 2)
            self.assertEqual(''.join(part['value'] for part in row['parts']), row['display'])
            self.assertEqual(row['supported'], [row['requested_locale']])
            self.assertEqual(row['observation_status'], 'observed')
        aggregate = next(row for row in report['numbers'] if row['requested_locale'] == 'es-419')
        self.assertEqual(aggregate['explicit_currency'], 'COP')
        self.assertIn('not a market default', aggregate['currency_scope'])

    def test_date_only_stays_civil_and_instant_keeps_timezone(self):
        report = self.report()
        self.assertEqual(report['date_only'], {'raw': '2026-10-25', 'value_kind': 'date-only', 'conversion': 'not-performed'})
        for row in report['instants']:
            self.assertEqual(row['raw_instant'], '2026-10-25T00:30:00Z')
            self.assertEqual(row['epoch_before'], row['epoch_after'])
            self.assertIn(row['explicit_timeZone'], ['UTC', 'Europe/Madrid', 'America/Mexico_City', 'America/Argentina/Buenos_Aires'])
            self.assertTrue(row['resolved']['timeZone'])  # ICU may canonicalize timezone aliases.
            self.assertEqual(''.join(part['value'] for part in row['parts']), row['display'])
        self.assertEqual(report['native_host'], 'not-checked')
        self.assertEqual(report['editorial_acceptance'], 'not-checked')
