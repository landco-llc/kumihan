#!/usr/bin/env python3
"""Measure installation entry points from the canonical host guides."""
import argparse
from pathlib import Path
from html import escape
from seo_metadata import render_metadata
from web_fonts import format_static
from site_share import apply
import edition_versions as V
ROOT = Path(__file__).resolve().parents[1]

def outputs():
    files = {}
    facts = V.load()['editions']['en']
    for lang in ('en', 'ja'):
        ja = lang == 'ja'
        name = f'install-measure.{lang}.html'
        title = 'KUMIHAN｜Measure — ' + ('導入' if ja else 'Install')
        description = '利用するAIを選び、英語版のSkillとプラグインを導入します。' if ja else 'Choose your AI platform and install English Skills or a plugin.'
        suffix = '.ja' if ja else ''
        links = ''.join(f'<li><a href="docs/install-measure-{host}{suffix}.html">{label}</a></li>' for host, label in [('chatgpt','ChatGPT / Codex'),('claude','Claude / Claude Code'),('gemini','Gemini')])
        version = facts['published_version'] if facts['release_status'] == 'published' else facts['source_version']
        note = '実機の導入・Office/PDF描画は未確認です。' if ja else 'Native installation and Office/PDF rendering remain not checked.'
        alts = {k:f'install-measure.{k}.html' for k in ('en','ja')};alts['x-default']=alts['en']
        html = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="assets/hlela-site.css"><link rel="stylesheet" href="assets/measure-site.css">{render_metadata(title,description,lang,name,alts)}</head><body><a class="skip-link" href="#main">{'本文へ' if ja else 'Skip to content'}</a><header class="site-header"><div class="shell"><a class="brand" href="kumihan-en{suffix}.html">KUMIHAN｜Measure</a></div></header><main id="main" class="shell measure-intro" tabindex="-1"><h1>{'英語版を導入する' if ja else 'Install Measure.'}</h1><p>{description}</p><p>v{escape(version)}</p><section id="install"><ul>{links}</ul></section><p>{note}</p><p><a href="install-measure.{'en' if ja else 'ja'}.html" lang="{'en' if ja else 'ja'}">{'English' if ja else '日本語'}</a></p></main><footer class="shell">© L&amp;Co. LLC · Apache-2.0</footer></body></html>
'''
        files[name] = format_static(apply(html), name)
    return files

if __name__ == '__main__':
    p = argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    for name,content in outputs().items():
        path=ROOT/name
        if a.check:
            if not path.is_file() or path.read_text()!=content:raise SystemExit('Stale '+name)
        else:path.write_text(content)
    print('Measure installation entry points: 2 '+('verified' if a.check else 'built'))
