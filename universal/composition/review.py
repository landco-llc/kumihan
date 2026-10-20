"""Read-only exact-target static audit. Caller observations never confer authority."""
from __future__ import annotations
import copy
import hashlib
import platform
from pathlib import Path
from contract import VERSION, validate_record
from core import BINDING_NS, ENGINE, MAX_BYTES, check_range, decode_utf8, extensions, fail, object_digest, resolve, text_digest, unique, validate_request

BIDI_CONTROLS=set('\u061c\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069')

def bind_plan(request,plan,registry):
    validate_record(plan);extensions(plan)
    bindings=[e for e in plan['extensions'] if e['namespace']==BINDING_NS]
    if len(bindings)!=1 or bindings[0]['version']!='1':fail('E_REFERENCE','/plan/extensions','One supported immutable binding required')
    payload=bindings[0]['payload']
    if payload.get('request_digest')!=object_digest(request): fail('E_SOURCE_DIGEST','/plan','Plan request binding stale')
    expected=resolve(request,registry,candidates=payload.get('candidates',[]))
    if plan!=expected:fail('E_SOURCE_DIGEST','/plan','Plan content/dependencies differ from deterministic candidate; regenerate')

def bind_observations(observations, request, plan):
    sources={s['id']:s for s in request['sources']}
    scopes=set(sources)|{r['id'] for r in request['regions']}|{plan['id']}
    unique(observations,'observations')
    for i,o in enumerate(observations):
        validate_record(o);extensions(o)
        if o['kind']!='observation':fail('E_REFERENCE',f'/observations/{i}/kind','Observation required')
        source=sources.get(o['artifact_ref'])
        if source is None or o['artifact_digest']!=source['text_digest']:
            fail('E_SOURCE_DIGEST',f'/observations/{i}/artifact_digest','Observation must bind an exact logical source')
        for scope in o['scopes']:
            if scope not in scopes:fail('E_REFERENCE',f'/observations/{i}/scopes','Unknown observation scope')
            region=next((r for r in request['regions'] if r['id']==scope),None)
            if (region is not None and region['range']['source_id']!=source['id']) or (scope in sources and scope!=source['id']):
                fail('E_REFERENCE',f'/observations/{i}/scopes','Scope belongs to different source')
        for j,m in enumerate(o['mapping']):
            check_range(m['range'],sources,f'/observations/{i}/mapping/{j}/range')
            if m['range']['source_id']!=source['id']:fail('E_REFERENCE',f'/observations/{i}/mapping/{j}','Mapping belongs to different source')

def validate_audit_binding(audit,request,plan,observations):
    validate_record(audit);extensions(audit)
    if audit['kind']!='audit' or audit['request_id']!=request['id'] or audit['plan_id']!=plan['id']:
        fail('E_REFERENCE','/audit','Audit/plan/request identity mismatch')
    sources={s['id']:s for s in request['sources']}
    if audit['artifact_ref'] not in sources or sources[audit['artifact_ref']]['text_digest']!=audit['artifact_digest']:
        fail('E_SOURCE_DIGEST','/audit/artifact_digest','Stale audit artifact')
    bind_observations(observations,request,plan)
    evidence={o['id']:o for o in observations}
    scopes=set(sources)|{r['id'] for r in request['regions']}
    for i,c in enumerate(audit['checks']):
        if c['scope'] not in scopes:fail('E_REFERENCE',f'/audit/checks/{i}/scope','Unknown check scope')
        if c['status']=='passed':
            expected_fact={'MIX-001':'exact-utf8-sha256','MIX-004':'run-coverage','MIX-016':'immutable-plan-binding'}.get(c['rule_id'])
            if expected_fact is None or c['method']!='static':
                fail('E_REFERENCE',f'/audit/checks/{i}','Only implemented static checks may pass')
            if not c['evidence_refs'] or any(not any(f['name']==expected_fact for f in evidence.get(ref,{}).get('facts',[])) for ref in c['evidence_refs']):
                fail('E_REFERENCE',f'/audit/checks/{i}','Evidence lacks the checked static fact')
        if c['status']=='waived':fail('E_PERMISSION',f'/audit/checks/{i}/waiver','External approval validation not implemented; no waived results accepted')
        for ref in c['evidence_refs']:
            o=evidence.get(ref)
            if o is None or c['scope'] not in o['scopes'] or o['artifact_ref']!=audit['artifact_ref'] or o['artifact_digest']!=audit['artifact_digest'] or o['method']!=c['method']:
                fail('E_REFERENCE',f'/audit/checks/{i}/evidence_refs','Unbound evidence or method mismatch')
    return copy.deepcopy(audit)

