"""Exact reviewed Accord source transition; published release remains v0.1.1."""
import hashlib
import json
from pathlib import Path
RECORD = 'tests/contracts/fr-accord-v012-source-transition.json'
RECORD_SHA = 'f90951c46fcc4f38b7ab7b378b0dedade2892cbb40e412ce56293510a2eed89e'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def admitted(root, path, expected, raw, family):
    try:
        root = Path(root)
        encoded = (root / RECORD).read_bytes()
        if sha(encoded) != RECORD_SHA: return False
        data = json.loads(encoded)
        if data['scope'] != 'fr-v012-source-only-published-v011': return False
        if sha((root/'tests/contracts/release-preservation.json').read_bytes()) != data['frozen_contract_sha256']: return False
        if sha((root/'assets/edition-versions.json').read_bytes()) != data['facts_sha256']: return False
        return any(r['path']==path and r['family']==family and r['historical']==expected and r['successor']==sha(raw) for r in data['rows'])
    except (OSError, ValueError, KeyError, TypeError):
        return False
