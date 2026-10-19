#!/usr/bin/env python3
"""Build the KUMIHAN privacy policy (privacy.html in English, privacy-ja.html); --check verifies.

The text lives in assets/privacy-copy.json. The page uses the install-guide
design (assets/kumihan-install.css: header, hero, table of contents, text
pane) and the shared footer, fonts and link-preview tags. Japanese and English
are the only texts; the footer of every other language links to English.
"""
from seo_adapter import seo_outputs
import argparse
import json
from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://landco-llc.github.io/kumihan/"
REPO = "https://github.com/landco-llc/kumihan"
LOGO = "KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"
LABELS = {"en": "English", "ja": "日本語"}

_wf_spec = spec_from_file_location("kumihan_web_fonts", Path(__file__).with_name("web_fonts.py"))
WEB_FONTS = module_from_spec(_wf_spec)
_wf_spec.loader.exec_module(WEB_FONTS)
_gw_spec = spec_from_file_location("kumihan_build_gateways", Path(__file__).with_name("build_gateways.py"))
GATEWAYS = module_from_spec(_gw_spec)
_gw_spec.loader.exec_module(GATEWAYS)


def x(value):
    return escape(str(value), quote=True)


def page(lang, c, copy):
    home = GATEWAYS.GATEWAYS[lang][0]
    alternates = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{copy[k]["file"]}">' for k in copy)
    alternates += f'<link rel="alternate" hreflang="x-default" href="{BASE}{copy["en"]["file"]}">'
    langs = "".join(
        f'<a href="{x(copy[k]["file"])}" lang="{k}" hreflang="{k}" data-language'
        + (' aria-current="page"' if k == lang else "") + f'>{LABELS[k]}</a>' for k in copy)
    toc = "".join(f'<li><a href="#{s["id"]}">{x(s["h2"])}</a></li>' for s in c["sections"])
    body = "".join(
        f'<section id="{s["id"]}"><h2>{i:02d} / {x(s["h2"])}</h2>' + "".join(f"<p>{p.replace('&', '&amp;')}</p>" for p in s["body"]) + "</section>"
        for i, s in enumerate(c["sections"], 1))
    out = f"""<!doctype html>
<html lang="{c['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#f5f3ee">
<title>{x(c['page_title'])}</title>
<meta name="description" content="{x(c['description'])}">
<link rel="canonical" href="{BASE}{c['file']}">
{alternates}
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">
<link rel="stylesheet" href="assets/kumihan-install.css">
{WEB_FONTS.head(c['html_lang'])}
</head>
<body>
<a class="skip skip-link" href="#main">{x(c['skip'])}</a>
<header class="site-header">
  <div class="shell header-inner">
    <a class="brand" href="{home}">KUMIHAN</a>
    <nav class="header-nav" aria-label="{x(c['nav'])}"><a href="{REPO}" target="_blank" rel="noopener noreferrer">GitHub</a></nav>
  </div>
</header>
<section class="hero" aria-labelledby="page-title">
  <div class="shell">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{home}">KUMIHAN</a><span aria-hidden="true">/</span><span>{x(c['breadcrumb'])}</span></nav>
    <div class="hero-grid">
      <div>
        <div class="eyebrow">{x(c['head_label'])} / PRIVACY</div>
        <h1 id="page-title">{x(c['title'])}</h1>
        <p class="hero-desc">{x(c['lead'])}</p>
        <nav class="language-switch" aria-label="{x(c['language'])}">{langs}</nav>
      </div>
      <div class="hero-logo"><img src="assets/{LOGO}" alt="KUMIHAN official logo" width="1254" height="1254"></div>
    </div>
  </div>
</section>
<div class="shell content-layout">
  <aside class="toc" aria-label="{x(c['toc_title'])}">
    <details class="toc-details" open>
      <summary>{x(c['toc_summary'])}</summary>
      <h2 class="toc-title">{x(c['toc_title'])}</h2>
      <ol>{toc}</ol>
    </details>
    <div class="toc-note"><strong>{x(c['note_title'])}</strong><p>{x(c['note'])}</p></div>
  </aside>
  <main class="guide" id="main" tabindex="-1">
    <div class="guide-head"><span>{x(c['head_label'])} / L&amp;Co. LLC</span><span class="step-label">{x(c['updated'])}</span></div>
    <div class="guide-pane">{body}</div>
  </main>
</div>
{WEB_FONTS.FOOTER.footer(c['html_lang'])}
</body>
</html>
"""
    return WEB_FONTS.SHARE.apply(out)


@seo_outputs
def outputs():
    copy = json.loads((ROOT / "assets" / "privacy-copy.json").read_text(encoding="utf-8"))
    return {c["file"]: page(lang, c, copy) for lang, c in copy.items()}


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
        raise SystemExit("Stale privacy pages: " + ", ".join(stale))
    print("Privacy pages: " + ("verified" if args.check else "built"))


if __name__ == "__main__":
    main()
