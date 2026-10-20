#!/usr/bin/env python3
"""Build only 字衡, never Japanese distributions. Python 3.9+, stdlib only.

Canonical inputs: plugins/kumihan-ziheng excluding skills/, downloads/ and the
Codex overlay; shared policies are read-only inputs in skills/kumihan. Generated
files are compared by --check and may not be edited independently.
"""
import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path

from ziheng_retention import retained_outputs
from locale_resolver import COMMON, MEDIA, resolve_context, resolve_rules

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = 'plugins/kumihan-ziheng'
NAMES = ('kumihan-ziheng', 'kumihan-ziheng-web', 'kumihan-ziheng-documents', 'kumihan-ziheng-review')
DATE = (2026, 10, 18, 0, 0, 0)
VERSION_RE = r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)'


def encode(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def archive(files):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        for path, data in sorted(files.items()):
            info = zipfile.ZipInfo(path, DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data, compresslevel=9)
    return buf.getvalue()


def plan_outputs(root=ROOT):
    """Return generated repo-relative paths/bytes, with no writes or side effects."""
    root = Path(root)
    base = root / PRODUCT
    manifest = json.loads((base/'plugin.json').read_text(encoding='utf-8'))
    version = manifest['version']
    if re.fullmatch(VERSION_RE, version) is None:
        raise ValueError('Invalid product version')
    if manifest['name'] != 'kumihan-ziheng':
        raise ValueError('Unexpected product identity')
    shared = {}
    provenance = []
    common_records = []
    for group in COMMON:
        rel = f'skills/kumihan/rules/{group}.json'
        data = (root/rel).read_bytes()
        common_records.extend(json.loads(data))
        provenance.append(dict(path=rel, sha256=digest(data)))
    zh_records = json.loads((base/'rules/zh-hant.json').read_text(encoding='utf-8'))
    records = common_records + zh_records
    ids = [r['id'] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate rule ID')
    shared['rules/catalog.json'] = encode(records)
    required_sources = {s for r in records for s in r['source_refs']}
    inherited = json.loads((root/'skills/kumihan/sources/public-sources.json').read_text(encoding='utf-8'))['sources']
    own = json.loads((base/'sources.json').read_text(encoding='utf-8'))['sources']
    selected = [s for s in inherited if s['id'] in required_sources] + own
    if not required_sources <= {s['id'] for s in selected}:
        raise ValueError('Unresolved source ID')
    shared['sources/public-sources.json'] = encode(dict(registry_version='1.0.0', sources=selected))
    shared['sources/common-provenance.json'] = encode(dict(
        note='Generated from canonical Japanese shared policies; never independently edit shipped copies.',
        inputs=provenance))
    for folder in ['references', 'schemas', 'locales', 'fixtures']:
        for p in sorted((base/folder).rglob('*')):
            if p.is_file():
                shared[p.relative_to(base).as_posix()] = p.read_bytes()
    for script in ('checks', 'context', 'evidence'):
        shared[f'scripts/{script}.py'] = (base/f'runtime/{script}.py').read_bytes()
    shared['LICENSE'] = (root/'LICENSE').read_bytes()
    shared['THIRD_PARTY_NOTICES.md'] = (base/'THIRD_PARTY_NOTICES.md').read_bytes()
    for medium in MEDIA:
        by_locale = {tag: [r['id'] for r in resolve_rules(resolve_context(tag, medium), root)]
                     for tag in ['zh-Hant-TW', 'zh-Hant-HK']}
        shared[f'profiles/{medium}.json'] = encode(dict(
            id=medium, revision=1, rules_by_locale=by_locale,
            guidance='Select explicit locale before reading records. Rule selection is not a detector pass.'))
    outputs = {}
    plugin_files = {'plugin.json': (base/'plugin.json').read_bytes(),
                    'LICENSE': shared['LICENSE'],
                    'THIRD_PARTY_NOTICES.md': shared['THIRD_PARTY_NOTICES.md']}
    outputs[f'{PRODUCT}/LICENSE'] = shared['LICENSE']
    for doc in ['README.md', 'INSTALL.md', 'UPDATES.md']:
        plugin_files[doc] = (base/doc).read_bytes()
    from legacy_release_documents import documents
    for name,raw in documents(root, f'kumihan-ziheng-{version}.zip').items():
        plugin_files[name.removeprefix('kumihan-ziheng/')] = raw
    # Use the approved repository master logo as the only canonical image source.
    # Ship an unmodified local copy so the standalone plugin can render its icon.
    logo_rel = 'assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png'
    logo_bytes = (root / logo_rel).read_bytes()
    outputs[f'{PRODUCT}/{logo_rel}'] = logo_bytes
    plugin_files[logo_rel] = logo_bytes
    # Portable root identity is canonical. Overlay is generated for older Codex hosts.
    overlay = {k: v for k, v in manifest.items() if k not in ['$schema', 'extensions']}
    overlay.update(manifest['extensions']['com.openai'])
    overlay['skills'] = './skills/'
    outputs[f'{PRODUCT}/.codex-plugin/plugin.json'] = encode(overlay)
    plugin_files['.codex-plugin/plugin.json'] = encode(overlay)
    archives = {}
    for name in NAMES:
        files = dict(shared)
        files['SKILL.md'] = (base/'entrypoints'/f'{name}.md').read_bytes()
        files['inventory.json'] = encode(dict(format='kumihan-ziheng-standalone-1', skill=name,
            version=version, path_base='skill-folder-root',
            self_digest='Inventory excludes itself; distribution checksums cover the complete archive.',
            files=[dict(path=p, bytes=len(b), sha256=digest(b)) for p, b in sorted(files.items())]))
        for p, b in files.items():
            outputs[f'{PRODUCT}/skills/{name}/{p}'] = b
            plugin_files[f'skills/{name}/{p}'] = b
        archives[f'skills/{name}-{version}.zip'] = archive({f'{name}/{p}': b for p, b in files.items()})
    archives[f'plugins/kumihan-ziheng-{version}.zip'] = archive({f'kumihan-ziheng/{p}': b for p,b in plugin_files.items()})
    dist = dict(product='KUMIHAN｜字衡', name='kumihan-ziheng', version=version,
        status='Source distribution candidate; native host discovery/invocation not checked.',
        archives=[dict(file=p, bytes=len(b), sha256=digest(b)) for p,b in sorted(archives.items())])
    archives['MANIFEST.json'] = encode(dist)
    archives['SHA256SUMS.txt'] = ''.join(f'{digest(b)}  {p}\n' for p,b in sorted(archives.items())).encode()
    for p,b in archives.items():
        outputs[f'{PRODUCT}/downloads/{p}'] = b
    retained = retained_outputs(root, ('downloads',))
    for path, data in retained.items():
        if path in outputs and outputs[path] != data:
            raise ValueError('Historical output collision: ' + path)
        outputs[path] = data
    return outputs


def generated_files(root=ROOT):
    base = Path(root)/PRODUCT
    return {p.relative_to(root).as_posix() for folder in ['skills', 'downloads', '.codex-plugin', 'assets']
            for p in (base/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--set-version', help='Change only the 字衡 canonical manifest version, then rebuild')
    args = parser.parse_args()
    if args.set_version:
        if args.check or re.fullmatch(VERSION_RE, args.set_version) is None:
            parser.error('Use a valid version; --set-version cannot be combined with --check')
        path = ROOT/PRODUCT/'plugin.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        data['version'] = args.set_version
        path.write_bytes(encode(data))
    planned = plan_outputs(ROOT)
    changed = [p for p,b in planned.items() if not (ROOT/p).is_file() or (ROOT/p).read_bytes()!=b]
    stale = generated_files(ROOT)-set(planned)
    if args.check:
        if changed or stale:
            for p in sorted(set(changed)|stale): print(f'out of date: {p}')
            return 1
        print(f'OK: 字衡 {len(planned)} generated files up to date')
        return 0
    for p in changed:
        target = ROOT/p
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(planned[p])
    for p in stale: (ROOT/p).unlink()
    print(f'Built 字衡: {len(planned)} files; {len(changed)} updated; {len(stale)} stale removed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
