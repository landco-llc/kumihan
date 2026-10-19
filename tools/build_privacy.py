#!/usr/bin/env python3
"""Build the KUMIHAN privacy policy, one page in every language (privacy.html); --check verifies.

The text lives in assets/privacy-copy.json: Japanese and English are
authoritative (Japanese prevails), the others are reference translations.
Each language is a section with its own lang (and dir) and an id equal to
its gateway key, so footers link to privacy.html#<key>. The page uses the
install-guide design (assets/kumihan-install.css) with the shared footer,
fonts and link previews. privacy-ja.html, the first address of the Japanese
text, forwards to privacy.html#ja.
"""
import argparse
from seo_adapter import seo_outputs
import json
import re
from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://landco-llc.github.io/kumihan/"
REPO = "https://github.com/landco-llc/kumihan"
LOGO = "KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"
PAGE = "privacy.html"
REDIRECTS = {"privacy-ja.html": PAGE + "#ja"}
LINKS = {"GH": "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement",
         "GHJA": "https://docs.github.com/ja/site-policy/privacy-policies/github-general-privacy-statement",
         "LANDCO": "https://landco.co.jp/"}

_wf_spec = spec_from_file_location("kumihan_web_fonts", Path(__file__).with_name("web_fonts.py"))
WEB_FONTS = module_from_spec(_wf_spec)
_wf_spec.loader.exec_module(WEB_FONTS)


def x(value):
    return escape(str(value), quote=True)


def link(key, html):
    return f'<a href="{x(LINKS[key])}" target="_blank" rel="noopener noreferrer">{html}</a>'


def para(text, lang):
    """Escape a paragraph and turn {KEY|text} and {LANDCO} into links."""
    out = re.sub(r"\{(\w+)\|([^}]*)\}|\{LANDCO\}",
                 lambda m: link(m.group(1), m.group(2)) if m.group(1) else link("LANDCO", x(LINKS["LANDCO"])),
                 x(text))
    if lang == "pl":
        # Polish one-letter words stay with the next word (as on the Szyk pages).
        out = "".join(part if part.startswith("<") else re.sub(r"(?<!\w)([aiouwzAIOUWZ]) ", "\\1\u00a0", part)
                      for part in re.split(r"(<[^>]*>)", out))
    return out


def fonts(languages):
    """Shared fonts for the page plus each script's own Google Fonts family."""
    keys = []
    for l in languages:
        key = WEB_FONTS.script(l["lang"])
        if key != "latin" and key not in keys:
            keys.append(key)
    extra = "".join(f'<link rel="stylesheet" href="{WEB_FONTS.local_css(WEB_FONTS.own_url(k))}">' for k in keys)
    return WEB_FONTS.head("en") + extra


def section(l, ids):
    attrs = f' lang="{l["lang"]}"' + (f' dir="{l["dir"]}"' if l.get("dir") else "")
    notice = f'<blockquote><p>{x(l["notice"])}</p></blockquote>' if l.get("notice") else ""
    parts = "".join(
        f'<section id="{l["key"]}-{sid}"><h3>{i:02d} / {x(h)}</h3>' + "".join(f"<p>{para(p, l['key'])}</p>" for p in ps)
        + "</section>"
        for i, (sid, (h, ps)) in enumerate(zip(ids, l["sections"]), 1))
    return (f'<section id="{l["key"]}" class="privacy-language"{attrs}>'
            f'<h2><span lang="en" dir="ltr">{l["key"].upper()}</span> / {x(l["title"])}</h2>{notice}{parts}</section>')


