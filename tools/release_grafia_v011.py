#!/usr/bin/env python3
"""Finish only the protected-main, reviewed Grafía v0.1.1 draft request.

No release creation, asset replacement, deletion or arbitrary tag is supported.
Retained v0.1.0 archives never enter the manifest-selected 17-asset payload.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]
REPO='landco-llc/kumihan'
TAG='kumihan-grafia-v0.1.1'
TITLE='KUMIHAN｜Grafía v0.1.1'
PRODUCT='plugins/kumihan-grafia'
FOLDER=Path('releases')/TAG


def digest(raw):return hashlib.sha256(raw).hexdigest()


def local_assets(root=ROOT):
    destination=Path(root)/PRODUCT/'downloads'
    manifest_raw=(destination/'MANIFEST.json').read_bytes()
    manifest=json.loads(manifest_raw)
    if (manifest.get('product'),manifest.get('version'),manifest.get('tag'))!=('KUMIHAN｜Grafía','0.1.1',TAG):
        raise ValueError('Wrong Grafía product, version or tag')
    rows=manifest['archives'];files={}
    if len(rows)!=15:raise ValueError('Exactly 15 manifest archives required')
    for row in rows:
        name=row['file']
        if not re.fullmatch(r'kumihan-grafia-[A-Za-z0-9-]+-v0\.1\.1\.zip',name) or name in files:
            raise ValueError('Unsafe, duplicate or wrong-version archive')
        raw=(destination/name).read_bytes()
        if row['bytes']!=len(raw) or row['sha256']!=digest(raw):
            raise ValueError('Manifest size/hash mismatch')
        files[name]=raw
    expected_names={f'{skill}-{host}-skill-v0.1.1.zip'
                    for skill in ('kumihan-grafia','kumihan-grafia-web','kumihan-grafia-documents','kumihan-grafia-review')
                    for host in ('GPT-Codex','Claude','Gemini-Apps')}
    expected_names.update(f'kumihan-grafia-{host}-v0.1.1.zip'
                          for host in ('GPT-Codex-plugin','Claude-Code-plugin','Gemini-CLI-extension'))
    if set(files)!=expected_names:raise ValueError('Missing or replaced host/skill role')
    sums=(destination/'SHA256SUMS.txt').read_bytes()
    expected={}
    for line in sums.decode('utf-8').splitlines():
        match=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
        if not match or match[2] in expected:raise ValueError('Invalid or duplicate checksum row')
        expected[match[2]]=match[1]
    checksummed={name:digest(raw) for name,raw in files.items()}
    checksummed['MANIFEST.json']=digest(manifest_raw)
    if expected!=checksummed:
        raise ValueError('Checksum set differs from 15 archives and manifest')
    files.update({'MANIFEST.json':manifest_raw,'SHA256SUMS.txt':sums})
    return files


def request(root=ROOT):
    root=Path(root);folder=root/FOLDER
    if {p.name for p in folder.iterdir()}!={'REQUEST.json','RELEASE_NOTES.md'}:
        raise ValueError('Unexpected release request payload')
    r=json.loads((folder/'REQUEST.json').read_bytes())
    if (r.get('schema_version'),r.get('repository'),r.get('product'),r.get('version'),r.get('tag'),r.get('title'))!=(1,REPO,'kumihan-grafia','0.1.1',TAG,TITLE):
        raise ValueError('Wrong fixed release request identity')
    if (not re.fullmatch(r'[0-9a-f]{40}',r.get('target_commit','')) or
        not re.fullmatch(r'[0-9a-f]{40}',r.get('product_tree','')) or
        type(r.get('draft_id')) is not int or r['draft_id']<=0 or
        not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ',r.get('created_at',''))):
        raise ValueError('Invalid pinned target, product tree or draft')
    return r


def check(root=ROOT):
    root=Path(root);r=request(root);files=local_assets(root)
    if digest((root/FOLDER/'RELEASE_NOTES.md').read_bytes())!=r['notes_sha256']:
        raise ValueError('Release notes changed')
    if {n:{'bytes':len(b),'sha256':digest(b)} for n,b in files.items()}!=r['assets']:
        raise ValueError('Exact 17-asset request changed')
    return files


def gh(*args):return subprocess.check_output(['gh',*args],cwd=ROOT,text=True)
def api(path):return json.loads(gh('api',path))


def assert_tag_absent():
    result=subprocess.run(['gh','api','--include',f'repos/{REPO}/git/ref/tags/{TAG}'],cwd=ROOT,capture_output=True,text=True)
    statuses=re.findall(r'^HTTP/\S+\s+(\d+)',result.stdout,re.M)
    if result.returncode==0 or not statuses or statuses[-1]!='404':
        raise ValueError('New tag absence not proven')


def validate_release(release,r,notes,*,draft):
    if (release.get('id')!=r['draft_id'] or release.get('draft') is not draft or release.get('prerelease') is not False or
        release.get('tag_name')!=TAG or release.get('target_commitish')!=r['target_commit'] or
        (draft and release.get('created_at')!=r['created_at']) or release.get('name')!=TITLE or
        (release.get('body') or '').strip()!=notes.strip()):
        raise ValueError('Pinned release identity or state changed')


def verify_remote_subset(release,files):
    rows=release['assets'];names=[row['name'] for row in rows]
    if len(names)!=len(set(names)) or set(names)-set(files):raise ValueError('Unknown or duplicate remote asset')
    for row in rows:
        raw=files[row['name']]
        if row['size']!=len(raw) or row.get('digest')!='sha256:'+digest(raw):
            raise ValueError('Remote size or digest differs')
    return set(files)-set(names)


def verify_download(files):
    with tempfile.TemporaryDirectory(prefix='grafia-v011-readback-') as temporary:
        # Individual exact patterns also support resuming a matching partial draft.
        args=['release','download',TAG,'--repo',REPO,'--dir',temporary]
        for name in sorted(files):args+=['--pattern',name]
        gh(*args)
        folder=Path(temporary)
        if {p.name for p in folder.iterdir()}!=set(files):raise ValueError('Downloaded asset set differs')
        for name,raw in files.items():
            if (folder/name).read_bytes()!=raw:raise ValueError('Downloaded asset bytes differ')


def verify_complete(release,r,notes,files,*,draft):
    validate_release(release,r,notes,draft=draft)
    if verify_remote_subset(release,files) or len(release['assets'])!=17:
        raise ValueError('Incomplete exact 17-asset release')
    verify_download(files)
    if not draft:
        if (not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', release.get('published_at') or '') or release.get('html_url')!='https://github.com/'+REPO+'/releases/tag/'+TAG or
            api(f'repos/{REPO}/git/ref/tags/{TAG}')['object']['sha']!=r['target_commit']):
            raise ValueError('Published tag, URL or date differs')


def publish():
    if (os.environ.get('GITHUB_REPOSITORY'),os.environ.get('GITHUB_REF'),os.environ.get('GITHUB_EVENT_NAME'))!=(REPO,'refs/heads/main','push'):
        raise ValueError('Only native protected-main push may publish')
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    if head!=os.environ.get('GITHUB_SHA') or api(f'repos/{REPO}/commits/main')['sha']!=head:
        raise ValueError('Checkout, workflow and current main differ')
    files=check();r=request();notes=(ROOT/FOLDER/'RELEASE_NOTES.md').read_text()
    target=r['target_commit']
    subprocess.run(['git','merge-base','--is-ancestor',target,head],cwd=ROOT,check=True)
    subprocess.run(['git','diff','--exit-code',target,'--',PRODUCT],cwd=ROOT,check=True)
    if subprocess.check_output(['git','rev-parse',target+':'+PRODUCT],cwd=ROOT,text=True).strip()!=r['product_tree']:
        raise ValueError('Pinned product tree differs')
    pages=json.loads(gh('api','--paginate','--slurp',f'repos/{REPO}/releases?per_page=100'))
    matches=[release for page in pages for release in page if release.get('tag_name')==TAG]
    if len(matches)!=1 or matches[0]['id']!=r['draft_id']:raise ValueError('Draft is not uniquely pinned')
    release=api(f'repos/{REPO}/releases/{r["draft_id"]}')
    if release.get('draft') is False:
        verify_complete(release,r,notes,files,draft=False)
        print(release['html_url']);return
    validate_release(release,r,notes,draft=True);assert_tag_absent()
    missing=verify_remote_subset(release,files)
    existing={name:raw for name,raw in files.items() if name not in missing}
    if existing:verify_download(existing)
    with tempfile.TemporaryDirectory(prefix='grafia-v011-upload-') as temporary:
        for name in missing:(Path(temporary)/name).write_bytes(files[name])
        if missing:gh('release','upload',TAG,'--repo',REPO,*(str(Path(temporary)/name) for name in sorted(missing)))
    fresh=api(f'repos/{REPO}/releases/{r["draft_id"]}')
    verify_complete(fresh,r,notes,files,draft=True);assert_tag_absent()
    gh('release','edit',TAG,'--repo',REPO,'--draft=false','--latest=false')
    published=api(f'repos/{REPO}/releases/tags/{TAG}')
    verify_complete(published,r,notes,files,draft=False)
    print(published['html_url'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check',action='store_true');group.add_argument('--publish',action='store_true');args=parser.parse_args()
    if args.check:print(f'Grafía fixed request and {len(check())} assets verified; no writes.')
    else:publish()
