import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
B=ROOT/'plugins/kumihan-ar'
NAMES=('kumihan-ar','kumihan-ar-web','kumihan-ar-documents','kumihan-ar-review')
class DistributionTests(unittest.TestCase):
 def test_fifteen_exact_names_and_bytes(self):
  expected={'kumihan-ar-GPT-Codex-plugin-v0.1.0.zip','kumihan-ar-Claude-Code-plugin-v0.1.0.zip','kumihan-ar-Gemini-CLI-extension-v0.1.0.zip'}
  for n in NAMES:
   expected.update((n+'-v0.1.0.zip',n+'-Claude-skill-v0.1.0.zip',n+'-Gemini-Apps-skill-v0.1.0.zip'))
  manifest=json.loads((B/'downloads/MANIFEST.json').read_text());self.assertEqual(manifest['product'],'KUMIHAN｜نضيد')
  self.assertEqual({x['file'] for x in manifest['archives']},expected)
  self.assertEqual({p.name for p in (B/'downloads').rglob('*.zip')},expected)
  for x in manifest['archives']:
   raw=(B/'downloads'/x['file']).read_bytes();self.assertEqual(len(raw),x['bytes']);self.assertEqual(hashlib.sha256(raw).hexdigest(),x['sha256'])
 def test_every_archive_inventory_paths_and_standalone_runtime(self):
  for path in (B/'downloads').glob('*.zip'):
   with self.subTest(archive=path.name), zipfile.ZipFile(path) as z:
    names=z.namelist();roots={p.split('/')[0] for p in names};self.assertEqual(len(roots),1);prefix=next(iter(roots))+'/'
    for n in names:self.assertFalse(n.startswith('/'));self.assertNotIn('..',Path(n).parts)
    inventories=[n for n in names if n.endswith('/inventory.json')]
    for inv in inventories:
     data=json.loads(z.read(inv));base=inv[:-len('inventory.json')]
     entries=data['files']; self.assertTrue(entries)
     for entry in entries:
      raw=z.read(base+entry['path']);self.assertEqual(len(raw),entry['bytes']);self.assertEqual(hashlib.sha256(raw).hexdigest(),entry['sha256'])
     actual={p[len(base):] for p in names if p.startswith(base)}
     # A plugin root inventory covers all nested skill inventories too.
     self.assertEqual(actual,{e['path'] for e in entries}|{'inventory.json'})
    if '-plugin-' not in path.name and '-extension-' not in path.name:
     for required in ('SKILL.md','runtime/check_source.py','references/contract.md','rules/catalog.json','locales/ar.json','LICENSE'):
      self.assertIn(prefix+required,names)
     with tempfile.TemporaryDirectory() as t:
      z.extractall(t);sample=Path(t)/'sample.html';sample.write_text('<html lang="ar" dir="rtl"><p>نص</p></html>')
      result=subprocess.run([sys.executable,str(Path(t)/prefix/'runtime/check_source.py'),str(sample)],capture_output=True,text=True)
      self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(json.loads(result.stdout)['rendered'],'not-checked')
 def test_host_contracts_and_bilingual_metadata(self):
  def bilingual(s):
   self.assertLess(re.search('[\u0600-\u06ff]',s).start(),re.search('[A-Za-z]{3}',s).start())
  for filename in ('plugin.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json','gemini-extension.json'):
   d=json.loads((B/filename).read_text());self.assertEqual(d['name'],'kumihan-ar');self.assertEqual(d['version'],'0.1.0');bilingual(d['description'])
  claude=json.loads((B/'.claude-plugin/plugin.json').read_text());self.assertNotIn('displayName',claude)
  gemini=json.loads((B/'gemini-extension.json').read_text());self.assertEqual(gemini['contextFileName'],'GEMINI.md')
  codex=json.loads((B/'.codex-plugin/plugin.json').read_text());self.assertEqual(codex['interface']['displayName'],'KUMIHAN｜نضيد')
  for key in ('shortDescription','longDescription'):bilingual(codex['interface'][key])
  for name in NAMES:
   text=(B/'skills'/name/'SKILL.md').read_text();self.assertIn('name: '+name,text);bilingual(re.search('^description: (.+)$',text,re.M).group(1));self.assertIn('Audit is read-only',text)
 def test_scope_catalog_truthful(self):
  d=json.loads((B/'rules/catalog.json').read_text());self.assertEqual(len(d['rules']),36)
  self.assertEqual(sum(x['status']=='implemented-and-tested' for x in d['rules']),10)
  for r in d['rules']:
   self.assertTrue(all(u.startswith('https://') for u in r['source_urls']))
   if r['status']=='implemented-and-tested':self.assertTrue((ROOT/r['test']).is_file())
 def test_generator_is_fresh_and_reproducible(self):
  spec=importlib.util.spec_from_file_location('build_ar',ROOT/'tools/build_ar.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  a=m.plan_outputs();self.assertEqual(a,m.plan_outputs());self.assertFalse(m.generated_files()-set(a))
  for p,data in a.items():self.assertEqual((ROOT/p).read_bytes(),data,p)
 def test_per_host_five_packages(self):
  for host in ('codex','claude','gemini'):
   d=json.loads((B/'downloads'/host/'MANIFEST.json').read_text());self.assertEqual(len(d['archives']),5)
if __name__=='__main__':unittest.main()
