"""Exact published Measure facts and EN-only gateway-card admission."""
import hashlib
import json
from pathlib import Path
from en_measure_v011_transition import predecessor
RECORD='tests/contracts/en-measure-v011-published-transition.json'
RECORD_SHA='029c2e4573ec6b5ecd6f5222242ec61539ef654a1624f5e18bf6bb6d5bde61ee'
FACTS='tests/contracts/en-measure-v011-published-facts.json'

def sha(raw):return hashlib.sha256(raw).hexdigest()

def load(root):
    root=Path(root);raw=(root/RECORD).read_bytes()
    if sha(raw)!=RECORD_SHA:raise ValueError('Changed Measure published admission')
    data=json.loads(raw);facts_raw=(root/FACTS).read_bytes()
    if sha(facts_raw)!=data['facts_sha256']:raise ValueError('Changed Measure published facts')
    facts=json.loads(facts_raw)
    if (data['scope']!='measure-v011-published-site' or data['release_id']!=422834442 or
        data['tag']!='kumihan-measure-v0.1.1' or data['target_commit']!='db6f453160e46c568a007c76afd2030bc8e61512' or
        facts['release_id']!=data['release_id'] or facts['tag']!=data['tag'] or
        facts['source_commit']!=data['target_commit'] or facts['published_at']!=data['published_at'] or
        facts['published_version']!='0.1.1' or facts['source_version']!='0.1.1' or
        len(facts['verified_assets'])!=15 or len(facts['verified_metadata'])!=2):
        raise ValueError('Changed exact Measure publication identity')
    return data,facts

def predecessor_body(root,path,raw):
    """Recover the exact prior gateway for historical admission tests."""
    data,_=load(root);row=data['paths'].get(path)
    if not row or row['family']!='bodies':return raw
    if sha(raw)==row['preimage_sha256']:return raw
    if sha(raw)!=row['after_sha256']:raise ValueError('Changed current gateway body')
    before=row['before_card'].encode();after=row['after_card'].encode()
    if raw.count(after)!=1:raise ValueError('Missing exact EN card')
    old=raw.replace(after,before,1)
    if sha(old)!=row['preimage_sha256']:raise ValueError('Changed non-English gateway content')
    return old

def admitted(root,path,before,raw,family):
    try:
        data,_=load(root);row=data['paths'].get(path)
        if not row or row['family']!=family or row['baseline_sha256']!=before or sha(raw)!=row['after_sha256']:return False
        if family=='bodies':
            return sha(predecessor_body(root,path,raw))==row['preimage_sha256']
        if path=='README.md' and family=='protected':
            source,old=predecessor(root)
            old=old.replace(source['before_line'].encode(),source['after_line'].encode(),1)
            a=row['before_line'].encode();b=row['after_line'].encode()
            return sha(old)==row['preimage_sha256'] and old.count(a)==1 and raw==old.replace(a,b,1)
        return False
    except (OSError,ValueError,KeyError,TypeError):return False
