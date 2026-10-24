"""The one-time publisher cannot select another release or replace existing assets."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import release_measure_v011 as release

class ExactMeasurePublisher(unittest.TestCase):
    def setUp(self):
        self.request=release.request()
        self.notes=(ROOT/release.NOTES).read_text()
        self.draft={'id':release.DRAFT,'draft':True,'prerelease':False,'tag_name':release.TAG,
            'target_commitish':release.TARGET,'created_at':self.request['created_at'],
            'name':self.request['title'],'body':self.notes,'assets':[]}

    def test_exact_draft_only_and_partial_assets_stop(self):
        release.validate_release(self.draft,self.request,self.notes,draft=True,empty=True)
        for key,value in [('id',1),('draft',False),('prerelease',True),('tag_name','other'),
                          ('target_commitish','a'*40),('created_at','changed'),('name','changed'),
                          ('body','changed'),('assets',[{'name':'already-uploaded.zip'}])]:
            draft=copy.deepcopy(self.draft);draft[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):
                release.validate_release(draft,self.request,self.notes,draft=True,empty=True)

    def test_remote_asset_set_sizes_and_digests_are_exact(self):
        files={name:b'x' for name in self.request['assets']}
        rows=[{'name':n,'size':1,'digest':'sha256:'+release.digest(b'x')} for n in files]
        release.verify_remote_assets({'assets':rows},files)
        for changed in (rows[:-1],rows+[rows[0]], [dict(rows[0],size=2)]+rows[1:],
                        [dict(rows[0],digest='sha256:'+'0'*64)]+rows[1:]):
            with self.assertRaises(ValueError):release.verify_remote_assets({'assets':changed},files)

    def test_duplicate_or_other_draft_identity_is_rejected(self):
        for rows in ([],[dict(self.draft,id=1)],[self.draft,self.draft]):
            with patch.object(release,'gh',return_value=json.dumps([rows])):
                with self.assertRaises(ValueError):release.assert_unique_draft()
        with patch.object(release,'gh',return_value=json.dumps([[self.draft]])):
            release.assert_unique_draft()

    def test_changed_request_cannot_be_rebound(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);p=root/release.REQUEST;p.parent.mkdir(parents=True)
            request=copy.deepcopy(self.request);request['target_commit']='a'*40
            p.write_text(json.dumps(request))
            with self.assertRaises(ValueError):release.request(root)

    def test_no_publication_outside_native_main_push(self):
        with patch.dict(os.environ,{},clear=True),patch.object(release,'gh') as gh:
            with self.assertRaises(ValueError):release.publish()
            gh.assert_not_called()

    def test_partial_upload_state_stops_before_any_write(self):
        env={'GITHUB_REPOSITORY':release.REPO,'GITHUB_REF':'refs/heads/main','GITHUB_EVENT_NAME':'push','GITHUB_SHA':'a'*40}
        partial=dict(self.draft,assets=[{'name':'partial.zip'}])
        with patch.dict(os.environ,env,clear=True),patch.object(release.subprocess,'check_output',return_value='a'*40+'\n'),patch.object(release.subprocess,'run'),patch.object(release,'api',side_effect=[{'sha':'a'*40},partial]),patch.object(release,'check',return_value={}),patch.object(release,'request',return_value=self.request),patch.object(release,'assert_tag_absent'),patch.object(release,'assert_unique_draft'),patch.object(release,'gh') as gh:
            with self.assertRaises(ValueError):release.publish()
            gh.assert_not_called()

    def test_complete_native_flow_verifies_fresh_state_before_publish(self):
        import contextlib
        import io
        env={'GITHUB_REPOSITORY':release.REPO,'GITHUB_REF':'refs/heads/main','GITHUB_EVENT_NAME':'push','GITHUB_SHA':'a'*40}
        files={name:b'x' for name in self.request['assets']}
        rows=[{'name':n,'size':1,'digest':'sha256:'+release.digest(b'x')} for n in files]
        uploaded=dict(self.draft,assets=rows)
        published=dict(uploaded,draft=False,published_at=release.PUBLISHED_AT,html_url='https://github.com/'+release.REPO+'/releases/tag/'+release.TAG)
        responses=[{'sha':'a'*40},self.draft,uploaded,uploaded,published,{'object':{'sha':release.TARGET}}]
        with patch.dict(os.environ,env,clear=True),patch.object(release.subprocess,'check_output',return_value='a'*40+'\n'),patch.object(release.subprocess,'run'),patch.object(release,'api',side_effect=responses) as api,patch.object(release,'check',return_value=files),patch.object(release,'request',return_value=self.request),patch.object(release,'assert_tag_absent') as tag,patch.object(release,'assert_unique_draft') as unique,patch.object(release,'verify_download') as download,patch.object(release,'gh') as gh,contextlib.redirect_stdout(io.StringIO()):
            release.publish()
            self.assertEqual(api.call_count,6)
            self.assertEqual(tag.call_count,2)
            self.assertEqual(unique.call_count,2)
            self.assertEqual(download.call_count,2)
            self.assertEqual(gh.call_count,2)
            self.assertEqual(gh.call_args_list[0].args[:3],('release','upload',release.TAG))
            self.assertNotIn('--clobber',gh.call_args_list[0].args)
            self.assertEqual(gh.call_args_list[1].args,('release','edit',release.TAG,'--repo',release.REPO,'--draft=false','--latest=false'))

    def test_verified_partial_assets_are_skipped_and_only_missing_uploaded(self):
        import contextlib
        import io
        env={'GITHUB_REPOSITORY':release.REPO,'GITHUB_REF':'refs/heads/main','GITHUB_EVENT_NAME':'push','GITHUB_SHA':'a'*40}
        files={name:b'x' for name in self.request['assets']}
        first=next(iter(files));existing={first:files[first]}
        rows=[{'name':n,'size':1,'digest':'sha256:'+release.digest(b'x')} for n in files]
        initial=dict(self.draft,assets=[rows[0]]);uploaded=dict(self.draft,assets=rows)
        published=dict(uploaded,draft=False,published_at=release.PUBLISHED_AT,html_url='https://github.com/'+release.REPO+'/releases/tag/'+release.TAG)
        responses=[{'sha':'a'*40},initial,uploaded,uploaded,published,{'object':{'sha':release.TARGET}}]
        with patch.dict(os.environ,env,clear=True),patch.object(release.subprocess,'check_output',return_value='a'*40+'\n'),patch.object(release.subprocess,'run'),patch.object(release,'api',side_effect=responses),patch.object(release,'check',return_value=files),patch.object(release,'request',return_value=self.request),patch.object(release,'assert_tag_absent'),patch.object(release,'assert_unique_draft'),patch.object(release,'verify_download') as download,patch.object(release,'gh') as gh,contextlib.redirect_stdout(io.StringIO()):
            release.publish()
            self.assertEqual(download.call_args_list[0].args,(existing,))
            names={Path(x).name for x in gh.call_args_list[0].args[5:]}
            self.assertEqual(names,set(files)-{first})
            self.assertNotIn('--clobber',gh.call_args_list[0].args)

    def test_existing_download_mismatch_stops_without_writes(self):
        env={'GITHUB_REPOSITORY':release.REPO,'GITHUB_REF':'refs/heads/main','GITHUB_EVENT_NAME':'push','GITHUB_SHA':'a'*40}
        files={name:b'x' for name in self.request['assets']};first=next(iter(files))
        initial=dict(self.draft,assets=[{'name':first,'size':1,'digest':'sha256:'+release.digest(b'x')}])
        with patch.dict(os.environ,env,clear=True),patch.object(release.subprocess,'check_output',return_value='a'*40+'\n'),patch.object(release.subprocess,'run'),patch.object(release,'api',side_effect=[{'sha':'a'*40},initial]),patch.object(release,'check',return_value=files),patch.object(release,'request',return_value=self.request),patch.object(release,'assert_tag_absent'),patch.object(release,'assert_unique_draft'),patch.object(release,'verify_download',side_effect=ValueError('Downloaded bytes differ')),patch.object(release,'gh') as gh:
            with self.assertRaises(ValueError):release.publish()
            gh.assert_not_called()

    def test_already_published_is_read_only_even_when_created_at_changed(self):
        import contextlib
        import io
        env={'GITHUB_REPOSITORY':release.REPO,'GITHUB_REF':'refs/heads/main','GITHUB_EVENT_NAME':'push','GITHUB_SHA':'a'*40}
        files={name:b'x' for name in self.request['assets']}
        rows=[{'name':n,'size':1,'digest':'sha256:'+release.digest(b'x')} for n in files]
        published=dict(self.draft,draft=False,created_at='2026-10-24T16:06:25Z',assets=rows,
            published_at=release.PUBLISHED_AT,html_url='https://github.com/'+release.REPO+'/releases/tag/'+release.TAG)
        with patch.dict(os.environ,env,clear=True),patch.object(release.subprocess,'check_output',return_value='a'*40+'\n'),patch.object(release.subprocess,'run'),patch.object(release,'api',side_effect=[{'sha':'a'*40},published,{'object':{'sha':release.TARGET}}]),patch.object(release,'check',return_value=files),patch.object(release,'request',return_value=self.request),patch.object(release,'assert_tag_absent') as absent,patch.object(release,'assert_unique_draft') as unique,patch.object(release,'verify_download') as download,patch.object(release,'gh') as gh,contextlib.redirect_stdout(io.StringIO()):
            release.publish()
            gh.assert_not_called();absent.assert_not_called();unique.assert_not_called()
            download.assert_called_once_with(files)

    def test_published_state_cannot_accept_wrong_identity_date_target_or_bytes(self):
        files={name:b'x' for name in self.request['assets']}
        rows=[{'name':n,'size':1,'digest':'sha256:'+release.digest(b'x')} for n in files]
        published=dict(self.draft,draft=False,created_at='changed by GitHub',assets=rows,
            published_at=release.PUBLISHED_AT,html_url='https://github.com/'+release.REPO+'/releases/tag/'+release.TAG)
        for field,value in [('id',1),('tag_name','other'),('target_commitish','a'*40),('body','changed'),('published_at','2026-10-25T00:00:00Z'),('assets',rows[:-1])]:
            modified=dict(published,**{field:value})
            with patch.object(release,'api',return_value={'object':{'sha':release.TARGET}}),patch.object(release,'verify_download'),patch.object(release,'gh') as gh:
                with self.assertRaises(ValueError):release.verify_published(modified,self.request,self.notes,files)
                gh.assert_not_called()
        with patch.object(release,'api',return_value={'object':{'sha':'0'*40}}),patch.object(release,'verify_download') as download:
            with self.assertRaises(ValueError):release.verify_published(published,self.request,self.notes,files)
            download.assert_not_called()
        with patch.object(release,'api',return_value={'object':{'sha':release.TARGET}}),patch.object(release,'verify_download',side_effect=ValueError('Downloaded bytes differ')),patch.object(release,'gh') as gh:
            with self.assertRaises(ValueError):release.verify_published(published,self.request,self.notes,files)
            gh.assert_not_called()
