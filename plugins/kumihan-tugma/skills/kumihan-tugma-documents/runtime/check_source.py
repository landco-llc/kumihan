#!/usr/bin/env python3
"""Read-only Tagalog source integrity checks; not a renderer or proofreader."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import unicodedata

BASE = Path(__file__).resolve().parents[1]
MAX_BYTES = 1048576


def checked_text(raw):
    if not isinstance(raw, bytes):
        raise TypeError('Supply exact source bytes')
    if len(raw) > MAX_BYTES:
        raise ValueError('Source exceeds bounded 1 MiB scope')
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError as error:
        raise ValueError('Source must be valid UTF-8; keep original unchanged') from error


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def compare(source, candidate, source_metadata=None, candidate_metadata=None):
    a, b = checked_text(source), checked_text(candidate)
    equal = source == candidate and source_metadata == candidate_metadata
    return {'status': 'passed' if equal else 'failed', 'bytes_equal': source == candidate,
            'metadata_equal': source_metadata == candidate_metadata,
            'source_sha256': digest(source), 'candidate_sha256': digest(candidate),
            'derived_nfc_equal': unicodedata.normalize('NFC', a) == unicodedata.normalize('NFC', b),
            'note': 'Derived equivalence never authorizes rewriting.'}


def review_bytes(raw, locale='und', medium='review', candidate=None, source_metadata=None,
                 candidate_metadata=None, text_permission='immutable', expression_mode='reading'):
    text = checked_text(raw)
    if medium not in ('entry', 'web', 'documents', 'presentation', 'display', 'review'):
        raise ValueError('Unsupported medium')
    if text_permission not in ('immutable', 'suggestions', 'rewrite-authorized'):
        raise ValueError('Unsupported text permission')
    if expression_mode not in ('reading', 'expressive', 'hybrid'):
        raise ValueError('Unsupported expression mode')
    config = json.loads((BASE / 'locales/supported.json').read_text(encoding='utf-8'))
    canonical = {tag.lower(): tag for tag in config['locales']}.get(locale.lower()) if isinstance(locale, str) else None
    rules = json.loads((BASE / 'rules/catalog.json').read_text(encoding='utf-8')) if canonical else []
    diagnostic = []

    def note(code, evidence):
        diagnostic.append({'code': code, 'status': 'needs-review', 'scope': 'static-source', 'evidence': evidence})

    if not canonical:
        note('locale-unresolved', 'Explicit tl or tl-PH is required; preserve requested locale, including fil. No language-specific guidance applied.')
    if any(unicodedata.combining(c) for c in text):
        note('combining-marks-preserved', 'Combining sequences retained; segmentation, accent placement and clipping require the actual font and renderer.')
    controls = [{'offset': i, 'codepoint': f'U+{ord(c):04X}'} for i, c in enumerate(text)
                if c in '\u061c\u200b\u200c\u200d\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069']
    if controls:
        note('format-controls-preserved', controls)
    if canonical:
        if re.search(r'\b(?:ng|nang|din|rin|daw|raw)\b', text, re.I):
            note('contextual-orthography-review', 'These forms require syntax, meaning and editorial context; no replacements made.')
        if re.search(r'[\u1700-\u171f\u1735\u1736]', text):
            note('baybayin-preserved', 'Baybayin code points retained without transliteration or substitutions. Modern/archaic RA and virama/pamudpod stay distinct.')
        if '₱' in text or re.search(r'[ñÑáéíóúàèìòùâêîôûÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛ]', text):
            note('font-repertoire-review', 'Test actual font files, fallback and export for source diacritics, ñ and currency; no glyph claim made.')
        if re.search(r'\S{30,}', text):
            note('long-token-wrap-review', 'Inspect wrapping in the actual medium; never insert breaks into names or identifiers automatically.')
    applicable = 'documents' if medium in ('presentation', 'display') else medium
    selected = [r for r in rules if applicable in r['media']]
    integrity = compare(raw, raw if candidate is None else candidate, source_metadata,
                        source_metadata if candidate_metadata is None else candidate_metadata)
    return {'schema_version': '1.0', 'source': text, 'source_sha256': digest(raw),
            'source_integrity': integrity, 'requested_locale': locale, 'locale': canonical or 'und',
            'resolved_language': 'tl' if canonical else 'und', 'direction': 'ltr' if canonical else 'unspecified',
            'medium': medium, 'context': {'text_permission': text_permission, 'expression_mode': expression_mode},
            'guidance': [{'rule_id': r['id'], 'title': r['title'], 'source_ids': r['source_ids'], 'status': 'guidance-only'} for r in selected],
            'diagnostics': diagnostic, 'annotations': [], 'language_quality': 'needs-review',
            'native_rendering': 'not_checked', 'host_invocation': 'not_checked', 'office_pdf': 'not_checked',
            'limitations': ['UTF-8 preservation and supplied metadata comparison only.',
                            'No normalization, translation, casing, punctuation substitution or source rewriting.',
                            'No proof of linguistic correctness, browser behavior, font shaping, accessibility, Office/PDF or native-host acceptance.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--locale', default='und')
    parser.add_argument('--medium', default='review')
    parser.add_argument('--candidate', type=Path)
    args = parser.parse_args()
    result = review_bytes(args.source.read_bytes(), args.locale, args.medium,
                          args.candidate.read_bytes() if args.candidate else None)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(result['source_integrity']['status'] == 'failed')


if __name__ == '__main__':
    raise SystemExit(main())
