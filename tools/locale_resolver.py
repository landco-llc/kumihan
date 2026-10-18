"""Additive context adapter. Existing Japanese schemas/data stay authoritative.

No locale inference from text, file names, fonts or the user's interface language.
This module selects guidance records; it neither renders nor rewrites content.
"""
import json
from pathlib import Path

MEDIA = ('web-editorial', 'web-marketing', 'web-ui', 'report-document',
         'presentation', 'display-copy')
LOCALES = {'ja-jp': ('ja-JP', 'ja', 'Jpan', 'JP'),
           'zh-hant-tw': ('zh-Hant-TW', 'zh', 'Hant', 'TW'),
           'zh-hant-hk': ('zh-Hant-HK', 'zh', 'Hant', 'HK'),
           'th-th': ('th-TH', 'th', 'Thai', 'TH')}
COMMON = ('content', 'design', 'evidence')


def resolve_context(locale, medium):
    """Return explicit language/script/region/media; reject missing/unknown parts."""
    if not isinstance(locale, str) or locale.lower() not in LOCALES:
        raise ValueError('Supported explicit locales: ja-JP, zh-Hant-TW, zh-Hant-HK, th-TH')
    if medium not in MEDIA:
        raise ValueError('Unknown medium')
    tag, language, script, region = LOCALES[locale.lower()]
    return dict(locale=tag, language=language, script=script, region=region, medium=medium)


def resolve_rules(context, root=None):
    """Select records in stable profile order. Japanese output is an exact adapter."""
    valid = resolve_context(context['locale'], context['medium'])
    if context != valid:
        raise ValueError('Contradictory context fields')
    root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    ja = root / 'skills/kumihan'
    if valid['language'] == 'ja':
        profile = json.loads((ja/'profiles'/f"{valid['medium']}.json").read_text(encoding='utf-8'))
        records = json.loads((ja/'rules/catalog.json').read_text(encoding='utf-8'))
        by_id = {r['id']: r for r in records}
        return [by_id[rid] for rid in profile['rule_ids']]
    if valid['language'] == 'th':
        records = json.loads((root/'plugins/kumihan-th/rules/catalog.json').read_text(encoding='utf-8'))
        return [r for r in records if valid['medium'] in r['media']]
    zh = root / 'plugins/kumihan-ziheng'
    records = []
    for name in COMMON:
        records.extend(json.loads((ja/'rules'/f'{name}.json').read_text(encoding='utf-8')))
    records.extend(json.loads((zh/'rules/zh-hant.json').read_text(encoding='utf-8')))
    return [r for r in records if valid['medium'] in r['media']
            and valid['locale'] in r.get('locales', [valid['locale']])]
