"""Synthetic strings test contracts, never native editorial acceptance."""
import hashlib

VERSION = '0.1.0-design.1'

def digest(text):
    return 'sha256:' + hashlib.sha256(text.encode('utf-8')).hexdigest()

def record(kind, **fields):
    return dict(contract_version=VERSION, kind=kind, id=kind + '-fixture', **fields)

def request(parts=(('ja', '原稿'),)):
    sources, runs, regions = [], [], []
    for i, (tag, text) in enumerate(parts):
        sid, rid = f's{i}', f'r{i}'
        sources.append(dict(id=sid, text=text, text_digest=digest(text), origin_ref='fixture:synthetic'))
        if text:
            scope = dict(source_id=sid, start=0, end=len(text))
            runs.append(dict(id=f'run{i}', range=scope.copy(), language_tag=tag,
                             script_hint=None, origin='author', confidence=None, method='fixture:explicit'))
            regions.append(dict(id=rid, range=scope.copy(), parent_id=None, reading_order=i,
                                level='paragraph', role='body', expression='reading', direction='auto',
                                writing_mode='horizontal-tb', required_content=True, register='fixture'))
    return record('request', operation='resolve', sources=sources, language_runs=runs, regions=regions,
                  relationships=[], policies=dict(source_text_protected=True, allowed_layout_changes=[],
                  editorial_conventions=[], language_priority='coequal', ranked_language_tags=[], approval_refs=[]),
                  target=dict(profile='web-editorial', output='web', viewing_conditions='not-rendered', host_capability_refs=[]),
                  dependencies=[], extensions=[])

def plan(req):
    return record('plan', request_id=req['id'], source_digests=[dict(source_id=s['id'], text_digest=s['text_digest']) for s in req['sources']],
                  decisions=[], constraints=[], font_instances=[], optical_profiles=[], discretionaries=[],
                  required_capabilities=[], conflicts=[], limitations=[], extensions=[])

def observation(req):
    return record('observation', artifact_ref=req['sources'][0]['id'], artifact_digest=req['sources'][0]['text_digest'],
                  host_ref='fixture:host', environment=dict(application='fixture', version='1', operating_system='unknown',
                  renderer='none', font_instance_refs=[], conditions={}), scopes=['r0'], method='static', facts=[], mapping=[],
                  limitations=['No rendered evidence'], extensions=[])

def module():
    return record('module', module_id='ja', module_version='fixture', language_tags=['ja'], script_hints=[], rule_refs=[],
                  capabilities=[], dependencies=[], extensions=[])

def audit(req, p):
    return record('audit', request_id=req['id'], plan_id=p['id'], artifact_ref='s0', artifact_digest=req['sources'][0]['text_digest'],
                  checks=[dict(rule_id='MIX-009', scope='r0', status='not-checked', method='static', evidence_refs=[], reason='No rendering')],
                  limitations=[], extensions=[])

def error():
    return record('error', request_id='request-fixture', code='E_RANGE', scope='regions/0/range',
                  message='Invalid range', recoverable=True, resume_hint='Reload exact source and correct range')
