"""Canonical KUMIHAN install-guide frame shared by the product sites.

Mirrors the structure of _layouts/installation.html (header with host links,
hero with breadcrumb, eyebrow, title, language switch and logo, platform tabs,
table of contents, guide pane, footer) as static HTML with no runtime
translation. Styling lives in assets/kumihan-install.css.
"""

from dataclasses import dataclass, field
from html import escape

LOGO = "KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"

# Language gateway (the KUMIHAN index) for each page language, with the label
# used for the "back to index" link. Paths are relative to the site root.
GATEWAYS = {
    "ja": ("index.html", "KUMIHAN トップ"),
    "en": ("top-en.html", "KUMIHAN home"),
    "zh-Hant-TW": ("top-zh-han.html", "KUMIHAN 首頁"),
    "zh-Hans-CN": ("top-zh-cn.html", "KUMIHAN 首页"),
    "ko-KR": ("top-ko.html", "KUMIHAN 홈"),
    "th": ("top-th.html", "หน้าแรก KUMIHAN"),
}


def e(value: str) -> str:
    return escape(str(value), quote=True)


@dataclass
class Frame:
    lang: str
    head: str                 # <meta>/<link>/<title> lines placed in <head>
    css: str                  # href of assets/kumihan-install.css
    asset_root: str           # prefix for assets/ (e.g. "../" or "/kumihan/")
    brand: str                # brand HTML, e.g. 'KUMIHAN<span class="brand-sub">｜字律</span>'
    home: str                 # product landing href
    hosts: list               # [(label, href, current: bool)], three entries
    languages: list           # [(code, label, href, current: bool)]
    number: str               # "01" .. "03"
    title: str                # h1 text (escaped by caller)
    description: str          # hero description (escaped by caller)
    toc: list                 # [(id, label)]
    content: str              # guide-pane HTML
    platform: str             # name shown in the guide head
    ui: dict                  # see UI keys below
    footer_sub: str = ""      # footer text HTML
    footer_links: list = field(default_factory=list)  # [(label, href, external)]
    scripts: str = ""
    language_class: str = ""  # extra class for the language switch nav
    gateway: tuple = ()       # (href, label) of the language-matched KUMIHAN index
    dir: str = ""             # "rtl" for right-to-left page languages

# UI keys: skip, nav, language, breadcrumb, toc_title, toc_summary,
# platforms, note_title, note, source, source_href, steps, top


def render(f: Frame) -> str:
    u = f.ui
    host_links = "".join(
        f'<a href="{e(href)}"' + (' aria-current="page"' if current else "") + f'>{e(label)}</a>'
        for label, href, current in f.hosts)
    tabs = "".join(
        f'<a href="{e(href)}"' + (' aria-current="page"' if current else "")
        + f'><span>{i:02d} / {e(label)}</span><span class="arrow" aria-hidden="true">↗</span></a>'
        for i, (label, href, current) in enumerate(f.hosts, 1))
    langs = "".join(
        f'<a href="{e(href)}" lang="{e(code)}" hreflang="{e(code)}" data-language'
        + (' aria-current="page"' if current else "") + f'>{e(label)}</a>'
        for code, label, href, current in f.languages)
    toc = "".join(f'<li><a href="#{e(anchor)}">{e(label)}</a></li>' for anchor, label in f.toc)
    crumb = (f'<a href="{e(f.gateway[0])}">{e(f.gateway[1])}</a><span aria-hidden="true">/</span>'
             if f.gateway else "")
    footer_links = ([(f.gateway[1], f.gateway[0], False)] if f.gateway else []) + list(f.footer_links)
    links = " · ".join(
        f'<a href="{e(href)}"' + (' target="_blank" rel="noopener noreferrer"' if external else "")
        + f'>{e(label)}</a>' for label, href, external in footer_links)
    return f"""<!doctype html>
<html lang="{e(f.lang)}"{(' dir="' + e(f.dir) + '"') if f.dir else ""}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#f5f3ee">
{f.head}
<link rel="stylesheet" href="{e(f.css)}">
<script src="{e(f.asset_root)}assets/kumihan-install.js" defer></script>{f.scripts}
</head>
<body>
<a class="skip skip-link" href="#main">{e(u['skip'])}</a>
<header class="site-header">
  <div class="shell header-inner">
    <a class="brand" href="{e(f.home)}">{f.brand}</a>
    <nav class="header-nav" aria-label="{e(u['nav'])}">{host_links}</nav>
  </div>
</header>
<section class="hero" aria-labelledby="page-title">
  <div class="shell">
    <nav class="breadcrumb" aria-label="Breadcrumb">{crumb}<a href="{e(f.home)}">{f.brand}</a><span aria-hidden="true">/</span><span>{e(u['breadcrumb'])}</span></nav>
    <div class="hero-grid">
      <div>
        <div class="eyebrow">INSTALL GUIDE / {e(f.number)} OF 03</div>
        <h1 id="page-title">{f.title}</h1>
        <p class="hero-desc">{f.description}</p>
        <nav class="language-switch{(" " + f.language_class) if f.language_class else ""}" aria-label="{e(u['language'])}">{langs}</nav>
      </div>
      <div class="hero-logo"><img src="{e(f.asset_root)}assets/{LOGO}" alt="KUMIHAN official logo" width="1254" height="1254"></div>
    </div>
  </div>
</section>
<nav class="platform-nav" aria-label="{e(u['platforms'])}">
  <div class="shell platform-inner">{tabs}</div>
</nav>
<div class="shell content-layout">
  <aside class="toc" aria-label="{e(u['toc_title'])}">
    <details class="toc-details" open>
      <summary>{e(u['toc_summary'])}</summary>
      <h2 class="toc-title">{e(u['toc_title'])}</h2>
      <ol>{toc}</ol>
    </details>
    <div class="toc-note"><strong>{e(u['note_title'])}</strong><p>{e(u['note'])}</p></div>
    <a class="source-link" href="{e(u['source_href'])}" target="_blank" rel="noopener noreferrer">{e(u['source'])} ↗</a>
  </aside>
  <main class="guide" id="main" tabindex="-1">
    <div class="guide-head"><span>DOCUMENTATION / {e(f.platform)}</span><span class="step-label">{e(u['steps'])}</span></div>
    <div class="guide-pane">{f.content}</div>
  </main>
</div>
<footer class="footer">
  <div class="shell footer-inner">
    <div><strong>{f.brand}</strong><p>{f.footer_sub}</p></div>
    <div><a href="{e(f.home)}">{e(u['top'])}</a> · {links}</div>
  </div>
</footer>
</body>
</html>
"""
