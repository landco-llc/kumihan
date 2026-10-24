"""Static preservation checks; these do not execute proposed visual acceptance."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'plugins/kumihan-measure'


def runtime():
    spec = importlib.util.spec_from_file_location('regional_rendering_runtime', P / 'runtime/check_source.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RegionalRenderingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((P / 'fixtures/regional-acceptance.json').read_text())
        cls.checker = runtime()

    def test_all_32_candidates_have_bounded_evidence_mapping(self):
        cases = self.data['cases']
        self.assertEqual([f'EN-REG-{i:03}' for i in range(1, 33)], [c['case_id'] for c in cases])
        for case in cases:
            with self.subTest(case=case['case_id']):
                self.assertEqual('not-run', case['execution_status'])
                self.assertIsNone(case['actual_result'])
                self.assertIn(case['expected_status'], ('needs-review', 'not-checked'))
                self.assertTrue(case['expected'])
                self.assertTrue(case['product_static_test'])
                self.assertTrue(case['remaining_check'])

    def test_every_candidate_preserves_bytes_and_metadata(self):
        for case in self.data['cases']:
            with self.subTest(case=case['case_id']):
                raw = case['text'].encode('utf-8')
                metadata = case['context']
                result = self.checker.review_bytes(raw, 'en', source_metadata=metadata)
                self.assertEqual(raw, result['source'].encode('utf-8'))
                self.assertEqual(hashlib.sha256(raw).hexdigest(), result['source_sha256'])
                self.assertEqual('passed', result['source_integrity']['status'])
                # Preservation is not a language, visual, or host acceptance result.
                self.assertEqual('needs-review', result['language_quality'])
                self.assertEqual('not-checked', result['native_rendering'])
                self.assertEqual('not-checked', result['office_pdf'])
                self.assertEqual('failed', self.checker.review_bytes(raw, 'en', candidate=raw + b'!')['source_integrity']['status'])
                self.assertEqual('failed', self.checker.review_bytes(raw, 'en', source_metadata=metadata, candidate_metadata={'changed': True})['source_integrity']['status'])

    def test_mixed_script_and_logical_order_survive_negative_candidates(self):
        samples = [
            ('te reo Māori', 'te reo Maori'),
            ('Green Tea（煎茶）', 'Green Tea(煎茶)'),
            ('English 日本語 简体中文 繁體中文 한국어', 'English'),
            ('English العربية עברית 123', 'English 321 תירבע ةيبرعلا'),
            ('e\u0301 A\u200dB فارسی\u200cنام', 'é AB فارسی نام'),
            ('USD 1\u00a0234,50', 'SGD 1234.50'),
        ]
        for source, changed in samples:
            with self.subTest(source=source):
                result = self.checker.review_bytes(source.encode(), 'en', candidate=changed.encode())
                self.assertEqual(source, result['source'])
                self.assertEqual('failed', result['source_integrity']['status'])
                self.assertEqual('not-checked', result['native_rendering'])

    def test_date_currency_timezone_are_not_interpreted(self):
        raw = b'03/04/2026 / USD 1234.50 / 2026-04-05T13:05:00'
        result = self.checker.review_bytes(raw, 'en')
        self.assertEqual(raw, result['source'].encode())
        self.assertTrue(any(d['code'] == 'ambiguous-date' for d in result['diagnostics']))
        self.assertEqual([], result['annotations'])

    def test_inline_clipping_is_a_review_not_rendered_failure_or_pass(self):
        text = '<p style="overflow:hidden;white-space:nowrap">Green Tea（煎茶） العربية 123</p>'
        result = self.checker.review_bytes(text.encode(), 'en', format='html')
        self.assertTrue(any(d['code'] == 'inline-wrap-risk' and d['status'] == 'needs-review' for d in result['diagnostics']))
        self.assertEqual('not-checked', result['native_rendering'])
        self.assertEqual(text, result['source'])

    def test_runtime_references_are_not_portable_number_acceptance(self):
        cases = {c['case_id']: c for c in self.data['cases']}
        for case_id in ('EN-REG-018', 'EN-REG-019'):
            case = cases[case_id]
            self.assertEqual('not-checked', case['expected_status'])
            self.assertEqual('not-run', case['execution_status'])
            self.assertIn('Node 22.16.0 / ICU 77.1 / CLDR 47.0', case['context']['reference_environment'])
        self.assertIn('\u00a0', cases['EN-REG-019']['context']['reference_display'])


if __name__ == '__main__':
    unittest.main()
