#!/usr/bin/env python3
"""Offline development CLI. Its stdout container is not a public transport contract."""
import argparse
import json
from pathlib import Path
from contract import CompositionError, validate_record
from core import MAX_BYTES, decode_utf8, fail, resolve, validate_request
from review import evaluate

# Registry includes existing source guidance; allow a bounded larger local registry file.
MAX_RECORD_BYTES=16*MAX_BYTES

def load(path):
    with Path(path).open('rb') as f:raw=f.read(MAX_RECORD_BYTES+1)
    if len(raw)>MAX_RECORD_BYTES:fail('E_RESOURCE_LIMIT','/input','Split oversized input record')
    try:return json.loads(decode_utf8(raw),parse_constant=lambda _:fail('E_REFERENCE','/input','Nonfinite JSON number'))
    except (json.JSONDecodeError,RecursionError):fail('E_REFERENCE','/input','Invalid or excessively nested JSON')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=['validate','resolve','evaluate'])
    parser.add_argument('request')
    parser.add_argument('--registry')
    parser.add_argument('--plan')
    parser.add_argument('--target')
    parser.add_argument('--source-id')
    args=parser.parse_args()
    try:
        r=load(args.request)
        if args.operation=='validate':
            validate_record(r)
            if r['kind']=='request':validate_request(r)
            result={'validated_kind':r['kind'],'coverage':'schema + request semantics; no rendering or external approval validation'}
        else:
            if not args.registry:fail('E_REFERENCE','/registry','Local registry path required')
            registry=load(args.registry)
            if args.operation=='resolve':result=resolve(r,registry)
            else:
                if not args.plan:fail('E_REFERENCE','/plan','Local plan path required')
                audit,obs=evaluate(r,load(args.plan),registry,target=args.target,source_id=args.source_id)
                result={'audit':audit,'observations':obs}
        print(json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2))
        return 0
    except CompositionError as error:
        print(json.dumps(error.record(),ensure_ascii=True));return 2
    except (OSError,ValueError,TypeError,KeyError,RecursionError):
        print(json.dumps(CompositionError('E_REFERENCE','/input','Unreadable or invalid bounded local input').record()));return 2

if __name__=='__main__':raise SystemExit(main())
