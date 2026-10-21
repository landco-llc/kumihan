#!/usr/bin/env python3
"""Hindi site: canonical product_site, editable hi-site-copy, master JA/EN parity.

Install guides come from tools/build_install_guides.py.
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
SOURCE = REPO + "/tree/main/plugins/kumihan-hi"
VERSION = "0.1.0"
RELEASE = REPO + f"/releases/tag/kumihan-hi-v{VERSION}"
BRAND = 'KUMIHAN<span class="brand-sub">｜अक्षर-संगति</span>'
LANGS = {"hi": "", "en": ".en", "ja": ".ja"}
LABELS = {"hi": "हिन्दी", "en": "EN", "ja": "日本語"}
OG = {"hi": "hi_IN", "en": "en_US", "ja": "ja_JP"}
SKILLS = ("kumihan-hi", "kumihan-hi-web", "kumihan-hi-documents", "kumihan-hi-review")
SKILL_TYPES = ("01 / ENTRY", "02 / WEB", "03 / DOCUMENTS", "04 / REVIEW")
SKILL_SYMBOLS = ("«»", "↗", "¶", "◎")
HOSTS = {"chatgpt": "ChatGPT / Codex", "claude": "Claude / Claude Code", "gemini": "Gemini"}
GATEWAY = {"hi": "top-hi.html", "en": "index.html", "ja": "top-ja.html"}


OVERRIDES = r"""
@font-face { font-family: "Kumihan Devanagari"; src: url("fonts/NotoSansDevanagari.ttf") format("truetype"); font-weight: 100 900; font-style: normal; font-display: swap; }
body { font-family: "Kumihan Devanagari", "Noto Sans Devanagari", "Noto Sans JP", sans-serif; }
:lang(hi), .brand, .brand-sub, .footer-mark { letter-spacing: normal !important; word-break: normal; overflow-wrap: normal; line-height: 1.65; }
html[lang="hi"] :is(h1,h2,h3) { letter-spacing: normal; line-height: 1.5; }
html[lang="hi"] .hero h1 { font-size: clamp(32px,4.4vw,64px); }
.brand .brand-sub { display: inline-block; font-weight: 700; }
.brand { min-width: 0; max-width: 100%; white-space: normal; }
.header-content, .header-nav { flex-wrap: wrap; row-gap: 12px; }
.hero-foot { flex-wrap: wrap; }
.hero-stage::after { content: "KUMIHAN / HI"; }
.hero-copy, .hero-stage, .feature, .skill-card, .platform-info, .install-layout > *, .idea-layout > *, .cta-layout > * { min-width: 0; }
.skill-name, .skill-name bdi { overflow-wrap: anywhere !important; }
.feature-motif { font-family: "Kumihan Devanagari", "Noto Sans Devanagari", sans-serif !important; line-height: 1.8; height: auto; min-height: 80px; padding-block: .2em; letter-spacing: normal !important; }
.language-switch a { display: inline-flex; min-height: 38px; padding: 7px 10px; }
.language-switch a[aria-current="page"] { background: var(--ink); color: white; border-radius: 30px; }
.status-meta { white-space: normal; }
.status-meta a { color: var(--red-dark); }
html[lang="ja"] body { line-break: strict; }
html[lang="en"] .hero h1 { font-size: clamp(34px,4.4vw,64px); line-height: 1.25; }
@media(max-width:560px) { .header-nav { gap: 12px; } .header-nav a { white-space: normal; } .idea-layout { grid-template-columns: minmax(0,1fr); } .brand { font-size: 20px; } .hero h1 { font-size: 34px; } }
"""


_ps_spec = spec_from_file_location("kumihan_product_site", Path(__file__).with_name("product_site.py"))
SITE = module_from_spec(_ps_spec)
_ps_spec.loader.exec_module(SITE)
x = SITE.x


def landing_path(lang):
    return f"kumihan-hi{LANGS[lang]}.html"


def guide_path(host, lang):
    return f"docs/install-kumihan-hi-{host}{LANGS[lang]}.html"


def landing(lang, c):
    page = landing_path(lang)
    alternates = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{landing_path(k)}">' for k in LANGS)
    head = (f"<title>{x(c['title'])}</title>\n<meta name=\"description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:type" content="website">\n<meta property="og:locale" content="{OG[lang]}">\n'
            f"<meta property=\"og:title\" content=\"{x(c['title'])}\">\n<meta property=\"og:description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:url" content="{BASE}{page}">\n<meta property="og:image" content="{BASE}{LOGO}">\n'
            f'<link rel="canonical" href="{BASE}{page}">\n{alternates}\n'
            f'<link rel="alternate" hreflang="x-default" href="{BASE}{landing_path("hi")}">\n'
            f'<link rel="icon" href="assets/favicon-32x32.png" type="image/png">\n<link rel="stylesheet" href="assets/hi-site.css">')
    return SITE.landing(dict(
        lang=lang, dir="ltr", head=head, brand=f"<span>{BRAND}</span>", home_label="KUMIHAN｜अक्षर-संगति",
        languages=[(k, LABELS[k], landing_path(k), k == lang) for k in LANGS],
        logo=LOGO, repo=REPO, release=RELEASE, license=REPO + "/blob/main/LICENSE",
        skills=[(name, f"{SOURCE}/skills/{name}", SKILL_SYMBOLS[i]) for i, name in enumerate(SKILLS)],
        hosts=[(name, guide_path(host, lang)) for host, name in HOSTS.items()],
        gateway=(GATEWAY[lang], c["gateway_label"]), family=c["family"]), c)


@version_outputs
@seo_outputs
def outputs():
    copy = json.loads((ROOT / "assets" / "hi-site-copy.json").read_text(encoding="utf-8"))
    files = {landing_path(lang): landing(lang, copy[lang]) for lang in LANGS}
    files["assets/hi-site.css"] = SITE.canonical_css("KUMIHAN｜अक्षर-संगति index: canonical KUMIHAN index CSS + अक्षर-संगति settings.", OVERRIDES)
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
        raise SystemExit("Stale अक्षर-संगति site files: " + ", ".join(stale))
    print(f"अक्षर-संगति site: {len(outputs())} files " + ("verified" if args.check else "built"))


if __name__ == "__main__":
    main()
