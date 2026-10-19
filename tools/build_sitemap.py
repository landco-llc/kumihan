#!/usr/bin/env python3
"""Deterministic canonical-only sitemap. --check never writes."""
import argparse
from pathlib import Path
from xml.sax.saxutils import escape
from seo_inventory import ROOT, pages, indexable


def sitemap(root=ROOT):
    urls=sorted(p.canonical for p in indexable(pages(root)))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{escape(url)}</loc></url>\n' for url in urls) + '</urlset>\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--site-dir',type=Path)
    args=parser.parse_args()
    try:
        root=args.site_dir or args.root
        content=sitemap(root)
        target=root/'sitemap.xml'
        if args.check:
            if not target.exists() or target.read_text(encoding='utf-8')!=content:
                raise ValueError('sitemap.xml drift; run python tools/build_seo.py')
        else: target.write_text(content,encoding='utf-8')
        print(f'Sitemap {"check" if args.check else "build"}: PASS ({content.count("<loc>")} URLs)')
    except ValueError as error:
        parser.exit(1,str(error)+'\n')


if __name__=='__main__': main()
