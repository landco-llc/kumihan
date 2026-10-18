#!/usr/bin/env python3
"""Deterministic independent Thai distributions; Python standard library only."""
import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = 'plugins/kumihan-th'
NAMES = ('kumihan-th', 'kumihan-th-web', 'kumihan-th-documents', 'kumihan-th-review')
LOGO = 'assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png'
LOGO_SHA = '1d1ae2cb4f7f69f7b5f54b050ff8c6fb2c315b75ded8003f8b605855d633f96e'


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def archive(files):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as z:
        for path, data in sorted(files.items()):
            if Path(path).is_absolute() or '..' in Path(path).parts:
                raise ValueError('Unsafe archive path')
            info = zipfile.ZipInfo(path, (2026, 10, 18, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data, compresslevel=9)
    return stream.getvalue()


def inventory(files, **identity):
    return encode(dict(**identity, path_base='package-root', self_digest='Inventory excludes itself.',
        files=[dict(path=p, bytes=len(b), sha256=digest(b)) for p,b in sorted(files.items())]))


def bilingual(value):
    # Thai must precede the English explanation; reject missing language metadata.
    thai = re.search(r'[\u0e00-\u0e7f]', value)
    english = re.search(r'[A-Za-z]{3}', value)
    if not thai or not english or thai.start() > english.start():
        raise ValueError('Thai first and English descriptions required')


def plan_outputs(root=ROOT):
    root = Path(root)
    base = root/PRODUCT
    manifest = json.loads((base/'plugin.json').read_text())
    if (manifest['name'], manifest['version'], manifest['locale']) != ('kumihan-th', '0.1.1', 'th-TH'):
        raise ValueError('Unexpected Thai identity/version/locale')
    interface = manifest['extensions']['com.openai']['interface']
    if interface['displayName'] != 'KUMIHAN｜ดุลอักษร':
        raise ValueError('Unexpected display name')
    for value in (manifest['description'], interface['shortDescription'], interface['longDescription']):
        bilingual(value)
    for host_manifest in ('.claude-plugin/plugin.json', 'gemini-extension.json'):
        host = json.loads((base/host_manifest).read_text())
        if (host['name'], host['version']) != ('kumihan-th', manifest['version']):
            raise ValueError('Host identity/version mismatch')
        bilingual(host['description'])
        if 'displayName' in host and host['displayName'] != interface['displayName']:
            raise ValueError('Host display name mismatch')
    for name in NAMES:
        text = (base/'entrypoints'/f'{name}.md').read_text()
        description = re.search(r'^description: (.+)$', text, re.M)
        if not description:
            raise ValueError('Missing Thai and English skill description')
        bilingual(description.group(1))
    logo = (root/LOGO).read_bytes()
    if digest(logo) != LOGO_SHA:
        raise ValueError('Approved logo digest mismatch')
    shared = {}
    for folder in ('rules', 'references', 'schemas', 'locales', 'runtime'):
        for path in sorted((base/folder).rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts:
                if path.is_symlink():
                    raise ValueError('Symlink source is not allowed')
                shared[path.relative_to(base).as_posix()] = path.read_bytes()
    for required in ('rules/catalog.json', 'runtime/check_source.py', 'schemas/report.schema.json', 'locales/th-TH.json'):
        if required not in shared:
            raise ValueError('Missing required support: '+required)
    for name in ('sources.json', 'THIRD_PARTY_NOTICES.md'):
        shared[name] = (base/name).read_bytes()
    shared['LICENSE'] = (root/'LICENSE').read_bytes()
    outputs = {f'{PRODUCT}/LICENSE': shared['LICENSE'], f'{PRODUCT}/{LOGO}': logo}
    plugin = {p:(base/p).read_bytes() for p in ('plugin.json','README.md','INSTALL.md','UPDATES.md','THIRD_PARTY_NOTICES.md')}
    plugin.update({'LICENSE':shared['LICENSE'], LOGO:logo})
    overlay = {k:v for k,v in manifest.items() if k not in ('$schema','extensions')}
    overlay.update(manifest['extensions']['com.openai'])
    overlay['skills'] = './skills/'
    overlay_bytes = encode(overlay)
    outputs[f'{PRODUCT}/.codex-plugin/plugin.json'] = overlay_bytes
    plugin['.codex-plugin/plugin.json'] = overlay_bytes
    archives = {}
    standalone = {}
    for name in NAMES:
        files = dict(shared)
        files['SKILL.md'] = (base/'entrypoints'/f'{name}.md').read_bytes()
        files['inventory.json'] = inventory(files, skill=name, version='0.1.1')
        for p,b in files.items():
            outputs[f'{PRODUCT}/skills/{name}/{p}'] = b
            plugin[f'skills/{name}/{p}'] = b
        standalone[name] = files
        for host, suffix in (('', ''), ('claude/', '-Claude-skill'), ('gemini/', '-Gemini-Apps-skill')):
            archives[f'{host}skills/{name}{suffix}-v0.1.1.zip'] = archive({f'{name}/{p}':b for p,b in files.items()})
    plugin['inventory.json'] = inventory(plugin, plugin='kumihan-th', version='0.1.1')
    outputs[f'{PRODUCT}/inventory.json'] = plugin['inventory.json']
    archives['plugins/kumihan-th-plugin-v0.1.1.zip'] = archive({f'kumihan-th/{p}':b for p,b in plugin.items()})
    for host, metadata, filename in (
        ('claude', '.claude-plugin/plugin.json', 'kumihan-th-Claude-Code-plugin'),
        ('gemini', 'gemini-extension.json', 'kumihan-th-Gemini-CLI-extension')):
        package = {p:(base/p).read_bytes() for p in ('README.md','INSTALL.md','UPDATES.md')}
        package.update({'LICENSE':shared['LICENSE'], LOGO:logo, metadata:(base/metadata).read_bytes()})
        if host == 'gemini':
            package['GEMINI.md'] = (base/'GEMINI.md').read_bytes()
        for name, files in standalone.items():
            package.update({f'skills/{name}/{p}':b for p,b in files.items()})
        package['inventory.json'] = inventory(package, plugin='kumihan-th', host=host, version='0.1.1')
        archives[f'{host}/plugins/{filename}-v0.1.1.zip'] = archive({f'kumihan-th/{p}':b for p,b in package.items()})
    archives['MANIFEST.json'] = encode(dict(product='KUMIHAN｜ดุลอักษร', version='0.1.1', locale='th-TH',
        logo_sha256=LOGO_SHA, archives=[dict(file=p, release_asset=Path(p).name, source_path=f'{PRODUCT}/downloads/{p}', bytes=len(b), sha256=digest(b)) for p,b in sorted(archives.items())]))
    # Flattened release names match GitHub assets; nested paths remain available locally.
    archives['SHA256SUMS.txt'] = ''.join(f'{digest(b)}  {Path(p).name}\n' for p,b in sorted(archives.items())).encode()
    for p,b in archives.items():
        outputs[f'{PRODUCT}/downloads/{p}'] = b
    for host in ('claude', 'gemini'):
        host_archives = {p[len(host)+1:]:b for p,b in archives.items() if p.startswith(host+'/')}
        host_manifest = encode(dict(product=interface['displayName'], host=host, version=manifest['version'],
            locale='th-TH', archives=[dict(file=p, release_asset=Path(p).name, bytes=len(b), sha256=digest(b))
                for p,b in sorted(host_archives.items())]))
        outputs[f'{PRODUCT}/downloads/{host}/MANIFEST.json'] = host_manifest
        host_archives['MANIFEST.json'] = host_manifest
        outputs[f'{PRODUCT}/downloads/{host}/SHA256SUMS.txt'] = ''.join(
            f'{digest(b)}  {Path(p).name}\n' for p,b in sorted(host_archives.items())).encode()
    return outputs


def generated_files(root=ROOT):
    base = Path(root)/PRODUCT
    return {p.relative_to(root).as_posix() for folder in ('skills','downloads','.codex-plugin','assets')
        for p in (base/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    planned = plan_outputs()
    changed = [p for p,b in planned.items() if not (ROOT/p).is_file() or (ROOT/p).read_bytes()!=b]
    stale = generated_files()-set(planned)
    if args.check:
        for p in sorted(set(changed)|stale):
            print('out of date: '+p)
        if changed or stale:
            return 1
        print(f'OK: Thai {len(planned)} generated files up to date')
        return 0
    for p in changed:
        path = ROOT/p
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(planned[p])
    for p in stale:
        (ROOT/p).unlink()
    print(f'Built Thai: {len(planned)} files; {len(changed)} updated; {len(stale)} stale removed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
