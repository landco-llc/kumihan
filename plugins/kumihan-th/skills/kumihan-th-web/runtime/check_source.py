"""Read-only bounded source comparison. No normalization, rendering or dictionary.

Offsets are UTF-16 half-open ranges. A split surrogate is rejected, not repaired.
CLI: python check_source.py original.txt candidate.txt [--protected ranges.json]
"""
import argparse
import hashlib
import json
from pathlib import Path
import unicodedata

MAX_BYTES = 1024 * 1024
CONTROLS = {'\u200b', '\u200c', '\u200d', '\u2060', '\ufeff', '\u00a0'}


def bounded(text):
    if not isinstance(text, str) or len(text.encode('utf-8')) > MAX_BYTES:
        raise ValueError('Expected UTF-8 text no larger than 1 MiB')
    return text.encode('utf-8')


def inspect(text):
    data = bounded(text)
    offset = 0
    controls = []
    for char in text:
        if char in CONTROLS:
            controls.append({'utf16_offset': offset, 'code_point': f'U+{ord(char):04X}',
                             'name': unicodedata.name(char, 'UNKNOWN')})
        offset += len(char.encode('utf-16-le')) // 2
    return {'sha256_utf8': hashlib.sha256(data).hexdigest(), 'utf8_bytes': len(data),
            'utf16_units': offset, 'code_points': len(text), 'controls': controls,
            'graphemes': 'not-checked', 'word_segmentation': 'unsupported',
            'rendering': 'not-checked'}


def span(text, start, end):
    raw = text.encode('utf-16-le')
    if type(start) is not int or type(end) is not int or not 0 <= start <= end <= len(raw)//2:
        raise ValueError('Invalid UTF-16 half-open range')
    return raw[start*2:end*2].decode('utf-16-le')


def compare(original, candidate, protected=()):
    before, after = inspect(original), inspect(candidate)
    if not isinstance(protected, (list, tuple)) or len(protected) > 10000:
        raise ValueError('At most 10000 protected ranges')
    findings = []
    for item in protected:
        try:
            expected = span(original, item['start'], item['end'])
            actual = span(candidate, item['start'], item['end'])
            status = 'passed' if expected == actual else 'failed'
        except (ValueError, UnicodeError, KeyError, TypeError):
            status = 'not-checked'
        findings.append({'range': item, 'status': status})
    return {'status': 'passed' if bounded(original) == bounded(candidate) else 'failed',
            'scope': 'exact supplied UTF-8 bytes and valid supplied UTF-16 protected spans only',
            'original': before, 'candidate': after, 'protected': findings,
            'source_modified': False}


def read(path):
    with Path(path).open('rb') as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError('File exceeds 1 MiB')
    return data.decode('utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original'); parser.add_argument('candidate')
    parser.add_argument('--protected')
    args = parser.parse_args()
    try:
        ranges = json.loads(read(args.protected)) if args.protected else []
        report = compare(read(args.original), read(args.candidate), ranges)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report['status'] == 'failed' else 0

if __name__ == '__main__':
    raise SystemExit(main())
