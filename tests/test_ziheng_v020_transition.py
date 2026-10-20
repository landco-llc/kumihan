import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from test_ziheng_v020_context import ROOT
class TransitionTests(unittest.TestCase):
    def test_old_hash_and_candidate_hash_must_both_match(self):
        p=ROOT/'tools/ziheng_v020_transition.py';self.assertTrue(p.exists(),'independent transition validation helper missing')
        spec=importlib.util.spec_from_file_location('ziheng_transition',p);api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api)
        prefix='docs/development/zh-hant-v020-20261020/'
        rel='plugins/kumihan-ziheng/plugin.json'
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for name in [prefix+'source-transition.json',prefix+'source-transition-baseline.json','docs/seo/evidence/20261019-main-preservation.json',rel]:
                target=root/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,target)
            self.assertTrue(api.allowed(rel,'protected',root))
            ledger=root/prefix/'source-transition.json';d=json.loads(ledger.read_text());row=d['updates']['protected'][rel];row['main_before']='0'*64;ledger.write_text(json.dumps(d))
            self.assertFalse(api.allowed(rel,'protected',root))
            shutil.copy2(ROOT/(prefix+'source-transition.json'),ledger)
            (root/rel).write_text('{}');self.assertFalse(api.allowed(rel,'protected',root))
            self.assertFalse(api.allowed('README.md','protected',root))
    def test_history_exemption_only_accepts_exact_retained_ziheng_manifests(self):
        import ziheng_retention
        self.assertTrue(hasattr(ziheng_retention,'is_retained_manifest'),'scoped history admission missing')
        valid=ROOT/'plugins/kumihan-ziheng/downloads/history/0.1.0/MANIFEST.json'
        self.assertTrue(ziheng_retention.is_retained_manifest(ROOT,valid))
        for path in ['plugins/kumihan-ziheng/downloads/history/unregistered/MANIFEST.json','plugins/kumihan-zilu/downloads/history/0.1.0/MANIFEST.json','plugins/kumihan-ziheng/downloads/MANIFEST.json']:
            self.assertFalse(ziheng_retention.is_retained_manifest(ROOT,ROOT/path),path)
