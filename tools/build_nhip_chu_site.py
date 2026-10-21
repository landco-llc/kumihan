#!/usr/bin/env python3
"""Build the KUMIHAN｜Nhịp Chữ site (vi / en / ja); --check verifies committed output.

Landings follow the canonical KUMIHAN index (_layouts/landing.html); install
guides come from tools/build_install_guides.py. Copy lives
in assets/nhip-chu-site-copy.json. Following kumihan-nhip-chu-web, Vietnamese
pages declare lang="vi"; supplied text is reproduced byte for byte and never
normalized. Japanese copy follows kumihan-web.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_adapter import seo_outputs
from version_display import version_outputs
import argparse
import json
from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://landco-llc.github.io/kumihan/"
LOGO = "assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"
REPO = "https://github.com/landco-llc/kumihan"
SOURCE = REPO + "/tree/main/plugins/kumihan-nhip-chu"
VERSION = "0.1.0"
RELEASE = REPO + f"/releases/tag/kumihan-vi-v{VERSION}"
BRAND = 'KUMIHAN<span class="brand-sub">｜Nhịp Chữ</span>'
LANGS = {"vi": "", "en": ".en", "ja": ".ja"}
LABELS = {"vi": "VI", "en": "EN", "ja": "日本語"}
OG = {"vi": "vi_VN", "en": "en_US", "ja": "ja_JP"}
SKILLS = ("kumihan-nhip-chu", "kumihan-nhip-chu-web", "kumihan-nhip-chu-documents", "kumihan-nhip-chu-review")
SKILL_TYPES = ("01 / ENTRY", "02 / WEB", "03 / DOCUMENTS", "04 / REVIEW")
SKILL_SYMBOLS = ("Ắ", "↗", "¶", "◎")
HOSTS = {"chatgpt": "ChatGPT / Codex", "claude": "Claude / Claude Code", "gemini": "Gemini"}
GATEWAY = {"vi": "top-vi.html", "en": "index.html", "ja": "top-ja.html"}


OVERRIDES = r"""
    :root { --display: "Be Vietnam Pro", "Noto Sans", system-ui, -apple-system, Arial, sans-serif; }
    /* KUMIHAN｜Nhịp Chữ (kumihan-nhip-chu-web): lang="vi" with dictionary hyphenation
       for running text only; headings, names and URLs are never hyphenated. */
    html[lang="vi"] body { line-break: auto; }
    html[lang="vi"] :is(.hero-desc, .intro-text p, .feature p, .idea-band p, .skill-desc, .install-intro p, .status-box p, .cta-layout p) { hyphens: manual; }
    html[lang="vi"] :is(h1, h2, h3, .brand, .skill-name, .platform-name, a) { hyphens: manual; }
    html:is([lang="vi"], [lang="en"]) .hero h1 { font-size: clamp(42px,4.9vw,72px); letter-spacing: -.05em; line-height: 1.12; text-wrap: balance; }
    html:is([lang="vi"], [lang="en"]) :is(.intro-text h2, .section-heading h2, .idea-band h2, .install-intro h2, .cta-layout h2) { letter-spacing: -.045em; line-height: 1.25; }
    html:is([lang="vi"], [lang="en"]) :is(h1, h2, h3, .eyebrow, .button, .feature p) { overflow-wrap: break-word; }
    html[lang="ja"] body { line-break: strict; }
    @supports (word-break: auto-phrase) {
      html[lang="ja"] :is(h2, h3) { word-break: auto-phrase; }
    }
    .brand .brand-sub { margin-inline-start: 2px; font-weight: 700; letter-spacing: -.02em; }
    .language-switch a { display: inline-flex; align-items: center; justify-content: center; min-height: 38px; min-width: 38px; border-radius: 40px; color: var(--muted); padding: 7px 10px; font-size: 11px; font-weight: 800; letter-spacing: .05em; }
    .language-switch a[aria-current="page"] { background: var(--ink); color: white; }
    .language-switch a:hover:not([aria-current="page"]) { color: var(--red-dark); background: #ebe7df; }
    .hero-stage::after { content: "KUMIHAN / VI"; }
    .hero-foot { flex-wrap: wrap; }
    .hero-cta .button { max-width: 100%; }
    .feature-motif { font-family: Georgia, "Times New Roman", serif !important; letter-spacing: 0 !important; font-weight: 400 !important; }
    .skill-symbol { font-family: Georgia, "Times New Roman", serif; letter-spacing: 0; }
    .status-meta { white-space: normal; }
    /* Enlarged text: header items, brand and the band heading wrap instead of widening the page. */
    .header-content { flex-wrap: wrap; row-gap: 10px; }
    .header-nav { flex-wrap: wrap; min-width: 0; row-gap: 8px; }
    .brand { min-width: 0; flex: 0 1 auto; }
    .brand > span { white-space: normal; overflow-wrap: anywhere; }
    .idea-layout > * { min-width: 0; }
    .card-top > * { min-width: 0; }
    .feature-index { overflow-wrap: anywhere; }
    .skill-type { overflow-wrap: anywhere; }
    .cta-layout > * { min-width: 0; }
    .cta-layout .button { flex: 0 1 auto; max-width: 100%; }
    .status-meta a { color: var(--red-dark); }
    .skill-card, .platform-info, .status-box > *, .hero-copy, .hero-stage, .feature, .install-layout > * { min-width: 0; }
    @media (max-width: 560px) {
      html:is([lang="vi"], [lang="en"]) .hero h1 { font-size: clamp(34px,9.6vw,46px); line-height: 1.16; }
      .header-nav { flex-wrap: wrap; overflow: visible; gap: 12px 18px; }
      .header-nav a { white-space: normal; }
      .idea-layout { grid-template-columns: minmax(0,1fr); }
    }

/* Applied after KUMIHAN｜Nhịp Chữ skill source: VI-01/04/08/13/14/15/25/31.
 * Real font collision verification remains separate from CSS policy. */
html[lang="vi"] body { font-family: "Be Vietnam Pro","Noto Sans",system-ui,Arial,sans-serif; }
html[lang="vi"] :is(h1,h2,h3,.brand,.feature h3,.skill-name) { word-break: normal; hyphens: manual; letter-spacing: -.025em; }
html[lang="vi"] .hero h1 { letter-spacing: -.036em; line-height: 1.31; }
html[lang="vi"] :is(.hero-desc,.intro-text p,.feature p,.skill-desc,.install-intro p) { word-break: normal; hyphens: manual; }
html[lang="vi"] .feature-motif { letter-spacing: 0; line-height: 1.55; }
html[lang="vi"] a[href^="https://"] { overflow-wrap: anywhere; }
@media(max-width:560px) { html[lang="vi"] .hero h1 { font-size: clamp(35px,9vw,46px); line-height:1.4; } }
"""


_ps_spec = spec_from_file_location("kumihan_product_site", Path(__file__).with_name("product_site.py"))
SITE = module_from_spec(_ps_spec)
_ps_spec.loader.exec_module(SITE)
x = SITE.x


def landing_path(lang):
    return f"kumihan-vi{LANGS[lang]}.html"


def guide_path(host, lang):
    return f"docs/install-nhip-chu-{host}{LANGS[lang]}.html"


def landing(lang, c):
    page = landing_path(lang)
    alternates = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{landing_path(k)}">' for k in LANGS)
    head = (f"<title>{x(c['title'])}</title>\n<meta name=\"description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:type" content="website">\n<meta property="og:locale" content="{OG[lang]}">\n'
            f"<meta property=\"og:title\" content=\"{x(c['title'])}\">\n<meta property=\"og:description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:url" content="{BASE}{page}">\n<meta property="og:image" content="{BASE}{LOGO}">\n'
            f'<link rel="canonical" href="{BASE}{page}">\n{alternates}\n'
            f'<link rel="alternate" hreflang="x-default" href="{BASE}{landing_path("vi")}">\n'
            f'<link rel="icon" href="assets/favicon-32x32.png" type="image/png">\n<link rel="stylesheet" href="assets/nhip-chu-site.css">')
    return SITE.landing(dict(
        lang=lang, head=head, brand=f"<span>{BRAND}</span>", home_label="KUMIHAN｜Nhịp Chữ",
        languages=[(k, LABELS[k], landing_path(k), k == lang) for k in LANGS],
        logo=LOGO, repo=REPO, release=RELEASE, license=REPO + "/blob/main/LICENSE",
        skills=[(name, f"{SOURCE}/skills/{name}", SKILL_SYMBOLS[i]) for i, name in enumerate(SKILLS)],
        hosts=[(name, guide_path(host, lang)) for host, name in HOSTS.items()],
        gateway=(GATEWAY[lang], c["gateway_label"])), c)


@version_outputs
@seo_outputs
def outputs():
    copy = json.loads((ROOT / "assets" / "nhip-chu-site-copy.json").read_text(encoding="utf-8"))
    files = {landing_path(lang): landing(lang, copy[lang]) for lang in LANGS}
    files["assets/nhip-chu-site.css"] = SITE.canonical_css("KUMIHAN｜Nhịp Chữ index: canonical KUMIHAN index CSS + Nhịp Chữ settings.", OVERRIDES)
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for name, content in outputs().items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale Nhịp Chữ site files: " + ", ".join(stale))
    print(f"Nhịp Chữ site: {len(outputs())} files " + ("verified" if args.check else "built"))


if __name__ == "__main__":
    main()
