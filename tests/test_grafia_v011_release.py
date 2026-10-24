"""The v0.1.1 publisher must never include retained v0.1.0 archives."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('grafia_v011_release', ROOT/'tools/release_grafia_v011.py')

class PublisherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.release = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.release)

    def product(self, root):
        destination = root/'plugins/kumihan-grafia/downloads'
        destination.mkdir(parents=True)
        rows=[]
        names=[f'{skill}-{host}-skill-v0.1.1.zip' for skill in ('kumihan-grafia','kumihan-grafia-web','kumihan-grafia-documents','kumihan-grafia-review') for host in ('GPT-Codex','Claude','Gemini-Apps')]
        names += [f'kumihan-grafia-{host}-v0.1.1.zip' for host in ('GPT-Codex-plugin','Claude-Code-plugin','Gemini-CLI-extension')]
        for i,name in enumerate(names):
            raw=f'zip-{i}'.encode()
            (destination/name).write_bytes(raw)
            rows.append(dict(file=name,bytes=len(raw),sha256=self.release.digest(raw)))
        manifest=json.dumps(dict(product='KUMIHAN｜Grafía',version='0.1.1',tag=self.release.TAG,archives=rows)).encode()
        (destination/'MANIFEST.json').write_bytes(manifest)
        (destination/'SHA256SUMS.txt').write_text(''.join(f"{r['sha256']}  {r['file']}\n" for r in rows)+f"{self.release.digest(manifest)}  MANIFEST.json\n")
        (destination/'kumihan-grafia-old-v0.1.0.zip').write_bytes(b'old immutable')
        return destination

    def test_exact_manifest_assets_exclude_retained_old_zips(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);self.product(root)
            files=self.release.local_assets(root)
            self.assertEqual(len(files),17)
            self.assertFalse(any('v0.1.0' in n for n in files))

    def test_manifest_checksum_is_required_and_verified(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);d=self.product(root)
            files=self.release.local_assets(root)
            self.assertEqual(len(files),17)
            sums=(d/'SHA256SUMS.txt').read_text()
            self.assertIn(self.release.digest(files['MANIFEST.json'])+'  MANIFEST.json',sums)
            for changed in (''.join(line+'\n' for line in sums.splitlines() if not line.endswith('  MANIFEST.json')),
                            sums.replace(self.release.digest(files['MANIFEST.json'])+'  MANIFEST.json','0'*64+'  MANIFEST.json')):
                (d/'SHA256SUMS.txt').write_text(changed)
                with self.assertRaises(ValueError):self.release.local_assets(root)

    def test_actual_v011_product_has_the_exact_seventeen_asset_payload(self):
        manifest=json.loads((ROOT/'plugins/kumihan-grafia/downloads/MANIFEST.json').read_bytes())
        if manifest['version']!='0.1.1':self.skipTest('v0.1.1 product not adopted on publisher preparation branch')
        files=self.release.local_assets(ROOT)
        self.assertEqual(len(files),17)
        self.assertEqual(sum(name.endswith('.zip') for name in files),15)
        self.assertFalse(any('v0.1.0' in name for name in files))

    def test_manifest_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);d=self.product(root)
            m=json.loads((d/'MANIFEST.json').read_text());m['archives'][0]['file']='../other-v0.1.1.zip'
            (d/'MANIFEST.json').write_text(json.dumps(m))
            with self.assertRaises(ValueError):self.release.local_assets(root)

    def test_wrong_version_and_corrupt_checksum_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);d=self.product(root)
            (d/'SHA256SUMS.txt').write_text('0'*64+'  kumihan-grafia-role-0-v0.1.1.zip\n')
            with self.assertRaises(ValueError):self.release.local_assets(root)
            m=json.loads((d/'MANIFEST.json').read_text());m['version']='0.1.0';(d/'MANIFEST.json').write_text(json.dumps(m))
            with self.assertRaises(ValueError):self.release.local_assets(root)

    def test_fifteen_wrong_roles_are_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);d=self.product(root)
            m=json.loads((d/'MANIFEST.json').read_text())
            old=m['archives'][0]['file'];new='kumihan-grafia-unrequested-v0.1.1.zip'
            (d/old).rename(d/new);m['archives'][0]['file']=new
            (d/'MANIFEST.json').write_text(json.dumps(m))
            sums=(d/'SHA256SUMS.txt').read_text().replace(old,new);(d/'SHA256SUMS.txt').write_text(sums)
            with self.assertRaises(ValueError):self.release.local_assets(root)

    def test_remote_unknown_duplicate_corrupt_assets_rejected(self):
        r=self.release;files={'a.zip':b'a'}
        row=dict(name='a.zip',size=1,digest='sha256:'+r.digest(b'a'))
        self.assertEqual(r.verify_remote_subset({'assets':[row]},files),set())
        for rows in ([row,row],[dict(row,name='old.zip')],[dict(row,digest='sha256:'+'0'*64)]):
            with self.assertRaises(ValueError):r.verify_remote_subset({'assets':rows},files)

    def test_release_identity_bound_to_fixed_tag_target_and_draft(self):
        r=self.release;request=dict(target_commit='a'*40,draft_id=123,created_at='2026-10-24T17:00:00Z')
        release=dict(id=123,draft=True,prerelease=False,tag_name=r.TAG,target_commitish='a'*40,created_at=request['created_at'],name=r.TITLE,body='notes',assets=[])
        r.validate_release(release,request,'notes',draft=True)
        for key,value in [('tag_name','kumihan-grafia-v0.1.0'),('target_commitish','b'*40),('id',124),('body','changed')]:
            with self.assertRaises(ValueError):r.validate_release(dict(release,**{key:value}),request,'notes',draft=True)

    def test_published_identity_allows_github_creation_timestamp_recalculation(self):
        r=self.release;request=dict(target_commit='a'*40,draft_id=123,created_at='2026-10-24T17:00:00Z')
        release=dict(id=123,draft=False,prerelease=False,tag_name=r.TAG,target_commitish='a'*40,
                     created_at='2026-10-24T17:30:00Z',name=r.TITLE,body='notes',assets=[])
        r.validate_release(release,request,'notes',draft=False)
        with self.assertRaises(ValueError):r.validate_release(dict(release,draft=True),request,'notes',draft=True)

    def test_reviewed_request_rejects_changed_notes_or_asset_set(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);self.product(root);r=self.release
            files=r.local_assets(root);folder=root/r.FOLDER;folder.mkdir(parents=True)
            notes=b'Public release notes';(folder/'RELEASE_NOTES.md').write_bytes(notes)
            request=dict(schema_version=1,repository=r.REPO,product='kumihan-grafia',version='0.1.1',tag=r.TAG,title=r.TITLE,
                         target_commit='a'*40,product_tree='b'*40,draft_id=123,created_at='2026-10-24T17:00:00Z',
                         notes_sha256=r.digest(notes),assets={n:dict(bytes=len(b),sha256=r.digest(b)) for n,b in files.items()})
            (folder/'REQUEST.json').write_text(json.dumps(request));self.assertEqual(r.check(root),files)
            (folder/'RELEASE_NOTES.md').write_bytes(b'changed')
            with self.assertRaises(ValueError):r.check(root)
            (folder/'RELEASE_NOTES.md').write_bytes(notes);request['assets'].pop('MANIFEST.json')
            (folder/'REQUEST.json').write_text(json.dumps(request))
            with self.assertRaises(ValueError):r.check(root)

    def test_publication_refuses_non_native_environment_before_network(self):
        from unittest.mock import patch
        with patch.dict('os.environ',{},clear=True):
            with self.assertRaises(ValueError):self.release.publish()

if __name__=='__main__':unittest.main()
