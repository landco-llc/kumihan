import hashlib, importlib.util, json, subprocess, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'plugins/kumihan-equilibrio'
class ItalianTests(unittest.TestCase):
 def helper(self):
  p=BASE/'runtime/checks.py';self.assertTrue(p.exists(),'Italian helper required')
  s=importlib.util.spec_from_file_location('italian_checks',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
 def test_context_axes(self):
  m=self.helper();self.assertIsNone(m.resolve()['locale'])
  for loc in ('it-IT','it-CH'):
   c=m.resolve(loc,house_style='EU',content_role='quotation',editorial_voice='Lei');self.assertEqual(c['house_style'],'EU');self.assertIsNone(c['currency']);self.assertEqual(c['content_role'],'quotation')
  for loc in ('it_CH','en','it',False):
   with self.assertRaises(ValueError):m.resolve(loc)
 def test_preservation_counterexamples(self):
  m=self.helper()
  texts=['perché caffè È PERCHÉ','e è da dà si sì','qual è', 'un po’ / Il Po','«qual’è»','café São Tomé München','se stesso / sé stesso','Se stessi meglio, verrei.','ad esempio od', '«Una forma “aperta”»','“Una forma ‘aperta’”','dell’\narchitettura','caffè caffe\u0300',"https://example.org/a?q='e'",'''{"id":"E'","price":"1.234"}''',"const x = 'caffe';",'ISBN 01234 1.234 CHF 0.125','2026-10-19T12:00:00Z','1º 1° 20 °C','tu Lei voi ə *','à è é ì ò ù À È É Ì Ò Ù']
  for text in texts:
   for loc in ('it-IT','it-CH'):
    with self.subTest(text=text,locale=loc):
     b=text.encode();r=m.review(b,loc);self.assertEqual(r['preservation']['status'],'passed');self.assertEqual(r['original_hash'],hashlib.sha256(b).hexdigest());self.assertEqual(r['findings'],[])
 def test_mutations_detected(self):
  m=self.helper()
  for a,b in [('caffè','caffe\u0300'),('Po','po’'),('1.234','1234'),('è','é'),('dell’\na','della\na'),('a','')]:self.assertEqual(m.review(a.encode(),candidate=b.encode())['preservation']['status'],'failed')
 def test_css_is_only_candidate_evidence(self):
  r=self.helper().review(b'p {word-break: break-all}')
  self.assertEqual(r['findings'][0]['status'],'needs-review');self.assertEqual(r['rendering'],'not-checked')
  self.assertEqual(r['findings'][0]['rule_id'],'R21');self.assertFalse(r['findings'][0]['edits_authorized'])
 def test_research_registration_is_not_success(self):
  self.assertTrue((BASE/'rules/catalog.json').exists(),'Italian research catalog required')
  rules=json.loads((BASE/'rules/catalog.json').read_text());self.assertEqual(len(rules),40)
  sources={s['id'] for s in json.loads((BASE/'sources/public-sources.json').read_text())['sources']}
  for r in rules:
   self.assertTrue(set(r['source_refs'])<=sources);self.assertTrue({'severity','context','scope','expected','status'}<=r.keys())
  cases=json.loads((BASE/'fixtures/acceptance-ledger.json').read_text())['fixtures'];self.assertEqual(len(cases),48);self.assertEqual({f['status'] for f in cases},{'not-checked'})
 def test_cli_read_only(self):
  self.helper()
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'original';p.write_bytes('caffe\u0300\r\nPo'.encode());before=p.read_bytes()
   r=subprocess.run(['python',str(BASE/'runtime/checks.py'),str(p),'--locale','it-CH'],capture_output=True,check=True);self.assertEqual(p.read_bytes(),before);self.assertEqual(json.loads(r.stdout)['locale'],'it-CH')
