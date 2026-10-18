"""Thai host identities and closed self-contained archives, independent of native acceptance."""
import importlib.util
import hashlib
import io
import json
from pathlib import Path
import re
import posixpath
import shutil
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('builder', ROOT/'tools/build_th.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)

class HostParity(unittest.TestCase):
 def test_rejects_single_language_metadata(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)
   shutil.copytree(ROOT/'plugins/kumihan-th',root/'plugins/kumihan-th')
   (root/'assets').mkdir();shutil.copy(ROOT/builder.LOGO,root/builder.LOGO);shutil.copy(ROOT/'LICENSE',root/'LICENSE')
   path=root/'plugins/kumihan-th/entrypoints/kumihan-th.md'
   path.write_text(re.sub(r'^description:.*$', 'description: English only',path.read_text(),flags=re.M))
   with self.assertRaisesRegex(ValueError,'Thai.*English'):
    builder.plan_outputs(root)
 def test_per_host_manifests(self):
  outputs=builder.plan_outputs(ROOT)
  for host in ('claude','gemini'):
   base=f'plugins/kumihan-th/downloads/{host}/'
   manifest=json.loads(outputs[base+'MANIFEST.json'])
   self.assertEqual(len(manifest['archives']),5)
   for item in manifest['archives']:
    data=outputs[base+item['file']]
    self.assertEqual(item['sha256'],hashlib.sha256(data).hexdigest())
    self.assertEqual(item['bytes'],len(data))
   self.assertEqual(len(outputs[base+'SHA256SUMS.txt'].decode().splitlines()),6)
 def test_host_manifests_and_closed_references(self):
  outputs=builder.plan_outputs(ROOT)
  for path,data in outputs.items():
   if not path.endswith('.zip'):continue
   with zipfile.ZipFile(io.BytesIO(data)) as z:
    names=set(z.namelist());root=next(iter(names)).split('/')[0]+'/'
    if '-Claude-Code-plugin-' in path:
     meta=json.loads(z.read(root+'.claude-plugin/plugin.json'))
     self.assertEqual(meta['displayName'],'KUMIHAN｜ดุลอักษร')
     self.assertEqual(meta['name'],'kumihan-th')
     self.assertEqual(meta['version'],'0.1.0')
    if '-Gemini-CLI-extension-' in path:
     meta=json.loads(z.read(root+'gemini-extension.json'))
     self.assertEqual(meta['name'],'kumihan-th');self.assertEqual(meta['contextFileName'],'GEMINI.md')
     self.assertIn(root+'GEMINI.md',names)
    for name in names:
     if name.endswith('SKILL.md'):
      text=z.read(name).decode();description=next(x for x in text.splitlines() if x.startswith('description:'))
      self.assertRegex(description,r'[\u0e00-\u0e7f]');self.assertRegex(description,r'[A-Za-z]{3}')
      parent=Path(name).parent
      for link in re.findall(r'\]\(([^)]+)\)',text):
       if '://' not in link:self.assertIn((parent/link).as_posix(),names)
    for name in names:
     if name.endswith('.md'):
      for link in re.findall(r'\]\(([^)]+)\)',z.read(name).decode()):
       if '://' not in link:
        self.assertIn(posixpath.normpath((Path(name).parent/link).as_posix()),names)
    for name in names:
     if name.endswith(('.md','.json','.py')):
      text=z.read(name).decode()
      self.assertNotIn('drive.google.com',text)
      self.assertNotIn('BEGIN PRIVATE KEY',text)
