"""Exact Measure source-version cell transition; publication facts stay unchanged."""
import hashlib
import json
from pathlib import Path
RECORD='tests/contracts/en-measure-v011-source-transition.json'
RECORD_SHA='374a9997fff877e13c922286d67a7c434d84a5ae45259c5992c0af0c1dfc0091'
PREDECESSOR='tests/contracts/en-measure-v010-readme.txt'
def predecessor(root):
    raw=(Path(root)/RECORD).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=RECORD_SHA:raise ValueError('Changed Measure source admission')
    data=json.loads(raw);old=(Path(root)/PREDECESSOR).read_bytes()
    if hashlib.sha256(old).hexdigest()!=data['preimage_sha256']:raise ValueError('Changed Measure predecessor')
    return data,old

def admitted(root,path,before,raw,family):
    if path!='README.md' or family!='protected':return False
    try:
        data,old=predecessor(root)
        a=data['before_line'].encode();b=data['after_line'].encode()
        return (data['scope']=='measure-v011-source-only' and before==data['baseline_sha256']
            and old.count(a)==1 and b==a.replace(b'| v0.1.0 |',b'| v0.1.1 |',1)
            and raw==old.replace(a,b,1) and hashlib.sha256(raw).hexdigest()==data['after_sha256'])
    except (OSError,ValueError,KeyError,TypeError):return False
