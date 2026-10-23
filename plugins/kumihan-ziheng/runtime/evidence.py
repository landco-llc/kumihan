"""Validate declared evidence requirements only. No rendering or authentication.

References must bind to the reviewed artifact digest. This checks declarations,
not file existence, evidence truth, regional glyph correctness or native review.
"""
import re

STATUSES = ('passed', 'failed', 'needs-review', 'not-checked', 'unsupported', 'not-applicable', 'waived')
METHODS = ('static', 'rendered', 'interaction', 'manual', 'native-review')

# Additive vertical sidecar; v2 browser-specific records stay compatible.
VERTICAL_METHODS = ('static', 'rendered', 'interaction', 'native-application', 'native-proofreading')
VERTICAL_SCOPES = {
    'source-preservation': 'static', 'fixture-integrity': 'static',
    'font-coverage': 'static', 'font-metrics': 'static', 'font-features': 'static',
    'logical-text-order': 'static', 'pdf-extraction': 'static', 'pdf-structure': 'static',
    'vertical-glyph': 'rendered', 'regional-glyph': 'rendered',
    'punctuation-placement': 'rendered', 'run-orientation': 'rendered',
    'column-layout': 'rendered', 'line-breaking': 'rendered',
    'text-decoration': 'rendered', 'ruby-bopomofo': 'rendered',
    'reflow': 'rendered', 'pdf-appearance': 'rendered',
    'copy-search': 'interaction', 'focus-order': 'interaction',
    'assistive-technology': 'interaction', 'writing-mode-switch': 'interaction',
    'native-reopen': 'native-application', 'native-export': 'native-application',
    'native-proofreading': 'native-proofreading',
}


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


