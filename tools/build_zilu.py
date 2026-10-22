#!/usr/bin/env python3
"""Deterministic, offline ZiLu packages. --check never writes files."""
import argparse
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = 'plugins/kumihan-zilu'
VERSION = '0.1.2'
NAMES = ('kumihan-zilu', 'kumihan-zilu-web', 'kumihan-zilu-documents', 'kumihan-zilu-review')


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def archive(files):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as z:
        for path, data in sorted(files.items()):
            if path.startswith('/') or '..' in Path(path).parts or '\\' in path:
                raise ValueError('Unsafe ZIP member')
            info = zipfile.ZipInfo(path, (2026,10,18,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data, compresslevel=9)
    return stream.getvalue()


def plan_outputs(root=ROOT):
    root = Path(root)
    base = root / PRODUCT
    manifest = json.loads((base/'plugin.json').read_text())
    if (manifest['name'],manifest['version']) != ('kumihan-zilu',VERSION):
        raise ValueError('Unexpected ZiLu identity/version')
    shared = {'rules/catalog.json':(base/'rules/zh-hans-cn.json').read_bytes(),
              'rules/vertical.json':(base/'rules/vertical.json').read_bytes(),
              'sources/public-sources.json':(base/'sources.json').read_bytes(),
              'scripts/checks.py':(base/'runtime/checks.py').read_bytes(),
              'LICENSE':(root/'LICENSE').read_bytes(),
              'THIRD_PARTY_NOTICES.md':(base/'THIRD_PARTY_NOTICES.md').read_bytes()}
    for folder in ('references','schemas','locales'):
        for p in sorted((base/folder).rglob('*')):
            if p.is_symlink():
                raise ValueError('Symlinks are not allowed')
            if p.is_file():
                shared[p.relative_to(base).as_posix()] = p.read_bytes()
    for p in (base/'locales/profiles').glob('*.json'):
        shared['profiles/'+p.name] = p.read_bytes()
    outputs = {PRODUCT+'/LICENSE':shared['LICENSE']}
    plugin = {p:(base/p).read_bytes() for p in ('plugin.json','README.md','README.en.md','INSTALL.md','UPDATES.md','THIRD_PARTY_NOTICES.md')}
    plugin['LICENSE'] = shared['LICENSE']
    plugin['rules/zh-hans-cn.json'] = shared['rules/catalog.json']
    plugin['rules/vertical.json'] = shared['rules/vertical.json']
    plugin['sources.json'] = shared['sources/public-sources.json']
    logo = 'assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png'
    plugin[logo] = (root/logo).read_bytes()
    outputs[PRODUCT+'/'+logo] = plugin[logo]
    overlay = {k:v for k,v in manifest.items() if k not in ('$schema','extensions')}
    overlay.update(manifest['extensions']['com.openai'])
    overlay['skills'] = './skills/'
    plugin['.codex-plugin/plugin.json'] = encode(overlay)
    outputs[PRODUCT+'/.codex-plugin/plugin.json'] = encode(overlay)
    skills = {}
    for name in NAMES:
        files = dict(shared)
        files['SKILL.md'] = (base/'entrypoints'/f'{name}.md').read_bytes()
        files['inventory.json'] = encode(dict(skill=name, version=VERSION,
            files=[dict(path=p, bytes=len(b), sha256=digest(b)) for p,b in sorted(files.items())]))
        skills[name] = files
        for p,b in files.items():
            outputs[f'{PRODUCT}/skills/{name}/{p}'] = b
            plugin[f'skills/{name}/{p}'] = b
    archives = {f'plugins/kumihan-zilu-plugin-v{VERSION}.zip':archive({'kumihan-zilu/'+p:b for p,b in plugin.items()})}
    for host in ('claude','gemini'):
        host_files = {p:b for p,b in plugin.items() if p not in ('plugin.json','.codex-plugin/plugin.json')}
        for p in (['.claude-plugin/plugin.json'] if host=='claude' else ['gemini-extension.json','GEMINI.md']):
            host_files[p] = (base/p).read_bytes()
        # Gemini requires gemini-extension.json at the directory passed to install.
        prefix = 'kumihan-zilu/' if host=='claude' else ''
        kind = 'claude-plugin' if host=='claude' else 'gemini-extension'
        archives[f'{host}/kumihan-zilu-{kind}-v{VERSION}.zip'] = archive({prefix+p:b for p,b in host_files.items()})
    for i,name in enumerate(NAMES):
        role = ('entry','web','documents','review')[i]
        for host in ('','claude','gemini'):
            folder = host or 'skills'
            host_suffix = '-'+host if host else ''
            # All three support directory-based agent skills. App upload support is host-dependent.
            archives[f'{folder}/kumihan-zilu-{role}{host_suffix}-skill-v{VERSION}.zip'] = archive({name+'/'+p:b for p,b in skills[name].items()})
    meta = dict(product='KUMIHAN｜字律', name='kumihan-zilu', version=VERSION,locale='zh-Hans-CN',
        native_host_invocation='NOT_CHECKED', marketplace_listing='NOT_VERIFIED',
        archives=[dict(file=p,bytes=len(b),sha256=digest(b)) for p,b in sorted(archives.items())])
    archives['MANIFEST.json'] = encode(meta)
    archives['SHA256SUMS.txt'] = ''.join(f'{digest(b)}  {p}\n' for p,b in sorted(archives.items())).encode()
    outputs.update({PRODUCT+'/downloads/'+p:b for p,b in archives.items()})
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    outputs = plan_outputs()
    changed = [p for p,b in outputs.items() if not (ROOT/p).is_file() or (ROOT/p).read_bytes()!=b]
    generated = {p.relative_to(ROOT).as_posix() for folder in ('skills','downloads','assets','.codex-plugin')
                 for p in (ROOT/PRODUCT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    # Retain immutable older release ZIPs; only current generated sources are pruned.
    retained = {p for p in generated if '/downloads/history/' in p or ('/downloads/' in p and p.endswith('.zip') and f'-v{VERSION}.zip' not in p)}
    stale = generated-set(outputs)-retained
    if args.check:
        for p in sorted(set(changed)|stale):print('out of date: '+p)
        if changed or stale:return 1
        print(f'OK: ZiLu {len(outputs)} generated files current');return 0
    for p in changed:
        target = ROOT/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(outputs[p])
    for p in stale:(ROOT/p).unlink()
    print(f'Built ZiLu: {len(outputs)} outputs, 15 ZIPs');return 0


if __name__=='__main__':
    sys.exit(main())
