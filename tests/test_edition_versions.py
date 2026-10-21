"""Release admission tests: promotion must require complete, matching actual bytes."""
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import unittest
import zipfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import edition_versions as v


class ReleaseAdmission(unittest.TestCase):
    def setUp(self):
        self.spec = dict(zip_templates=['xx-v{version}.zip'], product='xx', edition='xx', source_manifest='plugin.json', tag_prefix='xx-v', zip_count=1)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w') as z:
            z.writestr('xx/plugin.json', json.dumps({'version': '1.2.3'}))
        self.payload = buf.getvalue()
        sha = hashlib.sha256(self.payload).hexdigest()
        self.manifest = json.dumps(dict(version='1.2.3', archives=[dict(file='xx-v1.2.3.zip', sha256=sha, bytes=len(self.payload))])).encode()
        self.release = dict(id=1, tag_name='xx-v1.2.3', draft=False, prerelease=False, published_at='2026-10-19T12:00:00Z', html_url=v.REPO+'/releases/tag/xx-v1.2.3', assets=[
            dict(name='MANIFEST.json', size=len(self.manifest), browser_download_url=v.REPO+'/releases/download/xx-v1.2.3/MANIFEST.json'),
            dict(name='xx-v1.2.3.zip', size=len(self.payload), digest='sha256:'+sha, browser_download_url=v.REPO+'/releases/download/xx-v1.2.3/xx-v1.2.3.zip')])
        self.sums = (sha+'  xx-v1.2.3.zip\n').encode()
        self.release['assets'].append(dict(name='SHA256SUMS.txt',size=len(self.sums),browser_download_url=v.REPO+'/releases/download/xx-v1.2.3/SHA256SUMS.txt'))
        self.fetch = lambda url: self.manifest if url.endswith('MANIFEST.json') else self.sums if url.endswith('.txt') else self.payload
        self.source = lambda tag, path: json.dumps({'version': '1.2.3'}).encode()

    def verify(self, r=None, fetch=None, source=None):
        return v.verify_release(self.spec, r or self.release, fetch or self.fetch, source or self.source)

    def test_complete_promotion_and_idempotence(self):
        result = self.verify()
        self.assertEqual(result['published_version'], '1.2.3')
        self.assertEqual(result['verified_assets'][0]['sha256'], hashlib.sha256(self.payload).hexdigest())
        old = dict(source_version='1.2.4', **result)
        self.assertEqual(v.select_release(self.spec, old, [self.release], self.fetch, self.source), old)

    def test_rejects_draft_prerelease_unrelated_and_partial(self):
        for changes in [dict(draft=True), dict(prerelease=True), dict(tag_name='yy-v1.2.3'), dict(assets=self.release['assets'][:1])]:
            r = dict(self.release, **changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError): self.verify(r)

    def test_rejects_bytes_size_manifest_and_source_mismatch(self):
        for fetch, source in [
            (lambda url: self.manifest if url.endswith('.json') else b'corrupted', self.source),
            (lambda url: self.manifest.replace(b'1.2.3', b'9.9.9') if url.endswith('.json') else self.payload, self.source),
            (self.fetch, lambda tag, path: b'{"version":"1.2.4"}')]:
            with self.subTest(fetch=fetch), self.assertRaises(ValueError): self.verify(fetch=fetch, source=source)

    def test_failure_keeps_snapshot_unchanged(self):
        old = {'source_version': '1.2.3', 'published_version': None, 'release_status': 'unpublished'}
        before = copy.deepcopy(old)
        def offline(url): raise OSError('network unavailable')
        with self.assertRaises(OSError): v.select_release(self.spec, old, [self.release], offline, self.source)
        self.assertEqual(old, before)

    def test_rejects_missing_or_corrupt_checksums(self):
        r=copy.deepcopy(self.release);r['assets']=r['assets'][:2]
        with self.assertRaises(ValueError):self.verify(r)
        fetch=lambda url: b'0'*len(self.sums) if url.endswith('.txt') else self.fetch(url)
        with self.assertRaises(ValueError):self.verify(fetch=fetch)

    def test_old_formal_release_does_not_downgrade(self):
        old = dict(source_version='1.2.4', **self.verify())
        r = dict(self.release, tag_name='xx-v1.2.2')
        self.assertEqual(v.select_release(self.spec, old, [r,self.release], self.fetch, self.source), old)

    def test_same_count_wrong_package_role_is_rejected(self):
        r=copy.deepcopy(self.release)
        r['assets'][1]['name']='xx-unrelated-v1.2.3.zip'
        r['assets'][1]['browser_download_url']=v.REPO+'/releases/download/xx-v1.2.3/xx-unrelated-v1.2.3.zip'
        manifest=self.manifest.replace(b'xx-v',b'xx-unrelated-v')
        sums=self.sums.replace(b'xx-v',b'xx-unrelated-v')
        r['assets'][0]['size']=len(manifest);r['assets'][2]['size']=len(sums)
        fetch=lambda url: manifest if url.endswith('.json') else sums if url.endswith('.txt') else self.payload
        with self.assertRaises(ValueError):self.verify(r,fetch=fetch)

    def test_withdrawn_current_release_fails_without_mutation(self):
        old=dict(source_version='1.2.3',**self.verify());before=copy.deepcopy(old)
        for releases in ([],[dict(self.release,draft=True)],[dict(self.release,prerelease=True)],[dict(self.release,tag_name='xx-v1.2.2')]):
            with self.subTest(releases=releases),self.assertRaises(ValueError):
                v.select_release(self.spec,old,releases,self.fetch,self.source)
            self.assertEqual(old,before)

    def test_unadopted_flat_contract_does_not_promote(self):
        self.spec['zip_templates']=None
        with self.assertRaisesRegex(ValueError,'Owner naming decision required'):self.verify()

    def test_ignores_unrelated_and_draft_events(self):
        old = {'source_version': '1.2.3', 'published_version': None, 'release_status': 'unpublished'}
        self.assertEqual(v.select_release(self.spec, old, [dict(self.release, draft=True), dict(self.release, tag_name='v99.0.0')], self.fetch, self.source), old)


