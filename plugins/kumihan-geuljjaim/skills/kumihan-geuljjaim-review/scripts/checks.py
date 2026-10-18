"""Read-only Korean candidate recognition. Stdlib; no network or automatic repair.
Call on explicitly classified extracted text, never raw HTML. Findings are editorial
candidates, not grammar verdicts or rendered layout failures.
"""
import hashlib
import re

ROLES = ('prose', 'name', 'code', 'url', 'quote', 'protected')

def check_preservation(source, returned):
    if not isinstance(source, bytes) or not isinstance(returned, bytes):
        raise TypeError('Exact extraction bytes required')
    return dict(rule_id='KO-TYPE-002', status='passed' if source == returned else 'failed',
                method='static', source_sha256=hashlib.sha256(source).hexdigest(),
                returned_sha256=hashlib.sha256(returned).hexdigest(),
                scope='supplied bytes only; no normalization or semantic inference')

def review_text(text, locale, role):
    if locale != 'ko-KR' or role not in ROLES:
        raise ValueError('Explicit ko-KR locale and supported role required')
    if not isinstance(text, str):
        raise TypeError('Text must be str')
    if role != 'prose':
        return []
    patterns = [
        ('KO-ORTH-001', r'(?<=[가-힣]) +(에서|에게|으로|까지|부터)(?=\s|$)',
         'Possible separated particle; quoted examples, names and poetry may be intentional.'),
        ('KO-ORTH-002', r'(?:할수|될수|알수)(?=\s|$)',
         'Possible dependent noun 수 spacing; confirm syntax and protected names.'),
        ('KO-TYPE-010', r'(?<=\d)[\r\n]+(?:원|개|명|kg|g|%)(?=\s|$)',
         'Explicit newline before a Korean price/count unit; table boundaries may be intentional.'),
        ('KO-TYPE-001', r'[\u1100-\u115f][\r\n]+[\u1160-\u11a7]',
         'Explicit newline between Hangul leading and vowel Jamo; educational decomposition may be intentional.')]
    return [dict(rule_id=rid, status='needs-review', method='static',
                 positions=[m.start() for m in matches], reason=reason)
            for rid, pattern, reason in patterns
            if (matches := list(re.finditer(pattern, text)))]
