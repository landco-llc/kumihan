#!/usr/bin/env python3
"""Read-only bounded UTF-8 diagnostics; no renderer, proofreader or encoding detector."""
import argparse, hashlib, json, re
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
def digest(raw): return hashlib.sha256(raw).hexdigest()
def checked(raw):
    if not isinstance(raw,bytes): raise TypeError('Supply exact bytes')
    if len(raw)>1048576: raise ValueError('Source exceeds 1 MiB static scope')
    return raw.decode('utf-8')
def review_bytes(raw, locale='und', medium='review', candidate=None):
    text=checked(raw)
    if medium not in ('entry','web','documents','review','presentation','display'): raise ValueError('Unsupported medium')
    canonical={'my':'my','my-mm':'my-MM'}.get(locale.lower()) if isinstance(locale,str) else None
    diagnostics=[]
    if not canonical: diagnostics.append({'code':'locale-unresolved','status':'needs-review','evidence':'Explicit Burmese my/my-MM required; script alone is insufficient.'})
    else:
        diagnostics.append({'code':'encoding-provenance','status':'needs-review','evidence':'UTF-8 validity does not distinguish Unicode Myanmar from Zawgyi; no detector or conversion is performed.'})
        if re.search('[\u102b-\u103e\u1056-\u1059]',text): diagnostics.append({'code':'myanmar-combining-structure','status':'needs-review','evidence':'Marks retained; inspect shaping, cluster boundaries and clipping in actual engine.'})
        if 'ဝ' in text or '၀' in text: diagnostics.append({'code':'wa-zero-distinction','status':'needs-review','evidence':'Letter WA and digit zero retained without substitution.'})
        if re.search(r'word-break\s*:\s*break-all|overflow(?:-[xy])?\s*:\s*hidden|letter-spacing\s*:\s*(?!0(?:px|em|rem)?(?:;|\s|$)|normal)',text,re.I): diagnostics.append({'code':'static-layout-risk','status':'needs-review','evidence':'Inspect supplied break-all/tracking/clipping declaration in target renderer; no automatic edit.'})
    other=raw if candidate is None else candidate
    checked(other)
    rules=json.loads((BASE/'rules/catalog.json').read_text(encoding='utf-8')) if canonical else []
    effective='documents' if medium=='presentation' else 'web' if medium=='display' else medium
    rules=[r for r in rules if effective in r['media']]
    return {'schema_version':'1.0','source':text,'source_sha256':digest(raw),'source_integrity':{'status':'passed' if raw==other else 'failed','bytes_equal':raw==other,'source_sha256':digest(raw),'candidate_sha256':digest(other)},'requested_locale':locale,'locale':canonical or 'und','resolved_language':'my' if canonical else 'und','medium':medium,'encoding_identification':'not_checked','native_rendering':'not_checked','native_copy_review':'not_checked','host_invocation':'not_checked','office_pdf':'not_checked','guidance':[{'rule_id':r['id'],'title':r['title'],'source_ids':r['source_ids'],'status':'guidance-only'} for r in rules],'diagnostics':diagnostics,'limitations':['Exact bytes and bounded static patterns only.','No language inference, normalization, encoding detection, conversion or rewriting.','No native shaping, font, readability, screen reader, Office/PDF or host acceptance.']}
def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('source',type=Path); ap.add_argument('--candidate',type=Path); ap.add_argument('--locale',default='und'); ap.add_argument('--medium',default='review'); a=ap.parse_args()
    report=review_bytes(a.source.read_bytes(),a.locale,a.medium,a.candidate.read_bytes() if a.candidate else None)
    print(json.dumps(report,ensure_ascii=False,indent=2)); return int(report['source_integrity']['status']=='failed')
if __name__=='__main__': raise SystemExit(main())