def evaluate(request,plan,registry,observations=(),target=None,source_id=None):
    r=validate_request(request);bind_plan(r,plan,registry)
    supplied=copy.deepcopy(list(observations));bind_observations(supplied,r,plan)
    sources={s['id']:s for s in r['sources']}
    # One exact logical story per audit. Caller must choose for multi-source requests.
    if source_id is None:
        if len(sources)!=1:fail('E_REFERENCE','/source_id','Choose one exact source for each audit')
        source_id=next(iter(sources))
    if source_id not in sources:fail('E_REFERENCE','/source_id','Unknown target source')
    s=sources[source_id];raw=s['text'].encode('utf-8');path=None
    if target is not None:
        path=Path(target)
        # This adapter accepts only exact UTF-8 text files, never DOCX/PDF extraction.
        with path.open('rb') as f: raw=f.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES:fail('E_RESOURCE_LIMIT','/target','Target exceeds byte budget')
        if decode_utf8(raw)!=s['text'] or 'sha256:'+hashlib.sha256(raw).hexdigest()!=s['text_digest']:
            fail('E_SOURCE_DIGEST','/target','Target text differs from selected SourceStory')
    regions=[x for x in r['regions'] if x['range']['source_id']==source_id]
    scopes=[source_id]+[x['id'] for x in regions]
    oid='static-'+object_digest(dict(source_id=source_id,digest=s['text_digest'],plan=plan['id']))[7:]
    o=dict(contract_version=VERSION,kind='observation',id=oid,artifact_ref=source_id,artifact_digest=s['text_digest'],
           host_ref='internal:'+ENGINE,environment=dict(application=ENGINE,version='1',operating_system=platform.system() or 'unknown',
           renderer='none',font_instance_refs=[],conditions={'target_kind':'utf8-file' if path else 'logical-source','index_unit':'unicode-scalar'}),
           scopes=scopes,method='static',facts=[dict(name='exact-utf8-sha256',value=s['text_digest'],unit=None),
           dict(name='scalar-count',value=len(s['text']),unit='unicode-scalar'),dict(name='run-coverage',value='complete-nonoverlapping',unit=None),dict(name='immutable-plan-binding',value=plan['id'],unit=None)],
           mapping=[],limitations=['No rendering; no trusted external observation or approval validation.'],extensions=[])
    validate_record(o)
    # Supplied observations are checked for references, never used to promote statuses.
    if any(x['id']==oid for x in supplied):fail('E_REFERENCE','/observations/id','Caller cannot replace generated static evidence')
    checks=[]
    def add(rule,scope,status,reason,checked=False):
        checks.append(dict(rule_id=rule,scope=scope,status=status,method='static',evidence_refs=[oid] if checked else [],reason=reason))
    add('MIX-001',source_id,'passed','Exact UTF-8 source digest computed on this selected story.',True)
    add('MIX-004',source_id,'passed','All source ranges and language coverage validated in scalar offsets.',True)
    add('MIX-016',source_id,'passed','Exact design schema, immutable plan/request/registry binding and extensions checked.',True)
    add('MIX-002',source_id,'needs-review','Language tag syntax checked; IANA registration/deprecation and native applicability remain unverified.')
    add('MIX-006',source_id,'needs-review' if any(c in BIDI_CONTROLS for c in s['text']) else 'not-checked',
        'Existing Bidi controls retained; context requires host review.' if any(c in BIDI_CONTROLS for c in s['text']) else 'Bidi host rendering not inspected.')
    for d in plan['decisions']:
        if d['region_id'] not in scopes:continue
        selected=d['value']['runs']
        add('MIX-003',d['region_id'],'unsupported' if any(x['module_id'] is None for x in selected) else 'needs-review',
            'Exact locale declarations only; language-specific guidance remains preview/unverified.')
        if any(c['region_id']==d['region_id'] for c in plan['conflicts']):
            add('MIX-002',d['region_id'],'needs-review','Conflicting annotations retained in deterministic plan trace.')
        add('MIX-013',d['region_id'],'not-checked','Display intent does not authorize loss of required content; actual visibility not inspected.')
        add('MIX-017',d['region_id'],'needs-review' if d['value']['relationships'] else 'not-applicable',
            'Translation/reviewer references do not establish independent alignment approval.' if d['value']['relationships'] else 'No relationship declared for this region.')
    for rule in ('MIX-005','MIX-007','MIX-009','MIX-010','MIX-011','MIX-018'):
        add(rule,source_id,'not-checked','No actual host/font/layout/accessibility/native editorial evidence; static declarations cannot pass this check.')
    a=dict(contract_version=VERSION,kind='audit',id='audit-'+object_digest(dict(plan=plan['id'],observation=o,checks=checks))[7:],
           request_id=r['id'],plan_id=plan['id'],artifact_ref=source_id,artifact_digest=s['text_digest'],checks=checks,
           limitations=copy.deepcopy(plan['limitations'])+['Only selected logical UTF-8 story inspected; supplied observations are untrusted and do not upgrade checks.'],extensions=[])
    output_observations=[o]+supplied
    validate_audit_binding(a,r,plan,output_observations)
    if path is not None:
        with path.open('rb') as f: after=f.read(MAX_BYTES+1)
        if after!=raw:fail('E_SOURCE_DIGEST','/target','Target changed during read-only review')
    return a,output_observations
