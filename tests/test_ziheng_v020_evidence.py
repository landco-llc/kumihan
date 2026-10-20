import copy
import json
import unittest
from test_ziheng_v020_context import BASE,load
class EvidenceTests(unittest.TestCase):
    def api(self):
        api=load('evidence');self.assertIsNotNone(api,'evidence validator missing');return api
    def static(self):
        return dict(schema_version='2.0',artifact={'path':'sample.txt','sha256':'a'*64},scope='supplied bytes',method='static',status='passed',evidence_refs=[{'path':'comparison.json','artifact_sha256':'a'*64,'kind':'byte-comparison'}],limitations=['Extraction completeness not established'])
    def test_preservation_exact_not_normalized(self):
        api=load('checks')
        for text,changed in [('臺','台'),('裏','裡'),('HK$1,250','HK$1250'),('Ａ①','A1'),('e\u0301','é'),('禰\U000e0100','禰'),('👩\u200d💻','👩💻'),('\ufeffa\r\n','a\n'),('',' ')]:
            a=text.encode();self.assertEqual(api.check_preservation(a,a)['status'],'passed');self.assertEqual(api.check_preservation(a,changed.encode())['status'],'failed')
    def test_segment_roles_unknown_and_code_point_positions(self):
        api=load('checks');self.assertTrue(hasattr(api,'review_segment'),'segment wrapper missing')
        for role in ['name','url','code','english-quote','protected']:
            r=api.review_segment({'text':'😀e\u0301, https://example.org/a,b','role':role},{'content_locale':'zh-Hant-TW'})
            self.assertEqual(r['findings'],[]);self.assertFalse(r['source_changed']);self.assertNotIn('artifact_status',r)
        r=api.review_segment({'text':'😀e\u0301,文','role':'prose'},{'content_locale':'zh-Hant-TW'})
        self.assertEqual(r['findings'][0]['positions'],[3]);self.assertEqual(r['position_unit'],'unicode-code-point')
        r=api.review_segment({'text':'文,文','role':'prose'},{'content_locale':'zh-Hant-MO'})
        self.assertEqual(r['findings'],[]);self.assertTrue(r['limitations'])
        r=api.review_segment({'text':'文,文','role':'unknown'},{'content_locale':'zh-Hant-HK'})
        self.assertEqual(r['coverage']['status'],'needs-review')
    def test_static_evidence_not_browser_required(self):
        self.assertEqual(self.api().validate_evidence_context(self.static()),[])
    def test_evidence_rejects_empty_mismatched_and_css_only(self):
        for changes in [{'evidence_refs':[]},{'evidence_refs':[{'path':'x','artifact_sha256':'b'*64,'kind':'byte-comparison'}]},{'method':'rendered'},{'status':'PASS'}]:
            r=self.static();r.update(changes);self.assertTrue(self.api().validate_evidence_context(r),changes)
    def test_rendered_needs_real_conditions_and_glyph_proof(self):
        r=self.static();r['method']='rendered';r['scope']='regional-glyph'
        r['environment']={'writing_mode':'horizontal-tb','viewport':{'width':320,'height':800},'zoom':{'method':'none','factor':1},'os':'Linux','browser':{'name':'Chromium','version':'test-observation','engine':'Blink','engine_version':'unknown'},'fonts':[{'family':'unknown','face':'unknown','version':'unknown','fallback':'unknown','actual_used':False}]}
        r['evidence_refs'][0]['kind']='screenshot'
        self.assertTrue(self.api().validate_evidence_context(r))
        r['status']='not-checked';self.assertEqual(self.api().validate_evidence_context(r),[])
    def test_schemas_validate_static_and_context(self):
        import jsonschema
        for name in ['review-context-v2','review-evidence-v2']:
            p=BASE/f'schemas/{name}.schema.json';self.assertTrue(p.exists());jsonschema.Draft202012Validator.check_schema(json.loads(p.read_text()))
        jsonschema.validate(self.static(),json.loads((BASE/'schemas/review-evidence-v2.schema.json').read_text()))
    def test_glyph_scopes_cannot_pass_with_static_byte_evidence(self):
        for scope in ['regional-glyph','ivs-glyph']:
            r=self.static();r['scope']=scope
            self.assertTrue(self.api().validate_evidence_context(r),scope)
