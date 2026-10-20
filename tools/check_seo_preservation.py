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
    # Version work explicitly changes display bodies and README. Admit only the
    # exact reviewed hash pair; never rewrite the historical SEO snapshot.
    overlay_path = ROOT / 'docs/version-automation/preservation.json'
    overlay = json.loads(overlay_path.read_text()) if overlay_path.exists() else {}
    if overlay and (overlay.get('baseline') != snapshot['baseline'] or
                    overlay.get('authority') != 'KUMI-VERSION-AUTO-WG00-WG04-20261019-01'):
        return ['Invalid edition-version preservation overlay']
    from build_version_site import preservation_allowed
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
            update = overlay.get('updates', {}).get(family, {}).get(path, {})
            actual = hashlib.sha256(content).hexdigest()
            admitted = (update.get('before') == expected and update.get('after') == actual
                        and preservation_allowed(path, family))
            from ziheng_v020_transition import allowed
            admitted = admitted or allowed(path, family, root)
            if actual != expected and not admitted:
                errors.append(f'{family}: main bytes changed: {path}')
    return errors

if __name__ == '__main__':
    errors = audit()
    if errors: raise SystemExit('\n'.join(errors))
    print('Main distribution, body and Jekyll source preservation: PASS')
