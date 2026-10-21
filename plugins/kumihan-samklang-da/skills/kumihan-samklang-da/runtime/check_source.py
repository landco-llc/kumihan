#!/usr/bin/env python3
"""Bounded, read-only source diagnostics. This is not a renderer or proofreader."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unicodedata

BASE = Path(__file__).resolve().parents[1]
MAX_BYTES = 1048576


def load(relative):
    return json.loads((BASE / relative).read_text(encoding='utf-8'))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def checked_text(raw):
    if not isinstance(raw, bytes):
        raise TypeError('Supply exact source bytes')
    if len(raw) > MAX_BYTES:
        raise ValueError('Source exceeds bounded 1 MiB static scope')
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError as error:
        raise ValueError('Source must be valid UTF-8; keep the original file unchanged') from error


def compare(source, candidate, source_metadata=None, candidate_metadata=None):
    a, b = checked_text(source), checked_text(candidate)
    same = source == candidate and source_metadata == candidate_metadata
    return {'status': 'passed' if same else 'failed', 'scope': 'exact supplied bytes and metadata',
            'bytes_equal': source == candidate, 'metadata_equal': source_metadata == candidate_metadata,
            'source_sha256': digest(source), 'candidate_sha256': digest(candidate),
            'derived_nfc_equal': unicodedata.normalize('NFC', a) == unicodedata.normalize('NFC', b),
            'note': 'Derived equivalence never authorizes rewriting original bytes.'}


class StaticHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.nodes, self.stack, self.text = [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        parent = self.stack[-1] if self.stack else {}
        node = {'tag': tag, 'attrs': attrs, 'line': self.getpos()[0],
                'lang': attrs.get('lang', parent.get('lang', '')),
                'dir': attrs.get('dir', parent.get('dir', '')),
                'isolated': tag == 'bdi' or attrs.get('dir') in ('ltr', 'rtl', 'auto') or parent.get('isolated', False)}
        self.nodes.append(node)
        if tag not in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                del self.stack[i:]
                break

    def handle_data(self, text):
        if self.stack and self.stack[-1]['tag'] not in ('style', 'script'):
            self.text.append((self.stack[-1], text))


def review_bytes(raw, locale='und', medium='review', candidate=None, source_metadata=None,
                 candidate_metadata=None, format='text', editorial_mode=None,
                 house_style=None, expression_mode='reading', text_permission='immutable'):
    """Return supplied text intact, locale-scoped guidance and reproducible diagnostics.

    Locale must be explicit; script, names and shared vocabulary never select a language.
    A candidate is compared, never written. Metadata is compared only if supplied.
    """
    text = checked_text(raw)
    if expression_mode not in ('reading', 'expressive', 'hybrid'):
        raise ValueError('Unsupported expression mode')
    if text_permission not in ('immutable', 'suggestions', 'rewrite-authorized'):
        raise ValueError('Unsupported text permission')
    if house_style is not None and not isinstance(house_style, str):
        raise ValueError('House style must be supplied text')
    if medium not in ('entry', 'web', 'documents', 'presentation', 'display', 'review'):
        raise ValueError('Unsupported medium')
    if format not in ('text', 'html'):
        raise ValueError('Supported formats are text and bounded static html')
    config = load('locales/supported.json')
    supported = {tag.lower(): tag for tag in config['locales']}
    canonical = supported.get(locale.lower()) if isinstance(locale, str) else None
    language = config['language'] if canonical else 'und'
    direction = 'rtl' if language == 'he' or canonical and '-Arab' in canonical else (
        'unspecified' if language in ('und', 'ms') and not (canonical and '-Latn' in canonical) else 'ltr')
    modes = ('classical', 'medieval', 'ecclesiastical', 'modern', 'editorial')
    if editorial_mode is not None and (language != 'la' or editorial_mode not in modes):
        raise ValueError('Unsupported editorial mode for this language')
    diagnostics = []

    def note(code, evidence, status='needs-review'):
        diagnostics.append({'code': code, 'status': status, 'scope': 'static-source', 'evidence': evidence})

    if language == 'und':
        note('locale-unresolved', 'No supported explicit locale. Original is preserved; no edition-specific guidance.')
    if any(unicodedata.combining(c) for c in text):
        note('combining-marks-preserved', 'Combining marks are present. Grapheme segmentation and glyph placement require the target engine.')
    controls = [{'offset': i, 'codepoint': f'U+{ord(c):04X}'} for i, c in enumerate(text)
                if c in '\u061c\u200b\u200c\u200d\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069']
    if controls:
        note('format-controls-preserved', controls)
    if language == 'da':
        note('danish-context-review', {'locale': canonical, 'house_style': house_style or 'unspecified', 'message': 'Danish only; comma system, names and formatting require context. No automatic correction.'})
        if re.search(r'\b[Aa]a\w*', text):
            note('danish-aa-name-preserved', 'Aa/Å names require authoritative spelling; no global replacement.')
        if re.search(r'[ÆØÅæøå]', text):
            note('danish-glyph-review', 'Preserve independent Danish letters; inspect actual font and copy round trip.')
        if re.search(r'\S{20,}', text):
            note('danish-compound-wrap-review', 'Long token: check width and Danish hyphenation; do not insert spaces or hard hyphens.')
        if re.search(r'[0-9].*[%€$]|\bkr\.', text):
            note('danish-value-review', 'Preserve numeric value, currency and input unit; Danish does not imply DKK.')
        note('danish-comma-choice', 'Preserve existing startkomma practice unless the user specifies a system; syntax remains human review.')
    if format == 'html':
        parser = StaticHTML()
        parser.feed(text)
        root = next((n for n in parser.nodes if n['tag'] == 'html'), None)
        if root:
            declared = root['lang'].lower()
            if canonical and declared != canonical.lower():
                note('document-locale-review', {'supplied_locale': canonical, 'root_lang': root['lang']})
            if direction == 'rtl' and root['dir'] != 'rtl':
                note('base-direction-review', 'Known RTL source lacks explicit root dir=rtl; alignment alone does not establish direction.')
        for node in parser.nodes:
            style = node['attrs'].get('style', '')
            if re.search(r'word-break\s*:\s*break-all|white-space\s*:\s*nowrap|overflow(?:-[xy])?\s*:\s*hidden', style, re.I):
                note('inline-wrap-risk', {'line': node['line'], 'style': style})
            if direction == 'rtl' and re.search(r'letter-spacing\s*:\s*(?!normal\b|0(?:px|em|rem)?(?:\s|;|$))', style, re.I):
                note('rtl-tracking-review', {'line': node['line'], 'style': style})
    rules = load('rules/catalog.json') if canonical else []
    integrity = compare(raw, raw if candidate is None else candidate, source_metadata,
                        source_metadata if candidate_metadata is None else candidate_metadata)
    return {'schema_version': '1.0', 'source': text, 'source_sha256': digest(raw),
            'source_integrity': integrity, 'requested_locale': locale, 'locale': canonical or 'und',
            'resolved_language': language, 'direction': direction, 'medium': medium, 'format': format,
            'language_quality': 'needs-review', 'native_rendering': 'not-checked',
            'editorial_mode': (editorial_mode or 'needs-review') if language == 'la' else 'not-applicable',
            'annotations': [], 'host_invocation': 'not-checked', 'office_pdf': 'not-checked',
            'guidance': [{'rule_id': r['id'], 'title': r['title'], 'status': 'guidance-only'} for r in rules],
            'diagnostics': diagnostics,
            'context': {'house_style': house_style, 'expression_mode': expression_mode, 'text_permission': text_permission},
            'limitations': ['Static UTF-8 preservation and supplied metadata comparison only.',
                            'No normalization, casing, transliteration, punctuation substitution or source rewriting.',
                            'No browser, font, glyph, screen-reader, Office, PDF or native-host acceptance.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--locale', default='und')
    parser.add_argument('--medium', default='review')
    parser.add_argument('--format', choices=('text', 'html'), default='text')
    parser.add_argument('--candidate', type=Path)
    parser.add_argument('--editorial-mode', choices=('classical','medieval','ecclesiastical','modern','editorial'))
    args = parser.parse_args()
    result = review_bytes(args.source.read_bytes(), args.locale, args.medium,
                          args.candidate.read_bytes() if args.candidate else None, format=args.format, editorial_mode=args.editorial_mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(result['source_integrity']['status'] == 'failed')


if __name__ == '__main__':
    raise SystemExit(main())
