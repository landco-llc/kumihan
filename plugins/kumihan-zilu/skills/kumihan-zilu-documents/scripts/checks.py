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


def audit(text, candidate=None, locale='zh-Hans-CN'):
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
    raw = text.encode('utf-8')
    preservation = dict(status='not-checked', reason='No candidate text supplied; source digest alone is not comparison evidence.')
    if candidate is not None:
        preservation = dict(status='passed' if raw == candidate.encode('utf-8') else 'failed',
                            method='exact UTF-8 byte comparison; no normalization',
                            candidate_sha256=digest(candidate.encode('utf-8')))
    return dict(version='0.1.0', mode='audit', locale=locale, region=region,
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
    args = parser.parse_args()
    try:
        # decode bytes directly: preserve CRLF and BOM, do not normalize newlines.
        text = args.source.read_bytes().decode('utf-8')
        candidate = args.candidate.read_bytes().decode('utf-8') if args.candidate else None
        result = audit(text, candidate, args.locale)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['preservation']['status'] == 'failed' else 0


if __name__ == '__main__':
    sys.exit(main())
