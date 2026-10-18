import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'plugins/kumihan-geuljjaim'

class ProductTests(unittest.TestCase):
    def checks(self):
        path = BASE/'runtime/checks.py'
        self.assertTrue(path.exists(), 'Korean read-only runtime required')
        spec = importlib.util.spec_from_file_location('ko_checks', path)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        return module

    def test_exact_bytes_never_normalize(self):
        c = self.checks()
        for text in ['한글 👩🏽\u200d💻\r\n 13,000원', '한글\n3개']:
            raw = text.encode()
            self.assertEqual(c.check_preservation(raw, raw)['status'], 'passed')
            self.assertEqual(c.check_preservation(raw, raw+b' ')['status'], 'failed')
        with self.assertRaises(TypeError): c.check_preservation('한', '한')

    def test_four_candidates_and_safe_exceptions(self):
        c = self.checks()
        cases = [('KO-ORTH-001','서울 에서 출발','서울에서 출발'),
                 ('KO-ORTH-002','할수 있다','할 수 있다'),
                 ('KO-TYPE-010','13,000\n원','13,000원'),
                 ('KO-TYPE-001','ᄒ\nᅡᆫ','한')]
        for rid, positive, negative in cases:
            self.assertIn(rid, [f['rule_id'] for f in c.review_text(positive, 'ko-KR', 'prose')])
            self.assertNotIn(rid, [f['rule_id'] for f in c.review_text(negative, 'ko-KR', 'prose')])
            for role in ['name','code','url','quote','protected']:
                self.assertEqual(c.review_text(positive, 'ko-KR', role), [])
        self.assertEqual(c.review_text('3개 / 3 개', 'ko-KR', 'prose'), [])
        with self.assertRaises(ValueError): c.review_text('한글','ja-JP','prose')

    def test_catalog_fixture_contract(self):
        rules=json.loads((BASE/'rules/ko-kr.json').read_text())
        self.assertEqual(len(rules),36)
        self.assertEqual(sum(r['priority']=='P0' for r in rules),13)
        self.assertEqual(len({r['id'] for r in rules}),36)
        sources=json.loads((BASE/'sources.json').read_text())['sources']
        self.assertTrue({s for r in rules for s in r['source_refs']} <= {s['id'] for s in sources})
        self.assertFalse(any('docs.google.com' in str(s) for s in sources))
        self.assertEqual(len(json.loads((BASE/'references/fixture-ledger.json').read_text())),40)

if __name__=='__main__': unittest.main()

class DistributionTests(unittest.TestCase):
    def test_archives_integrity_inventory_and_independence(self):
        import hashlib
        import zipfile
        manifest=json.loads((BASE/'downloads/MANIFEST.json').read_text())
        self.assertEqual(len(manifest['archives']),15)
        self.assertEqual(len({Path(a['file']).name for a in manifest['archives']}),15, 'Release assets need unique basenames')
        for item in manifest['archives']:
            p=BASE/'downloads'/item['file'];raw=p.read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),item['sha256'])
            self.assertEqual(len(raw),item['bytes'])
            with zipfile.ZipFile(p) as z:
                names=z.namelist();self.assertEqual(len(names),len(set(names)))
                self.assertIsNone(z.testzip())
                self.assertTrue(all(not n.startswith('/') and '..' not in Path(n).parts for n in names))
                self.assertFalse(any('ziheng' in n for n in names))
                entries=[n for n in names if n.endswith('/SKILL.md')]
                self.assertEqual(len(entries),4 if item['file'].startswith('plugins/') or '-bundle-' in item['file'] else 1)
                for entry in entries:
                    root=entry[:-len('SKILL.md')]
                    for required in ['rules/catalog.json','sources/public-sources.json','scripts/checks.py','references/preservation-policy.md','profiles/web-ui.json']:
                        self.assertIn(root+required,names)
                    inv=json.loads(z.read(root+'inventory.json'))
                    for f in inv['files']:
                        b=z.read(root+f['path'])
                        self.assertEqual(hashlib.sha256(b).hexdigest(),f['sha256'])
                        self.assertEqual(len(b),f['bytes'])

    def test_reproducible_builder_plan(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        import build_geuljjaim
        first=build_geuljjaim.plan_outputs(ROOT)
        self.assertEqual(first,build_geuljjaim.plan_outputs(ROOT))
        self.assertTrue(all((ROOT/p).read_bytes()==b for p,b in first.items()))

    def test_fixture_preservation_claim_is_replayable(self):
        import sys
        sys.path.insert(0,str(BASE/'runtime'))
        import checks
        for f in json.loads((BASE/'references/fixture-ledger.json').read_text()):
            raw=(f.get('input') or f.get('candidate')).encode('utf-8')
            self.assertEqual(checks.check_preservation(raw,raw)['status'],f['static_preservation_result'])
            self.assertEqual(f['actual_result'],'not-checked')
