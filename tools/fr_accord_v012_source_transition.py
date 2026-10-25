"""Exact reviewed Accord source transition; published release remains v0.1.1."""
import hashlib
import json
from pathlib import Path
RECORD = 'tests/contracts/fr-accord-v012-source-transition.json'
RECORD_SHA = '6b30cef4256159b2c935484c919fb4d98f2a88b1b74e5d032ee850377bbb78ce'
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

def predecessor(raw, root, name):
    encoded=(Path(root)/RECORD).read_bytes()
    if sha(encoded)!=RECORD_SHA: raise ValueError('Changed FR source admission')
    row=json.loads(encoded)['predecessors'][name]
    if sha(raw)==row['before']: return raw
    if sha(raw)!=row['after']: raise ValueError('Unknown FR successor')
    if name=='assets/edition-versions.json':
        data=json.loads(raw)
        if data['editions']['fr']['source_version']!='0.1.2': raise ValueError('Changed FR source')
        data['editions']['fr']['source_version']='0.1.1'
        previous=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
    else:
        old,new=row['before_line'].encode(),row['after_line'].encode()
        if raw.count(new)!=1: raise ValueError('Changed FR README row')
        previous=raw.replace(new,old,1)
    if sha(previous)!=row['before']: raise ValueError('Changed non-FR content')
    return previous