def page(copy):
    p, languages, ids = copy["page"], copy["languages"], copy["sections"]
    # English and Japanese (the authoritative texts) stay listed; the others are in a menu.
    pinned = [l for l in languages if l["key"] in ("en", "ja")]
    toc = "".join(f'<li><a href="#{l["key"]}" lang="{l["lang"]}" hreflang="{l["lang"]}">{x(l["name"])}</a></li>'
                  for l in pinned)
    menu = "".join(f'<li><a href="#{l["key"]}" hreflang="{l["lang"]}"><span class="code">{l["key"].upper()}</span>'
                   f' <span lang="{l["lang"]}">{x(l["name"])}</span></a></li>'
                   for l in languages if l not in pinned)
    body = "".join(section(l, ids) for l in languages)
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#f5f3ee">
<title>{x(p['page_title'])}</title>
<meta name="description" content="{x(p['description'])}">
<link rel="canonical" href="{BASE}{PAGE}">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">
<link rel="stylesheet" href="assets/kumihan-install.css">
<style>
.privacy-language + .privacy-language {{ margin-top: 92px; }} .privacy-language > h2 {{ margin-top: 0; }}
.lang-pick {{ position: relative; margin-top: 18px; }}
.lang-pick summary {{ list-style: none; display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 42px; box-sizing: border-box; padding: 9px 16px; border: 1px solid var(--line); border-radius: 12px; background: #fffefa; color: var(--ink); cursor: pointer; font-size: 12px; font-weight: 700; }}
.lang-pick summary::-webkit-details-marker {{ display: none; }}
.lang-pick summary::after {{ content: ""; width: 6px; height: 6px; border-right: 2px solid currentColor; border-bottom: 2px solid currentColor; transform: translateY(-2px) rotate(45deg); transition: transform .15s ease; }}
.lang-pick[open] summary::after {{ transform: translateY(2px) rotate(225deg); }}
.lang-pick summary:focus-visible {{ outline: 3px solid var(--red); outline-offset: 3px; }}
.lang-pick:not([open]) ul {{ display: none; }}
.lang-pick ul {{ position: absolute; inset-inline: 0; top: calc(100% + 6px); z-index: 30; max-height: min(50vh, 360px); overflow-y: auto; overscroll-behavior: contain; margin: 0; padding: 6px 0; list-style: none; background: #fbf9f4; border: 1px solid #d8d2c6; border-radius: 12px; box-shadow: 0 18px 40px rgba(0,0,0,.14); }}
.lang-pick li a {{ display: block; margin: 0; padding: 8px 16px; border: 0; color: var(--ink-2); font-size: 13px; line-height: 1.5; text-decoration: none; }}
.lang-pick li a .code {{ display: inline-block; min-width: 4.6em; color: var(--muted); font: 800 11px/1.5 Arial, Helvetica, sans-serif; letter-spacing: .04em; }}
.lang-pick li a:hover, .lang-pick li a:focus-visible {{ background: #ede8de; color: var(--ink); }}
.page-jump {{ display: flex; gap: 10px; margin-top: 14px; }}
.page-jump a {{ display: inline-flex; align-items: center; justify-content: center; width: 42px; height: 42px; box-sizing: border-box; border: 1px solid var(--line); border-radius: 50%; background: #fffefa; color: var(--ink-2); font: 700 17px/1 Arial, Helvetica, sans-serif; text-decoration: none; }}
.page-jump a:hover, .page-jump a:focus-visible {{ border-color: var(--ink); color: var(--ink); }}
</style>
{fonts(languages)}
</head>
<body>
<a class="skip skip-link" href="#main">{x(p['skip'])}</a>
<header class="site-header">
  <div class="shell header-inner">
    <a class="brand" href="index.html">KUMIHAN</a>
    <nav class="header-nav" aria-label="{x(p['nav'])}"><a href="{REPO}" target="_blank" rel="noopener noreferrer">GitHub</a></nav>
  </div>
</header>
<section class="hero" aria-labelledby="page-title">
  <div class="shell">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">KUMIHAN</a><span aria-hidden="true">/</span><span>{x(p['breadcrumb'])}</span></nav>
    <div class="hero-grid">
      <div>
        <div class="eyebrow">LEGAL / PRIVACY</div>
        <h1 id="page-title">{x(p['title'])}</h1>
        <p class="hero-desc">{x(p['lead'])}<br><span lang="ja">{x(p['lead_ja'])}</span></p>
      </div>
      <div class="hero-logo"><img src="assets/{LOGO}" alt="KUMIHAN official logo" width="1254" height="1254"></div>
    </div>
  </div>
</section>
<div class="shell content-layout">
  <aside class="toc" aria-label="{x(p['languages'])}">
    <details class="toc-details" open>
      <summary>{x(p['languages'])}</summary>
      <h2 class="toc-title">{x(p['languages'])}</h2>
      <ol>{toc}</ol>
    </details>
    <details class="lang-pick"><summary>{x(p['other_languages'])}</summary><ul>{menu}</ul></details>
    <nav class="page-jump" aria-label="{x(p['jump'])}"><a href="#top" aria-label="{x(p['to_top'])}" title="{x(p['to_top'])}"><span aria-hidden="true">↑</span></a><a href="#page-bottom" aria-label="{x(p['to_bottom'])}" title="{x(p['to_bottom'])}"><span aria-hidden="true">↓</span></a></nav>
    <div class="toc-note"><strong>{x(p['note_title'])}</strong><p>{x(p['note'])}</p><p lang="ja">{x(p['note_ja'])}</p></div>
  </aside>
  <main class="guide" id="main" tabindex="-1">
    <div class="guide-head"><span>LEGAL / L&amp;Co. LLC</span><span class="step-label">{x(p['updated'])}</span></div>
    <div class="guide-pane">{body}</div>
  </main>
</div>
{WEB_FONTS.FOOTER.footer('en')}
<div id="page-bottom"></div>
<script>document.querySelectorAll(".lang-pick a").forEach(a => a.addEventListener("click", () => a.closest("details").removeAttribute("open")));</script>
</body>
</html>
"""
    return WEB_FONTS.SHARE.apply(out)


def redirect(target):
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8"/>
<title>KUMIHAN</title>
<meta content="noindex" name="robots"/>
<link href="{BASE}{target}" rel="canonical"/>
<meta content="0; url={target}" http-equiv="refresh"/>
</head>
<body><p><a href="{target}">KUMIHAN</a></p></body>
</html>
"""


@seo_outputs
def outputs():
    copy = json.loads((ROOT / "assets" / "privacy-copy.json").read_text(encoding="utf-8"))
    return {PAGE: page(copy), **{old: redirect(new) for old, new in REDIRECTS.items()}}


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
