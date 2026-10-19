#!/usr/bin/env python3
"""Bounded read-only German review; preserve original UTF-8 bytes."""
import argparse, hashlib, json, re
from pathlib import Path
LOCALES=('de-DE','de-AT','de-CH')
def resolve(locale=None, **context):
    if locale is not None and locale not in LOCALES: raise ValueError('Choose explicit de-DE, de-AT or de-CH; no inferred region')
    allowed={'currency','timeZone','pronoun','gender_policy','house_style','medium','mode'}
    if context.keys()-allowed: raise ValueError('Unknown context field')
    result=dict(locale=locale,currency=None,timeZone=None,pronoun='inherit',gender_policy='inherit',house_style='inherit',medium=None,mode='typesetting_only')
    result.update(context)
    if result['mode'] not in ('typesetting_only','proofread','rewrite'): raise ValueError('Unsupported mode')
    if result['medium'] not in (None,'web-editorial','web-marketing','web-ui','report-document','presentation','display-copy'): raise ValueError('Unsupported medium')
    return result
def review(data,locale=None,candidate=None,**context):
    ctx=resolve(locale,**context);text=data.decode('utf-8');other=data if candidate is None else candidate;other.decode('utf-8')
    original_hash=hashlib.sha256(data).hexdigest()
    findings=[dict(rule_id='DE-WEB-001',status='needs-review',test_method='bounded-static-candidate',evidence=dict(character_offset=m.start(),match=m.group()),original_hash=original_hash,proposal='Check CSS scope and actual wrapping; layout first. Quoted code may be exempt.',edits_authorized=False) for m in re.finditer(r'word-break\s*:\s*break-all|overflow-wrap\s*:\s*anywhere',text)]
    return dict(original_hash=original_hash,original_bytes=len(data),locale=locale,context=ctx,preservation=dict(status='passed' if data==other else 'failed',candidate_hash=hashlib.sha256(other).hexdigest(),candidate_bytes=len(other),test_method='exact-byte-comparison'),findings=findings,rendering='not-checked',editorial_review='needs-review',native_host='not-checked')
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('original',type=Path);p.add_argument('--candidate',type=Path);p.add_argument('--locale',choices=LOCALES)
    a=p.parse_args()
    try:r=review(a.original.read_bytes(),a.locale,a.candidate.read_bytes() if a.candidate else None)
    except (ValueError,OSError) as e:p.error(str(e))
    print(json.dumps(r,ensure_ascii=False,indent=2));return int(r['preservation']['status']=='failed')
if __name__=='__main__':raise SystemExit(main())
