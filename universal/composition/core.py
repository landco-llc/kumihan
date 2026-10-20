"""Experimental static, source-preserving core. No rendering, fetching or target writes."""
from __future__ import annotations
import copy
import hashlib
import json
import re
from contract import VERSION, CompositionError, validate_record, unicode_check

ENGINE = 'composition-static-1'
MAX_BYTES = 1_048_576
MAX_ITEMS = 4096
BINDING_NS = 'kumihan:composition-binding'
# RFC5646 syntax only. No IANA registry/deprecation or locale support assertion.
TAG = re.compile(r'^(?:[a-z]{2,3}(?:-[a-z]{3}){0,3}|[a-z]{4}|[a-z]{5,8})(?:-[a-z]{4})?(?:-(?:[a-z]{2}|[0-9]{3}))?(?:-(?:[a-z0-9]{5,8}|[0-9][a-z0-9]{3}))*(?:-[0-9a-wy-z](?:-[a-z0-9]{2,8})+)*(?:-x(?:-[a-z0-9]{1,8})+)?$',re.I|re.ASCII)
GRANDFATHERED = set('en-gb-oed i-ami i-bnn i-default i-enochian i-hak i-klingon i-lux i-mingo i-navajo i-pwn i-tao i-tay i-tsu sgn-be-fr sgn-be-nl sgn-ch-de art-lojban cel-gaulish no-bok no-nyn zh-guoyu zh-hakka zh-min zh-min-nan zh-xiang'.split())

def fail(code, scope, message):
    raise CompositionError(code, scope, message)

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')

def object_digest(value):
    return 'sha256:'+hashlib.sha256(canonical(value)).hexdigest()

def text_digest(text):
    unicode_check(text)
    return 'sha256:'+hashlib.sha256(text.encode('utf-8')).hexdigest()

def decode_utf8(raw):
    try: return raw.decode('utf-8',errors='strict')
    except UnicodeError: fail('E_INVALID_UNICODE','/source','Invalid UTF-8')

def byte_range_to_scalar(text, start, end):
    unicode_check(text)
    raw=text.encode('utf-8')
    if type(start) is not int or type(end) is not int or not 0<=start<end<=len(raw):
        fail('E_RANGE','/byte_range','Invalid half-open byte range')
    try: return len(raw[:start].decode('utf-8')),len(raw[:end].decode('utf-8'))
    except UnicodeError: fail('E_RANGE','/byte_range','Byte offset splits UTF-8 scalar')

def valid_tag(tag):
    low=tag.lower()
    if low in GRANDFATHERED: return True
    if re.fullmatch(r'x(?:-[a-z0-9]{1,8})+',low,re.ASCII): return True
    if not TAG.fullmatch(tag): return False
    parts=low.split('-')
    # Extensions and variants cannot repeat (private use is opaque).
    used=set()
    for part in parts[1:]:
        if part=='x': break
        if len(part)==1 or len(part)>=5 or (len(part)==4 and part[0].isdigit()):
            if part in used: return False
            used.add(part)
    return True

def extensions(record):
    for i,ext in enumerate(record.get('extensions',[])):
        # Binding extension is output-only, not a command or trusted caller assertion.
        if ext['critical']:
            fail('E_CRITICAL_EXTENSION',f'/extensions/{i}','No critical extensions supported in this prototype')

def unique(items, scope, seen=None):
    seen=set() if seen is None else seen
    for i,item in enumerate(items):
        if item['id'] in seen: fail('E_REFERENCE',f'/{scope}/{i}/id','Duplicate identifier')
        seen.add(item['id'])
    return seen

def check_range(scope, sources, location):
    sid=scope['source_id']
    if sid not in sources: fail('E_REFERENCE',location+'/source_id','Unknown source')
    if not 0<=scope['start']<scope['end']<=len(sources[sid]['text']):
        fail('E_RANGE',location,'Invalid scalar half-open range')

