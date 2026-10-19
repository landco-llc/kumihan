#!/usr/bin/env python3
"""Verify latest-main distribution and public body bytes captured before integration."""
import hashlib
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def audit(root=ROOT):
    root = Path(root)
    snapshot = json.loads((ROOT / 'docs/seo/evidence/20261019-main-preservation.json').read_text())
    errors = []
    for family in ('protected', 'bodies', 'jekyll_sources'):
        for path, expected in snapshot[family].items():
            target = root / path
            if not target.is_file():
                errors.append(f'{family}: missing {path}'); continue
            content = target.read_bytes()
            if family == 'bodies':
                body = re.search(rb'<body\b[\s\S]*', content, re.I)
                content = body[0] if body else b''
            if hashlib.sha256(content).hexdigest() != expected:
                errors.append(f'{family}: main bytes changed: {path}')
    return errors

if __name__ == '__main__':
    errors = audit()
    if errors: raise SystemExit('\n'.join(errors))
    print('Main distribution, body and Jekyll source preservation: PASS')
