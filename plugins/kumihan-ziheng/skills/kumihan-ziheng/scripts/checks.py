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
