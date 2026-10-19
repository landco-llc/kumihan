#!/usr/bin/env python3
"""Shared, deterministic SEO contract; page copy remains in existing sources.

CLI: python tools/seo_metadata.py relative/page.html < source.html
"""
import json
import re
import sys
from functools import lru_cache
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'assets/seo-config.json').read_text(encoding='utf-8'))


def canonical_url(path):
    url = urljoin(CONFIG['site_url'], str(path))
    return CONFIG['site_url'] if url == CONFIG['site_url'] + 'index.html' else url


def locale(lang):
    """OG uses language_TERRITORY, never BCP47 script subtags."""
    parts = lang.replace('_', '-').split('-')
    language = parts[0].lower()
    territory = next((p.upper() for p in parts[1:] if len(p) == 2), None)
    defaults = dict(ar='SA', bn='BD', de='DE', en='US', es='ES', fr='FR', hi='IN',
                    id='ID', it='IT', ja='JP', ko='KR', pl='PL', pt='BR', ru='RU',
                    sw='KE', th='TH', vi='VN', zh='CN')
    if language == 'zh' and 'Hant' in parts:
        territory = territory or 'TW'
    return language + '_' + (territory or defaults.get(language, language.upper()))


@lru_cache(maxsize=1)
def _groups():
    # Lazy import avoids a module initialization cycle in gateway generation.
    import build_gateways
    gateways = build_gateways.GATEWAYS
    groups = {}
    group = {v[1]: canonical_url(v[0]) for v in gateways.values()}
    group['x-default'] = CONFIG['site_url']
    for v in gateways.values():
        groups[v[0]] = group
    language_tags = {k: v[1] for k, v in gateways.items()}
    for product in build_gateways.PRODUCTS.values():
        pages = product['pages']
        group = {language_tags.get(k, k): canonical_url(v) for k, v in pages.items()}
        group['x-default'] = canonical_url(next(iter(pages.values())))
        for path in pages.values():
            groups[path] = group
    return groups


def render_metadata(title, description, lang, canonical, alternates=None):
    """Render one complete head metadata block from authoritative page values."""
    canonical = canonical_url(canonical)
    x = lambda s: escape(str(s), quote=True)
    image = CONFIG['image']
    image_url = canonical_url(image['path'])
    lines = [f'<title>{x(title)}</title>',
             f'<meta name="description" content="{x(description)}">',
             f'<link rel="canonical" href="{x(canonical)}">']
    lines += [f'<link rel="alternate" hreflang="{x(k)}" href="{x(canonical_url(v))}">'
              for k, v in sorted((alternates or {}).items())]
    og = {'type': 'website', 'title': title, 'description': description, 'url': canonical,
          'locale': locale(lang), 'image': image_url, 'image:alt': image['alt'],
          'image:width': image['width'], 'image:height': image['height']}
    lines += [f'<meta property="og:{k}" content="{x(v)}">' for k, v in og.items()]
    card = 'summary_large_image' if image['width'] / image['height'] >= 1.8 else 'summary'
    twitter = dict(card=card, title=title, description=description, image=image_url)
    twitter['image:alt'] = image['alt']
    lines += [f'<meta name="twitter:{k}" content="{x(v)}">' for k, v in twitter.items()]
    publisher = CONFIG['publisher']
    org_id = publisher['url'] + '#organization'
    site_id = CONFIG['site_url'] + '#website'
    graph = [
        {'@type': 'Organization', '@id': org_id, 'name': publisher['name'], 'url': publisher['url']},
        {'@type': 'WebSite', '@id': site_id, 'url': CONFIG['site_url'],
         'name': CONFIG['site_name'], 'publisher': {'@id': org_id}},
        {'@type': 'WebPage', '@id': canonical + '#webpage', 'url': canonical,
         'name': title, 'description': description, 'inLanguage': lang,
         'isPartOf': {'@id': site_id}, 'publisher': {'@id': org_id}}]
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False,
                      separators=(',', ':')).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    lines.append('<script type="application/ld+json">' + data + '</script>')
    return '\n'.join(lines)


class _Head(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ''
        self.description = ''
        self.canonical = ''
        self.alternates = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang = a.get('lang', '')
        if tag == 'meta' and a.get('name', '').lower() == 'description':
            self.description = a.get('content', '')
        if tag == 'link':
            rel = a.get('rel', '').lower().split()
            if 'canonical' in rel:
                self.canonical = a.get('href', '')
            if 'alternate' in rel and a.get('hreflang'):
                self.alternates[a['hreflang']] = a.get('href', '')


def _seo_tag(match):
    tag = match.group()
    # Parse attributes, irrespective of order, quote style, or whitespace.
    class Attributes(HTMLParser):
        def handle_starttag(self, name, attrs):
            self.name, self.attrs = name, dict(attrs)
    p = Attributes()
    p.feed(tag)
    a = p.attrs
    rel = a.get('rel', '').lower().split()
    key = (a.get('name') or a.get('property') or '').lower()
    if (p.name == 'link' and ('canonical' in rel or ('alternate' in rel and 'hreflang' in a))) or (
            p.name == 'meta' and (key == 'description' or key.startswith(('og:', 'twitter:')))):
        return ''
    return tag


def enrich_html(html, path):
    """Replace SEO head only; preserve all body text, style, and page language."""
    match = re.search(r'<head\b[^>]*>(.*?)</head\s*>', html, re.I | re.S)
    if not match:
        raise ValueError(f'{path}: missing head')
    parser = _Head()
    parser.feed(html[:match.end()])
    title_match = re.search(r'<title\b[^>]*>(.*?)</title\s*>', match[1], re.I | re.S)
    title = unescape(title_match[1]) if title_match else ''
    if not title or not parser.description or not parser.lang:
        raise ValueError(f'{path}: title, description and html lang are required')
    canonical = canonical_url(parser.canonical or path)
    alternates = _groups().get(str(path), parser.alternates)
    head = re.sub(r'<title\b[^>]*>.*?</title\s*>', '', match[1], flags=re.I | re.S)
    head = re.sub(r'<script\b[^>]*type\s*=\s*[\'"]application/ld\+json[\'"][^>]*>.*?</script\s*>', '', head, flags=re.I | re.S)
    head = re.sub(r'<(?:meta|link)\b[^>]*>', _seo_tag, head, flags=re.I)
    # Strip whitespace left by prior metadata to guarantee repeated builds agree.
    head = '\n'.join(line for line in head.splitlines() if line.strip())
    metadata = render_metadata(title, parser.description, parser.lang, canonical, alternates)
    return html[:match.start(1)] + '\n' + head + '\n' + metadata + '\n' + html[match.end(1):]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: seo_metadata.py RELATIVE_PATH < source.html')
    sys.stdout.write(enrich_html(sys.stdin.read(), sys.argv[1]))
