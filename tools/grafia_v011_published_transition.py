"""Exact verified Grafía publication; shared gateways change only their ES card."""
import hashlib
import json
from pathlib import Path

RECORD='tests/contracts/grafia-v011-published-transition.json'
RECORD_SHA='85d366d91b6b811af263c07391a991a689eea2171a5f0b113bab02ae6319a98c'
FACTS='tests/contracts/grafia-v011-published-facts.json'
FROZEN=('tests/contracts/release-preservation.json','tests/contracts/grafia-v011-source-transition.json')

def sha(raw):return hashlib.sha256(raw).hexdigest()


def load(root):
    root=Path(root);raw=(root/RECORD).read_bytes()
    if sha(raw)!=RECORD_SHA:raise ValueError('Changed Grafía published admission')
    data=json.loads(raw);facts_raw=(root/FACTS).read_bytes()
    if sha(facts_raw)!=data['facts_sha256']:raise ValueError('Changed verified Grafía facts')
    facts=json.loads(facts_raw)
    if (data['scope']!='grafia-v011-published-site' or data['release_id']!=422889710 or
        data['tag']!='kumihan-grafia-v0.1.1' or data['target_commit']!='087d8c94e4d25ca83ba1aba871dbdf942afa0841' or
        data['published_at']!='2026-10-24T18:02:19Z' or facts['release_id']!=data['release_id'] or
        facts['tag']!=data['tag'] or facts['source_commit']!=data['target_commit'] or
        facts['published_at']!=data['published_at'] or facts['published_version']!='0.1.1' or
        facts['source_version']!='0.1.1' or len(facts['verified_assets'])!=15 or len(facts['verified_metadata'])!=2):
        raise ValueError('Changed fixed Grafía release identity')
    if set(data['frozen_inputs'])!=set(FROZEN):raise ValueError('Changed frozen input scope')
    for name,expected in data['frozen_inputs'].items():
        if sha((root/name).read_bytes())!=expected:raise ValueError('Changed historical admission')
    source=json.loads((root/FROZEN[1]).read_bytes())
    if (data['facts']['before_sha256']!=source['facts']['after_sha256'] or
        data['facts']['before_es']!=source['facts']['after_es'] or
        data['readme']['before_sha256']!=source['readme']['after_sha256']):
        raise ValueError('Changed exact Grafía source predecessor')
    from fr_accord_v012_source_transition import predecessor
    current_facts=predecessor((root/'assets/edition-versions.json').read_bytes(),root,'assets/edition-versions.json')
    if sha(current_facts)!=data['facts']['after_sha256']:
        raise ValueError('Changed current edition facts')
    return data,facts


def predecessor_facts(raw,root):
    data,facts=load(root);row=data['facts']
    from fr_accord_v012_source_transition import predecessor
    raw=predecessor(raw,root,'assets/edition-versions.json')
    if sha(raw)==row['before_sha256']:return raw
    if sha(raw)!=row['after_sha256']:raise ValueError('Changed current edition facts')
    content=json.loads(raw)
    if content['editions']['es']!=facts:raise ValueError('Changed verified ES facts')
    content['editions']['es']=row['before_es']
    previous=(json.dumps(content,ensure_ascii=False,indent=2)+'\n').encode()
    if sha(previous)!=row['before_sha256']:raise ValueError('Changed non-ES edition facts')
    return previous


def predecessor_readme(raw,root):
    data,_=load(root);row=data['readme']
    from fr_accord_v012_source_transition import predecessor
    raw=predecessor(raw,root,'README.md')
    if sha(raw)==row['before_sha256']:return raw
    if sha(raw)!=row['after_sha256']:raise ValueError('Changed current README')
    before,after=row['before_line'].encode(),row['after_line'].encode()
    if raw.count(after)!=1 or not after.startswith(b'| ES |'):raise ValueError('Missing exact ES row')
    previous=raw.replace(after,before,1)
    if sha(previous)!=row['before_sha256']:raise ValueError('Changed non-ES README content')
    return previous


def predecessor_body(root,path,raw):
    data,_=load(root);row=data['paths'].get(path)
    if not row or row.get('kind')!='gateway-es-card':return raw
    if sha(raw)==row['preimage_sha256']:return raw
    if sha(raw)!=row['after_sha256']:raise ValueError('Changed current gateway body')
    before,after=row['before_card'].encode(),row['after_card'].encode()
    if before.replace(b'v0.1.0',b'v0.1.1')!=after or raw.count(after)!=1 or b'aria-labelledby="language-es"' not in after:
        raise ValueError('Changed ES card beyond the version')
    previous=raw.replace(after,before,1)
    if sha(previous)!=row['preimage_sha256']:raise ValueError('Changed non-ES gateway content')
    return previous


def admitted(root,path,before,raw,family):
    try:
        data,_=load(root);row=data['paths'].get(path)
        if path=='README.md':
            from fr_accord_v012_source_transition import predecessor
            raw=predecessor(raw,root,path)
        if not row or row['family']!=family or row['baseline_sha256']!=before or sha(raw)!=row['after_sha256']:return False
        if row['kind']=='gateway-es-card':return sha(predecessor_body(root,path,raw))==row['preimage_sha256']
        if row['kind']=='readme-es-row':return sha(predecessor_readme(raw,root))==data['readme']['before_sha256']
        if row['kind']=='grafia-page':
            source=json.loads((Path(root)/FROZEN[1]).read_bytes())
            return row['preimage_sha256']==source['changes']['bodies'][path]['after']
        return False
    except (OSError,ValueError,KeyError,TypeError):return False
