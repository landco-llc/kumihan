import importlib.util
import pathlib
import unittest

BASE=pathlib.Path(__file__).resolve().parents[2]/'plugins/kumihan-zilu'

class Checks(unittest.TestCase):
    def load(self):
        self.assertTrue((BASE/'runtime/checks.py').exists(), 'read-only checker not implemented')
        spec=importlib.util.spec_from_file_location('zilu_checks',BASE/'runtime/checks.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

    def test_preserves_source_and_detects_changes(self):
        m=self.load()
        for text in ['無印良品 ¥1,280.00 350 mL', '① ² Ａ ， ㍑', 'nǚ 👨‍👩‍👧‍👦 𠮷', '《春茶》“引号”——…… https://example.com?a=1']:
            report=m.audit(text, candidate=text)
            self.assertEqual(report['preservation']['status'],'passed')
            self.assertEqual(report['source_sha256'],m.digest(text.encode('utf-8')))
            self.assertEqual(m.audit(text,candidate=text+' ')['preservation']['status'],'failed')

    def test_no_rendering_claim_and_region_inference(self):
        m=self.load();r=m.audit('lang=zh-Hans-CN; line-break:strict',locale='zh-Hans-SG')
        self.assertEqual(r['region'],'SG')
        self.assertEqual(r['profile_status'],'unsupported')
        self.assertEqual(m.audit('你好',locale='zh-Hans')['region'],'unknown')
        self.assertTrue(all(x['status']=='not-checked' for x in r['rendering']))
        self.assertEqual(r['mode'],'audit')

    def test_contextual_candidates_never_edit(self):
        m=self.load();text='他说：“第一段。\n\n“第二段。” 最适合今天的一杯茶 红茶……等'
        r=m.audit(text)
        self.assertNotIn('replacement',r)
        self.assertEqual(r['findings'][0]['status'],'needs-review')
        self.assertFalse(any(f['rule_id']=='KH-CN-R010' for f in r['findings']))
        with self.assertRaises(ValueError):m.audit('x',locale='../../bad')
