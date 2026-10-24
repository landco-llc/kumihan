import importlib.util
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('vertical_checks', ROOT/'plugins/kumihan-zilu/runtime/checks.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class Vertical(unittest.TestCase):
    def test_scope_is_explicit_and_rendering_is_never_inferred(self):
        self.assertIn('context', __import__('inspect').signature(m.audit).parameters)
        for profile in ('cn-vertical-reading','cn-vertical-display','cn-vertical-publication-gb','cn-classical-reference'):
            r = m.audit('《边城》 BCD188型 J12号 ① Ａ nǚ', context={'profile':profile,'writing_mode':'vertical-rl'})
            self.assertEqual(r['vertical']['status'], 'requires-review')
            self.assertEqual(len(r['vertical']['rendering']), 26)
            self.assertTrue(all(x['status']=='not-checked' for x in r['vertical']['rendering']))
        self.assertEqual(m.audit('你好')['vertical']['status'], 'not-requested')

    def test_static_risks_and_byte_preservation(self):
        self.assertIn('context', __import__('inspect').signature(m.audit).parameters)
        text = '我正在读《边城》。https://example.com/a?x=1 BCD188型 J12号\r\n① Ａ'
        c = {'profile':'cn-vertical-reading','writing_mode':'horizontal-tb','css':'width:1em; font-feature-settings: "vrt2" 1;', 'per_character_breaks':True}
        r = m.audit(text, candidate=text, context=c)
        self.assertEqual(r['preservation']['status'],'passed')
        self.assertEqual(r['vertical']['status'],'requires-review')
        self.assertTrue({'KH-CN-V003','KH-CN-V006'} <= {f['rule_id'] for f in r['findings']})
        self.assertEqual(m.audit(text,candidate=text.replace('《',''),context=c)['preservation']['status'],'failed')
        with self.assertRaises(ValueError): m.audit(text, context={'profile':'unknown'})
        with self.assertRaises(ValueError): m.audit(text, context={'profile':'cn-vertical-reading','writing_mode':'sideways'})

    def test_lr_and_gb_need_explicit_scope(self):
        self.assertIn('context', __import__('inspect').signature(m.audit).parameters)
        r = m.audit('第12期',context={'profile':'cn-vertical-publication-gb','writing_mode':'vertical-lr'})
        self.assertTrue({'KH-CN-V001','KH-CN-V004'} <= {f['rule_id'] for f in r['findings']})
        r = m.audit('第12期',context={'profile':'cn-vertical-publication-gb','writing_mode':'vertical-lr','direction_reason':'exhibition','selected_standards':['GB/T 15835-2011']})
        self.assertFalse({'KH-CN-V001','KH-CN-V004'} & {f['rule_id'] for f in r['findings']})

    def test_vertical_unicode_corpus_preservation(self):
        samples = ['① ² Ａ ， ㍑ nǚ 👨‍👩‍👧‍👦 𠮷', '我正在读《边城》。', '——……“括号”（引号）', 'BCD188型 J12号 第12期 编号123 2026年', 'https://example.com/a?x=1&y=2', 'English words keep spaces', '第一段。\r\n\r\n第二段。', '价格 ¥1,280.00 350 mL']
        for profile in m.PROFILES:
            for text in samples:
                with self.subTest(profile=profile,text=text):
                    c = {'profile':profile,'writing_mode':'vertical-rl'}
                    r = m.audit(text,candidate=text,context=c)
                    self.assertEqual(r['preservation']['status'],'passed')
                    self.assertEqual(m.audit(text,candidate=text+' ',context=c)['preservation']['status'],'failed')
                    self.assertEqual(r['vertical']['status'],'requires-review')

    def test_transition_does_not_admit_mutated_bytes_or_other_products(self):
        import sys, tempfile
        sys.path.insert(0,str(ROOT/'tools'))
        from zilu_v012_transition import allowed, EXPECTED
        self.assertFalse(allowed('plugins/kumihan-ziheng/plugin.json','protected',ROOT))
        path = 'README.md'
        self.assertIn(path, EXPECTED)
        with tempfile.TemporaryDirectory() as d:
            target = Path(d)/path; target.parent.mkdir(parents=True,exist_ok=True)
            # Exercise the frozen ZiLu admission against its exact retained README.
            from en_measure_v011_transition import predecessor
            target.write_bytes(predecessor(ROOT)[1])
            self.assertTrue(allowed(path,'protected',d))
            target.write_bytes(target.read_bytes()+b' ')
            self.assertFalse(allowed(path,'protected',d))
            self.assertFalse(allowed(path,'bodies',ROOT))

    def test_malformed_context_is_rejected_as_input_error(self):
        for extra in ({'css':None},{'per_character_breaks':'false'},{'selected_standards':'x'},{'selected_standards':[3]},{'direction_reason':3}):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                m.audit('你好',context=dict(profile='cn-vertical-reading',**extra))
