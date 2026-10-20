import importlib.util
import json
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'plugins/kumihan-ziheng'
sys.path.insert(0, str(ROOT/'tools'))
def load(name):
    path = BASE/'runtime'/f'{name}.py'
    if not path.exists(): return None
    spec = importlib.util.spec_from_file_location('ziheng_v2_'+name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
class ContextTests(unittest.TestCase):
    def api(self):
        api=load('context'); self.assertIsNotNone(api, 'v2 local context contract missing'); return api
    def records(self):
        import build_ziheng
        return json.loads(build_ziheng.plan_outputs(ROOT)['plugins/kumihan-ziheng/skills/kumihan-ziheng/rules/catalog.json'])
    def select(self, raw):
        api=self.api(); c=api.resolve_review_context(raw)
        import build_ziheng
        p=json.loads(build_ziheng.plan_outputs(ROOT)['plugins/kumihan-ziheng/skills/kumihan-ziheng/profiles/web-editorial.json'])
        return c, api.select_review_rules(c, self.records(),p)
    def test_regions_and_sets(self):
        for region,other in [('TW','004'),('HK','003')]:
            c,s=self.select(dict(content_locale='zh-Hant-'+region, medium='web-editorial',editorial_style='corner'))
            self.assertEqual(c['editorial_region'],region)
            self.assertNotIn('ZH-HANT-'+other,s['applicable_rule_ids'])
            self.assertTrue(s['selection_only']); self.assertNotIn('status',s)
            self.assertEqual(set(s['candidate_rule_ids']),set(s['applicable_rule_ids'])|{x['rule_id'] for x in s['deferred_rules']})
            self.assertNotIn('ZH-HANT-013',s['applicable_rule_ids'])
    def test_unknown_mo_and_foreign_stay_neutral(self):
        for tag in [None,'zh-Hant','zh-Hant-MO','en-US','yue-Hant-HK']:
            c,s=self.select(dict(content_locale=tag,medium='web-editorial'))
            self.assertNotIn('ZH-HANT-003',s['applicable_rule_ids']);self.assertNotIn('ZH-HANT-004',s['applicable_rule_ids'])
            self.assertIn('CONTENT-001',s['applicable_rule_ids'])
            self.assertEqual(c['content_locale'],tag)
            self.assertIsNone(c['register'])
        self.assertEqual(self.api().resolve_review_context({'content_locale':'zh-Hant-MO'})['editorial_region'],'MO')
    def test_conflicts_and_types_rejected(self):
        for raw in [{'content_locale':'zh-Hant-TW','editorial_region':'HK'}, {'source_policy':'rewrite'}, {'features':'ruby'}, {'content_locale':42}, {'expression_mode':'huge'}, {'extra':True}]:
            with self.subTest(raw=raw),self.assertRaises((ValueError,TypeError)): self.api().resolve_review_context(raw)
    def test_explicit_modes_and_no_style_default(self):
        c,s=self.select({'content_locale':'zh-Hant-TW','expression_mode':'display','element_role':'title','source_policy':'fixed','medium':'web-editorial'})
        self.assertEqual(c['expression_mode'],'display');self.assertIsNone(c['editorial_style'])
        self.assertNotIn('ZH-HANT-003',s['applicable_rule_ids'])
    def test_research_mapping_and_sources(self):
        path=BASE/'fixtures/research-v020/cases.json';self.assertTrue(path.exists(),'32 fixtures missing')
        cases=json.loads(path.read_text())['cases'];self.assertEqual(len(cases),32)
        self.assertEqual(len({x['proposal_id'] for x in cases}),32)
        self.assertEqual({p:sum(x['priority']==p for x in cases) for p in 'ABC'},{'A':18,'B':10,'C':4})
        sources={s['id'] for s in json.loads((BASE/'sources.json').read_text())['sources']}
        ids={r['id'] for r in self.records()}
        for c in cases:
            self.assertTrue(set(c['source_refs'])<=sources)
            self.assertTrue(set(c['existing_rule_ids'])<=ids)
            for k in ['scope','input','expected','exceptions','method','execution_status','result','evidence','limitations']:self.assertIn(k,c)
    def test_strict_legacy_resolver_preserved(self):
        import locale_resolver
        for tag in ['ja-JP','ko-KR','th-TH','zh-Hant-TW','zh-Hant-HK']:
            c=locale_resolver.resolve_context(tag,'web-ui');before=locale_resolver.resolve_rules(c,ROOT)
            self.api().resolve_review_context({'content_locale':'zh-Hant-MO'})
            self.assertEqual(before,locale_resolver.resolve_rules(c,ROOT))
            with self.assertRaises(ValueError):locale_resolver.resolve_rules(dict(c,expression_mode='display'),ROOT)
