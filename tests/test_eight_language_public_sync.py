"""Public release scope: eight non-English v0.1.0 product sources and their ZIPs."""
import hashlib
import json
from pathlib import Path
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ED = {'tr':'ahenk','ms':'jalin','hu':'arany','cs':'soulad','la':'concinnitas',
      'he':'miktsav','el':'metro','nl':'zetwerk'}

class EightProductSync(unittest.TestCase):
    def test_scope_excludes_english_measure(self):
        from sys import path
        path.insert(0,str(ROOT/'tools'))
        import edition_versions
        self.assertNotIn('en',edition_versions.catalogue())
        # The English edition may exist from an unrelated upstream change; this PR must not alter it.

    def test_eight_source_packages_and_checksums(self):
        facts=json.loads((ROOT/'assets/edition-versions.json').read_text())['editions']
        for code, slug in ED.items():
            with self.subTest(code=code):
                d=ROOT/'plugins'/('kumihan-'+slug)
                self.assertEqual(facts[code]['source_version'],'0.1.0')
                self.assertEqual(json.loads((d/'plugin.json').read_text())['locale'],code)
                self.assertFalse((d/'GOAL.md').exists())
                self.assertEqual(sum(x.name=='SKILL.md' for x in (d/'skills').rglob('SKILL.md')),4)
                m=json.loads((d/'downloads/manifest.json').read_text())
                self.assertNotIn('GOAL.md',{x['path'] for x in m['source_files']})
                sh=hashlib.sha256(json.dumps(m['source_files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
                self.assertEqual(m['source_sha256'],sh)
                self.assertEqual(len(m['packages']),15)
                sums={line.split('  ',1)[1]:line.split('  ',1)[0]
                      for line in (d/'downloads/SHA256SUMS').read_text().splitlines()}
                self.assertEqual(len(sums),15)
                for row in m['packages']:
                    file=d/'downloads'/row['file']
                    self.assertTrue(file.is_file(),file)
                    self.assertEqual(file.stat().st_size,row['bytes'])
                    self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(),row['sha256'])
                    self.assertEqual(sums[row['file']],row['sha256'])
                    with zipfile.ZipFile(file) as z:
                        self.assertNotIn('GOAL.md',' '.join(z.namelist()))
                        self.assertEqual(len(z.namelist()),row['members'])
