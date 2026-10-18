import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT/'plugins/kumihan-ziheng/runtime/checks.py'

class ChecksTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(RUNTIME.is_file(), 'readonly checker has not been implemented')
        spec = importlib.util.spec_from_file_location('checks', RUNTIME)
        self.api = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.api)

    def test_exact_bytes_never_normalized(self):
        samples = ['臺灣／香港，名字：陳𠮷；ＨＫ＄１２３', '禰\U000e0100 e\u0301 👩\u200d💻', 'https://example.invalid/a?q=1,2&v=Ａ', '\ufeff原稿\r\n第二行\u00a0']
        for text in samples:
            raw = text.encode('utf-8')
            self.assertEqual(self.api.check_preservation(raw, raw)['status'], 'passed')
            self.assertEqual(self.api.check_preservation(raw, raw+b' ')['status'], 'failed')
        self.assertEqual(self.api.check_preservation('e\u0301'.encode(), 'é'.encode())['status'], 'failed')
        self.assertEqual(self.api.check_preservation('臺'.encode(), '台'.encode())['status'], 'failed')

    def test_original_regional_fixture_cases(self):
        cases = json.loads((ROOT/'tests/ziheng/fixtures.json').read_text())
        for case in cases:
            with self.subTest(case=case['id']):
                raw = case['text'].encode('utf-8')
                findings = self.api.review_text(case['text'], case['locale'], case['role'], case.get('quote_style'))
                self.assertEqual([f['rule_id'] for f in findings], case['expected_rule_ids'])
                self.assertTrue(all(f['status']=='needs-review' and f['method']=='static' for f in findings))
                self.assertEqual(raw, case['text'].encode('utf-8'))

    def test_unknown_context_rejected(self):
        for tag in ['zh', 'zh-TW', 'ja-JP', 'zh-Hans-HK']:
            with self.assertRaises(ValueError): self.api.review_text('文字', tag, 'prose')
        with self.assertRaises(ValueError): self.api.review_text('文字', 'zh-Hant-HK', 'unknown')
        with self.assertRaises(ValueError): self.api.review_text('文字', 'zh-Hant-TW', 'prose', 'unknown')

if __name__ == '__main__': unittest.main()
