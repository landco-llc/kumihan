"""Edition catalogue and fail-closed Release admission. Offline renderers never use APIs."""
import copy
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/landco-llc/kumihan'
FACTS = ROOT / 'assets/edition-versions.json'
# Existing product tag slugs are intentionally independent of language codes.
PRODUCTS = {
    'ja': ('', '', 15), 'ar': ('ar', 'ar', 15), 'bn': ('bn', 'bn', 7),
    'de': ('satzbild', 'de', 15), 'es': ('grafia', 'grafia', 15),
    'fa': ('fa', 'fa', 15), 'fr': ('accord', 'fr', 15), 'hi': ('hi', 'hi', 15),
    'id': ('laras', 'id', 15), 'it': ('equilibrio', 'it', 15),
    'km': ('lumnung', 'km', 15), 'ko': ('geuljjaim', 'ko', 15),
    'pl': ('szyk', 'szyk', 15), 'pt': ('compasso', 'pt', 15),
    'ru': ('lad', 'ru', 15), 'sw': ('mizani', 'sw', 15),
    'th': ('th', 'th', 15), 'vi': ('nhip-chu', 'vi', 15),
    'zh-hans': ('zilu', 'zilu', 15), 'zh-hant': ('ziheng', 'ziheng', 15),
    'zu': ('hlela', 'zu', 15),
}


def catalogue():
    return {code: dict(edition=code, product=('kumihan-'+slug if slug else 'kumihan'),
                       source_manifest=(f'plugins/kumihan-{slug}/plugin.json' if slug else 'plugin.json'),
                       tag_prefix=(f'kumihan-{tag}-v' if tag else 'v'), zip_count=count)
            for code, (slug, tag, count) in PRODUCTS.items()}


def numeric(version):
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Not a stable numeric version: '+version)
    return tuple(map(int, version.split('.')))


def source_version(spec, read=None, tag=None):
    data = read(tag, spec['source_manifest']) if read else (ROOT / spec['source_manifest']).read_bytes()
    version = json.loads(data)['version'].removeprefix('v')
    numeric(version)
    return version


def git_source(tag, path):
    # tag has already passed exact product-prefix + numeric-version validation.
    return subprocess.check_output(['git', 'show', f'{tag}:{path}'], cwd=ROOT)


def manifest_entries(data):
    rows = data.get('archives', data.get('packages', data.get('files', [])))
    if not isinstance(rows, list):
        raise ValueError('Invalid archive manifest')
    result = {}
    for row in rows:
        name = Path(row.get('release_asset', row.get('file', row.get('name', '')))).name
        if not name.endswith('.zip'): continue
        if name in result: raise ValueError('Duplicate manifest asset: '+name)
        result[name] = row
    return result