def validate_request(request):
    unicode_check(request)
    if isinstance(request,dict):
        for field in ('sources','language_runs','regions','relationships','dependencies','extensions'):
            if isinstance(request.get(field),list) and len(request[field])>MAX_ITEMS:
                fail('E_RESOURCE_LIMIT','/'+field,'Split by source into bounded requests')
        if sum(len(s.get('text','').encode('utf-8')) for s in request.get('sources',[]) if isinstance(s,dict) and isinstance(s.get('text'),str))>MAX_BYTES:
            fail('E_RESOURCE_LIMIT','/sources','UTF-8 source budget exceeded; split by source')
    validate_record(request)
    if request['kind']!='request': fail('E_REFERENCE','/kind','Request required')
    if len(request['sources'])>128: fail('E_RESOURCE_LIMIT','/sources','At most 128 stories; split by source')
    extensions(request)
    if any(e['namespace']==BINDING_NS for e in request['extensions']):
        fail('E_REFERENCE','/extensions','Output binding namespace is reserved')
    seen=set()
    for field in ('sources','language_runs','regions','relationships'): unique(request[field],field,seen)
    sources={s['id']:s for s in request['sources']}
    for i,s in enumerate(request['sources']):
        if text_digest(s['text'])!=s['text_digest']: fail('E_SOURCE_DIGEST',f'/sources/{i}/text_digest','Exact UTF-8 digest mismatch')
    runs={sid:[] for sid in sources}
    for i,run in enumerate(request['language_runs']):
        check_range(run['range'],sources,f'/language_runs/{i}/range')
        if not valid_tag(run['language_tag']): fail('E_REFERENCE',f'/language_runs/{i}/language_tag','Malformed tag (syntax-only parser)')
        runs[run['range']['source_id']].append(run)
    for sid,items in runs.items():
        cursor=0
        for run in sorted(items,key=lambda r:(r['range']['start'],r['id'])):
            if run['range']['start']!=cursor: fail('E_RANGE','/language_runs','Runs overlap or omit scalar values')
            cursor=run['range']['end']
        if cursor!=len(sources[sid]['text']): fail('E_RANGE','/language_runs','Runs must cover every nonempty source exactly')
    regions={r['id']:r for r in request['regions']}
    orders=set()
    for i,r in enumerate(request['regions']):
        check_range(r['range'],sources,f'/regions/{i}/range')
        parent=r['parent_id']
        key=(parent,r['reading_order'])
        if key in orders: fail('E_REFERENCE',f'/regions/{i}/reading_order','Duplicate sibling reading order')
        orders.add(key)
        if parent is not None:
            if parent not in regions: fail('E_REFERENCE',f'/regions/{i}/parent_id','Unknown parent')
            pr=regions[parent]['range']; rr=r['range']
            if pr['source_id']!=rr['source_id'] or not pr['start']<=rr['start']<rr['end']<=pr['end']:
                fail('E_RANGE',f'/regions/{i}/parent_id','Parent must contain child within source')
        ancestry={r['id']}
        while parent is not None:
            if parent in ancestry or parent not in regions: fail('E_REFERENCE',f'/regions/{i}/parent_id','Cyclic or missing parent')
            ancestry.add(parent)
            if len(ancestry)>128: fail('E_RESOURCE_LIMIT',f'/regions/{i}/parent_id','Hierarchy exceeds 128 levels')
            parent=regions[parent]['parent_id']
    for i,rel in enumerate(request['relationships']):
        if rel['from_region'] not in regions or rel['to_region'] not in regions:
            fail('E_REFERENCE',f'/relationships/{i}','Unknown relationship region')
    for i,tag in enumerate(request['policies']['ranked_language_tags']):
        if not valid_tag(tag): fail('E_REFERENCE',f'/policies/ranked_language_tags/{i}','Malformed tag')
    if request['policies']['language_priority']=='explicit-ranked' and not request['policies']['ranked_language_tags']:
        fail('E_REFERENCE','/policies/ranked_language_tags','Explicit ranking requires tags')
    return copy.deepcopy(request)

def module_for(tag, registry):
    matches=[]
    for module_id,m in sorted(registry['modules'].items()):
        if any(tag.lower()==locale.lower() for locale in m['locales']): matches.append((module_id,m))
    # Ambiguous overlapping declarations remain unresolved.
    return matches[0] if len(matches)==1 else (None,None)

def candidate_check(candidates, runs):
    if len(candidates)>MAX_ITEMS: fail('E_RESOURCE_LIMIT','/candidates','Too many candidate annotations')
    for i,c in enumerate(candidates):
        if not isinstance(c,dict) or set(c)!={'run_id','language_tag','origin'} or c['run_id'] not in runs or not isinstance(c['language_tag'],str) or not valid_tag(c['language_tag']) or c['origin'] not in ('author','user','document-metadata','detected','fallback'):
            fail('E_REFERENCE',f'/candidates/{i}','Invalid candidate annotation')

