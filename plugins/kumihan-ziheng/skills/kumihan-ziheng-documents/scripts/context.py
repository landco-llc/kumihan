"""Local v2 selection adapter. No inference from text, rendering or pass/fail.

candidate = profile/medium universe, applicable = conditions resolved for review,
deferred = candidates lacking conditions (including out-of-scope features).
Applicable is an obligation to inspect, never an executed check or denominator.
The v1 shared locale resolver and its strict contract are unchanged.
"""
from copy import deepcopy

MEDIA = ('web-editorial', 'web-marketing', 'web-ui', 'report-document', 'presentation', 'display-copy')
ENUMS = {
    'editorial_region': (None, 'TW', 'HK', 'MO', 'unknown'),
    'expression_mode': (None, 'reading', 'display', 'hybrid'),
    'source_policy': ('fixed', 'propose-edits', 'approved-revision'),
    'writing_mode': (None, 'horizontal-tb', 'vertical-rl', 'vertical-lr'),
    'medium': (None,) + MEDIA,
}
DEFAULTS = dict(content_locale=None, editorial_region=None, register=None,
                editorial_style=None, element_role=None, expression_mode=None,
                medium=None, writing_mode=None, source_policy='fixed', features=[],
                audience_and_distance=None)
# Audited neutral policies, not all Chinese typography records.
NEUTRAL = {'ZH-HANT-001', 'ZH-HANT-009', 'ZH-HANT-011', 'ZH-HANT-015',
           'ZH-HANT-016', 'ZH-HANT-018'}
VERTICAL = ('vertical-rl', 'vertical-lr')
DECORATIONS = {'proper-name-mark', 'title-mark', 'text-emphasis'}
TAGS = {'zh-hant-tw': 'zh-Hant-TW', 'zh-hant-hk': 'zh-Hant-HK',
        'zh-hant-mo': 'zh-Hant-MO', 'zh-hant': 'zh-Hant'}


def resolve_review_context(raw):
    """Validate explicit metadata; unknown language tags remain unvalidated."""
    if not isinstance(raw, dict):
        raise TypeError('Context must be an object')
    if set(raw) - set(DEFAULTS):
        raise ValueError('Unknown context fields: ' + ', '.join(sorted(set(raw)-set(DEFAULTS))))
    c = deepcopy(DEFAULTS)
    c.update(deepcopy(raw))
    for key, values in ENUMS.items():
        if c[key] not in values:
            raise ValueError('Unsupported context value: ' + key)
    for key in ('content_locale', 'register', 'editorial_style', 'element_role', 'audience_and_distance'):
        if c[key] is not None and (not isinstance(c[key], str) or not c[key].strip()):
            raise TypeError(key + ' must be a nonempty string or null')
    if not isinstance(c['features'], list) or any(not isinstance(v, str) or not v.strip() for v in c['features']):
        raise TypeError('features must be a list of nonempty strings')
    tag = c['content_locale']
    if tag:
        c['content_locale'] = TAGS.get(tag.lower(), tag)
    region = {'zh-Hant-TW':'TW', 'zh-Hant-HK':'HK', 'zh-Hant-MO':'MO'}.get(c['content_locale'])
    if region and c['editorial_region'] not in (None, 'unknown', region):
        raise ValueError('Contradictory explicit locale and editorial_region')
    if region and c['editorial_region'] in (None, 'unknown'):
        c['editorial_region'] = region
    return c


def select_review_rules(context, records, profile):
    """Return stable candidate/applicable/deferred sets with scoped reasons."""
    c = resolve_review_context(context)
    if not isinstance(records, list) or not isinstance(profile, dict):
        raise TypeError('Records list and profile object required')
    if c['medium'] is None or profile.get('id') != c['medium']:
        raise ValueError('Explicit medium must match profile id')
    ids = [r['id'] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate rule ID')
    profile_ids = set(profile.get('rule_ids', []))
    for values in profile.get('rules_by_locale', {}).values():
        profile_ids.update(values)
    if not profile_ids <= set(ids):
        raise ValueError('Unresolved profile rule ID')
    candidates = [r for r in records if r['id'] in profile_ids and c['medium'] in r.get('media', [])]
    applicable, deferred = [], []
    chinese = c['content_locale'] in ('zh-Hant', 'zh-Hant-TW', 'zh-Hant-HK', 'zh-Hant-MO')
    supported = chinese and c['editorial_region'] in ('TW', 'HK')
    for r in candidates:
        rid = r['id']; reasons = []
        if rid.startswith('ZH-HANT-'):
            if rid not in NEUTRAL and not supported:
                reasons.append('TW/HK Chinese editorial context unresolved or unsupported; retain neutral scope')
            if rid in ('ZH-HANT-003', 'ZH-HANT-004'):
                required = 'TW' if rid.endswith('003') else 'HK'
                if c['editorial_region'] != required: reasons.append('Requires editorial_region=' + required)
                if c['editorial_style'] is None: reasons.append('Requires selected editorial_style')
                if c['element_role'] != 'prose': reasons.append('Requires declared Chinese prose role')
            if rid == 'ZH-HANT-005' and c['element_role'] != 'prose':
                reasons.append('Requires caller-classified Chinese prose')
            if rid in ('ZH-HANT-012', 'ZH-HANT-016', 'ZH-HANT-017', 'ZH-HANT-018') and c['writing_mode'] not in VERTICAL:
                reasons.append('Vertical writing not selected')
            if rid in ('ZH-HANT-016', 'ZH-HANT-018') and not chinese:
                reasons.append('Traditional Chinese content context required')
            if rid == 'ZH-HANT-017':
                if not DECORATIONS & set(c['features']):
                    reasons.append('Semantic text decoration feature not selected')
                if c['editorial_style'] is None:
                    reasons.append('Requires selected editorial_style for decoration placement')
            if rid == 'ZH-HANT-018':
                if c['element_role'] is None or c['expression_mode'] is None:
                    reasons.append('Requires declared element_role and expression_mode')
            if rid == 'ZH-HANT-013' and not {'ruby', 'bopomofo'} & set(c['features']):
                reasons.append('Ruby/Bopomofo feature not selected')
            if rid == 'ZH-HANT-014' and c['medium'] not in ('report-document', 'presentation') and 'pdf-export' not in c['features']:
                reasons.append('Office/PDF output not selected')
        if reasons: deferred.append({'rule_id':rid, 'reasons':reasons})
        else: applicable.append(rid)
    limitations = ['Selection is not execution or typography acceptance.',
                   'Unknown tags are not BCP47-validated; MO regional guidance is unsupported.']
    if c['writing_mode'] == 'vertical-lr':
        limitations.append('vertical-lr is an explicit layout choice requiring editorial justification; selection does not endorse ordinary Chinese column order.')
    if chinese and not supported:
        limitations.append('Neutral font identity and reading-order obligations do not establish TW/HK regional glyph acceptance.')
    return dict(selection_only=True, candidate_rule_ids=[r['id'] for r in candidates],
                applicable_rule_ids=applicable, deferred_rules=deferred,
                limitations=limitations)
