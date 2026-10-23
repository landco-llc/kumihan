"""Immutable old downloads and one-version release boundary regression tests."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'plugins/kumihan-ziheng'
sys.path.insert(0,str(ROOT/'tools'))
import ziheng_retention as retention
import release_ziheng_v022 as release


class HistoricalZihengDownloads(unittest.TestCase):
    def test_both_historical_versions_are_exact_and_separate_from_current(self):
        files = retention.retained_outputs(ROOT,retention.FOLDERS)
        self.assertEqual(len(files),42)
        for version in ('0.1.0','0.2.0'):
            archives = {p:b for p,b in files.items() if p.endswith('-'+version+'.zip')}
            self.assertEqual(len(archives),15)
            for folder in retention.FOLDERS:
                manifest = BASE/folder/'history'/version/'MANIFEST.json'
                self.assertTrue(retention.is_retained_manifest(ROOT,manifest))
                rows = json.loads(manifest.read_bytes())
                self.assertEqual(rows['version'],version)
                for row in rows['archives']:
                    raw = files[(BASE/folder/row['file']).relative_to(ROOT).as_posix()]
                    self.assertEqual(len(raw),row['bytes'])
                    self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
        self.assertFalse(any(p.endswith('-0.2.2.zip') for p in files))

    def test_v020_corruption_and_unknown_historical_version_stop_build(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base = root/'plugins/kumihan-ziheng'
            base.mkdir(parents=True)
            shutil.copy2(BASE/'retained-distributions.json',base/'retained-distributions.json')
            shutil.copytree(BASE/'downloads',base/'downloads')
            target = base/'downloads/plugins/kumihan-ziheng-0.2.0.zip'
            original = target.read_bytes()
            target.write_bytes(original+b'changed')
            with self.assertRaisesRegex(ValueError,'Corrupt retained distribution'):
                retention.retained_outputs(root,('downloads',))
            target.write_bytes(original)
            ledger = json.loads((base/'retained-distributions.json').read_bytes())
            entry = dict(ledger['entries'][0])
            entry['path'] = entry['path'].replace('0.1.0','0.2.1')
            ledger['entries'].append(entry)
            (base/'retained-distributions.json').write_text(json.dumps(ledger))
            with self.assertRaisesRegex(ValueError,'Only fixed historical'):
                retention.retained_outputs(root,('downloads',))

    def test_historical_source_links_survive_new_source_and_published_versions(self):
        import edition_versions
        import version_display
        facts = copy.deepcopy(edition_versions.load()['editions']['zh-hant'])
        facts['source_version'] = '0.2.2'
        for version in ('0.1.0','0.2.0'):
            path = '../plugins/kumihan-ziheng/downloads/plugins/kumihan-ziheng-'+version+'.zip'
            self.assertTrue(version_display.is_source_download(path,facts))
            self.assertIn('href="'+path+'"',version_display.rewrite_downloads(f'<a href="{path}">History</a>',facts))
        self.assertFalse(version_display.is_source_download(
            '../plugins/kumihan-ziheng/downloads/plugins/kumihan-ziheng-0.2.1.zip',facts))


class ZihengOneVersionRelease(unittest.TestCase):
    def test_workflow_cannot_publish_from_pr_or_another_version(self):
        import yaml
        workflow = yaml.load((ROOT/'.github/workflows/publish-ziheng-v022.yml').read_text(),Loader=yaml.BaseLoader)
        self.assertEqual(workflow['on'],{'push':{'branches':['main'],
                         'paths':['releases/kumihan-ziheng-v0.2.2/REQUEST.json',
                                  'tools/release_ziheng_v022.py']}})
        self.assertEqual(workflow['permissions'],{'contents':'read'})
        self.assertEqual(workflow['jobs']['publish']['needs'],'verify')
        self.assertEqual(workflow['jobs']['publish']['permissions'],{'contents':'write'})
        for job in workflow['jobs'].values():
            self.assertIn("github.repository == 'landco-llc/kumihan'",job['if'])

    def test_release_contract_has_all_hosts_and_no_uncontrolled_paths(self):
        names = release.asset_names(ROOT)
        self.assertEqual(len(names),15)
        for host in ('openai-codex','claude','gemini'):
            self.assertEqual(sum(name.startswith('kumihan-ziheng-'+host+'-') for name in names),5)
        self.assertTrue(all(Path(name).name == name for name in names))

    def test_remote_asset_identity_hash_size_and_extras_are_rejected(self):
        files = {name:(name+' bytes').encode() for name in release.asset_names(ROOT)}
        files.update({'MANIFEST.json':b'{}','SHA256SUMS.txt':b'sums'})
        rows = [{'name':name,'size':len(raw),'digest':'sha256:'+release.digest(raw)} for name,raw in files.items()]
        release.verify_remote_assets({'assets':rows},files)
        for changed in (rows[:-1],rows+[rows[0]],
                        [dict(rows[0],size=0)]+rows[1:],
                        [dict(rows[0],digest='sha256:'+'0'*64)]+rows[1:]):
            with self.assertRaises(ValueError):
                release.verify_remote_assets({'assets':changed},files)

    def test_publication_rejects_private_repository_or_non_push_before_network(self):
        contexts = [
            {'GITHUB_REPOSITORY':'landco-llc/kumihan-internal','GITHUB_REF':'refs/heads/main','GITHUB_EVENT_NAME':'push'},
            {'GITHUB_REPOSITORY':'landco-llc/kumihan','GITHUB_REF':'refs/heads/feature','GITHUB_EVENT_NAME':'push'},
            {'GITHUB_REPOSITORY':'landco-llc/kumihan','GITHUB_REF':'refs/heads/main','GITHUB_EVENT_NAME':'pull_request'},
        ]
        for context in contexts:
            with mock.patch.dict(os.environ,context,clear=True), mock.patch.object(release,'gh') as gh:
                with self.assertRaisesRegex(ValueError,'restricted'):
                    release.publish()
                gh.assert_not_called()

    def test_draft_recovery_accepts_only_the_exact_empty_interrupted_draft(self):
        notes = (ROOT / release.NOTES).read_text(encoding='utf-8')
        source = {
            'id': 420671387,
            'draft': True,
            'prerelease': False,
            'tag_name': release.TAG,
            'target_commitish': release.RECOVERY_TARGET_SHA,
            'created_at': release.RECOVERY_CREATED_AT,
            'name': 'KUMIHAN｜字衡 v0.2.2',
            'body': notes,
            'assets': [],
        }
        self.assertEqual(release.validate_recovery_draft(source, notes),
                         release.RECOVERY_TARGET_SHA)
        for key, value in [
            ('id', 420671388), ('draft', False), ('prerelease', True),
            ('tag_name', 'kumihan-ziheng-v0.2.0'),
            ('target_commitish', '0' * 40), ('created_at', 'not-the-original'),
            ('name', 'Wrong release'), ('body', 'Unreviewed text'),
            ('assets', [{'name': 'unknown.zip'}])
        ]:
            with self.subTest(field=key):
                mutated = dict(source, **{key: value})
                with self.assertRaises(ValueError):
                    release.validate_recovery_draft(mutated, notes)
        with self.assertRaises(ValueError):
            release.validate_recovery_draft(None, notes)


    def test_absence_check_rejects_existing_tag_and_authentication_errors(self):
        for code,stdout in ((0,'HTTP/2.0 200 OK\n'),(1,'HTTP/2.0 403 Forbidden\n'),(1,'')):
            completed = mock.Mock(returncode=code,stdout=stdout)
            with mock.patch.object(release.subprocess,'run',return_value=completed):
                with self.assertRaises(ValueError):
                    release.assert_tag_absent()
        with mock.patch.object(release.subprocess,'run',return_value=mock.Mock(returncode=1,stdout='HTTP/2.0 404 Not Found\n')):
            release.assert_tag_absent()


if __name__ == '__main__':
    unittest.main()
