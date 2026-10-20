"""Optional read-only helpers, stdlib only. No files, network, rendering or repair.

review_text produces narrowly scoped editorial candidates, never rendered failures.
Call it on an extracted, explicitly classified text segment, not raw HTML or code.
"""
import hashlib

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
