"""Validate declared evidence requirements only. No rendering or authentication.

References must bind to the reviewed artifact digest. This checks declarations,
not file existence, evidence truth, regional glyph correctness or native review.
"""
import re

STATUSES = ('passed', 'failed', 'needs-review', 'not-checked', 'unsupported', 'not-applicable', 'waived')
METHODS = ('static', 'rendered', 'interaction', 'manual', 'native-review')


def validate_evidence_context(record):
    """Return scoped errors; static checks do not need browser metadata."""
    errors = []
    def error(field, reason): errors.append({'field':field, 'reason':reason})
    def text(value): return isinstance(value, str) and bool(value.strip())
    if not isinstance(record, dict): return [{'field':'record', 'reason':'Object required'}]
    if record.get('schema_version') != '2.0': error('schema_version', 'Expected 2.0')
    artifact = record.get('artifact')
    if not isinstance(artifact, dict): artifact = {}
    if not text(artifact.get('path')): error('artifact.path', 'Artifact reference required')
    digest = artifact.get('sha256')
    if not isinstance(digest, str) or re.fullmatch('[a-f0-9]{64}', digest) is None:
        error('artifact.sha256', 'Exact SHA256 required')
    if not text(record.get('scope')): error('scope', 'Named inspection scope required')
    method, status = record.get('method'), record.get('status')
    if method not in METHODS: error('method', 'Unknown inspection method')
    if status not in STATUSES: error('status', 'Unknown status')
    limits = record.get('limitations')
    if not isinstance(limits, list) or any(not text(v) for v in limits): error('limitations', 'Explicit list required')
    refs = record.get('evidence_refs')
    if not isinstance(refs, list): refs = []; error('evidence_refs', 'List required')
    if status == 'passed' and not refs: error('evidence_refs', 'Passed requires method/scope evidence')
    for ref in refs:
        if not isinstance(ref, dict): error('evidence_refs', 'Structured reference required'); continue
        if not text(ref.get('path')) or not text(ref.get('kind')): error('evidence_refs', 'Nonempty path and kind required')
        if ref.get('artifact_sha256') != digest: error('evidence_refs', 'Evidence belongs to another artifact')
    if status == 'passed' and record.get('scope') in ('regional-glyph', 'ivs-glyph') and method != 'rendered':
        error('method', 'Glyph acceptance requires rendered observations, never static byte comparison')
    if status == 'passed' and method in ('rendered', 'interaction'):
        env = record.get('environment')
        if not isinstance(env, dict): env = {}
        for k in ('writing_mode', 'os'):
            if not text(env.get(k)): error('environment.'+k, 'Observed condition required')
        viewport = env.get('viewport', {})
        if not isinstance(viewport, dict): viewport = {}
        for k in ('width','height'):
            v=viewport.get(k)
            if not isinstance(v,(int,float)) or isinstance(v,bool) or v <= 0: error('viewport.'+k,'Positive CSS dimension required')
        browser = env.get('browser', {})
        if not isinstance(browser, dict): browser = {}
        for k in ('name','version','engine','engine_version'):
            if not text(browser.get(k)): error('browser.'+k,'Observed value or explicit unknown required')
        zoom = env.get('zoom', {})
        if not isinstance(zoom, dict): zoom = {}
        if not text(zoom.get('method')): error('zoom.method','Actual enlargement method or none required')
        factor=zoom.get('factor')
        if not isinstance(factor,(int,float)) or isinstance(factor,bool) or factor <= 0: error('zoom.factor','Positive factor required')
        fonts=env.get('fonts')
        if not isinstance(fonts,list) or not fonts: fonts=[];error('fonts','Font observations or explicit unknown required')
        for font in fonts:
            if not isinstance(font,dict): error('fonts','Font object required');continue
            for k in ('family','face','version','fallback'):
                if not text(font.get(k)): error('fonts.'+k,'Observed value or explicit unknown required')
        kinds={r.get('kind') for r in refs if isinstance(r,dict)}
        if method=='rendered' and not kinds & {'screenshot','rendered-measurement'}:
            error('evidence_refs','CSS declaration alone cannot prove rendered acceptance')
        if method=='interaction' and 'interaction-log' not in kinds:
            error('evidence_refs','Actual interaction log required')
        if record.get('scope') in ('regional-glyph','ivs-glyph'):
            known = fonts and all(isinstance(f,dict) and f.get('actual_used') is True and all(f.get(k) != 'unknown' for k in ('family','face','version')) for f in fonts)
            if not known or 'glyph-observation' not in kinds:
                error('fonts','Requested glyph pass requires actual font and glyph evidence')
    return errors