def resolve(request, registry, candidates=()):
    r=validate_request(request)
    if not isinstance(registry,dict) or registry.get('schema_version')!='1.0' or not isinstance(registry.get('modules'),dict):
        fail('E_REFERENCE','/registry','Legacy registry 1.0 required')
    run_map={run['id']:run for run in r['language_runs']}
    candidate_check(candidates,run_map)
    binding=dict(engine=ENGINE,request_digest=object_digest(r),registry_digest=object_digest(registry),
                 candidates=sorted(copy.deepcopy(list(candidates)),key=lambda c:(c['run_id'],c['origin'],c['language_tag'])),
                 dependencies=copy.deepcopy(r['dependencies']),
                 parser='rfc5646-syntax-1; IANA registration/deprecation not checked')
    decisions=[];constraints=[];conflicts=[]
    limitations=['Static plan only; no rendered, native-editorial, accessibility or font optical measurements.',
                 'BCP47 syntax-only parser; registry/deprecation validation not performed.',
                 'Capability manifests are declarations; host capabilities remain unknown.',
                 'Font sizing not proposed: absolute/relative units and measured metrics unavailable.']
    for region in sorted(r['regions'],key=lambda x:(x['reading_order'],x['id'])):
        rid=region['id'];rr=region['range']; selections=[]
        for run in sorted(r['language_runs'],key=lambda x:(x['range']['start'],x['id'])):
            sr=run['range']
            if sr['source_id']!=rr['source_id'] or sr['end']<=rr['start'] or sr['start']>=rr['end']:continue
            choices=[dict(run_id=run['id'],language_tag=run['language_tag'],origin=run['origin'])]+[c for c in candidates if c['run_id']==run['id']]
            priority={'author':0,'user':1,'document-metadata':2,'detected':3,'fallback':4}
            choices.sort(key=lambda c:(priority[c['origin']],c['language_tag'].lower()))
            best=choices[0]; tags={c['language_tag'].lower() for c in choices}
            # Equal-priority contradictory declarations have no safe selected language.
            tied={c['language_tag'].lower() for c in choices if priority[c['origin']]==priority[best['origin']]}
            tag=best['language_tag'] if len(tied)==1 else 'und'
            mid,m=module_for(tag,registry)
            selection=dict(run_id=run['id'],range=copy.deepcopy(sr),language_tag=tag,
                           declared_language_tag=run['language_tag'],script_hint=run['script_hint'],origin=best['origin'],
                           module_id=mid,module_version=m['version'] if m else None,
                           module_sha256=m['module_sha256'] if m else None,module_status=m['status'] if m else None,
                           capability_state='declared' if m else 'unsupported',
                           declared_capabilities=copy.deepcopy(m['capabilities']) if m else [], candidates=copy.deepcopy(choices))
            selections.append(selection)
            if len(tags)>1:
                conflicts.append(dict(id=f'language-{rid}-{run["id"]}',region_id=rid,rule_refs=['MIX-002','MIX-003'],impact='review',
                                      reason='Language annotations disagree; trusted origin precedence recorded; equal priority stays und.',alternatives=sorted(tags)))
            if m is None: limitations.append(f'{rid}/{run["id"]}: language-specific rules unsupported for exact tag {tag}; source retained.')
        constraints.extend([dict(id=f'{rid}-{rule}',region_id=rid,rule_ref=rule,strength='hard',condition='always',requirement=requirement)
                            for rule,requirement in [('MIX-001','Preserve exact logical source and digest'),('MIX-004','Scalar ranges; host shaping boundaries require evidence'),('MIX-006','Delegate Bidi; never reverse source'),('MIX-013','Required content cannot be waived by display intent')]])
        value={k:copy.deepcopy(region[k]) for k in ('range','expression','direction','writing_mode','required_content','role','register')}
        value.update(runs=selections,language_priority=copy.deepcopy(r['policies']),
                     relationships=[copy.deepcopy(rel) for rel in r['relationships'] if rid in (rel['from_region'],rel['to_region'])])
        # No property is applied. Resolved means explicit metadata, never visual success.
        state='resolved' if all(s['module_id'] and s['origin'] in ('author','user','document-metadata') for s in selections) and len(selections)>0 else 'proposed'
        if any(c['region_id']==rid for c in conflicts):state='proposed'
        decisions.append(dict(id='metadata-'+rid,region_id=rid,property='composition-metadata',value=value,rule_refs=['MIX-001','MIX-002','MIX-014'],
                              reason='Hard source/direction/boundary constraints precede soft layout; stable region order then ID, origin precedence then exact locale.',state=state))
    for rel in r['relationships']:
        if rel['type']=='translation-of':limitations.append('translation alignment not independently verified; caller evidence references are untrusted.')
    for dep in r['dependencies']:
        if dep['state']=='unresolved':limitations.append('Unresolved dependency: '+dep['name'])
    if any(e['namespace']!=BINDING_NS for e in r['extensions']):limitations.append('Unknown noncritical extensions preserved without interpretation.')
    binding_ext=dict(namespace=BINDING_NS,version='1',critical=False,payload=binding)
    p=dict(contract_version=VERSION,kind='plan',id='plan-'+object_digest(binding)[7:],request_id=r['id'],
           source_digests=[dict(source_id=s['id'],text_digest=s['text_digest']) for s in r['sources']],
           decisions=decisions,constraints=constraints,font_instances=[],optical_profiles=[],discretionaries=[],
           required_capabilities=['shaping','bidi','font-metrics','render-observation'],conflicts=conflicts,
           limitations=list(dict.fromkeys(limitations)),extensions=copy.deepcopy(r['extensions'])+[binding_ext])
    validate_record(p)
    return p
