#!/usr/bin/env python3
"""Audit source contracts or actual built HTML; new root/docs HTML is discovered."""
import argparse
import re
import struct
from pathlib import Path
from seo_metadata import CONFIG, locale
from seo_inventory import ROOT, pages, indexable, local_path
from build_sitemap import sitemap


def compatible_language(left, right):
    # A regional alternate may target text marked with its general language.
    a, b = left.lower().split('-'), right.lower().split('-')
    if a[0] != b[0]: return False
    for length in (2, 4):
        x=[v for v in a[1:] if len(v)==length]
        y=[v for v in b[1:] if len(v)==length]
        if x and y and x!=y: return False
    return True


def audit(root=ROOT,check_sitemap=True):
    root=Path(root)
    errors=[]
    try: all_pages=pages(root)
    except (ValueError,UnicodeError) as e: return [str(e)]
    try: indexable(all_pages)
    except ValueError as e: errors.append(str(e))
    by_path={p.path:p for p in all_pages}
    for page in all_pages:
        if page.noindex or page.external: continue
        def fail(message): errors.append(f'{page.path}: {message}')
        if len(page.titles)!=1 or not page.titles[0].strip(): fail('exactly one nonempty title required')
        required=['description'] + ['og:'+k for k in ('type','title','description','url','locale','image','image:alt','image:width','image:height')] + ['twitter:'+k for k in ('card','title','description','image')]
        for key in required:
            if len(page.meta[key])!=1 or not page.meta[key][0].strip(): fail(f'exactly one nonempty {key} required')
        if not re.fullmatch(r'[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*',page.lang): fail('invalid html lang')
        if page.lang.split('-')[0]=='ar' and page.direction!='rtl': fail('Arabic html dir must be rtl')
        if '\ufffd' in page.html: fail('Unicode replacement character found')
        for key,value in [('og:url',page.canonical),('og:locale',locale(page.lang)),('og:image',CONFIG['site_url']+CONFIG['image']['path']),('og:image:width',str(CONFIG['image']['width'])),('og:image:height',str(CONFIG['image']['height']))]:
            if page.meta[key] != [value]: fail(f'{key} inconsistent with contract')
        for key in ('og:title','twitter:title'):
            if page.meta[key]!=page.titles: fail(f'{key} must match title')
        for key in ('og:description','twitter:description'):
            if page.meta[key]!=page.meta['description']: fail(f'{key} must match description')
        if page.meta['twitter:image']!=page.meta['og:image']: fail('Twitter image mismatch')
        alt=dict(page.alternates)
        if len(alt)!=len(page.alternates): fail('duplicate hreflang')
        if not any(compatible_language(lang,page.lang) and url==page.canonical for lang,url in page.alternates if lang!='x-default'): fail('hreflang self reference missing')
        for lang,url in page.alternates:
            target=by_path.get(local_path(url))
            if target is None: fail(f'hreflang {lang} nonexistent or external URL {url}'); continue
            if target.noindex or target.external or target.canonical!=url: fail(f'hreflang {lang} target not indexable canonical')
            if lang!='x-default' and not compatible_language(target.lang,lang): fail(f'hreflang {lang} differs from target lang {target.lang}')
            if dict(target.alternates)!=alt: fail(f'hreflang reciprocal group mismatch: {url}')
        graphs=page.graphs
        if len(graphs)!=1 or not isinstance(graphs[0],dict): fail('exactly one valid JSON-LD document required'); continue
        graph=graphs[0]
        nodes=graph.get('@graph',[])
        if graph.get('@context')!='https://schema.org': fail('JSON-LD schema context invalid')
        web=[n for n in nodes if n.get('@type')=='WebPage']
        if len(web)!=1 or web[0].get('url')!=page.canonical: fail('JSON-LD WebPage.url differs from canonical')
        if len(web)!=1 or web[0].get('inLanguage')!=page.lang: fail('JSON-LD inLanguage differs from html lang')
        if any(k in str(graph) for k in ('aggregateRating','offers','FAQPage')): fail('unapproved structured data claim')
    if check_sitemap:
        try:
            target=root/'sitemap.xml'
            if not target.exists() or target.read_text(encoding='utf-8')!=sitemap(root): errors.append('sitemap.xml missing or drifted')
        except ValueError as e: errors.append('sitemap: '+str(e))
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-dir',type=Path)
    args=parser.parse_args()
    root=args.site_dir or ROOT
    errors=audit(root)
    image=root/CONFIG['image']['path']
    if not image.exists(): errors.append('OG image file missing')
    else:
        data=image.read_bytes()
        if data[:8]!=b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',data[16:24])!=(CONFIG['image']['width'],CONFIG['image']['height']): errors.append('OG image MIME/dimensions mismatch')
    if errors:
        print('\n'.join(errors)); print('See docs/seo/ADD_LANGUAGE_OR_PAGE.md'); return 1
    print(f'SEO {"built HTML" if args.site_dir else "source contracts"}: PASS ({len(pages(root))} pages)')
    return 0


if __name__=='__main__': raise SystemExit(main())
