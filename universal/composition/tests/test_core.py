import copy
import json
import unittest
from pathlib import Path
from fixtures import request, digest

class SourceTests(unittest.TestCase):
    def check(self, r):
        from core import validate_request
        return validate_request(r)

    def reject(self, r, code):
        from contract import CompositionError
        with self.assertRaises(CompositionError) as ctx: self.check(r)
        self.assertEqual(ctx.exception.code, code)
        self.assertTrue(ctx.exception.scope.startswith('/'))

    def test_core_exists(self):
        self.assertTrue((Path(__file__).resolve().parents[1]/'core.py').exists(), 'Source integrity core is missing')

    def test_exact_unicode_and_empty_source(self):
        for text in ('ASCII', 'ひらがな漢字', 'ภาษาไทย', 'العربية', 'e\u0301', 'क्\u200dष', '👩\u200d🔬😀', '\r\n\u00a0\u200c\ufe0f', 'עברית 123 abc', ''):
            r = request((('und',text),)); before = copy.deepcopy(r)
            with self.subTest(text=ascii(text)):
                self.check(r); self.assertEqual(r,before)
                self.assertEqual(r['sources'][0]['text_digest'],digest(text))

    def test_invalid_unicode_utf8_and_byte_boundaries(self):
        from core import decode_utf8, byte_range_to_scalar
        from contract import CompositionError
        with self.assertRaises(CompositionError): decode_utf8(b'\xff')
        r=request();r['sources'][0]['text']='\ud800';self.reject(r,'E_INVALID_UNICODE')
        text='A漢😀e\u0301'
        self.assertEqual(byte_range_to_scalar(text,1,8), (1,3))
        for start,end in ((2,8),(1,7),(-1,1),(8,99),(1,1)):
            with self.subTest(start=start,end=end), self.assertRaises(CompositionError): byte_range_to_scalar(text,start,end)

    def test_digest_range_gaps_overlap_duplicate(self):
        mutations = [
            ('E_SOURCE_DIGEST', lambda r:r['sources'][0].update(text_digest='sha256:'+'0'*64)),
            ('E_RANGE',lambda r:r['language_runs'][0]['range'].update(end=99)),
            ('E_RANGE',lambda r:r['language_runs'].clear()),
            ('E_RANGE',lambda r:r['language_runs'].append(dict(copy.deepcopy(r['language_runs'][0]),id='overlap'))),
            ('E_REFERENCE',lambda r:r['regions'].append(copy.deepcopy(r['regions'][0]))),
            ('E_REFERENCE',lambda r:r['regions'][0]['range'].update(source_id='missing')),
            ('E_REFERENCE',lambda r:r['regions'][0].update(parent_id='r0')),
        ]
        for code, mutate in mutations:
            r=request(); mutate(r)
            with self.subTest(code=code,mutate=mutate):self.reject(r,code)

    def test_unknown_critical_resource_and_tag(self):
        r=request(); r['extensions']=[dict(namespace='example:unknown',version='1',critical=True,payload={})];self.reject(r,'E_CRITICAL_EXTENSION')
        r=request((('ja','a'*1_048_577),));self.reject(r,'E_RESOURCE_LIMIT')
        for tag in ('ja_JP','en--US','-ja','en-a','en-123456789','en-u-ca-u-nu','sl-rozaj-rozaj'):
            r=request(((tag,'a'),))
            with self.subTest(tag=tag):self.reject(r,'E_REFERENCE')
        for tag in ('x-private','zh-Hant-TW','sr-Latn','und','de-CH-1901','en-US-u-ca-japanese','i-klingon','en-u-ca-gregory-t-ca-gregory'):
            with self.subTest(tag=tag):self.check(request(((tag,'a'),)))

class ResolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import importlib.util
        p=Path(__file__).resolve().parents[2]/'tools/build_registry.py'
        spec=importlib.util.spec_from_file_location('composition_registry_fixture',p)
        b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
        cls.registry=b.build()

    def resolve(self,r,**kwargs):
        from core import resolve
        return resolve(r,self.registry,**kwargs)

    def test_exact_locale_only_no_script_or_english_fallback(self):
        for tag, expected in (('ar','ar'),('fa','fa'),('ru','ru'),('ja','ja'),('zh-Hant','zh-Hant'),('en',None),('he',None),('el',None),('nl',None),('uk',None),('und',None),('x-private',None),('ja-XX',None)):
            r=request(((tag,'漢 abc العربية'),));p=self.resolve(r)
            selected=p['decisions'][0]['value']['runs'][0]
            with self.subTest(tag=tag):
                self.assertEqual(selected['module_id'],expected)
                self.assertNotEqual(selected['capability_state'],'verified')
                if expected:self.assertEqual(selected['module_status'],'preview_unverified')

    def test_mixed_nonenglish_pairs_are_representable_deterministically(self):
        for tags in (('ja','zh-Hant'),('ar','he'),('ko','th'),('hi','bn'),('fa','ru'),('ja','ar','fr'),('fr','de')):
            r=request(tuple((tag,'Text漢😀') for tag in tags));before=copy.deepcopy(r)
            p=self.resolve(r)
            from contract import validate_record
            validate_record(p)
            self.assertEqual(p,self.resolve(r));self.assertEqual(r,before)
            self.assertEqual(len(p['decisions']),len(tags))
            self.assertTrue(all(c['strength']=='hard' for c in p['constraints']))
            self.assertEqual(p['font_instances'],[]);self.assertEqual(p['optical_profiles'],[])

    def test_metadata_disagreement_and_detected_only_remain_review(self):
        r=request(); candidates=[dict(run_id='run0', language_tag='zh-Hant',origin='detected')]
        p=self.resolve(r,candidates=candidates)
        self.assertTrue(p['conflicts'])
        self.assertEqual(p['decisions'][0]['value']['runs'][0]['module_id'],'ja')
        r['language_runs'][0]['origin']='detected'
        p=self.resolve(r)
        self.assertEqual(p['decisions'][0]['state'],'proposed')

    def test_unknown_noncritical_preserved_and_all_inputs_bound(self):
        r=request();r['extensions']=[dict(namespace='example:unknown',version='1',critical=False,payload={'data':'kept'})]
        p=self.resolve(r)
        self.assertIn(r['extensions'][0],p['extensions'])
        r2=copy.deepcopy(r);r2['regions'][0]['expression']='display'
        self.assertNotEqual(p['id'],self.resolve(r2)['id'])
        altered=copy.deepcopy(self.registry);altered['modules']['ja']['version']='changed'
        from core import resolve
        self.assertNotEqual(p['id'],resolve(r,altered)['id'])

    def test_translation_and_direction_limits_never_measure(self):
        r=request((('ar','العربية'),('he','עברית')))
        r['relationships']=[dict(id='t1',type='translation-of',from_region='r1',to_region='r0',alignment_status='unverified',evidence_refs=[],reviewer_ref=None)]
        r['regions'][0].update(expression='display',direction='rtl')
        p=self.resolve(r)
        self.assertTrue(any('translation' in x for x in p['limitations']))
        self.assertTrue(any('font' in x for x in p['limitations']))
        self.assertEqual(p['decisions'][0]['value']['direction'],'rtl')
        self.assertIn('shaping',p['required_capabilities'])

if __name__=='__main__':unittest.main()
