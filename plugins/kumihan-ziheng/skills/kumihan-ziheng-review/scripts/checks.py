"""Optional read-only helpers, stdlib only. No files, network, rendering or repair.

review_text produces narrowly scoped editorial candidates, never rendered failures.
Call it on an extracted, explicitly classified text segment, not raw HTML or code.
"""
import hashlib
import json

LOCALES = ('zh-Hant-TW', 'zh-Hant-HK')
ROLES = ('prose', 'name', 'url', 'code', 'english-quote', 'protected')
STYLES = (None, 'corner', 'curly', 'preserve')


def check_preservation(source, returned):
    """Compare exact extraction bytes; a pass says nothing about rendering."""
    if not isinstance(source, bytes) or not isinstance(returned, bytes):
        raise TypeError('Exact extraction bytes required; no implicit decoding or normalization')
    return {'rule_id': 'CONTENT-001', 'status': 'passed' if source == returned else 'failed',
            'method': 'static', 'source_sha256': hashlib.sha256(source).hexdigest(),
            'returned_sha256': hashlib.sha256(returned).hexdigest(),
            'scope': 'supplied extraction bytes only'}


def review_text(text, locale, role, quote_style=None):
    """Flag only ASCII ,;:!? in prose and curly quotes under a chosen corner style.

    Protected segments must be classified by the caller. Taiwan defaults to the
    educational corner style as a project recommendation; Hong Kong has no default
    quote style. English quotations, names, code and URLs are never coerced.
    """
    if locale not in LOCALES or role not in ROLES or quote_style not in STYLES:
        raise ValueError('Explicit supported locale, role and quote style required')
    if not isinstance(text, str):
        raise TypeError('Text must be a string')
    if role != 'prose':
        return []
    findings = []
    def candidate(rid, positions, reason):
        if positions:
            findings.append(dict(rule_id=rid, status='needs-review', method='static',
                                 positions=positions, reason=reason))
    candidate('ZH-HANT-005', [i for i, c in enumerate(text) if c in ',;:!?'],
              'ASCII punctuation in declared Chinese prose: confirm editorial intent; never auto-convert.')
    style = quote_style if quote_style is not None else ('corner' if locale.endswith('TW') else None)
    if style == 'corner':
        candidate('ZH-HANT-003' if locale.endswith('TW') else 'ZH-HANT-004',
                  [i for i, c in enumerate(text) if c in '“”‘’'],
                  'Curly quotation under selected corner style; quotations may be valid exceptions.')
    return findings


def review_segment(segment, context):
    """Review caller-classified text without parsing HTML or changing any text.

    v2 requires an explicit quote style; v1 review_text defaults stay unchanged.
    A segment's optional content_locale overrides the document's language.
    """
    if not isinstance(segment, dict) or not isinstance(context, dict):
        raise TypeError('Segment and context objects required')
    text, role = segment.get('text'), segment.get('role')
    if not isinstance(text, str) or not isinstance(role, str):
        raise TypeError('Segment text and caller-classified role required')
    locale = segment.get('content_locale', context.get('content_locale'))
    region = context.get('editorial_region')
    if locale == 'zh-Hant' and region in ('TW', 'HK'):
        locale = 'zh-Hant-' + region
    findings, limitations = [], ['Static candidates only; rendering, extraction and native review not established.']
    status = 'not-checked'
    if role not in ROLES:
        status = 'needs-review'; limitations.append('Ambiguous role: classify before prose inspection.')
    elif role != 'prose':
        status = 'not-applicable'; limitations.append('Protected/non-prose role excluded from punctuation scan.')
    elif locale not in LOCALES:
        limitations.append('Regional Chinese punctuation deferred; no TW/HK fallback.')
    elif region in ('TW', 'HK', 'MO') and region != locale[-2:]:
        raise ValueError('Contradictory explicit segment context')
    else:
        style = context.get('editorial_style')
        findings = review_text(text, locale, role, style if style in STYLES and style is not None else 'preserve')
        # An empty candidate set has no artifact-level pass meaning.
        status = 'needs-review' if findings else 'not-checked'
    return dict(findings=findings, coverage={'status':status, 'scope':'declared segment punctuation candidates only'},
                limitations=limitations, position_unit='unicode-code-point', source_changed=False)


def fixture_input_sha256(fixture):
    """Identify the complete fixture contract, excluding execution records.

    This includes text, annotations, variants and declared context. It does not
    normalize strings. The digest is different from text_utf8_sha256 and from
    the reviewed HTML/PDF/native artifact digest.
    """
    if not isinstance(fixture, dict):
        raise TypeError('Fixture object required')
    execution = {'execution_status_by_method', 'status', 'result', 'execution_evidence'}
    data = {k: v for k, v in fixture.items() if k not in execution}
    encoded = json.dumps(data, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':'), allow_nan=False).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def _range_errors(text, spans, field):
    errors = []
    if not isinstance(spans, list):
        return [{'field': field, 'reason': 'List required'}]
    for i, span in enumerate(spans):
        key = f'{field}[{i}]'
        if not isinstance(span, dict):
            errors.append({'field': key, 'reason': 'Object required'}); continue
        start, end = span.get('start_code_point'), span.get('end_code_point_exclusive')
        if (type(start) is not int or type(end) is not int or
                not 0 <= start < end <= len(text)):
            errors.append({'field': key, 'reason': 'Nonempty zero-based code-point range required'})
        elif span.get('text') != text[start:end]:
            errors.append({'field': key, 'reason': 'Exact source substring mismatch; no normalization permitted'})
    return errors


