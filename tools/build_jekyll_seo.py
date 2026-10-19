#!/usr/bin/env python3
"""Generate metadata includes from Jekyll frontmatter and authored head templates.

Only the deliberately small head-template subset (page values, escape, and
page.lang branches) is interpreted here. Actual complete layouts are still
rendered and checked by Jekyll in CI; unsupported head syntax fails explicitly.
"""
import argparse
from html import escape
from pathlib import Path
import re
import yaml
from seo_metadata import enrich_html
from seo_inventory import public_paths

ROOT = Path(__file__).resolve().parents[1]


def render_head(source, page):
    condition = re.compile(r"{%\s*if page.lang == '([^']+)'\s*%}(.*?){%\s*endif\s*%}", re.S)
    def choose(match):
        parts = re.split(r"{%\s*(elsif page.lang == '[^']+'|else)\s*%}", match[2])
        if page['lang'] == match[1]:
            return parts[0]
        for index in range(1, len(parts), 2):
            branch = parts[index]
            if branch == 'else' or page['lang'] == branch.split("'")[1]:
                return parts[index + 1]
        return ''
    source = condition.sub(choose, source)
    def value(match):
        expression = match[1].strip().split('|')
        key = expression[0].strip().removeprefix('page.')
        if key not in page:
            raise ValueError(f'Missing frontmatter key: {key}')
        result = str(page[key])
        for filter_name in expression[1:]:
            if filter_name.strip() != 'escape':
                raise ValueError(f'Unsupported head filter: {filter_name}')
            result = escape(result, quote=True)
        return result
    source = re.sub(r'{{(.*?)}}', value, source)
    if '{{' in source or '{%' in source:
        raise ValueError('Unsupported Liquid in SEO head template')
    return source


def outputs():
    files = {}
    for path in public_paths(ROOT):
        source = path.read_text(encoding='utf-8')
        if not source.startswith('---\n'):
            continue
        page = yaml.safe_load(source.split('---', 2)[1])
        layout = page.get('layout')
        template = ROOT / 'templates' / f'seo-{layout}-head.html'
        if not template.is_file():
            raise ValueError(f'Unregistered Jekyll SEO layout: {layout} ({path})')
        page.setdefault('lang', 'ja')
        head = render_head(template.read_text(encoding='utf-8'), page)
        relative = path.relative_to(ROOT).as_posix()
        document = f'<html lang="{escape(page["lang"], quote=True)}"><head>{head}</head><body></body></html>'
        enriched = enrich_html(document, relative)
        files['_includes/seo-pages/' + relative] = enriched.split('<head>', 1)[1].split('</head>', 1)[0].strip() + '\n'
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    planned = outputs()
    stale = [name for name, content in planned.items()
             if not (ROOT / name).is_file() or (ROOT / name).read_text(encoding='utf-8') != content]
    extra = [p.relative_to(ROOT).as_posix() for p in (ROOT / '_includes/seo-pages').rglob('*.html')
             if p.relative_to(ROOT).as_posix() not in planned]
    if args.check and (stale or extra):
        raise SystemExit('Stale Jekyll SEO includes: ' + ', '.join(stale + extra))
    if not args.check:
        for name in stale:
            target = ROOT / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(planned[name], encoding='utf-8')
        for name in extra:
            (ROOT / name).unlink()
    print(f'Jekyll SEO: {len(planned)} pages ' + ('verified' if args.check else 'built'))


if __name__ == '__main__':
    main()
