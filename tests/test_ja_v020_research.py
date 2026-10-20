"""Research contract checks; these do not certify rendered or native output."""
import unittest,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REF=ROOT/'skills/kumihan/references'
class JapaneseResearch(unittest.TestCase):
 def test_context_and_evidence(self):
  text=(REF/'typography-context.md').read_text()
  for term in ['readingTask','declared','inferred','unknown','exact-repeat','authorized-derived','decorative-echo','evidence_refs','not-checked']:
   self.assertIn(term,text)
 def test_no_unsafe_recipe_claims(self):
  web=(REF/'web-recipes.md').read_text(); doc=(REF/'document-recipes.md').read_text()
  for term in ['Every property here degrades safely','Headings and display copy only. Not for body text.']:
   self.assertNotIn(term,web)
  for term in ['the most common cause','usually easier to read than mincho','figure, table, .keep-together']:
   self.assertNotIn(term,doc)
 def test_cases_are_complete_and_scoped(self):
  cases=json.loads((ROOT/'tests/fixtures/ja_v020/cases.json').read_text())['cases']
  self.assertEqual([c['caseId'] for c in cases],[f'PV-{i:03}' for i in range(1,31)])
  for c in cases:
   self.assertTrue(c['expectedScopedResults']); self.assertTrue(c['wrongDecisionToAvoid'])
   self.assertEqual(c['execution']['observedResult'],None)
   self.assertEqual(c['execution']['status'],'not-run')
   import hashlib
   path=ROOT/c['fixture']['artifactPath']
   self.assertTrue(path.is_file())
   self.assertEqual('sha256:'+hashlib.sha256(path.read_bytes()).hexdigest(),c['fixture']['artifactDigest'])
   self.assertEqual(json.loads(path.read_text())['protectedSource'],c['fixture']['protectedSource'])
   ids={r['id'] for r in json.loads((ROOT/'skills/kumihan/rules/catalog.json').read_text())}
   self.assertEqual(len(ids),39)
   for result in c['expectedScopedResults']:
    self.assertIn(result['existingRuleId'],ids)
    self.assertIn(result['method'],['static','rendered','assisted','manual'])
    self.assertIn(result['expectedResult'],['passed','failed','needs-review','not-checked','unsupported','waived','not-applicable'])
    self.assertTrue(result['scope'])
    self.assertTrue(result['minimumEvidenceIfExecuted'])
 def test_entries_route_context(self):
  for name in ['kumihan','kumihan-web','kumihan-documents','kumihan-review']:
   self.assertIn('typography-context.md',(ROOT/'skills'/name/'SKILL.md').read_text())

class SourceTransition(unittest.TestCase):
 def test_no_active_file_deletion_or_outside_scope(self):
  import sys,tempfile,hashlib
  sys.path.insert(0,str(ROOT/'tools'))
  from ja_v020_preservation import admitted,RECORD,allowed
  self.assertFalse(allowed('LICENSE'));self.assertFalse(allowed('plugins/kumihan-ziheng/plugin.json'))
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); record=root/RECORD;record.parent.mkdir(parents=True)
   for path in ['plugin.json','skills/kumihan/SKILL.md','skills/kumihan/inventory.json']:
    record.write_text(json.dumps({'authority':'KUMI-JA-V020-RESEARCH-WG-20261020-01','paths':{path:{'before':'a'*64,'after':None}}}))
    self.assertFalse(admitted(root,path,'a'*64))
   path='plugin.json';target=root/path;target.write_text('fixed')
   record.write_text(json.dumps({'authority':'KUMI-JA-V020-RESEARCH-WG-20261020-01','paths':{path:{'before':'a'*64,'after':hashlib.sha256(b'fixed').hexdigest()}}}))
   self.assertTrue(admitted(root,path,'a'*64));target.write_text('mutated');self.assertFalse(admitted(root,path,'a'*64))
