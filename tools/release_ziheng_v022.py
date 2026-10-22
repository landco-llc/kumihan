#!/usr/bin/env python3
"""Prepare, verify or publish only the fixed ZiHeng v0.2.2 release.

Preparation is local. Publication is restricted to the public repository's
protected-main push workflow, after its independent verification job succeeds.
Existing published tags/releases are never replaced or deleted. A single pinned, empty interrupted draft can be resumed.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = 'kumihan-ziheng'
VERSION = '0.2.2'
TAG = PRODUCT + '-v' + VERSION
REPOSITORY = 'landco-llc/kumihan'
BASE = Path('plugins') / PRODUCT
RELEASE = Path('releases') / TAG
REQUEST = RELEASE / 'REQUEST.json'
NOTES = RELEASE / 'RELEASE_NOTES.md'
HOSTS = (('downloads', 'openai-codex'), ('downloads Claude', 'claude'),
         ('downloads Gemini', 'gemini'))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def asset_names(root=ROOT):
    contracts = json.loads((Path(root) / 'assets/edition-release-contracts.json').read_bytes())
    names = [name.format(version=VERSION) for name in contracts['editions']['zh-hant']]
    if len(names) != 15 or len(set(names)) != 15:
        raise ValueError('Requires the adopted 15 ZiHeng release roles')
    if any(Path(name).name != name or not name.startswith(PRODUCT+'-') or
           not name.endswith('-'+VERSION+'.zip') for name in names):
        raise ValueError('Unexpected ZiHeng release filename')
    return set(names)


def source_fingerprint(root=ROOT):
    """Pin authored product inputs without a circular commit or request hash."""
    root = Path(root)
    base = root / BASE
    names = {'plugin.json', 'README.md', 'INSTALL.md', 'UPDATES.md',
             'LICENSE', 'THIRD_PARTY_NOTICES.md', 'sources.json'}
    for folder in ('entrypoints', 'references', 'runtime', 'schemas', 'rules',
                   'locales', 'fixtures'):
        names.update(p.relative_to(base).as_posix() for p in (base/folder).rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts)
    return digest(encoded({name:digest((base/name).read_bytes()) for name in sorted(names)}))


def collect_source_archives(root=ROOT):
    from public_boundary import forbidden
    root = Path(root)
    manifest = json.loads((root / BASE / 'plugin.json').read_bytes())
    if manifest['name'] != PRODUCT or manifest['version'] != VERSION:
        raise ValueError('This publisher accepts only ZiHeng 0.2.2')
    result = {}
    for folder, host in HOSTS:
        base = root / BASE / folder
        dist = json.loads((base/'MANIFEST.json').read_bytes())
        if dist['version'] != VERSION or len(dist['archives']) != 5:
            raise ValueError('Unexpected active host distribution')
        for row in dist['archives']:
            relative = Path(row['file'])
            if relative.is_absolute() or '..' in relative.parts or len(relative.parts) != 2:
                raise ValueError('Unsafe source archive path')
            if relative.parts[0] not in ('plugins', 'extensions', 'skills'):
                raise ValueError('Unexpected source archive role')
            source = base / relative
            raw = source.read_bytes()
            if len(raw) != row['bytes'] or digest(raw) != row['sha256']:
                raise ValueError('Source archive hash/size mismatch: '+row['file'])
            if not source.name.endswith('-'+VERSION+'.zip'):
                raise ValueError('Source archive has a different version')
            role = 'plugin' if relative.parts[0] in ('plugins', 'extensions') else source.name.removesuffix('-'+VERSION+'.zip')
            name = f'{PRODUCT}-{host}-{role}-{VERSION}.zip'
            if name in result:
                raise ValueError('Duplicate release role')
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                if archive.testzip() is not None:
                    raise ValueError('Invalid ZIP CRC')
                members = archive.namelist()
                if len(members) != len(set(members)):
                    raise ValueError('Duplicate ZIP member')
                for member in members:
                    if member.startswith('/') or '..' in Path(member).parts or forbidden(member, archive.read(member)):
                        raise ValueError('Unsafe or internal ZIP member: '+member)
            result[name] = raw
    if set(result) != asset_names(root):
        raise ValueError('Source archives do not match the 15 adopted release roles')
    return result


def release_files(root=ROOT):
    """Return the exact 17 upload bytes, freshly checked against source packages."""
    files = collect_source_archives(root)
    files['MANIFEST.json'] = encoded({
        'product':'KUMIHAN ZiHeng', 'version':VERSION,
        'status':'Typography guidance and bounded checks. Vertical case definitions are separate from rendered, native-host, accessibility and native-language acceptance.',
        'archives':[{'file':name,'bytes':len(raw),'sha256':digest(raw)}
                    for name,raw in sorted(files.items())]})
    files['SHA256SUMS.txt'] = ''.join(
        f'{digest(raw)}  {name}\n' for name,raw in sorted(files.items())).encode('utf-8')
    return files


def expected_request(root, files):
    return {
        'schema_version':1, 'repository':REPOSITORY, 'product':PRODUCT,
        'version':VERSION, 'tag':TAG,
        'source_manifest_sha256':digest((Path(root)/BASE/'plugin.json').read_bytes()),
        'source_content_sha256':source_fingerprint(root),
        'release_notes_sha256':digest((Path(root)/NOTES).read_bytes()),
        'assets':{name:{'bytes':len(raw),'sha256':digest(raw)}
                  for name,raw in sorted(files.items())},
    }


def prepare(root=ROOT):
    root = Path(root)
    files = release_files(root)
    folder = root / RELEASE
    folder.mkdir(parents=True, exist_ok=True)
    allowed = set(files) | {'REQUEST.json', 'RELEASE_NOTES.md'}
    if any(p.name not in allowed or not p.is_file() for p in folder.iterdir()):
        raise ValueError('Unexpected file in the fixed candidate directory')
    for name,raw in files.items():
        (folder/name).write_bytes(raw)
    (root/NOTES).write_text(
        '# KUMIHAN｜字衡 v0.2.2\n\n'
        'Traditional Chinese vertical typography guidance for Taiwan and Hong Kong.\n\n'
        '- Separate reading, display and hybrid purposes for vertical and horizontal compositions.\n'
        '- Add contextual punctuation, quotations, mixed-script runs, font evidence and reading-order guidance.\n'
        '- Preserve fixed source text and Unicode sequences; retain earlier distribution files.\n'
        '- Add 30 vertical case definitions with explicit verification states. Case definitions and static checks do not establish browser, native Office, assistive-technology or native-language acceptance.\n\n'
        'Four independent Skills are available in three host families: 15 ZIPs. '
        'Verify the exact downloads with MANIFEST.json and SHA256SUMS.txt. '
        'Native host installation and invocation require acceptance in the target environment.\n',encoding='utf-8')
    (root/REQUEST).write_bytes(encoded(expected_request(root,files)))
    check(root)
    print('Prepared the fixed ZiHeng v0.2.2 request and 17 assets locally; not published.')


def check(root=ROOT):
    root = Path(root)
    files = release_files(root)
    request = json.loads((root/REQUEST).read_bytes())
    if request != expected_request(root,files):
        raise ValueError('Request/source/asset fingerprint mismatch')
    for name,raw in files.items():
        if (root/RELEASE/name).read_bytes() != raw:
            raise ValueError('Candidate bytes differ from verified source: '+name)
    allowed = set(files) | {'REQUEST.json','RELEASE_NOTES.md'}
    if {p.name for p in (root/RELEASE).iterdir()} != allowed:
        raise ValueError('Unexpected or missing fixed candidate file')
    if not (root/NOTES).read_text(encoding='utf-8').startswith('# KUMIHAN｜字衡 v0.2.2\n'):
        raise ValueError('Missing release notes for this exact version')
    return files


def gh(*args):
    return subprocess.check_output(['gh',*args],cwd=ROOT,text=True)


def api(path):
    return json.loads(gh('api',path))


def assert_tag_absent():
    result = subprocess.run(['gh','api','--include',f'repos/{REPOSITORY}/git/ref/tags/{TAG}'],
                            cwd=ROOT,capture_output=True,text=True)
    statuses = re.findall(r'^HTTP/\S+\s+(\d+)',result.stdout,re.M)
    if result.returncode == 0:
        raise ValueError('Tag already exists; earlier releases are never overwritten')
    if not statuses or statuses[-1] != '404':
        raise ValueError('Could not prove the tag is absent; publication stopped')


def listed_release():
    pages = json.loads(gh('api','--paginate','--slurp',f'repos/{REPOSITORY}/releases?per_page=100'))
    rows = [item for page in pages for item in page if item['tag_name'] == TAG]
    if len(rows) > 1:
        raise ValueError('Duplicate release identity')
    return rows[0] if rows else None


def verify_remote_assets(release, files):
    rows = release['assets']
    if len(rows) != len(files) or {r['name'] for r in rows} != set(files):
        raise ValueError('Remote release does not contain exactly the 17 approved assets')
    for row in rows:
        raw = files[row['name']]
        if row['size'] != len(raw) or row.get('digest') != 'sha256:'+digest(raw):
            raise ValueError('Remote size/digest mismatch: '+row['name'])


def verify_download(files):
    with tempfile.TemporaryDirectory(prefix='ziheng-v022-readback-') as folder:
        gh('release','download',TAG,'--repo',REPOSITORY,'--dir',folder)
        actual = Path(folder)
        if {p.name for p in actual.iterdir()} != set(files):
            raise ValueError('Downloaded asset set differs')
        for name,raw in files.items():
            if (actual/name).read_bytes() != raw:
                raise ValueError('Downloaded bytes differ: '+name)


# One-off recovery authorization for the empty draft created by the successful
# verify job and interrupted publisher on 2026-10-22. This is not a generic
# permission to resume any draft or to replace any old Release.
RECOVERY_DRAFT_ID = 420671387
RECOVERY_TARGET_SHA = '68005357d896cae8cc002052a4bc0f802a71d202'
RECOVERY_CREATED_AT = '2026-10-22T12:04:49Z'


def validate_recovery_draft(draft, notes):
    if not draft or draft.get('id') != RECOVERY_DRAFT_ID:
        raise ValueError('Expected the exact interrupted ZiHeng v0.2.2 draft ID')
    if (draft.get('draft') is not True or draft.get('prerelease') is True or
        draft.get('tag_name') != TAG or
        draft.get('target_commitish') != RECOVERY_TARGET_SHA or
        draft.get('created_at') != RECOVERY_CREATED_AT or
        draft.get('name') != 'KUMIHAN｜字衡 v0.2.2' or
        (draft.get('body') or '').strip() != notes.strip()):
        raise ValueError('Interrupted draft identity or notes changed; do not modify')
    if draft.get('assets') != []:
        raise ValueError('Draft assets are no longer empty; do not modify')
    return RECOVERY_TARGET_SHA


def publish():
    if (os.environ.get('GITHUB_REPOSITORY') != REPOSITORY or
        os.environ.get('GITHUB_REF') != 'refs/heads/main' or
        os.environ.get('GITHUB_EVENT_NAME') != 'push'):
        raise ValueError('Publication is restricted to the public main-push workflow')
    sha = os.environ.get('GITHUB_SHA','')
    if not re.fullmatch(r'[0-9a-f]{40}',sha):
        raise ValueError('Missing exact source commit')
    head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    if sha != head or api(f'repos/{REPOSITORY}/commits/main')['sha'] != sha:
        raise ValueError('Checkout and current protected main must match the tested workflow commit')
    # All source packages are freshly byte-checked at the new protected-main
    # commit. No source packages, release request or archived versions may change.
    files = check()
    assert_tag_absent()
    draft = listed_release()
    target = validate_recovery_draft(draft, (ROOT / NOTES).read_text(encoding='utf-8'))
    gh('release', 'upload', TAG, '--repo', REPOSITORY,
       *(str(ROOT / RELEASE / name) for name in sorted(files)))
    uploaded = api(f'repos/{REPOSITORY}/releases/{RECOVERY_DRAFT_ID}')
    verify_remote_assets(uploaded, files)
    verify_download(files)
    # Only a completely verified draft may become published.
    gh('release', 'edit', TAG, '--repo', REPOSITORY, '--draft=false', '--latest=false')
    published = api(f'repos/{REPOSITORY}/releases/tags/{TAG}')
    if published['draft'] or published['prerelease'] or not published.get('published_at'):
        raise ValueError('Publication readback did not confirm a stable public release')
    if api(f'repos/{REPOSITORY}/git/ref/tags/{TAG}')['object']['sha'] != target:
        raise ValueError('Published tag does not match the originally verified source commit')
    verify_remote_assets(published, files)
    verify_download(files)
    print(published['html_url'])

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--prepare',action='store_true')
    choice.add_argument('--check',action='store_true')
    choice.add_argument('--publish',action='store_true')
    args = parser.parse_args()
    if args.prepare:
        prepare()
    elif args.check:
        files = check()
        print(f'ZiHeng v0.2.2 fixed request and {len(files)} assets verified; no writes.')
    else:
        publish()


if __name__ == '__main__':
    main()
