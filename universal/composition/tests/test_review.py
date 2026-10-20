import copy
import tempfile
import unittest
from pathlib import Path
from fixtures import request, observation, audit, digest
import test_core

class ReviewTests(unittest.TestCase):
    setUpClass = classmethod(test_core.ResolverTests.setUpClass.__func__)
    resolve = test_core.ResolverTests.resolve
    def review(self,r,p,**kwargs):
        from review import evaluate
        return evaluate(r,p,self.registry,**kwargs)

    def test_evaluator_exists(self):
        self.assertTrue((Path(__file__).resolve().parents[1]/'review.py').exists(),'Read-only evaluator missing')

    def test_exact_target_readonly_and_source_bound_evidence(self):
        r=request((('ja','原稿\r\n👩\u200d🔬'),));p=self.resolve(r);before=copy.deepcopy((r,p))
        from contract import validate_record
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'target.txt';raw=r['sources'][0]['text'].encode();target.write_bytes(raw)
            a, observations=self.review(r,p,target=target,source_id='s0')
            self.assertEqual(target.read_bytes(),raw)
            self.assertEqual((r,p),before)
            validate_record(a)
            for o in observations:validate_record(o)
            self.assertEqual(a['artifact_digest'],digest(r['sources'][0]['text']))
            evidence={o['id']:o for o in observations}
            for check in a['checks']:
                if check['status']=='passed':
                    self.assertTrue(check['evidence_refs'])
                    self.assertTrue(all(ref in evidence for ref in check['evidence_refs']))
                    self.assertEqual(check['method'],'static')
            rendered=[c for c in a['checks'] if c['rule_id']=='MIX-009']
            self.assertTrue(rendered);self.assertTrue(all(c['status']=='not-checked' for c in rendered))

    def test_stale_or_modified_plan_target_observation_rejected(self):
        from contract import CompositionError
        r=request();p=self.resolve(r)
        stale=copy.deepcopy(p);stale['source_digests'][0]['text_digest']='sha256:'+'0'*64
        with self.assertRaises(CompositionError):self.review(r,stale)
        modified=copy.deepcopy(p);modified['decisions'][0]['state']='resolved';modified['decisions'][0]['value']['direction']='rtl'
        with self.assertRaises(CompositionError):self.review(r,modified)
        o=observation(r);o['artifact_digest']='sha256:'+'0'*64
        with self.assertRaises(CompositionError):self.review(r,p,observations=[o])
        o=observation(r);o['scopes']=['missing']
        with self.assertRaises(CompositionError):self.review(r,p,observations=[o])
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'wrong';target.write_text('different')
            with self.assertRaises(CompositionError):self.review(r,p,target=target,source_id='s0')
            self.assertEqual(target.read_text(),'different')

    def test_forged_evidence_cannot_upgrade_render_or_alignment_or_waiver(self):
        from review import validate_audit_binding
        from contract import CompositionError
        r=request();p=self.resolve(r);o=observation(r)
        o['method']='rendered';o['facts']=[dict(name='all-checks-passed',value=True,unit=None)]
        a,obs=self.review(r,p,observations=[o])
        self.assertTrue(all(c['status']=='not-checked' for c in a['checks'] if c['rule_id']=='MIX-009'))
        forged=copy.deepcopy(a);forged['checks'][0].update(status='passed',evidence_refs=['imaginary'])
        with self.assertRaises(CompositionError):validate_audit_binding(forged,r,p,obs,self.registry)
        forged=copy.deepcopy(a);forged['checks'][0].update(status='waived',waiver=dict(approval_ref='claim',scope='s0',reason='claimed',artifact_digest=a['artifact_digest']))
        with self.assertRaises(CompositionError):validate_audit_binding(forged,r,p,obs,self.registry)

    def test_static_evidence_cannot_be_relabelled_as_a_render_pass(self):
        from review import validate_audit_binding
        from contract import CompositionError
        r=request();p=self.resolve(r);a,obs=self.review(r,p)
        a['checks'][0]['rule_id']='MIX-009'
        with self.assertRaises(CompositionError):validate_audit_binding(a,r,p,obs,self.registry)

    def test_forged_static_fact_value_and_provenance_rejected(self):
        from review import validate_audit_binding
        from contract import CompositionError
        r=request();p=self.resolve(r);a,obs=self.review(r,p)
        o=observation(r);o['scopes']=['s0'];o['facts']=[dict(name='exact-utf8-sha256',value='WRONG',unit=None)]
        a['checks']=[dict(rule_id='MIX-001',scope='s0',status='passed',method='static',evidence_refs=[o['id']],reason='forged')]
        with self.assertRaises(CompositionError):validate_audit_binding(a,r,p,[o],self.registry)
        a,obs=self.review(r,p);obs[0]['facts'][0]['value']='WRONG'
        with self.assertRaises(CompositionError):validate_audit_binding(a,r,p,obs,self.registry)

    def test_missing_module_conflicts_and_bidi_are_reported(self):
        r=request((('he','עברית'),('ja','\u202e原稿')));p=self.resolve(r)
        a,_=self.review(r,p,source_id='s0')
        b,_=self.review(r,p,source_id='s1')
        self.assertIn('unsupported',[c['status'] for c in a['checks'] if c['rule_id']=='MIX-003'])
        self.assertIn('needs-review',[c['status'] for c in b['checks'] if c['rule_id']=='MIX-006'])

if __name__=='__main__':unittest.main()
