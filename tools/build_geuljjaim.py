#!/usr/bin/env python3
"""Deterministic standalone Korean distribution builder. Python 3.9+, stdlib only.
Canonical source: plugins/kumihan-geuljjaim excluding generated skills/downloads/assets/.codex-plugin.
No runtime network. --check performs no writes.
"""
import argparse
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = 'plugins/kumihan-geuljjaim'
NAMES = ('kumihan-geuljjaim', 'kumihan-geuljjaim-web', 'kumihan-geuljjaim-documents', 'kumihan-geuljjaim-review')
MEDIA = ('web-editorial', 'web-marketing', 'web-ui', 'report-document', 'presentation', 'display-copy')

def encode(data):
    return (json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def archive(files):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as z:
        for path, data in sorted(files.items()):
            if path.startswith('/') or '..' in Path(path).parts:
                raise ValueError('Unsafe archive path')
            info = zipfile.ZipInfo(path, (2026,10,18,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data, compresslevel=9)
    return stream.getvalue()

def plan_outputs(root=ROOT):
    root = Path(root); base = root/PRODUCT
    manifest=json.loads((base/'plugin.json').read_text())
    if manifest['name']!='kumihan-geuljjaim' or manifest['version']!='0.1.0':
        raise ValueError('Unexpected product identity/version')
    rules=json.loads((base/'rules/ko-kr.json').read_text())
    if len({r['id'] for r in rules})!=36:
        raise ValueError('36 unique Korean rule IDs required')
    sources=json.loads((base/'sources.json').read_text())
    if not {s for r in rules for s in r['source_refs']} <= {s['id'] for s in sources['sources']}:
        raise ValueError('Unresolved source')
    shared={'rules/catalog.json':encode(rules),'sources/public-sources.json':encode(sources),
            'scripts/checks.py':(base/'runtime/checks.py').read_bytes(),
            'LICENSE':(root/'LICENSE').read_bytes(),
            'THIRD_PARTY_NOTICES.md':(base/'THIRD_PARTY_NOTICES.md').read_bytes()}
    for folder in ('references','schemas','locales'):
        for p in sorted((base/folder).rglob('*')):
            if p.is_file():shared[p.relative_to(base).as_posix()]=p.read_bytes()
    for m in MEDIA:
        shared[f'profiles/{m}.json']=(base/'locales/profiles'/f'{m}.json').read_bytes()
    outputs={f'{PRODUCT}/LICENSE':shared['LICENSE']}
    plugin_files={p:(base/p).read_bytes() for p in ('plugin.json','README.md','README.en.md','README.ja.md','INSTALL.md','UPDATES.md','THIRD_PARTY_NOTICES.md')}
    plugin_files['LICENSE']=shared['LICENSE']
    logo='assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png'
    plugin_files[logo]=(root/logo).read_bytes();outputs[f'{PRODUCT}/{logo}']=plugin_files[logo]
    overlay={k:v for k,v in manifest.items() if k not in ('$schema','extensions')}
    overlay.update(manifest['extensions']['com.openai']);overlay['skills']='./skills/'
    outputs[f'{PRODUCT}/.codex-plugin/plugin.json']=encode(overlay)
    plugin_files['.codex-plugin/plugin.json']=encode(overlay)
    archives={}
    for name in NAMES:
        files=dict(shared);files['SKILL.md']=(base/'entrypoints'/f'{name}.md').read_bytes()
        files['inventory.json']=encode(dict(skill=name,version=manifest['version'],path_base='skill-folder-root',self_digest='Inventory excludes itself; archive checksum covers all bytes.',files=[dict(path=p,bytes=len(b),sha256=digest(b)) for p,b in sorted(files.items())]))
        for p,b in files.items():
            outputs[f'{PRODUCT}/skills/{name}/{p}']=b;plugin_files[f'skills/{name}/{p}']=b
        archives[f'skills/{name}-0.1.0.zip']=archive({f'{name}/{p}':b for p,b in files.items()})
    archives['plugins/kumihan-geuljjaim-plugin-0.1.0.zip']=archive({f'kumihan-geuljjaim/{p}':b for p,b in plugin_files.items()})
    archives['MANIFEST.json']=encode(dict(product='KUMIHAN｜글짜임',name='kumihan-geuljjaim',version='0.1.0',locale='ko-KR',host_status='Portable/Codex-format archives; native invocation not-checked. Claude/Gemini host-specific archives unsupported.',archives=[dict(file=p,bytes=len(b),sha256=digest(b)) for p,b in sorted(archives.items())]))
    archives['SHA256SUMS.txt']=''.join(f'{digest(b)}  {p}\n' for p,b in sorted(archives.items())).encode()
    for p,b in archives.items():outputs[f'{PRODUCT}/downloads/{p}']=b
    return outputs

def generated_files(root=ROOT):
    return {p.relative_to(root).as_posix() for folder in ('skills','downloads','assets','.codex-plugin') for p in (Path(root)/PRODUCT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    planned=plan_outputs();changed=[p for p,b in planned.items() if not (ROOT/p).is_file() or (ROOT/p).read_bytes()!=b];stale=generated_files()-set(planned)
    if args.check:
        for p in sorted(set(changed)|stale):print(f'out of date: {p}')
        if changed or stale:return 1
        print(f'OK: Korean {len(planned)} generated files up to date');return 0
    for p in changed:
        target=ROOT/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(planned[p])
    for p in stale:(ROOT/p).unlink()
    print(f'Built Korean: {len(planned)} files; {len(changed)} updated; {len(stale)} stale removed');return 0

if __name__=='__main__':sys.exit(main())