if __name__ == '__main__': unittest.main()

class DisplayContract(unittest.TestCase):
    def test_shared_renderer_replaces_downloads_and_marks_unpublished(self):
        from version_display import apply_html
        f = {'source_version':'1.2.4', 'published_version':'1.2.3', 'release_status':'published', 'published_at':'2026-10-19T12:00:00Z', 'release_url':v.REPO+'/releases/tag/v1.2.3', 'tag':'v1.2.3', 'verified_assets':[dict(name='kumihan-GPT-Codex-plugin-1.2.3.zip',url=v.REPO+'/releases/download/v1.2.3/kumihan-GPT-Codex-plugin-1.2.3.zip',sha256='a'*64,bytes=100)]}
        html = '<html lang="en"><head></head><body><div class="hero-copy"><h1>Hi</h1></div><section id="install"><a href="old/kumihan-GPT-Codex-plugin-0.1.8.zip">Download v0.1.8</a></section></body></html>'
        out = apply_html(html, 'kumihan.html', {'editions': {'ja': f}})
        self.assertIn(f['verified_assets'][0]['url'],out)
        self.assertNotIn('old/kumihan-',out)
        self.assertIn('Source v1.2.4',out)
        self.assertIn('2026-10-19T12:00:00Z',out)
        self.assertEqual(apply_html(out,'kumihan.html',{'editions':{'ja':f}}),out)
        f.update(published_version=None,release_status='unpublished',release_url=None,tag=None,verified_assets=[])
        out=apply_html(html,'kumihan.html',{'editions':{'ja':f}})
        self.assertIn('unpublished',out)
        self.assertNotIn('href="old/',out)
        self.assertNotIn('/releases/download/',out)