def validate_vertical_fixture(fixture):
    """Check an unexecuted fixture template, not its rendered acceptance."""
    if not isinstance(fixture, dict):
        return [{'field': 'fixture', 'reason': 'Object required'}]
    errors = []
    def error(field, reason): errors.append({'field': field, 'reason': reason})
    text = fixture.get('text')
    if not isinstance(text, str):
        return [{'field': 'text', 'reason': 'Exact Unicode text required'}]
    try:
        data = text.encode('utf-8')
    except UnicodeEncodeError:
        return [{'field': 'text', 'reason': 'Invalid UTF-8 scalar sequence'}]
    if fixture.get('text_encoding') != 'UTF-8': error('text_encoding', 'UTF-8 required')
    if type(fixture.get('text_code_point_count')) is not int or fixture['text_code_point_count'] != len(text):
        error('text_code_point_count', 'Decoded Unicode code-point count mismatch')
    if fixture.get('text_utf8_sha256') != hashlib.sha256(data).hexdigest():
        error('text_utf8_sha256', 'Exact decoded text UTF-8 digest mismatch')
    errors.extend(_range_errors(text, fixture.get('annotations'), 'annotations'))
    if fixture.get('source_policy') != 'fixed': error('source_policy', 'Original fixture text is fixed')
    if fixture.get('status') != 'not-checked' or fixture.get('result') is not None or fixture.get('execution_evidence') != []:
        error('status', 'Shipped contracts remain unexecuted; put real observations in a separate evidence record')
    methods = fixture.get('execution_status_by_method')
    if not isinstance(methods, dict) or not methods or any(v != 'not-checked' for v in methods.values()):
        error('execution_status_by_method', 'Template methods must remain not-checked')
    expected = fixture.get('expected')
    if not isinstance(expected, dict) or expected.get('not_an_execution_result') is not True:
        error('expected', 'Expected conditions must not be presented as execution results')
    return errors


def validate_vertical_suite(suite):
    """Validate count, IDs and exact text contracts; never award a fixture pass."""
    if not isinstance(suite, dict) or not isinstance(suite.get('fixtures'), list):
        return [{'field': 'fixtures', 'reason': 'Fixture list required'}]
    errors, fixtures = [], suite['fixtures']
    expected_ids = ({f'V-TW{i:02d}' for i in range(1, 13)} |
                    {f'V-HK{i:02d}' for i in range(1, 11)} |
                    {f'V-SH{i:02d}' for i in range(1, 9)})
    ids = [f.get('id') if isinstance(f, dict) and isinstance(f.get('id'), str) else None for f in fixtures]
    if len(fixtures) != 30 or set(ids) != expected_ids:
        errors.append({'field': 'fixtures', 'reason': 'Expected 30 unique TW12/HK10/shared8 contracts'})
    for i, fixture in enumerate(fixtures):
        for error in validate_vertical_fixture(fixture):
            errors.append(dict(field=f'fixtures[{i}].{error["field"]}', reason=error['reason']))
    return errors


def inspect_vertical_runs(text, runs):
    """Inspect caller-declared spans, without discovering words or graphemes.

    Code-point ranges must be verified against grapheme boundaries by the caller
    with a suitable Unicode segmenter. No width, font or orientation is measured.
    """
    if not isinstance(text, str): raise TypeError('Exact source text required')
    errors = _range_errors(text, runs, 'runs')
    findings = []
    orientations = {'mixed', 'upright', 'sideways', 'combine-upright', 'preserve'}
    if isinstance(runs, list):
        for i, run in enumerate(runs):
            if not isinstance(run, dict): continue
            if run.get('orientation') not in orientations:
                errors.append({'field': f'runs[{i}].orientation', 'reason': 'Explicit orientation policy required'})
            if not isinstance(run.get('role'), str) or not run['role'].strip():
                errors.append({'field': f'runs[{i}].role', 'reason': 'Semantic run role required'})
            if run.get('orientation') == 'combine-upright' and run.get('role') in ('url', 'email', 'identifier', 'latin-word'):
                findings.append({'rule_id': 'ZH-HANT-008', 'status': 'needs-review',
                                 'method': 'static', 'run_index': i,
                                 'reason': 'Selected TCY affects a meaningful run; compare recognition and copy/search without rewriting source.'})
    return {'errors': errors, 'findings': findings, 'source_changed': False,
            'limitations': ['Declared code-point ranges only; grapheme boundaries, shaping, actual glyph orientation and legibility not established.']}


def inspect_vertical_pair_breaks(text, break_offsets):
    """Flag supplied break positions inside paired —— or …… sequences.

    Offsets are observed boundaries between decoded Unicode code points, not
    source newlines or UTF-16 indices. This helper neither lays out text nor
    detects a browser's actual column ends.
    """
    if not isinstance(text, str) or not isinstance(break_offsets, list):
        raise TypeError('Source text and observed boundary list required')
    if any(type(v) is not int or not 0 <= v <= len(text) for v in break_offsets):
        raise ValueError('Boundaries must be zero-based code-point offsets')
    boundaries, findings = set(break_offsets), []
    for pair in ('——', '……'):
        start = 0
        while True:
            start = text.find(pair, start)
            if start < 0: break
            if start + 1 in boundaries:
                findings.append({'rule_id': 'ZH-HANT-006', 'status': 'needs-review',
                                 'method': 'static', 'break_code_point': start + 1,
                                 'reason': 'Supplied break splits a paired punctuation sequence; verify the actual column edge and editorial policy.'})
            start += len(pair)
    return {'findings': findings, 'source_changed': False,
            'limitations': ['Checks supplied boundary declarations only; no line-breaking or two-em geometry measured.']}
