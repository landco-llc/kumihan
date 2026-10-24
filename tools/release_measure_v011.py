#!/usr/bin/env python3
"""Verify and finish only the exact Measure v0.1.1 release draft.

Existing assets are resumed only after exact metadata and downloaded-byte checks.
No release creation, deletion, asset replacement or arbitrary target is supported.
The native main-push workflow verifies first; only its publisher can write.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from measure_consumer import check_distribution

ROOT=Path(__file__).resolve().parents[1]
REPO='landco-llc/kumihan'
TAG='kumihan-measure-v0.1.1'
TARGET='db6f453160e46c568a007c76afd2030bc8e61512'
DRAFT=422834442
FOLDER=Path('releases')/TAG
REQUEST=FOLDER/'REQUEST.json'
NOTES=FOLDER/'RELEASE_NOTES.md'
REQUEST_SHA='095564a7ece2e86ad54dd1058e1dd122d64f1cb2c4182248cbbda9d6ae6080e3'

def digest(raw):return hashlib.sha256(raw).hexdigest()

def request(root=ROOT):
    raw=(Path(root)/REQUEST).read_bytes()
    if digest(raw)!=REQUEST_SHA:raise ValueError('Changed exact Measure release request')
    result=json.loads(raw)
    if (result['repository'],result['tag'],result['target_commit'],result['draft_id'])!=(REPO,TAG,TARGET,DRAFT):
        raise ValueError('Changed release identity')
    return result

def check(root=ROOT):
    root=Path(root);r=request(root)
    if {p.name for p in (root/FOLDER).iterdir()}!={'REQUEST.json','RELEASE_NOTES.md'}:
        raise ValueError('Unexpected release request payload')
    if digest((root/NOTES).read_bytes())!=r['notes_sha256']:raise ValueError('Changed release notes')
    product=root/'plugins/kumihan-measure';destination=product/'downloads'
    manifest=check_distribution(product,destination)
    if manifest['source_sha256']!=r['source_sha256']:raise ValueError('Changed release product source')
    files={row['file']:(destination/row['file']).read_bytes() for row in manifest['packages']}
    files['MANIFEST.json']=(destination/'manifest.json').read_bytes()
    files['SHA256SUMS.txt']=(''.join(f'{digest(files[n])}  {n}\n' for n in sorted(files) if n.endswith('.zip'))+f'{digest(files["MANIFEST.json"])}  MANIFEST.json\n').encode()
    actual={name:{'bytes':len(raw),'sha256':digest(raw)} for name,raw in files.items()}
    if len(files)!=17 or actual!=r['assets']:raise ValueError('Changed exact 17 assets')
    return files

def gh(*args):return subprocess.check_output(['gh',*args],cwd=ROOT,text=True)
def api(path):return json.loads(gh('api',path))

def assert_tag_absent():
    result=subprocess.run(['gh','api','--include',f'repos/{REPO}/git/ref/tags/{TAG}'],cwd=ROOT,capture_output=True,text=True)
    statuses=re.findall(r'^HTTP/\S+\s+(\d+)',result.stdout,re.M)
    if result.returncode==0 or not statuses or statuses[-1]!='404':
        raise ValueError('Could not prove the new release tag is absent')

def assert_unique_draft():
    pages=json.loads(gh('api','--paginate','--slurp',f'repos/{REPO}/releases?per_page=100'))
    matches=[r for page in pages for r in page if r.get('tag_name')==TAG]
    if len(matches)!=1 or matches[0].get('id')!=DRAFT:
        raise ValueError('Release tag does not uniquely identify the exact draft')

def validate_release(release,r,notes,*,draft,empty=False):
    if (release.get('id')!=DRAFT or release.get('draft') is not draft or release.get('prerelease') is not False or
        release.get('tag_name')!=TAG or release.get('target_commitish')!=TARGET or
        release.get('created_at')!=r['created_at'] or release.get('name')!=r['title'] or
        (release.get('body') or '').strip()!=notes.strip()):
        raise ValueError('Exact draft identity or state changed')
    if empty and release.get('assets')!=[]:
        raise ValueError('Draft no longer empty; stop without replacing any asset')

def verify_remote_subset(release,files):
    rows=release['assets']
    names=[r['name'] for r in rows]
    if len(names)!=len(set(names)) or set(names)-set(files):raise ValueError('Unknown or duplicate remote asset')
    for row in rows:
        raw=files[row['name']]
        if row['size']!=len(raw) or row.get('digest')!='sha256:'+digest(raw):
            raise ValueError('Remote asset digest or size differs')
    return set(files)-set(names)

def verify_remote_assets(release,files):
    if verify_remote_subset(release,files) or len(release['assets'])!=17:
        raise ValueError('Wrong remote asset set')

def verify_download(files):
    with tempfile.TemporaryDirectory(prefix='measure-v011-readback-') as temporary:
        gh('release','download',TAG,'--repo',REPO,'--dir',temporary)
        folder=Path(temporary)
        if {p.name for p in folder.iterdir()}!=set(files):raise ValueError('Downloaded asset set differs')
        for name,raw in files.items():
            if (folder/name).read_bytes()!=raw:raise ValueError('Downloaded asset bytes differ')

def publish():
    if (os.environ.get('GITHUB_REPOSITORY'),os.environ.get('GITHUB_REF'),os.environ.get('GITHUB_EVENT_NAME'))!=(REPO,'refs/heads/main','push'):
        raise ValueError('Only the native protected-main push workflow may publish')
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    if head!=os.environ.get('GITHUB_SHA') or api(f'repos/{REPO}/commits/main')['sha']!=head:
        raise ValueError('Checkout, tested workflow and current main differ')
    subprocess.run(['git','merge-base','--is-ancestor',TARGET,head],cwd=ROOT,check=True)
    subprocess.run(['git','diff','--exit-code',TARGET,'--','plugins/kumihan-measure'],cwd=ROOT,check=True)
    files=check();r=request();notes=(ROOT/NOTES).read_text()
    assert_tag_absent()
    assert_unique_draft()
    release=api(f'repos/{REPO}/releases/{DRAFT}')
    validate_release(release,r,notes,draft=True)
    missing=verify_remote_subset(release,files)
    existing={name:raw for name,raw in files.items() if name not in missing}
    if existing:verify_download(existing)
    # Matching existing assets are never rewritten. Unknown or differing assets
    # stop before writes; only missing, pinned bytes may be uploaded.
    with tempfile.TemporaryDirectory(prefix='measure-v011-upload-') as temporary:
        for name,raw in files.items():(Path(temporary)/name).write_bytes(raw)
        if missing:
            gh('release','upload',TAG,'--repo',REPO,*(str(Path(temporary)/name) for name in sorted(missing)))
    uploaded=api(f'repos/{REPO}/releases/{DRAFT}')
    validate_release(uploaded,r,notes,draft=True);verify_remote_assets(uploaded,files);verify_download(files)
    # Fresh metadata and tag check immediately before the irreversible publication.
    fresh=api(f'repos/{REPO}/releases/{DRAFT}')
    validate_release(fresh,r,notes,draft=True);verify_remote_assets(fresh,files);assert_tag_absent();assert_unique_draft()
    gh('release','edit',TAG,'--repo',REPO,'--draft=false','--latest=false')
    published=api(f'repos/{REPO}/releases/tags/{TAG}')
    validate_release(published,r,notes,draft=False)
    if not published.get('published_at') or api(f'repos/{REPO}/git/ref/tags/{TAG}')['object']['sha']!=TARGET:
        raise ValueError('Published tag or date differs')
    verify_remote_assets(published,files);verify_download(files)
    print(published['html_url'])

if __name__=='__main__':
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--check',action='store_true');g.add_argument('--publish',action='store_true');a=p.parse_args()
    if a.check:print(f'Measure fixed request and {len(check())} assets verified; no writes.')
    else:publish()
