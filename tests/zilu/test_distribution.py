import hashlib
import importlib.util
import io
import json
from pathlib import Path, PurePosixPath
import stat
import unittest
import zipfile
import yaml

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'plugins/kumihan-zilu'

class Distribution(unittest.TestCase):
    def builder(self):
        self.assertTrue((ROOT/'tools/build_zilu.py').exists(),'distribution builder missing')
        spec=importlib.util.spec_from_file_location('build_zilu',ROOT/'tools/build_zilu.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

    def test_archives_are_reproducible_safe_and_self_contained(self):
        m=self.builder();a=m.plan_outputs();self.assertEqual(a,m.plan_outputs())
        zips={p:b for p,b in a.items() if p.endswith('.zip')};self.assertEqual(len(zips),15)
        for path,raw in zips.items():
            self.assertIn('v0.1.0',path)
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                self.assertIsNone(z.testzip());names=z.namelist();self.assertEqual(len(names),len(set(names)))
                for info in z.infolist():
                    p=PurePosixPath(info.filename);self.assertFalse(p.is_absolute());self.assertNotIn('..',p.parts)
                    self.assertFalse(stat.S_ISLNK(info.external_attr>>16))
                    if not info.filename.endswith('.png'):
                        self.assertNotIn(b'docs.google.com',z.read(info));self.assertNotIn(b'drive.google.com',z.read(info))
                for skill in [n for n in names if n.endswith('/SKILL.md')]:
                    prefix=skill[:-len('SKILL.md')];front=yaml.safe_load(z.read(skill).decode().split('---')[1])
                    self.assertTrue(front['name'].startswith('kumihan-zilu'))
                    self.assertIn(prefix+'scripts/checks.py',names)
                    inv=json.loads(z.read(prefix+'inventory.json'))
                    for member in inv['files']:
                        data=z.read(prefix+member['path'])
                        self.assertEqual(hashlib.sha256(data).hexdigest(),member['sha256'])

    def test_bundle_root_evidence_paths_exist(self):
        outputs=self.builder().plan_outputs()
        for path,raw in outputs.items():
            if not path.endswith('.zip') or '-skill-' in path:
                continue
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                prefix='' if '-gemini-extension-' in path else 'kumihan-zilu/'
                self.assertIn(prefix+'rules/zh-hans-cn.json',z.namelist())
                self.assertIn(prefix+'sources.json',z.namelist())

    def test_manifest_hashes_and_authority(self):
        outputs=self.builder().plan_outputs()
        manifest=json.loads(outputs['plugins/kumihan-zilu/downloads/MANIFEST.json'])
        for r in manifest['archives']:
            data=outputs['plugins/kumihan-zilu/downloads/'+r['file']]
            self.assertEqual(hashlib.sha256(data).hexdigest(),r['sha256'])
        rules=json.loads((BASE/'rules/zh-hans-cn.json').read_text());self.assertEqual(len(rules),36)
        sources={s['id'] for s in json.loads((BASE/'sources.json').read_text())['sources']}
        for r in rules:
            self.assertLessEqual(set(r['source_ids']),sources);self.assertFalse(r['autofix_allowed'])
        root=json.loads((BASE/'plugin.json').read_text())
        ui=root['extensions']['com.openai']['interface']
        self.assertEqual(ui['displayName'],'KUMIHAN｜字律');self.assertLessEqual(len(ui['shortDescription']),30)
