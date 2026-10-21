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
  """Guides (tools/build_install_guides.py) link exactly the host's verified Release assets."""
  import re
  m=json.loads((BASE/'downloads/MANIFEST.json').read_text())
  facts=json.loads((ROOT/'assets/edition-versions.json').read_text())['editions']['ko']
  released={a['name']:a for a in facts['verified_assets']}
  sums=next(x['url'] for x in facts['verified_metadata'] if x['name']=='SHA256SUMS.txt')
  for host,key in [('chatgpt','chatgpt-codex'),('claude','claude'),('gemini','gemini')]:
   names={Path(x['file']).name for x in m['archives'] if x['host']==key}
   self.assertEqual(len(names),5)
   self.assertTrue(names<=set(released),names-set(released))
   for x in m['archives']:
    if x['host']==key:self.assertEqual(released[Path(x['file']).name]['sha256'],x['sha256'],x['file'])
   expected={released[n]['url'] for n in names}|{sums}
   for suffix in ['', '.en','.ja']:
    body=(ROOT/f'docs/install-ko-{host}{suffix}.html').read_text()
    links=set(re.findall(r'href="([^"]*/releases/download/[^"]*)"',body))
    self.assertEqual(links,expected,f'install-ko-{host}{suffix}')
    if host!='chatgpt':self.assertIn(f'/kumihan-geuljjaim-{host}-bundle-v0.1.0.zip"',body)
    self.assertNotIn('/downloads/plugins/',body)
    self.assertNotIn('/downloads/skills/',body)