def validate_vertical_evidence(record):
    """Validate vertical evidence declarations without executing or certifying them.

    One record covers one artifact, fixture variant, method and scope. A valid
    static record cannot stand in for rendered, interactive or native acceptance.
    Unknown font details may be recorded while pending; a font/glyph pass needs
    the actual font instance and observation. Files and claims are not authenticated.
    """
    if not isinstance(record, dict): return [{'field': 'record', 'reason': 'Object required'}]
    errors = []
    def error(field, reason): errors.append({'field': field, 'reason': reason})
    def text(value): return isinstance(value, str) and bool(value.strip())
    def sha(value): return isinstance(value, str) and re.fullmatch('[a-f0-9]{64}', value) is not None
    def obj(value): return value if isinstance(value, dict) else {}
    def positive(value): return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0
    if record.get('schema_version') != '0.2.2': error('schema_version', 'Expected 0.2.2 vertical sidecar')
    for field in ('fixture_id', 'variant_id', 'observation'):
        if not text(record.get(field)): error(field, 'Explicit value required')
    if not sha(record.get('full_input_bundle_sha256')): error('full_input_bundle_sha256', 'Complete fixture input digest required')
    artifact = obj(record.get('artifact')); digest = artifact.get('sha256')
    if not text(artifact.get('path')) or not sha(digest): error('artifact', 'Artifact path and SHA256 required')
    method, scope, status = record.get('method'), record.get('scope'), record.get('status')
    if method not in VERTICAL_METHODS: error('method', 'Unknown vertical inspection method')
    scope_key = scope if isinstance(scope, str) else None
    if scope_key not in VERTICAL_SCOPES: error('scope', 'Unknown vertical inspection scope')
    if status not in STATUSES: error('status', 'Unknown verification status')
    if status == 'passed' and VERTICAL_SCOPES.get(scope_key) != method:
        error('method', 'This scope requires ' + str(VERTICAL_SCOPES.get(scope_key)) + ' evidence')
    if not isinstance(record.get('limitations'), list) or any(not text(v) for v in record['limitations']):
        error('limitations', 'Explicit limitation list required')
    reviewer = obj(record.get('reviewer'))
    for field in ('id', 'date'):
        if not text(reviewer.get(field)): error('reviewer.' + field, 'Reviewer identifier and date required')
    refs = record.get('evidence_refs')
    if not isinstance(refs, list): refs = []; error('evidence_refs', 'List required')
    for ref in refs:
        ref = obj(ref)
        if not text(ref.get('path')) or not text(ref.get('kind')) or ref.get('artifact_sha256') != digest:
            error('evidence_refs', 'Each structured reference must bind to this artifact digest')
    if status in ('waived', 'not-applicable', 'unsupported') and not text(record.get('reason')):
        error('reason', 'Non-execution status requires an explicit scoped reason')
    if status == 'waived':
        waiver = obj(record.get('waiver'))
        if not text(waiver.get('approval_ref')) or waiver.get('artifact_sha256') != digest:
            error('waiver', 'Scoped approval bound to this artifact required')
    if status != 'passed': return errors
    if not refs: error('evidence_refs', 'Passed requires method-specific observations')
    kinds = {r['kind'] for r in refs if isinstance(r, dict) and isinstance(r.get('kind'), str)}
    expected_kinds = {
        'static': {'static-measurement', 'byte-comparison', 'text-extraction', 'structure-inspection'},
        'rendered': {'screenshot', 'rendered-measurement'},
        'interaction': {'interaction-log'},
        'native-application': {'native-application-log'},
        'native-proofreading': {'editorial-review'},
    }
    if not kinds & expected_kinds.get(method if isinstance(method, str) else None, set()): error('evidence_refs', 'Method-specific evidence kind required')
    environment = obj(record.get('environment'))
    if method in ('rendered', 'interaction', 'native-application'):
        for field in ('os', 'application', 'application_version', 'engine', 'engine_version', 'target'):
            if not text(environment.get(field)): error('environment.' + field, 'Observed value or explicit unknown required')
        layout = obj(record.get('layout'))
        for field in ('writing_mode', 'text_orientation', 'font_size', 'font_weight', 'line_height', 'letter_spacing', 'inline_size', 'tcy'):
            if not text(layout.get(field)): error('layout.' + field, 'Actual layout condition required')
        if not isinstance(layout.get('enabled_font_features'), list): error('layout.enabled_font_features', 'Explicit feature list required; may be empty')
        dimensions = obj(environment.get('dimensions'))
        if not positive(dimensions.get('width')) or not positive(dimensions.get('height')) or not text(dimensions.get('unit')):
            error('environment.dimensions', 'Viewport/page width, height and units required')
        zoom = obj(environment.get('zoom'))
        if not text(zoom.get('method')) or not positive(zoom.get('factor')):
            error('environment.zoom', 'Actual enlargement method and factor required')
    if method == 'native-proofreading':
        if not text(reviewer.get('locale')) or not text(reviewer.get('editorial_scope')):
            error('reviewer', 'Proofreading requires reviewer locale and editorial scope; a native app is not a linguistic reviewer')
    if scope == 'assistive-technology':
        at = obj(environment.get('assistive_technology'))
        if not text(at.get('name')) or not text(at.get('version')):
            error('environment.assistive_technology', 'Actual AT name/version required')
    if scope == 'reflow':
        reflow = obj(record.get('reflow'))
        direction = reflow.get('scroll_direction')
        if direction not in ('horizontal', 'vertical'):
            error('reflow.scroll_direction', 'Observed scrolling direction required, separate from writing-mode')
        axis, size = ('height', 256) if direction == 'horizontal' else ('width', 320)
        if reflow.get('constraint_axis') != axis or reflow.get('constraint_css_px') != size:
            error('reflow', 'WCAG 1.4.10 reference condition must match actual scrolling direction')
        dimensions = obj(environment.get('dimensions'))
        if dimensions.get('unit') != 'CSS-px' or dimensions.get(axis) != size:
            error('environment.dimensions', 'Reflow acceptance must observe the declared CSS-pixel reference dimension')
    font_scope = scope in ('font-coverage', 'font-metrics', 'font-features', 'vertical-glyph',
                          'regional-glyph', 'punctuation-placement', 'run-orientation', 'text-decoration', 'ruby-bopomofo')
    if font_scope:
        fonts = record.get('fonts')
        if not isinstance(fonts, list) or not fonts: fonts = []; error('fonts', 'Actual font instances required')
        for font in fonts:
            font = obj(font)
            for field in ('family', 'face', 'release', 'internal_version', 'fallback'):
                if not text(font.get(field)) or font.get(field) == 'unknown': error('fonts.' + field, 'Identified font instance required for font/glyph acceptance')
            if not sha(font.get('sha256')): error('fonts.sha256', 'Exact font file digest required')
            if method == 'rendered' and font.get('actual_used') is not True:
                error('fonts.actual_used', 'Requested CSS family alone does not identify the rendered font')
    if scope in ('vertical-glyph', 'regional-glyph', 'punctuation-placement', 'run-orientation'):
        shaping = obj(record.get('shaping'))
        if not text(shaping.get('renderer_path')) or not text(shaping.get('vertical_metrics')) or not text(shaping.get('feature_application')):
            error('shaping', 'Renderer path, vertical metrics and feature application observations required')
        if 'glyph-observation' not in kinds: error('evidence_refs', 'Actual glyph observation required in addition to screenshot')
    return errors
