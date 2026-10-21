#!/usr/bin/env python3
"""Build the KUMIHAN｜Szyk site (pl / en / ja); --check verifies committed output.

Landings follow the canonical KUMIHAN index (_layouts/landing.html); install
guides come from tools/build_install_guides.py. Copy lives
in assets/szyk-site-copy.json; its ja/en copy is the shared KUMIHAN copy
(tools/base_copy.py). Following kumihan-szyk-web, Polish pages declare
lang="pl", emit only pl/en/ja alternates, never hide overflow, and do not rely
on hyphens:auto or break-all. The site's own Polish copy keeps one-letter words
(a, i, o, u, w, z) off line ends with a no-break space, added at render time so
assets/szyk-site-copy.json stays as written. Japanese copy follows kumihan-web.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_adapter import seo_outputs
from version_display import version_outputs
import argparse
import json
import re
from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://landco-llc.github.io/kumihan/"
LOGO = "assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"
REPO = "https://github.com/landco-llc/kumihan"
SOURCE = REPO + "/tree/main/plugins/kumihan-szyk"
VERSION = "0.1.0"
RELEASE = REPO + f"/releases/tag/kumihan-szyk-v{VERSION}"
BRAND = 'KUMIHAN<span class="brand-sub">｜Szyk</span>'
LANGS = {"pl": "", "en": ".en", "ja": ".ja"}
LABELS = {"pl": "PL", "en": "EN", "ja": "日本語"}
OG = {"pl": "pl_PL", "en": "en_US", "ja": "ja_JP"}
SKILLS = ("kumihan-szyk", "kumihan-szyk-web", "kumihan-szyk-documents", "kumihan-szyk-review")
SKILL_TYPES = ("01 / ENTRY", "02 / WEB", "03 / DOCUMENTS", "04 / REVIEW")
SKILL_SYMBOLS = ("Łż", "↗", "¶", "◎")
HOSTS = {"chatgpt": "ChatGPT / Codex", "claude": "Claude / Claude Code", "gemini": "Gemini"}
# KUMIHAN index (language gateway) for each page language.
GATEWAY = {"pl": "top-pl.html", "en": "index.html", "ja": "top-ja.html"}


OVERRIDES = r"""
    /* KUMIHAN｜Szyk (kumihan-szyk-web): lang="pl"; no break-all, no reliance on
       hyphens:auto, no hidden overflow. Long words wrap only where they must. */
    html[lang="pl"] body { line-break: auto; }
    html:is([lang="pl"], [lang="en"]) .hero h1 { font-size: clamp(42px,4.9vw,72px); letter-spacing: -.05em; line-height: 1.12; text-wrap: balance; }
    html:is([lang="pl"], [lang="en"]) :is(.intro-text h2, .section-heading h2, .idea-band h2, .install-intro h2, .cta-layout h2) { letter-spacing: -.045em; line-height: 1.25; }
    html:is([lang="pl"], [lang="en"]) :is(h1, h2, h3, .eyebrow, .button, .feature p) { overflow-wrap: break-word; }
    html[lang="ja"] body { line-break: strict; }
    @supports (word-break: auto-phrase) {
      html[lang="ja"] :is(h2, h3) { word-break: auto-phrase; }
    }
    .brand .brand-sub { margin-inline-start: 2px; font-weight: 700; letter-spacing: -.02em; }
    .language-switch a { display: inline-flex; align-items: center; justify-content: center; min-height: 38px; min-width: 38px; border-radius: 40px; color: var(--muted); padding: 7px 10px; font-size: 11px; font-weight: 800; letter-spacing: .05em; }
    .language-switch a[aria-current="page"] { background: var(--ink); color: white; }
    .language-switch a:hover:not([aria-current="page"]) { color: var(--red-dark); background: #ebe7df; }
    .hero-stage::after { content: "KUMIHAN / PL"; }
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
      html:is([lang="pl"], [lang="en"]) .hero h1 { font-size: clamp(34px,9.6vw,46px); line-height: 1.16; }
      .header-nav { flex-wrap: wrap; overflow: visible; gap: 12px 18px; }
      .header-nav a { white-space: normal; }
      .idea-layout { grid-template-columns: minmax(0,1fr); }
    }
"""


_ps_spec = spec_from_file_location("kumihan_product_site", Path(__file__).with_name("product_site.py"))
SITE = module_from_spec(_ps_spec)
_ps_spec.loader.exec_module(SITE)
x = SITE.x


def landing_path(lang):
    return f"kumihan-pl{LANGS[lang]}.html"


def guide_path(host, lang):
    return f"docs/install-szyk-{host}{LANGS[lang]}.html"


def landing(lang, c):
    page = landing_path(lang)
    alternates = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{landing_path(k)}">' for k in LANGS)
    head = (f"<title>{x(c['title'])}</title>\n<meta name=\"description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:type" content="website">\n<meta property="og:locale" content="{OG[lang]}">\n'
            f"<meta property=\"og:title\" content=\"{x(c['title'])}\">\n<meta property=\"og:description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:url" content="{BASE}{page}">\n<meta property="og:image" content="{BASE}{LOGO}">\n'
            f'<link rel="canonical" href="{BASE}{page}">\n{alternates}\n'
            f'<link rel="alternate" hreflang="x-default" href="{BASE}{landing_path("pl")}">\n'
            f'<link rel="icon" href="assets/favicon-32x32.png" type="image/png">\n<link rel="stylesheet" href="assets/szyk-site.css">')
    return SITE.landing(dict(
        lang=lang, head=head, brand=f"<span>{BRAND}</span>", home_label="KUMIHAN｜Szyk",
        languages=[(k, LABELS[k], landing_path(k), k == lang) for k in LANGS],
        logo=LOGO, repo=REPO, release=RELEASE, license=REPO + "/blob/main/LICENSE",
        skills=[(name, f"{SOURCE}/skills/{name}", SKILL_SYMBOLS[i]) for i, name in enumerate(SKILLS)],
        hosts=[(name, guide_path(host, lang)) for host, name in HOSTS.items()],
        gateway=(GATEWAY[lang], c["gateway_label"]), family=c["family"]), c)


# A one-letter Polish word (a, i, o, u, w, z) and the space after it; not inside a word,
# an option flag or a path.
ONE_LETTER = re.compile(r"(?<![\w/=-])([AaIiOoUuWwZz]) (?=\S)")


def bind_one_letter_words(value):
    """Keep one-letter Polish words with the next word (U+00A0), in every string of the copy."""
    if isinstance(value, str):
        return ONE_LETTER.sub("\\1\u00a0", value)
    if isinstance(value, list):
        return [bind_one_letter_words(v) for v in value]
    if isinstance(value, dict):
        return {k: bind_one_letter_words(v) for k, v in value.items()}
    return value


@version_outputs
@seo_outputs
def outputs():
    """The landings (guides: tools/build_install_guides.py)."""
    copy = json.loads((ROOT / "assets" / "szyk-site-copy.json").read_text(encoding="utf-8"))
    copy["pl"] = bind_one_letter_words(copy["pl"])
    files = {landing_path(lang): landing(lang, copy[lang]) for lang in LANGS}
    return files


def all_outputs():
    files = outputs()
    files["assets/szyk-site.css"] = SITE.canonical_css("KUMIHAN｜Szyk index: canonical KUMIHAN index CSS + Szyk settings.", OVERRIDES).replace("  \n", "\n")
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for name, content in all_outputs().items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale Szyk site files: " + ", ".join(stale))
    print(f"Szyk site: {len(all_outputs())} files " + ("verified" if args.check else "built"))


if __name__ == "__main__":
    main()
