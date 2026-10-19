import hashlib, importlib.util, json, subprocess, tempfile, unittest
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[2]; BASE=ROOT/'plugins/kumihan-satzbild'
spec=importlib.util.spec_from_file_location('satzbild_checks',BASE/'runtime/checks.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class RuntimeTests(unittest.TestCase):
 def test_unknown_locale_stays_unknown(self):
  self.assertIsNone(m.resolve()['locale'])
 def test_explicit_profiles_do_not_infer_financial_context(self):
  for loc in m.LOCALES:
   c=m.resolve(loc);self.assertIsNone(c['currency']);self.assertIsNone(c['timeZone']);self.assertEqual(c['pronoun'],'inherit')
 def test_explicit_context_wins(self):
  c=m.resolve('de-CH',currency='EUR',timeZone='UTC',pronoun='Sie',house_style='UZH');self.assertEqual(c['currency'],'EUR');self.assertEqual(c['timeZone'],'UTC')
 def test_invalid_locale(self):
  for loc in ('de','DE','de-LI','en',False):
   with self.assertRaises(ValueError):m.resolve(loc)
 def test_invalid_mode(self):
  with self.assertRaises(ValueError):m.resolve(mode='autocorrect')
 def test_invalid_medium(self):
  with self.assertRaises(ValueError):m.resolve(medium='guess')
 def test_invalid_context(self):
  with self.assertRaises(ValueError):m.resolve(country='CH')
 def test_representative_preservation(self):
  cases=['Straße Strasse','STRASSE STRAẞE','de-CH: Groß GmbH','Müller Mueller','ä a\u0308','ÄÖÜäöüßẞ','„Er sagt ‚ja‘.“','«‹Zürich›»','»Hausstil«',"O’Reilly's GmbH",'a@example.org https://example.org/a?b=1','500 g 500-g-Beutel','1.000 01234 0.1 1,00 EUR','Jänner Marille Billette','du Sie Ihr','Datenschutzeinstellungen','Barrierefreiheitserklärung','Donaudampfschifffahrt','Soft\u00adhyphen','line\r\nend\u00a0%']
  for text in cases:
   for loc in m.LOCALES:
    with self.subTest(text=text,locale=loc):
     b=text.encode();r=m.review(b,loc);self.assertEqual(r['preservation']['status'],'passed');self.assertEqual(r['original_hash'],hashlib.sha256(b).hexdigest());self.assertEqual(r['findings'],[])
 def test_candidate_mutations_fail(self):
  for a,b in [('ß','ss'),('ẞ','SS'),('ä','a\u0308'),('1.000','1000'),('„Zitat“','«Zitat»'),('du','Sie')]:self.assertEqual(m.review(a.encode(),'de-CH',b.encode())['preservation']['status'],'failed')
 def test_empty_candidate_is_not_missing(self):
  self.assertEqual(m.review(b'a',candidate=b'')['preservation']['status'],'failed')
 def test_bounded_css_candidates_are_not_errors(self):
  r=m.review(b'word-break:break-all; overflow-wrap: anywhere');self.assertEqual(len(r['findings']),2);self.assertEqual({f['status'] for f in r['findings']},{'needs-review'})
 def test_schema(self):
  schema=json.loads((BASE/'schemas/report.schema.json').read_text())
  for loc in (None,*m.LOCALES):jsonschema.validate(m.review(b'word-break:break-all',loc),schema)
 def test_invalid_utf8(self):
  with self.assertRaises(UnicodeDecodeError):m.review(b'\xff')
 def test_cli_preserves_bytes(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'source';p.write_bytes('ä a\u0308 Straße\r\n'.encode());before=p.read_bytes();r=subprocess.run(['python',str(BASE/'runtime/checks.py'),str(p),'--locale','de-CH'],capture_output=True,check=True);self.assertEqual(p.read_bytes(),before);self.assertEqual(json.loads(r.stdout)['locale'],'de-CH')
 def test_research_catalog_and_fixtures(self):
  rules=json.loads((BASE/'rules/catalog.json').read_text());self.assertEqual(len(rules),44);self.assertEqual(len({r['id'] for r in rules}),44)
  sources={s['id'] for s in json.loads((BASE/'sources/public-sources.json').read_text())['sources']}
  for r in rules:
   self.assertTrue(set(r['source_refs'])<=sources);self.assertTrue({'source_ref','authority_type','impact','scope','recommended_action','machine_check','render_check','editorial_review','exception'}<=r.keys())
  fx=json.loads((BASE/'fixtures/acceptance-ledger.json').read_text())['fixtures'];self.assertEqual(len(fx),48);self.assertEqual({x['status'] for x in fx},{'not-checked'})
 def test_host_identity_and_icons(self):
  for f in ('plugin.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json','gemini-extension.json'):
   v=json.loads((BASE/f).read_text());self.assertEqual(v['name'],'kumihan-satzbild');self.assertEqual(v['version'],'0.1.0');self.assertIn(' | ',v['description'])
   if f=='plugin.json':i=v['extensions']['com.openai']['interface']
   elif f=='.codex-plugin/plugin.json':i=v['interface']
   else:i=v
   self.assertEqual(i['displayName'],'KUMIHAN｜Satzbild')
   if 'logo' in i:self.assertTrue((BASE/i['logo']).is_file())
 def test_check_is_nonmutating(self):
  files=[p for p in BASE.rglob('*') if p.is_file() and '__pycache__' not in p.parts];before={str(p):(p.stat().st_mtime_ns,p.read_bytes()) for p in files};subprocess.run(['python',str(ROOT/'tools/build_satzbild.py'),'--check'],check=True,capture_output=True);self.assertEqual(before,{str(p):(p.stat().st_mtime_ns,p.read_bytes()) for p in files})
