#!/usr/bin/env python3
"""Verify the committed public release contract without development logs."""
import hashlib
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def audit(root=ROOT):
    contract=json.loads((ROOT/'tests/contracts/release-preservation.json').read_text())
    errors=[]
    for family, records in contract.items():
        for path, expected in records.items():
            target=Path(root)/path
            if not target.is_file():
                errors.append(f'{family}: missing {path}'); continue
            raw=target.read_bytes()
            if family == 'protected':
                from ja_release_transition import admitted
                if admitted(root, path, expected):
                    continue
            if family=='bodies':
                body=re.search(rb'<body\b[\s\S]*',raw,re.I); raw=body[0] if body else b''
            from en_measure_release_transition import admitted as en_admitted
            if en_admitted(root, path, expected, raw):
                continue
            from multilingual_release_transition import admitted as release_admitted
            if release_admitted(root,path,expected,raw,family):
                continue
            from multilingual_release_transition import admitted as release_admitted
            if release_admitted(root,path,expected,raw,family):
                continue
            from multilingual_release_transition import admitted as release_admitted
            if release_admitted(root,path,expected,raw,family):
                continue
            if hashlib.sha256(raw).hexdigest()!=expected:
                errors.append(f'{family}: main bytes changed: {path}')
    return errors

if __name__=='__main__':
    errors=audit()
    if errors:raise SystemExit('\n'.join(errors))
    print('Public release preservation: PASS')
