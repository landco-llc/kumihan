"""Unactivated exact Ziheng source transition helper; not publication permission.

The frozen fresh-main preimages are independent of the regenerated active
preservation overlay. The shared integration patch supplies the only call sites.
"""
import hashlib
import json
import re
from pathlib import Path

BASE = '8b647cc752d7a9bc3db48356fa0ab7b221bb66d6'
BASELINE_SHA256 = '0b4e74a497ea48f1a2602137359b11fce33b302c0c9a3a9f518363f4f3790b0f'
PREFIX = 'docs/development/zh-hant-v020-20261020/'


def allowed(path, family, root):
    root=Path(root)
    ledger=root/(PREFIX+'source-transition.json')
    baseline_path=root/(PREFIX+'source-transition-baseline.json')
    if not ledger.is_file() or not baseline_path.is_file(): return False
    raw=baseline_path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=BASELINE_SHA256: return False
    baseline=json.loads(raw)
    data=json.loads(ledger.read_text())
    if baseline.get('base')!=BASE or data.get('base')!=BASE: return False
    if data.get('authority')!='KUMI-ZIHENG-V020-RESEARCH-WG-20261020-01': return False
    scoped=(path.startswith('plugins/kumihan-ziheng/') and family=='protected') or (family=='bodies' and (path.startswith('kumihan-zh-han') or path.startswith('docs/install-ziheng')))
    if not scoped: return False
    row=data.get('updates',{}).get(family,{}).get(path,{})
    expected_before=baseline.get('updates',{}).get(family,{}).get(path)
    if not expected_before or row.get('main_before')!=expected_before: return False
    snapshot=json.loads((root/'docs/seo/evidence/20261019-main-preservation.json').read_text())
    if baseline.get('snapshot_baseline')!=snapshot.get('baseline'): return False
    historical=snapshot.get(family,{}).get(path)
    if not historical or row.get('snapshot_before')!=historical: return False
    target=root/path
    if not target.is_file(): return False
    raw=target.read_bytes()
    if family=='bodies':
        body=re.search(rb'<body\b[\s\S]*',raw,re.I);raw=body[0] if body else b''
    return row.get('after')==hashlib.sha256(raw).hexdigest()
