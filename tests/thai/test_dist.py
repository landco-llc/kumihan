"""Audit actual archive bytes and independently installable support trees."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import unittest
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('build_th', ROOT/'tools/build_th.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ThaiDistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = builder.plan_outputs(ROOT)

    def test_generated_bytes_and_repeatability(self):
        self.assertEqual(self.outputs, builder.plan_outputs(ROOT))
        for path,data in self.outputs.items():
            self.assertEqual((ROOT/path).read_bytes(), data, path)

    def test_fifteen_safe_archives_and_inventories(self):
        archives = {p:b for p,b in self.outputs.items() if p.endswith('.zip')}
        self.assertEqual(len(archives), 15)
        self.assertEqual(len({Path(p).name for p in archives}), 15)
        for path,data in archives.items():
            self.assertTrue(path.endswith('-v0.1.1.zip'), path)
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                names = z.namelist()
                self.assertEqual(len(names),len(set(names)))
                for info in z.infolist():
                    self.assertFalse(Path(info.filename).is_absolute())
                    self.assertNotIn('..',Path(info.filename).parts)
                    self.assertEqual(info.external_attr >> 16,0o100644)
                    self.assertEqual(info.date_time,(2026,10,18,0,0,0))
                root = names[0].split('/')[0]+'/'
                inventory = json.loads(z.read(root+'inventory.json'))
                self.assertEqual(set(names)-{root+'inventory.json'}, {root+f['path'] for f in inventory['files']})
                for entry in inventory['files']:
                    content = z.read(root+entry['path'])
                    self.assertEqual(len(content), entry['bytes'])
                    self.assertEqual(hashlib.sha256(content).hexdigest(),entry['sha256'])
                if '/skills/' in path:
                    for support in ('SKILL.md','rules/catalog.json','sources.json','runtime/check_source.py','schemas/report.schema.json','LICENSE'):
                        self.assertIn(root+support,names)

    def test_standalone_runtime_without_repository(self):
        source = '😀น้ำ กำลัง\u200bทดสอบ\r\n'
        for path,data in self.outputs.items():
            if not path.endswith('.zip') or '/skills/' not in path:
                continue
            with tempfile.TemporaryDirectory() as temporary:
                folder = Path(temporary)
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    z.extractall(folder)
                skill = next(folder.iterdir())
                original = folder/'original.txt'
                candidate = folder/'candidate.txt'
                original.write_bytes(source.encode())
                candidate.write_bytes(source.encode())
                command = [sys.executable, str(skill/'runtime/check_source.py'), str(original), str(candidate)]
                passed = subprocess.run(command,cwd=folder,capture_output=True,text=True)
                self.assertEqual(passed.returncode,0,passed.stderr)
                report = json.loads(passed.stdout)
                self.assertEqual(report['original']['sha256_utf8'],hashlib.sha256(source.encode()).hexdigest())
                candidate.write_bytes(source.replace('\u200b','').encode())
                failed = subprocess.run(command,cwd=folder,capture_output=True,text=True)
                self.assertEqual(failed.returncode,1,failed.stderr)
                self.assertEqual(json.loads(failed.stdout)['status'],'failed')
                self.assertEqual(original.read_bytes(),source.encode())

    def test_manifest_checksums_and_logo(self):
        base = 'plugins/kumihan-th/downloads/'
        manifest = json.loads(self.outputs[base+'MANIFEST.json'])
        self.assertEqual(manifest['version'],'0.1.1')
        for entry in manifest['archives']:
            data = self.outputs[base+entry['file']]
            self.assertEqual(hashlib.sha256(data).hexdigest(),entry['sha256'])
        sums = self.outputs[base+'SHA256SUMS.txt'].decode().splitlines()
        self.assertEqual(len(sums),16)
        by_name = {Path(p).name:data for p,data in self.outputs.items() if p.startswith(base) and (p.endswith('.zip') or p == base+'MANIFEST.json')}
        for line in sums:
            sha,name=line.split('  ')
            self.assertEqual(hashlib.sha256(by_name[name]).hexdigest(),sha)
        self.assertEqual(hashlib.sha256(self.outputs['plugins/kumihan-th/'+builder.LOGO]).hexdigest(),builder.LOGO_SHA)


if __name__ == '__main__':
    unittest.main()
