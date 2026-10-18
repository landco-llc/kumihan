import unittest,json,hashlib,zipfile
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'plugins/kumihan-compasso'
spec=spec_from_file_location('compasso_check',BASE/'runtime/checks.py');checker=module_from_spec(spec);spec.loader.exec_module(checker)
class Compasso(unittest.TestCase):
 def test_catalog(self):
  r=json.loads((BASE/'rules/catalog.json').read_text());self.assertEqual(len(r),36);self.assertEqual(len({x['id'] for x in r}),36)
 def test_region(self):
  for a in ('pt','pt-BR','pt-PT','pt-AO','pt-MZ'):self.assertEqual(checker.inspect('AÇÃO'.encode(),a)['locale'],a)
  with self.assertRaises(ValueError):checker.inspect(b'a','fr-FR')
 def test_source_preservation(self):
  b='AÇÃO · 1.234,56 · “texto”'.encode();self.assertEqual(checker.inspect(b,'pt-PT',candidate=b)['preservation'],'passed');self.assertEqual(checker.inspect(b,'pt-BR',candidate=b'other')['preservation'],'failed')
 def test_checker_advisory(self):
  data=checker.inspect(b'20km 7% word-break: break-all','pt-BR');self.assertEqual(len(data['findings']),3);self.assertEqual(data['rendering'],'not-checked')
 def test_plugins(self):
  for p in ('plugin.json','.claude-plugin/plugin.json','gemini-extension.json'):
   d=json.loads((BASE/p).read_text());self.assertEqual(d['name'],'kumihan-compasso');self.assertEqual(d['version'],'0.1.0');self.assertIn(' | ',d['description'])
 def test_skills(self):
  for n in ('kumihan-compasso','kumihan-compasso-web','kumihan-compasso-documents','kumihan-compasso-review'):
   p=BASE/'skills'/n;self.assertTrue((p/'SKILL.md').exists());self.assertTrue((p/'assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png').exists());self.assertTrue((p/'rules/catalog.json').exists())
 def test_archives(self):
  d=BASE/'downloads';names=list(d.glob('*.zip'));self.assertEqual(len(names),15)
  manifest=json.loads((d/'MANIFEST.json').read_text());self.assertEqual(len(manifest['packages']),15)
  for record in manifest['packages']:
   p=d/record['name'];self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),record['sha256']);self.assertIn('-v0.1.0.zip',p.name)
   with zipfile.ZipFile(p) as z:self.assertTrue(z.testzip() is None)
 def test_site(self):
  for lang in ('','.en','.ja'):
   page=ROOT/f'kumihan-pt{lang}.html';s=page.read_text();self.assertIn('KUMIHAN｜Compasso',s);self.assertIn('intro-strip',s);self.assertIn('status-section',s)
   for host in ('chatgpt','claude','gemini'):
    g=(ROOT/f'docs/install-compasso-{host}{lang}.html').read_text();self.assertIn('｜Compasso',g);self.assertIn('content-layout',g);self.assertNotIn('v0.1.1',g)
if __name__=='__main__':unittest.main()
