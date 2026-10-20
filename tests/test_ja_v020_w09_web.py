"""Observed W09 Web evidence: codepoints, line geometry, interaction and scope."""
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'docs/development/ja-v020-20261020/qa/w09/evidence/web'

class W09WebEvidence(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.observations=json.loads((EVIDENCE/'web-observations.json').read_text())
 def test_twenty_state_pairs_exact_dom_and_required_fields(self):
  rows=self.observations['web']
  self.assertEqual(len(rows),40)
  for before in (x for x in rows if x['stage']=='before'):
   after=next(x for x in rows if x['stage']=='after' and (x['width'],x['state'])==(before['width'],before['state']))
   self.assertEqual(before['domText'],after['domText'])
   for key in ['protectedExact','labelExact','dateExact','placeExact','eventExact','focus']:
    self.assertTrue(after[key],(after['width'],after['state'],key))
   self.assertEqual(after['document']['scrollWidth'],after['width'])
   self.assertLessEqual(after['scrollWidth'],after['clientWidth'])
   self.assertIn('操作デモを実行しました。',after['status'])
   for stage in ['before','after']:
    self.assertTrue((EVIDENCE/f"web-{stage}-{before['width']}-{before['state']}.png").is_file())
 def test_local_terms_share_rendered_line(self):
  for row in self.observations['web']:
   if row['stage']!='after':continue
   for selector,term in [('#reading','読む前に'),('.note','できません。'),('.note','認定しません。')]:
    regions=[r for r in row['regionLines'][selector] if term in r['text']]
    self.assertTrue(regions)
    for r in regions:
     self.assertTrue(any(term in line['text'] for line in r['lines']),(row['width'],row['state'],term))
 def test_baseline_reproduces_three_original_splits(self):
  before=next(r for r in self.observations['web'] if r['stage']=='before' and r['width']==320 and r['state']=='css200')
  for selector,term in [('#reading','読む前に'),('.note','できません。'),('.note','認定しません。')]:
   region=next(r for r in before['regionLines'][selector] if term in r['text'])
   self.assertFalse(any(term in line['text'] for line in region['lines']))
 def test_native_zoom_disclosed_and_negative_kept(self):
  self.assertTrue(any('Native browser text zoom not-checked' in x for x in self.observations['limits']))
  self.assertGreater(self.observations['negative']['button']['scrollWidth'],self.observations['negative']['button']['clientWidth'])
