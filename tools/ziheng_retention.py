"""Exact allowlist of historical Ziheng bytes; unknown stale files stay stale."""
import hashlib
import json
from pathlib import Path

PRODUCT = 'plugins/kumihan-ziheng'
FOLDERS = ('downloads', 'downloads Claude', 'downloads Gemini')
# Explicit immutable release baselines; arbitrary historical versions remain rejected.
VERSIONS = ('0.1.0', '0.2.0')


def retained_outputs(root, folders):
    root = Path(root)
    ledger = json.loads((root/PRODUCT/'retained-distributions.json').read_text(encoding='utf-8'))
    if ledger.get('format') != 'ziheng-retained-1':
        raise ValueError('Unknown retained distribution format')
    outputs = {}
    seen = set()
    for entry in ledger['entries']:
        path = entry['path']; rel = Path(path)
        if path in seen or rel.is_absolute() or '..' in rel.parts:
            raise ValueError('Unsafe/duplicate retained distribution path')
        seen.add(path)
        if len(rel.parts) < 4 or rel.parts[:2] != ('plugins','kumihan-ziheng') or rel.parts[2] not in FOLDERS:
            raise ValueError('Retention must stay within Ziheng downloads')
        suffix = rel.parts[3:]
        old_zip = len(suffix)==2 and suffix[0] in ('plugins','extensions','skills') and any(suffix[1].endswith('-'+version+'.zip') for version in VERSIONS)
        old_meta = len(suffix)==3 and suffix[0]=='history' and suffix[1] in VERSIONS and suffix[2] in ('MANIFEST.json','SHA256SUMS.txt')
        if not (old_zip or old_meta):
            raise ValueError('Only fixed historical archives/metadata may be retained')
        if rel.parts[2] not in folders: continue
        target=root/rel
        if not target.is_file(): raise ValueError('Missing retained distribution: '+path)
        data=target.read_bytes()
        if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:
            raise ValueError('Corrupt retained distribution: '+path)
        outputs[path]=data
    return outputs


def is_retained_manifest(root, path):
    """Admit only the exact historical Ziheng manifests after byte validation."""
    root=Path(root).resolve()
    try: rel=Path(path).resolve().relative_to(root).as_posix()
    except ValueError: return False
    known={PRODUCT+'/'+folder+'/history/'+version+'/MANIFEST.json'
           for folder in FOLDERS for version in VERSIONS}
    if rel not in known: return False
    return rel in retained_outputs(root,FOLDERS)
