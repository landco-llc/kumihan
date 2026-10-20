"""Selected P-case STATIC portions only; no rendered/native/editorial acceptance."""
import copy
import unittest
import test_core
from fixtures import request

CASES={
 'P01':(('ja','同じ漢字'),('zh-Hant','同樣漢字')),
 'P02':(('zh-Hans','汉语引用'),('zh-Hant','漢語引用')),
 'P03':(('ko','한국어'),('th','ภาษาไทย')),
 'P04':(('hi','क्\u200dष'),('bn','বাংলা')),
 'P05':(('ar','العربية'),('he','עִבְרִית')),
 'P06':(('fa','متن ۱۲۳'),('ru','текст 123')),
 'P07':(('ja','原稿'),('ar','العربية'),('fr','français')),
 'P09':(('fr','œuvre'),('de','Straße')),
 'P14':(('th','ภาษาไทย'),('km','ភាសាខ្មែរ')),
 'P16':(('vi','e\u0301'),('fa','می\u200cروم')),
 'P17':(('und',' 123 ! '),), 'P18':(('und','漢'),),
 'P19':(('x-private','text'),('ja-XX','漢')),
 'P23':(('und','∑ 😀 👩\u200d🔬 漢\ufe00'),),
 'P24':(('ar','\u2067العربية\u2069'),),
 'P25':(('ja','漢'),), 'P26':(('ja','見出し'),('fr','titre')),
 'P28':(('ja','本文'),('ja','広告')),
 'P29':(('ja','ロゴ'),('ja','本文')),
 'P30':(('ja','必須CTA'),), 'P40':(('und','data'),),
}

class AcceptanceTests(unittest.TestCase):
    setUpClass=classmethod(test_core.ResolverTests.setUpClass.__func__)

    def run_case(self,case):
        from core import resolve,validate_request
        from review import evaluate
        from contract import CompositionError
        r=request(CASES[case])
        candidates=[]
        if case=='P25':candidates=[dict(run_id='run0',language_tag='zh-Hant',origin='detected')]
        if case=='P26':r['relationships']=[dict(id='rel1',type='translation-of',from_region='r1',to_region='r0',alignment_status='unverified',evidence_refs=[],reviewer_ref=None)]
        if case in ('P28','P29','P30'):r['regions'][0]['expression']='display'
        if case=='P29':r['policies']['approval_refs']=['fixture:untrusted-approval']
        before=copy.deepcopy(r);p=resolve(r,self.registry,candidates)
        for s in r['sources']:
            a,obs=evaluate(r,p,self.registry,source_id=s['id'])
            self.assertTrue(all(c['status']=='not-checked' for c in a['checks'] if c['rule_id']=='MIX-009'))
            self.assertFalse(any(c['status']=='waived' for c in a['checks']))
        self.assertEqual(r,before)
        if case=='P25':self.assertTrue(p['conflicts'])
        if case=='P40':
            for change,code in ((lambda r:r['sources'][0].update(text_digest='sha256:'+'0'*64),'E_SOURCE_DIGEST'),
                                (lambda r:r['extensions'].append(dict(namespace='unknown:critical',version='1',critical=True,payload={})),'E_CRITICAL_EXTENSION')):
                bad=copy.deepcopy(r);change(bad)
                with self.assertRaises(CompositionError) as ctx:validate_request(bad)
                self.assertEqual(ctx.exception.code,code)

    def test_mixed_runs_in_single_story_stay_distinct(self):
        from core import resolve
        r=request((('ja','漢العربيةfrançais'),))
        base=r['language_runs'][0];r['language_runs']=[]
        for i,(start,end,tag) in enumerate(((0,1,'ja'),(1,8,'ar'),(8,16,'fr'))):
            run=copy.deepcopy(base);run.update(id='mixed'+str(i),language_tag=tag);run['range'].update(start=start,end=end);r['language_runs'].append(run)
        p=resolve(r,self.registry)
        self.assertEqual([s['module_id'] for s in p['decisions'][0]['value']['runs']],['ja','ar','fr'])

for case in CASES:
    def test(self,case=case):self.run_case(case)
    test.__name__='test_'+case+'_static_only'
    setattr(AcceptanceTests,test.__name__,test)

if __name__=='__main__':unittest.main()
