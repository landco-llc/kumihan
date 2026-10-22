import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from test_ziheng_v020_context import ROOT,BASE
sys.path.insert(0,str(ROOT/'tools'))
class PackagingTests(unittest.TestCase):
    def test_old_archives_survive_version_transition_and_corruption_is_rejected(self):
        import build_ziheng,build_ziheng_hosts
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for rel in ['plugins/kumihan-ziheng','skills/kumihan','assets','tools']:
                shutil.copytree(ROOT/rel,root/rel,ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copy2(ROOT/'LICENSE',root/'LICENSE')
            old={p.relative_to(root).as_posix():p.read_bytes() for p in (root/'plugins/kumihan-ziheng').rglob('*.zip') if p.name.endswith(('-0.1.0.zip','-0.2.0.zip'))}
            self.assertEqual(len(old),30)
            path=root/'plugins/kumihan-ziheng/plugin.json';m=json.loads(path.read_text());m['version']='0.2.2';path.write_text(json.dumps(m))
            planned=build_ziheng.plan_outputs(root)
            for rel,b in planned.items():
                p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
            planned.update(build_ziheng_hosts.plan_outputs(root))
            stale=(build_ziheng.generated_files(root)|build_ziheng_hosts.generated_files(root))-set(planned)
            self.assertFalse(set(old)&stale,'legacy download URLs would be deleted')
            for rel,b in old.items():self.assertEqual((root/rel).read_bytes(),b)
            rel=next(p for p in old if '/downloads/' in p);(root/rel).write_bytes(b'corrupted')
            with self.assertRaises(ValueError):build_ziheng.plan_outputs(root)
    def test_four_standalone_scripts_and_references(self):
        import build_ziheng
        outputs=build_ziheng.plan_outputs(ROOT)
        for name in build_ziheng.NAMES:
            for script in ['context','evidence','checks']:
                rel=f'plugins/kumihan-ziheng/skills/{name}/scripts/{script}.py'
                self.assertIn(rel,set(outputs))
                with tempfile.TemporaryDirectory() as td:
                    p=Path(td)/f'{script}.py';p.write_bytes(outputs[rel]);spec=importlib.util.spec_from_file_location('standalone',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
                    if script=='context':self.assertIsNone(m.resolve_review_context({})['editorial_region'])
                    elif script=='evidence':self.assertTrue(m.validate_evidence_context({}))
                    else:self.assertEqual(m.review_segment({'text':'','role':'protected'}, {})['findings'],[])
            self.assertIn(f'plugins/kumihan-ziheng/skills/{name}/fixtures/research-v020/cases.json',set(outputs))
    def test_historical_source_links_are_verified_against_retention(self):
        from version_display import source_archives
        source_archives.cache_clear()
        self.assertEqual(len(source_archives('zh-hant','0.1.0')),15)
        self.assertEqual(len(source_archives('zh-hant','0.2.0')),15)
    def test_current_fifteen_archives_crc_size_hash_icons_and_determinism(self):
        import io,zipfile,build_ziheng,build_ziheng_hosts
        first=build_ziheng.plan_outputs(ROOT);second=build_ziheng.plan_outputs(ROOT);self.assertEqual(set(first),set(second))
        self.assertTrue(all(v==second[k] for k,v in first.items()))
        hosts=build_ziheng_hosts.plan_outputs(ROOT);again=build_ziheng_hosts.plan_outputs(ROOT);self.assertTrue(all(v==again[k] for k,v in hosts.items()))
        count=0
        for folder in ['downloads','downloads Claude','downloads Gemini']:
            data=json.loads((BASE/folder/'MANIFEST.json').read_text());self.assertEqual(data['version'],json.loads((BASE/'plugin.json').read_text())['version']);self.assertEqual(len(data['archives']),5)
            for row in data['archives']:
                p=BASE/folder/row['file'];raw=p.read_bytes();self.assertEqual(len(raw),row['bytes']);self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
                with zipfile.ZipFile(io.BytesIO(raw)) as z:
                    self.assertIsNone(z.testzip());self.assertTrue(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist()))
                    if row['file'].startswith(('plugins/','extensions/')):self.assertTrue(any(n.endswith('assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png') for n in z.namelist()))
                count+=1
        self.assertEqual(count,15)
    def test_build_checks_are_read_only_and_unknown_stale_is_not_whitelisted(self):
        import build_ziheng
        def hashes():return {p:hashlib.sha256(p.read_bytes()).hexdigest() for p in BASE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        before=hashes()
        for name in ['build_ziheng.py','build_ziheng_hosts.py']:
            r=subprocess.run([sys.executable,str(ROOT/'tools'/name),'--check'],capture_output=True);self.assertEqual(r.returncode,0,r.stdout.decode())
        self.assertEqual(before,hashes())
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);p=root/'plugins/kumihan-ziheng/downloads/stale.zip';p.parent.mkdir(parents=True);p.write_bytes(b'unknown')
            self.assertIn(p.relative_to(root).as_posix(),build_ziheng.generated_files(root))
    def test_legacy_url_stays_admitted_after_shared_version_snapshot_updates(self):
        import edition_versions,copy
        from version_display import rewrite_downloads,source_archives
        f=copy.deepcopy(edition_versions.load()['editions']['zh-hant']);f['source_version']='0.2.2'
        path='../plugins/kumihan-ziheng/downloads/plugins/kumihan-ziheng-0.1.0.zip'
        out=rewrite_downloads(f'<a href="{path}">History</a>',f)
        self.assertIn('href="'+path+'"',out)