class SnapshotAndCoverage(unittest.TestCase):
    def test_catalogue_source_and_release_integrity(self):
        facts=v.load()['editions']
        self.assertEqual(set(facts),set(v.catalogue()))
        self.assertEqual(len(facts),29)
        for code,spec in v.catalogue().items():
            with self.subTest(edition=code):
                f=facts[code]
                self.assertEqual(f['source_version'],v.source_version(spec))
                if f['release_status']=='published':
                    self.assertEqual(f['tag'],spec['tag_prefix']+f['published_version'])
                    self.assertEqual(len(f['verified_assets']),spec['zip_count'])
                    self.assertEqual({a['name'] for a in f['verified_assets']},{t.format(version=f['published_version']) for t in spec['zip_templates']})
                    self.assertRegex(f['source_commit'],r'^[0-9a-f]{40}$')
                    self.assertRegex(f['source_manifest_sha256'],r'^[0-9a-f]{64}$')
                    for a in f['verified_assets']:
                        self.assertEqual(a['url'],v.REPO+'/releases/download/'+f['tag']+'/'+a['name'])
                        self.assertRegex(a['sha256'],r'^[0-9a-f]{64}$')
                        self.assertGreater(a['bytes'],0)
                else:
                    self.assertIsNone(f['published_version'])
                    self.assertIsNone(f['release_url'])
                    self.assertEqual(f['verified_assets'],[])
        self.assertGreaterEqual(v.numeric(facts['ja']['published_version']),(0,1,8))

    def test_all_generated_surfaces_and_idempotence(self):
        import re
        from version_display import apply_html, edition_for
        from build_version_site import outputs, readme
        from build_gateways import outputs as gateways, GATEWAYS
        facts=v.load()
        # 29 editions with version facts plus 9 shown as coming soon (no facts yet);
        # 38 tops: English (Measure) has no top of its own.
        self.assertEqual(len(GATEWAYS),38)
        for path,html in gateways().items():
            if 'http-equiv="refresh"' in html:continue
            self.assertEqual(html.count('class="version-state"'),38,path)
            self.assertEqual(len(re.findall(r'<span class="state" aria-label="[^"]+"><span class="version-state"',html)),9,path)
        pages=[*v.ROOT.glob('kumihan*.html'),v.ROOT/'en.html',v.ROOT/'zh-tw.html',*(v.ROOT/'docs').glob('install-*.html')]
        counts={'landing':0,'install':0}
        generated=outputs()
        for p in pages:
            relative=p.relative_to(v.ROOT).as_posix();code=edition_for(relative)
            if not code:continue
            html=p.read_text();install=relative.startswith('docs/')
            counts['install' if install else 'landing']+=1
            if html.startswith('---'):continue  # actual built Jekyll is checked separately
            with self.subTest(page=relative):
                self.assertEqual(apply_html(html,relative),html)
                self.assertEqual(html.count('data-edition-version='),1 if install else 2)
                from version_display import is_source_download
                for href in re.findall(r'href="([^"]+\.zip)"',html):
                    self.assertTrue(href in {a['url'] for a in facts['editions'][code]['verified_assets']}
                                    or is_source_download(href, facts['editions'][code]), (relative,href))
                for pre in re.findall(r'<pre\b.*?</pre>',html,re.S):self.assertNotIn('vX.Y.Z',pre)
        self.assertEqual(counts,{'landing':87,'install':258})
        self.assertEqual(readme(generated['README.md'],facts),generated['README.md'])
        self.assertNotIn('新版Release未作成',generated['README.md'])
        self.assertNotIn('await approval',generated['README.md'])
        for path in (v.ROOT/'docs').glob('install-*.html'):
            source=path.read_text()
            if source.startswith('---') and 'layout: installation\n' in source:
                self.assertNotIn('include_relative installation',source)
        # A future first Chinese Release must also update the prose summary.
        promoted=copy.deepcopy(facts)
        promoted['editions']['zh-hant'].update(release_status='published',published_version='0.1.0',published_at='2026-10-19T12:00:00Z',release_url=v.REPO+'/releases/tag/kumihan-ziheng-v0.1.0')
        changed=readme(generated['README.md'],promoted)
        self.assertIn('Traditional Chinese (字衡): published',changed)
        self.assertNotIn('both without a GitHub Release',changed)

    def test_sync_failure_never_replaces_facts_file(self):
        from unittest.mock import patch
        import tempfile
        import sync_edition_versions as sync
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'facts.json';before=v.FACTS.read_bytes();path.write_bytes(before)
            with patch.object(v,'FACTS',path),patch.object(sync,'releases',side_effect=OSError('offline')),patch.object(sys,'argv',['sync']):
                with self.assertRaises(OSError):sync.main()
            self.assertEqual(path.read_bytes(),before)

class PreservationGate(unittest.TestCase):
    def test_unlisted_mutations_still_fail(self):
        import tempfile
        from check_seo_preservation import audit
        from build_version_site import preservation_allowed
        self.assertFalse(preservation_allowed('LICENSE','protected'))
        self.assertFalse(preservation_allowed('privacy.html','bodies'))
        self.assertEqual(audit(),[])
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for p in v.ROOT.iterdir():
                if p.name!='.git':(root/p.name).symlink_to(p,target_is_directory=p.is_dir())
            (root/'README.md').unlink();(root/'README.md').write_text('unlisted change')
            self.assertIn('protected: main bytes changed: README.md',audit(root))

class PublishedZihengInstallLinks(unittest.TestCase):
    def test_current_guides_use_verified_host_assets_and_matching_checksums(self):
        import build_ziheng_site
        facts=v.load()['editions']['zh-hant']
        assets={a['name']:a for a in facts['verified_assets']}
        for path,body in build_ziheng_site.outputs().items():
            if not path.endswith('.html'):continue
            self.assertNotIn('retained download links are v0.1.0',body)
            self.assertNotIn('candidate is not a formal Release',body)
            self.assertNotRegex(body,r'kumihan-ziheng-(?:Claude-Code-plugin|Gemini-CLI-extension)-v?0.2.0.zip')
            self.assertNotRegex(body,r'href="[^"\n]+-0\.1\.0\.zip"')
            host='claude' if 'claude' in path else 'gemini' if 'gemini' in path else 'openai-codex'
            plugin=assets[f'kumihan-ziheng-{host}-plugin-0.2.0.zip']
            self.assertIn(plugin['url'],body)
            if path.startswith('docs/'):
                self.assertIn(plugin['sha256'],body)

class JapaneseCurrentGuideNames(unittest.TestCase):
    def test_current_zip_labels_and_commands_match_published_version(self):
        from build_version_site import generated_markdown
        f=v.load()['editions']['ja']
        source='[kumihan-GPT-Codex-plugin-0.1.8.zip](../downloads%20GPT-Codex/plugins/kumihan-GPT-Codex-plugin-0.1.8.zip)\nunzip kumihan-GPT-Codex-plugin-0.1.8.zip'
        out=generated_markdown(source,f)
        self.assertNotIn('0.1.8.zip',out)
        self.assertIn('unzip kumihan-GPT-Codex-plugin-0.2.0.zip',out)
