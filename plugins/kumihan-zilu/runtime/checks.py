#!/usr/bin/env python3
"""Read-only, offline evidence helper. Never edits input or certifies rendering."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


PROFILES = ('cn-vertical-reading', 'cn-vertical-display', 'cn-vertical-publication-gb', 'cn-classical-reference')


def vertical_context(context, findings):
    if context is None:
        return dict(status='not-requested', rendering=[])
    if not isinstance(context, dict) or context.get('profile') not in PROFILES:
        raise ValueError('Select an explicit vertical purpose profile')
    for key in ('css', 'direction_reason'):
        if key in context and not isinstance(context[key], str):
            raise ValueError(key + ' must be a string')
    if 'per_character_breaks' in context and not isinstance(context['per_character_breaks'], bool):
        raise ValueError('per_character_breaks must be a boolean')
    if 'selected_standards' in context and (not isinstance(context['selected_standards'], list) or
            not all(isinstance(item, str) and item.strip() for item in context['selected_standards'])):
        raise ValueError('selected_standards must be an array of nonempty strings')
    mode = context.get('writing_mode', 'unspecified')
    if mode not in ('unspecified', 'horizontal-tb', 'vertical-rl', 'vertical-lr'):
        raise ValueError('Unsupported writing mode')
    def flag(rule, message):
        findings.append(dict(rule_id=rule, status='needs-review', message=message))
    if context['profile'] == 'cn-vertical-publication-gb' and not context.get('selected_standards'):
        flag('KH-CN-V001', 'Specify selected GB edition, clauses, medium and authorized derivative; no universal GB claim.')
    if mode in ('unspecified', 'horizontal-tb') or context.get('per_character_breaks'):
        flag('KH-CN-V003', 'Use real writing-mode for continuous vertical text; width:1em or per-character breaks do not establish vertical layout.')
    if mode == 'vertical-lr' and not context.get('direction_reason'):
        flag('KH-CN-V004', 'Record why left-to-right columns are intended and compare visual and semantic reading order.')
    if re.search(r'[\"\']vrt2[\"\']\s+(?:1|on)', context.get('css', ''), re.I):
        flag('KH-CN-V006', 'Do not force vrt2 in shared CSS; inspect actual shaping under CSS Writing Modes.')
    return dict(status='requires-review', profile=context['profile'], writing_mode=mode,
                rendering=[dict(rule_id=f'KH-CN-V{n:03d}', status='not-checked',
                    reason='Context lint is not target-renderer, font, accessibility or publication evidence.') for n in range(1,27)])


def audit(text, candidate=None, locale='zh-Hans-CN', context=None):
    if not re.fullmatch(r'[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*', locale):
        raise ValueError('Invalid language tag')
    region = next((p.upper() for p in locale.split('-')[1:] if len(p) == 2 or p.isdigit()), 'unknown')
    findings = []
    # These are review candidates. Syntax/language context must be checked manually.
    for pattern, rule, message in [
        (r'……等', 'KH-CN-R015', '核对省略与“等”的语义；仅提供校阅候选。 / Review ellipsis redundancy in context.'),
        (r'最[^\s，。；]{0,12}', 'KH-CN-R025', '交由法律或编辑人员确认上下文；不作违法判定。 / Legal/editorial review only; no legality verdict.')
    ]:
        for match in re.finditer(pattern, text):
            findings.append(dict(rule_id=rule, status='needs-review', offset=match.start(),
                                 end=match.end(), evidence=match.group(), message=message))
    vertical = vertical_context(context, findings)
    raw = text.encode('utf-8')
    preservation = dict(status='not-checked', reason='No candidate text supplied; source digest alone is not comparison evidence.')
    if candidate is not None:
        preservation = dict(status='passed' if raw == candidate.encode('utf-8') else 'failed',
                            method='exact UTF-8 byte comparison; no normalization',
                            candidate_sha256=digest(candidate.encode('utf-8')))
    return dict(version='0.1.2', vertical=vertical, mode='audit', locale=locale, region=region,
                profile_status='supported' if locale.lower() == 'zh-hans-cn' else 'unsupported',
                source_sha256=digest(raw), source_bytes=len(raw), preservation=preservation,
                findings=findings, rendering=[dict(rule_id=f'KH-CN-R{n:03d}', status='not-checked',
                reason='Requires target renderer / output / human evidence; static text cannot establish this result.')
                for n in (7,10,12,13,14,18,20,21,26,27,28,29,30,31,32,33,34)],
                limits='Static candidates and byte comparison only. No automatic editing, glyph, GB, WCAG, Office/PDF or host certification.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--candidate', type=Path)
    parser.add_argument('--locale', default='zh-Hans-CN')
    parser.add_argument('--context', type=Path, help='Explicit purpose/writing-mode JSON; read-only context lint')
    args = parser.parse_args()
    try:
        # decode bytes directly: preserve CRLF and BOM, do not normalize newlines.
        text = args.source.read_bytes().decode('utf-8')
        candidate = args.candidate.read_bytes().decode('utf-8') if args.candidate else None
        context = json.loads(args.context.read_text(encoding='utf-8')) if args.context else None
        result = audit(text, candidate, args.locale, context)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['preservation']['status'] == 'failed' else 0


if __name__ == '__main__':
    sys.exit(main())