def verify_release(spec, release, fetch, read_source=git_source):
    tag = release['tag_name']
    if release['draft'] or release['prerelease'] or not tag.startswith(spec['tag_prefix']):
        raise ValueError('Not a formal edition release')
    version = tag[len(spec['tag_prefix']):]
    numeric(version)
    if source_version(spec, read_source, tag) != version:
        raise ValueError('Pinned source manifest version mismatch')
    url = REPO+'/releases/tag/'+tag
    if release['html_url'] != url or not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', release.get('published_at') or ''):
        raise ValueError('Invalid release URL/date')
    assets = {a['name']: a for a in release['assets']}
    if len(assets) != len(release['assets']): raise ValueError('Duplicate asset names')
    zips = {n: a for n, a in assets.items() if n.endswith('.zip')}
    if len(zips) != spec['zip_count']: raise ValueError('Incomplete ZIP contract: '+tag)
    for name in zips:
        if not name.startswith(spec['product']+'-') or not re.search(r'-v?'+re.escape(version)+r'\.zip$',name):
            raise ValueError('Wrong edition/version ZIP: '+name)
    manifests = []
    metadata = []
    checksums = {}
    # Japanese releases have 15 ZIPs only; their three per-host manifests live at the pinned tag.
    if spec['edition'] == 'ja':
        manifests = [json.loads(read_source(tag, folder+'/MANIFEST.json'))
                     for folder in ('downloads GPT-Codex', 'downloads Claude', 'downloads Gemini')]
    else:
        if not {'MANIFEST.json','SHA256SUMS.txt'} <= set(assets): raise ValueError('Missing release manifest/checksums')
        manifest_asset = assets['MANIFEST.json']
        manifest_bytes = fetch_asset(manifest_asset, tag, fetch)
        manifests = [json.loads(manifest_bytes)]
        sums = fetch_asset(assets['SHA256SUMS.txt'], tag, fetch)
        for line in sums.decode('utf-8').splitlines():
            match=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
            if not match: raise ValueError('Malformed SHA256SUMS')
            name=Path(match[2]).name
            if name in checksums: raise ValueError('Duplicate checksum asset')
            checksums[name]=match[1]
        for name,data in [('MANIFEST.json',manifest_bytes),('SHA256SUMS.txt',sums)]:
            metadata.append(dict(name=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),url=assets[name]['browser_download_url']))
        if 'MANIFEST.json' in checksums and checksums['MANIFEST.json'] != hashlib.sha256(manifest_bytes).hexdigest():
            raise ValueError('Manifest checksum mismatch')
        if {n for n in checksums if n.endswith('.zip')} != set(zips):
            raise ValueError('Incomplete checksum asset set')
    expected = {}
    for m in manifests:
        if m['version'].removeprefix('v') != version: raise ValueError('Release manifest version mismatch')
        for name, row in manifest_entries(m).items():
            if name in expected: raise ValueError('Duplicate archive across manifests')
            expected[name] = row
    if set(expected) != set(zips): raise ValueError('Manifest / Release asset set mismatch')
    verified = []
    for name, asset in sorted(zips.items()):
        data = fetch_asset(asset, tag, fetch)
        sha = hashlib.sha256(data).hexdigest()
        entry = expected[name]
        if entry['sha256'] != sha or ('bytes' in entry and entry['bytes'] != len(data)) or (checksums and checksums.get(name) != sha):
            raise ValueError('Manifest SHA/size mismatch: '+name)
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            if z.testzip() is not None: raise ValueError('Invalid ZIP CRC: '+name)
        verified.append(dict(name=name, bytes=len(data), sha256=sha, url=asset['browser_download_url']))
    result = dict(published_version=version, release_status='published', published_at=release['published_at'],
                release_url=url, tag=tag, release_id=release['id'], verified_assets=verified, verified_metadata=metadata,
                source_manifest_sha256=hashlib.sha256(read_source(tag, spec['source_manifest'])).hexdigest())
    if read_source is git_source:
        result['source_commit'] = subprocess.check_output(['git','rev-parse',tag+'^{commit}'],cwd=ROOT,text=True).strip()
        result['source_tree'] = subprocess.check_output(['git','rev-parse',tag+'^{tree}'],cwd=ROOT,text=True).strip()
    return result


def fetch_asset(asset, tag, fetch):
    url = REPO+'/releases/download/'+tag+'/'+asset['name']
    if asset['browser_download_url'] != url: raise ValueError('Unexpected asset URL')
    data = fetch(url)
    sha = hashlib.sha256(data).hexdigest()
    if asset['size'] != len(data): raise ValueError('API size mismatch: '+asset['name'])
    if asset.get('digest') and asset['digest'] != 'sha256:'+sha:
        raise ValueError('API digest mismatch: '+asset['name'])
    return data


def select_release(spec, old, releases, fetch, read_source=git_source):
    result = copy.deepcopy(old)
    candidates = []
    for r in releases:
        if r['draft'] or r['prerelease'] or not r['tag_name'].startswith(spec['tag_prefix']): continue
        suffix = r['tag_name'][len(spec['tag_prefix']):]
        if not re.fullmatch(r'\d+\.\d+\.\d+', suffix): continue
        if old.get('published_version') and numeric(suffix) < numeric(old['published_version']): continue
        candidates.append((numeric(suffix), r))
    if candidates:
        # Reverify identical events too: corrupted/removed assets must fail without writes.
        result.update(verify_release(spec, max(candidates, key=lambda pair: pair[0])[1], fetch, read_source))
    return result


def load():
    return json.loads(FACTS.read_text(encoding='utf-8'))
