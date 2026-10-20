#!/usr/bin/env python3
"""Generate Jekyll version fragments and README from the same edition facts."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, quote
import yaml
import edition_versions as v
from version_display import panel, role, x, rewrite_downloads, apply_html
ROOT=v.ROOT


def readme(text, facts):
    lines=[]
    for line in text.splitlines():
        if line.startswith('| ') and len(line.split(' | ')) == 6:
            cells=line.split(' | ')
            code=cells[0].removeprefix('| ').lower()
            if code in facts['editions']:
                f=facts['editions'][code]
                cells[2]='v'+f['source_version']
                status=(f'公開済 / Published **v{f["published_version"]}** · {f["published_at"]} · [Release]({f["release_url"]})'
                        if f['release_status']=='published' else 'Release未公開 / Unpublished — ソース版 / source v'+f['source_version'])
                cells[-1]=status+' |'
                line=' | '.join(cells)
        lines.append(line)
    text='\n'.join(lines)+'\n'
    f=facts['editions']['ja']
    ja=f'日本語の現行ソース版は v{f["source_version"]}、正式公開版は [v{f["published_version"]}]({f["release_url"]})（{f["published_at"]}）です。'
    en=f'The Japanese source version is v{f["source_version"]}; the published version is [v{f["published_version"]}]({f["release_url"]}) ({f["published_at"]}).'
    # Mark managed status spans once; subsequent generation replaces their exact region.
    for key,new,pattern in [('ja',ja,r'日本語の現行パッケージは .*?過去版として保持します。'),
                            ('en',en,r'The current Japanese package version is .*?remains available as history\.')]:
        begin=f'<!-- version-status:{key} -->';end=f'<!-- /version-status:{key} -->'
        replacement=begin+new+end
        if begin in text: text=re.sub(re.escape(begin)+'.*?'+re.escape(end),lambda _:replacement,text,flags=re.S)
        else: text=re.sub(pattern,lambda _:replacement,text)
    summary=[]
    for code,name in [('zh-hans','Simplified Chinese (字律)'),('zh-hant','Traditional Chinese (字衡)')]:
        item=facts['editions'][code]
        state=('published [v'+item['published_version']+']('+item['release_url']+')' if item['release_status']=='published' else 'source packages available; GitHub Release unpublished')
        summary.append(name+': '+state)
    begin='<!-- version-status:chinese -->';end='<!-- /version-status:chinese -->'
    replacement=begin+'; '.join(summary)+'.'+end
    if begin in text:text=re.sub(re.escape(begin)+'.*?'+re.escape(end),lambda _:replacement,text,flags=re.S)
    else:text=re.sub(r'Simplified Chinese \(字律\).*?both without a GitHub Release\.',lambda _:replacement,text)
    return text


def generated_markdown(text, f):
    assets={role(a['name']):a for a in f['verified_assets']}
    def link(m):
        label,url=m.groups()
        a=assets.get(role(url))
        if not a: raise ValueError('Unverified Japanese guide ZIP: '+url)
        return f'[{label}]({a["url"]})'
    text=re.sub(r'\[([^\]]+)\]\(([^)]+\.zip)\)',link,text)
    def metadata_link(m):
        label,url=m.groups()
        path=unquote(url).removeprefix('../')
        if path.endswith('SHA256SUMS.txt'):
            target='https://raw.githubusercontent.com/landco-llc/kumihan/'+f['source_commit']+'/'+quote(path)
        else: target=f['release_url']
        return f'[{label}]({target})'
    text=re.sub(r'\[([^\]]+)\]\((\.\./downloads[^)]+)\)',metadata_link,text)
    # All current-guide filenames and copy commands are concrete; historical guides
    # outside installation*.md remain untouched.
    text=re.sub(r'(?<!\d)0\.1\.8(?!\d)',f['published_version'],text)
    return '<!-- Generated from authored installation Markdown; do not edit. -->\n'+text


def outputs():
    facts=v.load();f=facts['editions']['ja']
    out={'README.md':readme((ROOT/'README.md').read_text(),facts),
         '_includes/version/ja-source-version.html':'v'+f['source_version']}
    for slot in ('hero','install','current'):
        def wrap(lang):
            attrs=(f'class="version-locale version-{lang}"' if slot!='current' else f'data-ui-{lang}'+(' hidden' if lang!='ja' else ''))
            return f'<div {attrs}>'+panel(f,{'ja':'ja','en':'en','zh':'zh-Hant-TW'}[lang],slot)+'</div>'
        out[f'_includes/version/ja-{slot}.html']='\n'.join(wrap(l) for l in ('ja','en','zh'))+'\n'
    for p in sorted((ROOT/'docs').glob('installation*.md')):
        out['_includes/version/docs/'+p.name]=generated_markdown(p.read_text(),f)
    ko=facts['editions']['ko']
    for p in [*ROOT.glob('kumihan-ko*.html'), *(ROOT/'docs').glob('install-ko-*.html')]:
        source=p.read_text();meta,body=source.split('---',2)[1:]
        lang=yaml.safe_load(meta)['lang']
        relative=p.relative_to(ROOT).as_posix()
        if relative.startswith('docs/'):
            body=rewrite_downloads(body,ko)
        else:
            wrapped=f'<html lang="{lang}"><head></head><body>'+body+'</body></html>'
            body=apply_html(wrapped,relative).split('<body>',1)[1].split('</body>',1)[0]
        out['_includes/version/pages/'+relative]=body
        out[f'_includes/version/ko-current-{lang}.html']=panel(ko,lang)+'\n'
    return out


def preservation_allowed(path, family):
    from version_display import edition_for
    from build_gateways import GATEWAYS
    if family=='protected': return path=='README.md'
    if family=='jekyll_sources': return bool(edition_for(path))
    return bool(edition_for(path) or path in {p[0] for p in GATEWAYS.values()} or path in
                {'_layouts/landing.html','_layouts/installation.html','_layouts/geuljjaim.html','_layouts/geuljjaim-index.html'})


def preservation():
    raise ValueError('Historical preservation generation belongs to private regression; public release contracts are reviewed immutable inputs')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');parser.add_argument('--preservation',action='store_true');args=parser.parse_args()
    stale=[]
    for name,content in (preservation() if args.preservation else outputs()).items():
        p=ROOT/name
        if args.check:
            if not p.exists() or p.read_text()!=content: stale.append(name)
        else:
            p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
    if stale: raise SystemExit('Stale version fragments/README: '+', '.join(stale))
    print('Jekyll version fragments and README '+('verified' if args.check else 'built'))

if __name__=='__main__':main()
