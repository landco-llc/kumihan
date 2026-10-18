"""Host packages must be independently installable and correctly routed."""
import json
from pathlib import Path
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'plugins/kumihan-geuljjaim'
class HostPackages(unittest.TestCase):
 def test_fifteen_unique_archives(self):
  m=json.loads((BASE/'downloads/MANIFEST.json').read_text())
  self.assertEqual(len(m['archives']),15)
  self.assertEqual(len({Path(x['file']).name for x in m['archives']}),15)
  for host in ['chatgpt-codex','claude','gemini']:
   self.assertEqual(sum(x['host']==host for x in m['archives']),5)
 def test_native_bundle_layouts(self):
  for host,manifest in [('claude','.claude-plugin/plugin.json'),('gemini','gemini-extension.json')]:
   archive=BASE/f'downloads/{host}/kumihan-geuljjaim-{host}-bundle-v0.1.0.zip'
   self.assertTrue(archive.is_file())
   with zipfile.ZipFile(archive) as z:
    prefix='kumihan-geuljjaim/'
    m=json.loads(z.read(prefix+manifest))
    self.assertEqual(m['name'],'kumihan-geuljjaim');self.assertEqual(m['version'],'0.1.0')
    self.assertEqual(len([p for p in z.namelist() if p.endswith('/SKILL.md')]),4)
    self.assertNotIn('mcpServers',m)
    if host=='gemini':self.assertIn(prefix+m['contextFileName'],z.namelist())
 def test_guides_link_their_host_packages(self):
  for host in ['claude','gemini']:
   for suffix in ['', '.en','.ja']:
    body=(ROOT/f'docs/install-ko-{host}{suffix}.html').read_text()
    self.assertIn(f'/downloads/{host}/kumihan-geuljjaim-{host}-bundle-v0.1.0.zip',body)
    self.assertNotIn('/downloads/plugins/',body)
    self.assertNotIn('/downloads/skills/',body)
