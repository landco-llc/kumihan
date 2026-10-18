import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
class Acceptance(unittest.TestCase):
    def test_original_cases_have_honest_reproducible_status(self):
        s=importlib.util.spec_from_file_location('checks',ROOT/'plugins/kumihan-zilu/runtime/checks.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
        fixtures=json.loads((ROOT/'tests/zilu/acceptance-fixtures.json').read_text())['cases']
        results=json.loads((ROOT/'tests/zilu/acceptance-results.json').read_text())['cases']
        self.assertEqual(len(fixtures),44);self.assertEqual(len(results),44)
        self.assertEqual({r for c in fixtures for r in c['rule_ids']},{f'KH-CN-R{i:03d}' for i in range(1,37)})
        for c,result in zip(fixtures,results):
            with self.subTest(case=c['id']):
                self.assertEqual(c['id'],result['case_id'])
                r=m.audit(c['input'],candidate=c['input']);self.assertEqual(r['preservation']['status'],'passed')
                self.assertEqual(m.audit(c['input'],candidate=c['input']+' ')['preservation']['status'],'failed')
                self.assertEqual(r['source_sha256'],result['source_sha256'])
                if c['id']=='KH-CN-T028':self.assertTrue(all(x['status']=='not-checked' for x in r['rendering']))
                if c['id']=='KH-CN-T033':self.assertTrue(any(x['rule_id']=='KH-CN-R025' and x['status']=='needs-review' for x in r['findings']))
                if result['status']=='pass':self.assertIn(c['id'],('KH-CN-T005','KH-CN-T028','KH-CN-T033'))
