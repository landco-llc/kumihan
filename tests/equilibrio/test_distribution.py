import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import tempfile
import unittest
import zipfile
import yaml
ROOT=Path(__file__).resolve().parents[2]
class DistributionTests(unittest.TestCase):
 def builder(self):
  p=ROOT/'tools/build_equilibrio.py';self.assertTrue(p.exists(),'Equilibrio builder must exist')
  spec=importlib.util.spec_from_file_location('build_equilibrio',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
 def test_exact_matrix_and_manifest(self):
  m=self.builder();outputs=m.plan_outputs();self.assertEqual(outputs,m.plan_outputs())
  prefix='plugins/kumihan-equilibrio/downloads/';files={p[len(prefix):]:b for p,b in outputs.items() if p.startswith(prefix)}
  names=set()
  for host,plugin,skill in [('GPT-Codex','GPT-Codex-plugin','GPT-Codex-skill'),('Claude','Claude-Code-plugin','Claude-skill'),('Gemini','Gemini-CLI-extension','Gemini-Apps-skill')]:
   names.add('kumihan-equilibrio-'+plugin+'-v0.1.0.zip')
   for suffix in ('','-web','-documents','-review'):names.add('kumihan-equilibrio'+suffix+'-'+skill+'-v0.1.0.zip')
  self.assertEqual(set(files),names|{'MANIFEST.json','SHA256SUMS.txt'})
  manifest=json.loads(files['MANIFEST.json']);self.assertEqual(len(manifest['archives']),15)
  for item in manifest['archives']:
   b=files[item['file']];self.assertEqual(item['sha256'],hashlib.sha256(b).hexdigest());self.assertEqual(item['bytes'],len(b))
  for line in files['SHA256SUMS.txt'].decode().splitlines():
   digest,name=line.split('  ');self.assertEqual(hashlib.sha256(files[name]).hexdigest(),digest)
  self.assertEqual(len(files['SHA256SUMS.txt'].decode().splitlines()),16)
 def test_archive_closure_host_roots_and_safety(self):
  outputs=self.builder().plan_outputs()
  for path,b in outputs.items():
   if not path.endswith('.zip'):continue
   with zipfile.ZipFile(io.BytesIO(b)) as z:
    names=z.namelist();self.assertIsNone(z.testzip());self.assertEqual(len(names),len(set(names)))
    self.assertTrue(all(not n.startswith('/') and '..' not in Path(n).parts and '\\' not in n for n in names))
    self.assertFalse(any('kumihan-zilu' in n or 'kumihan-th/' in n for n in names))
    if 'Gemini-CLI-extension' in path:self.assertIn('gemini-extension.json',names)
    if '-skill-' in path:self.assertEqual(sum(n.endswith('/SKILL.md') for n in names),1)
    else:self.assertEqual(sum(n.endswith('/SKILL.md') for n in names),4)
    for n in names:
     if n.endswith('SKILL.md'):
      text=z.read(n).decode();front=yaml.safe_load(text.split('---')[1]);self.assertIn(' | ',front['description'])
      parent=Path(n).parent
      for target in re.findall(r'\]\(([^)]+)\)',text):self.assertIn((parent/target).as_posix(),names)
     if n.endswith('/inventory.json') or n=='inventory.json':
      inv=json.loads(z.read(n));parent=Path(n).parent
      for f in inv['files']:
       value=z.read((parent/f['path']).as_posix());self.assertEqual(hashlib.sha256(value).hexdigest(),f['sha256'])
 def test_unsafe_members_rejected(self):
  m=self.builder()
  for path in ['/tmp/a','../escape','a/../../b','a\\b']:
   with self.assertRaises(ValueError):m.archive({path:b'bad'})
 def test_symlink_source_rejected(self):
  m=self.builder()
  with tempfile.TemporaryDirectory() as d:
   import shutil
   root=Path(d);shutil.copytree(ROOT/'plugins/kumihan-equilibrio',root/'plugins/kumihan-equilibrio');shutil.copytree(ROOT/'assets',root/'assets');shutil.copy(ROOT/'LICENSE',root/'LICENSE')
   (root/'plugins/kumihan-equilibrio/references/escape').symlink_to(ROOT/'README.md')
   with self.assertRaises(ValueError):m.plan_outputs(root)
 def test_missing_reference_rejected(self):
  m=self.builder()
  with tempfile.TemporaryDirectory() as d:
   import shutil
   root=Path(d);shutil.copytree(ROOT/'plugins/kumihan-equilibrio',root/'plugins/kumihan-equilibrio');(root/'assets').mkdir();shutil.copy(ROOT/m.LOGO,root/m.LOGO);shutil.copy(ROOT/'LICENSE',root/'LICENSE')
   (root/'plugins/kumihan-equilibrio/references/web.md').unlink()
   with self.assertRaises(ValueError):m.plan_outputs(root)
 def test_builder_check_nonwriting(self):
  import subprocess
  base=ROOT/'plugins/kumihan-equilibrio';files=[p for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
  before={p:(p.stat().st_mtime_ns,hashlib.sha256(p.read_bytes()).hexdigest()) for p in files}
  subprocess.run(['python',str(ROOT/'tools/build_equilibrio.py'),'--check'],check=True,capture_output=True)
  self.assertEqual(before,{p:(p.stat().st_mtime_ns,hashlib.sha256(p.read_bytes()).hexdigest()) for p in files})
