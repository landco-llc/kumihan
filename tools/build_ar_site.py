#!/usr/bin/env python3
"""Generate the three localized Arabic landings; install guides come from build_install_guides.py."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_adapter import seo_outputs
from version_display import version_outputs
import argparse
from html import escape as e
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='/kumihan/'
# KUMIHAN index (language gateway) for each page language.
GATEWAY={'ar':'top-ar.html','en':'index.html','ja':'top-ja.html'}
PUBLIC='https://landco-llc.github.io'+BASE
REPO='https://github.com/landco-llc/kumihan'
HOSTS={'chatgpt':'ChatGPT / Codex','claude':'Claude','gemini':'Gemini'}
ROLES=['kumihan-ar','kumihan-ar-web','kumihan-ar-documents','kumihan-ar-review']

def path(lang,host=None):
    suffix='' if lang=='ar' else '.'+lang
    return ('docs/install-kumihan-ar-'+host if host else 'kumihan-ar')+suffix+'.html'
def brand():return '<bdi dir="ltr">KUMIHAN｜نضيد</bdi>'
# Landing copy follows the KUMIHAN index (kumihan.html) with Arabic-specific
# content kept (direction, mixed scripts, diacritics, Tatweel); see
# assets/ar-site-copy.json. Install-guide steps above stay product-specific.
import json
from importlib.util import module_from_spec, spec_from_file_location
def _load(name,file):
    spec=spec_from_file_location(name,Path(__file__).with_name(file));mod=module_from_spec(spec);spec.loader.exec_module(mod);return mod
SITE=_load('kumihan_product_site','product_site.py')
SITE_COPY=json.loads((ROOT/'assets/ar-site-copy.json').read_text(encoding='utf-8'))
LOGO='assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png'
LABELS=[('ar','العربية'),('en','English'),('ja','日本語')]
SYMBOLS=('ع','↗','¶','◎')
# kumihan-ar-web: semantic direction first; the canonical index CSS uses physical
# edges, so they are mirrored for dir="rtl". No letter-spacing on Arabic (it
# breaks cursive joining); fallback stacks only make Arabic glyphs available.
OVERRIDES=r"""
    html[lang="ar"] body { font-family: "Noto Naskh Arabic", "Noto Sans Arabic", "Geeza Pro", "Segoe UI", Tahoma, system-ui, sans-serif; line-height: 1.9; }
    html[lang="ar"] :is(h1, h2, h3, p, .eyebrow, .brand, .footer-mark, .skill-desc, .button, .feature-index, .section-number) { letter-spacing: 0; text-transform: none; }
    html[lang="ar"] .hero h1 { font-size: clamp(40px,4.8vw,68px); line-height: 1.55; }
    html[lang="ar"] :is(.intro-text h2, .section-heading h2, .idea-band h2, .install-intro h2, .cta-layout h2) { line-height: 1.7; }
    html[lang="ja"] body { line-break: strict; }
    html:is([lang="en"]) .hero h1 { font-size: clamp(40px,4.6vw,66px); letter-spacing: -.05em; line-height: 1.12; text-wrap: balance; }
    html[lang="en"] :is(h1, h2, h3, .eyebrow, .button, .feature p) { overflow-wrap: break-word; }
    .brand { min-width: 0; flex: 0 1 auto; }
    .brand > bdi { white-space: normal; }
    .language-switch a { display: inline-flex; align-items: center; justify-content: center; min-height: 38px; min-width: 38px; border-radius: 40px; color: var(--muted); padding: 7px 10px; font-size: 11px; font-weight: 800; letter-spacing: .02em; }
    .language-switch a[aria-current="page"] { background: var(--ink); color: white; }
    .language-switch a:hover:not([aria-current="page"]) { color: var(--red-dark); background: #ebe7df; }
    .hero-stage::after { content: "KUMIHAN / AR"; }
    .hero-foot, .header-content, .header-nav { flex-wrap: wrap; }
    .header-nav { min-width: 0; row-gap: 8px; }
    .hero-cta .button, .cta-layout .button { max-width: 100%; }
    .feature-motif { letter-spacing: 0 !important; }
    .skill-name, .platform-name { direction: ltr; text-align: start; }
    .status-meta { white-space: normal; }
    .status-meta a { color: var(--red-dark); }
    .skill-card, .platform-info, .status-box > *, .hero-copy, .hero-stage, .feature, .install-layout > *, .idea-layout > *, .card-top > *, .cta-layout > * { min-width: 0; }
    .feature-index, .skill-type { overflow-wrap: anywhere; }
    bdi { unicode-bidi: isolate; }
    /* Latin index labels such as "01 / TYPE" keep their reading order in RTL. */
    html[dir="rtl"] :is(.feature-index, .skill-type, .platform-index, .status-title) { direction: ltr; unicode-bidi: isolate; text-align: right; }
    html[dir="rtl"] .footer-links a { unicode-bidi: isolate; }
    html[dir="rtl"] .footer-sub { unicode-bidi: plaintext; text-align: right; }
    /* Right-to-left: mirror the canonical physical edges. */
    html[dir="rtl"] .header-nav { margin-left: 0; margin-right: auto; }
    html[dir="rtl"] .header-controls { margin-left: 0; margin-right: 16px; }
    html[dir="rtl"] .eyebrow .line { margin-right: 0; margin-left: 9px; }
    html[dir="rtl"] .arrow { margin-left: 0; margin-right: 12px; }
    html[dir="rtl"] :is(.arrow, .platform-arrow, .skill-end > span:last-child) { display: inline-block; transform: scaleX(-1); }
    html[dir="rtl"] .feature { padding: 32px 0 36px 24px; }
    html[dir="rtl"] .feature:not(:first-child) { padding-left: 24px; padding-right: 25px; border-left: 0; border-right: 1px solid var(--line); }
    html[dir="rtl"] .platform-row { padding: 20px 4px 20px 12px; }
    html[dir="rtl"] .platform-row:hover { padding-left: 12px; padding-right: 15px; }
    html[dir="rtl"] .status-meta { text-align: left; }
    html[dir="rtl"] .hero-stage::after { right: auto; left: -18px; }
    html[dir="rtl"] .stage-label { left: auto; right: 27px; }
    @media (max-width: 1080px) {
      html[dir="rtl"] .header-controls { margin-right: 0; }
      html[dir="rtl"] .feature { padding-left: 18px; }
      html[dir="rtl"] .feature:not(:first-child) { padding-right: 18px; }
    }
    @media (max-width: 790px) {
      .hero-layout, .intro-layout, .install-layout { grid-template-columns: minmax(0,1fr); }
      html[dir="rtl"] .header-nav { margin: 0; }
      html[dir="rtl"] .header-controls { margin-right: auto; margin-left: 0; }
      html[dir="rtl"] .feature:nth-child(3) { border-right: 0; padding-right: 0; }
      html[dir="rtl"] .hero-stage::after { left: 10px; right: auto; }
    }
    @media (max-width: 560px) {
      html[lang="ar"] .hero h1 { font-size: clamp(32px,8.6vw,44px); line-height: 1.6; }
      html[lang="en"] .hero h1 { font-size: clamp(33px,8.5vw,45px); }
      .header-nav { overflow: visible; gap: 12px 18px; }
      .header-nav a { white-space: normal; }
      .idea-layout { grid-template-columns: minmax(0,1fr); }
      html[dir="rtl"] .feature:not(:first-child) { padding-right: 14px; }
      html[dir="rtl"] .feature:nth-child(3) { padding-right: 0; }
      html[dir="rtl"] .status-meta { text-align: right; }
      html[dir="rtl"] .stage-label { right: 15px; }
    }
    /* Narrow phones: one principle per row instead of splitting Arabic words. */
    @media (max-width: 420px) {
      html[lang="ar"] .feature-grid { grid-template-columns: minmax(0,1fr); }
      html[lang="ar"] .feature, html[lang="ar"] .feature:not(:first-child), html[lang="ar"] .feature:nth-child(3) { padding: 22px 0; min-height: 0; border-right: 0; border-left: 0; border-bottom: 1px solid var(--line); }
      html[lang="ar"] .feature:last-child { border-bottom: 0; }
    }
"""
def head_links(lang,host=None):
    name=path(lang,host)
    alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{PUBLIC+path(l,host)}">' for l,_ in LABELS)
    return f'<link rel="canonical" href="{PUBLIC+name}">{alternates}<link rel="alternate" hreflang="x-default" href="{PUBLIC+path("ar",host)}">\n<link rel="icon" href="{BASE}favicon.ico">'
def landing(lang):
    c=dict(SITE_COPY[lang]);c['skills']=[[r,d] for r,(_,d) in zip(ROLES,c['skills'])]
    head=(f"<title>{e(c['title'])}</title>\n<meta name=\"description\" content=\"{e(c['description'],quote=True)}\">\n"
          f'<meta property="og:type" content="website"><meta property="og:title" content="{e(c["title"],quote=True)}"><meta property="og:url" content="{PUBLIC+path(lang)}"><meta property="og:image" content="{PUBLIC+LOGO}">\n'
          +head_links(lang)+f'\n<link rel="stylesheet" href="{BASE}assets/kumihan-ar.css">')
    return SITE.landing(dict(
        lang=lang,dir='rtl' if lang=='ar' else 'ltr',head=head,brand=brand(),home_label='KUMIHAN｜نضيد',
        languages=[(l,label,BASE+path(l),l==lang) for l,label in LABELS],
        logo=BASE+LOGO,repo=REPO,release=REPO+'/releases/tag/kumihan-ar-v0.1.0',license=REPO+'/blob/main/LICENSE',
        skills=[(r,REPO+'/tree/main/plugins/kumihan-ar/skills/'+r,SYMBOLS[i]) for i,r in enumerate(ROLES)],
        hosts=[('Claude / Claude Code' if h=='claude' else t,BASE+path(lang,h)) for h,t in HOSTS.items()],
        gateway=(BASE+GATEWAY[lang],c['gateway_label']),family=(c['family'][0],BASE+c['family'][1])),c)
@version_outputs
@seo_outputs
def outputs():
    out={path(l):landing(l) for l,_ in LABELS}
    out['assets/kumihan-ar.css']=SITE.canonical_css('KUMIHAN｜نضيد index: canonical KUMIHAN index CSS + Arabic RTL settings.',OVERRIDES)
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();out=outputs()
    changed=[n for n,s in out.items() if not (ROOT/n).exists() or (ROOT/n).read_text()!=s]
    if a.check:
        for n in changed:print('out of date: '+n)
        return int(bool(changed))
    for n in changed:(ROOT/n).write_text(out[n])
    print('Generated 3 Arabic landings and kumihan-ar.css');return 0
if __name__=='__main__':raise SystemExit(main())
