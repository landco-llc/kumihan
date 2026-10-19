#!/usr/bin/env python3
"""Build the ZiHeng landings in the canonical KUMIHAN index structure; --check verifies.

Copy comes verbatim from assets/ziheng-site-copy.json (the approved page text).
Styles: the canonical index CSS from _layouts/landing.html plus ZiHeng locale
settings, written to assets/ziheng-site.css. Following kumihan-ziheng-web,
pages declare an explicit zh-Hant-TW locale, keep Taiwan full-width
punctuation (no squeezing), and never convert or normalize source text. The
Taiwan / Hong Kong band keeps the index's dark "idea" slot.
"""
import argparse
import json
import re
from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_wf_spec = spec_from_file_location("kumihan_web_fonts", Path(__file__).with_name("web_fonts.py"))
WEB_FONTS = module_from_spec(_wf_spec)
_wf_spec.loader.exec_module(WEB_FONTS)
BASE = "https://landco-llc.github.io/kumihan/"
LOGO = "assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"
SOURCE = "https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng"
ZIP = "https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads/plugins/kumihan-ziheng-0.1.0-preview.zip"
BRAND = 'KUMIHAN<span class="brand-rule">｜</span>字衡'
SECTIONS = ("hero", "intro-strip", "features", "idea-band", "skills-section",
            "install-section", "status-section", "cta-section")
LANGS = {"zh-Hant-TW": "", "en": ".en", "ja": ".ja"}
OG = {"zh-Hant-TW": "zh_TW", "en": "en_US", "ja": "ja_JP"}
_spec = spec_from_file_location("kumihan_install_frame", Path(__file__).with_name("install_frame.py"))
FRAME = module_from_spec(_spec)
_spec.loader.exec_module(FRAME)

# Labels the approved copy does not contain. Reused wording from the previous
# ZiHeng pages where it existed (ZIP labels, Japanese KUMIHAN links).
UI = {
    "zh-Hant-TW": dict(language="語言", features_idx="02 / WHAT MATTERS", zip="取得 ZIP", view="查看技能",
                       family=("日文版 KUMIHAN", "zh-tw.html"), regions="TAIWAN / HONG KONG", top="回到頁首"),
    "en": dict(language="Language", features_idx="02 / WHAT MATTERS", zip="Download ZIP", view="View skill",
               family=("Japanese KUMIHAN", "en.html"), regions="TAIWAN / HONG KONG", top="Back to top"),
    "ja": dict(language="表示言語", features_idx="02 / WHAT MATTERS", zip="ZIPを入手", view="スキルを見る",
               family=("日本語版 KUMIHAN", "kumihan.html"), regions="TAIWAN / HONG KONG", top="ページ上部へ"),
}
# Display-only line breaks at phrase boundaries (the copy text is unchanged):
# a heading longer than its column otherwise splits inside a word such as 脈絡.
# Headings stored as a list (the shared KUMIHAN copy) break between its items instead.
PHRASE_BREAKS = {"zh-Hant-TW": {"locale_h2": "同是繁體中文"}, "ja": {"locale_h2": "同じ繁体中国語でも"}, "en": {}}
FEATURE_INDEX = ("01 / REGION", "02 / SOURCE", "03 / LAYOUT", "04 / REVIEW")
SKILL_TYPES = ("01 / ENTRY", "02 / WEB", "03 / DOCUMENTS", "04 / REVIEW")
HOSTS = (("ChatGPT / Codex", "docs/install-ziheng{}.html"),
         ("Claude / Claude Code", "docs/install-ziheng-claude{}.html"),
         ("Gemini", "docs/install-ziheng-gemini{}.html"))

OVERRIDES = r"""
    /* ZiHeng locale settings (kumihan-ziheng-web). Fallback stacks only make
       Traditional Chinese glyphs available; they are not a recommended palette. */
    html[lang="zh-Hant-TW"] {
      --display: "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", "Noto Sans CJK TC", system-ui, sans-serif;
      --serif: "Songti TC", "Noto Serif TC", "PMingLiU", "Noto Serif CJK TC", serif;
    }
    html[lang="zh-Hant-TW"] body, html[lang="ja"] body { line-break: strict; }
    [lang="zh-Hant-TW"] { font-kerning: normal; }
    /* Taiwan keeps full-width punctuation: no palt / spacing-trim here. */
    html[lang="zh-Hant-TW"] .hero h1 { font-size: clamp(40px,4.8vw,70px); letter-spacing: -.04em; line-height: 1.3; }
    html[lang="zh-Hant-TW"] .intro-text h2, html[lang="zh-Hant-TW"] .section-heading h2,
    html[lang="zh-Hant-TW"] .idea-band h2, html[lang="zh-Hant-TW"] .install-intro h2,
    html[lang="zh-Hant-TW"] .cta-layout h2 { letter-spacing: -.04em; }
    html[lang="en"] .hero h1 { text-wrap: balance; }
    html[lang="en"] .intro-text h2, html[lang="en"] .section-heading h2, html[lang="en"] .idea-band h2,
    html[lang="en"] .install-intro h2, html[lang="en"] .cta-layout h2 { letter-spacing: -.045em; line-height: 1.3; }
    html[lang="en"] .hero h1, html[lang="en"] h2, html[lang="en"] h3, html[lang="en"] .eyebrow,
    html[lang="en"] .button, html[lang="en"] .hero-desc { overflow-wrap: anywhere; }
    /* Japanese headings: phrase-aware wrapping where supported (an aid, not proof). */
    @supports (word-break: auto-phrase) {
      html[lang="ja"] h2, html[lang="ja"] h3 { word-break: auto-phrase; }
    }
    .brand { gap: 0; }
    .brand .brand-rule { margin-inline: 2px; color: var(--red); font-weight: 400; }
    .brand [lang="zh-Hant-TW"], .footer-mark [lang="zh-Hant-TW"] { letter-spacing: 0; }
    /* Enlarged text on narrow screens: the brand wraps instead of widening the page. */
    .brand { min-width: 0; flex: 0 1 auto; }
    .brand > span { white-space: normal; overflow-wrap: anywhere; }
    .language-switch a { display: inline-flex; align-items: center; justify-content: center; min-height: 38px; min-width: 38px; border-radius: 40px; color: var(--muted); padding: 7px 10px; font-size: 11px; font-weight: 800; letter-spacing: .05em; }
    .language-switch a[aria-current="page"] { background: var(--ink); color: white; }
    .language-switch a:hover:not([aria-current="page"]) { color: var(--red-dark); background: #ebe7df; }
    .hero-stage::after { content: "KUMIHAN / ZH-HANT"; }
    .stage-label span { letter-spacing: 0; font-size: 12px; }
    .hero h1 { word-break: normal; }
    .hero-foot { flex-wrap: wrap; }
    .hero-cta .button { max-width: 100%; }
    .feature-motif { letter-spacing: 0 !important; }
    .locale-layout { grid-template-columns: minmax(0,1fr) minmax(0,1.1fr); }
    .locale-cards { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 14px; align-self: center; }
    .locale-cards article { padding: 24px 22px; border: 1px solid rgba(250,246,238,.22); background: rgba(250,246,238,.04); }
    .locale-tag { display: flex; align-items: baseline; gap: 10px; }
    .locale-tag span { font: 800 11px/1 Arial, sans-serif; letter-spacing: .14em; color: #ff8b85; }
    .locale-tag strong { font-size: 18px; }
    .locale-cards code { display: block; margin: 10px 0 8px; font: 600 12px/1.5 ui-monospace, Menlo, Consolas, monospace; color: #c4c0b9; }
    .idea-band .locale-cards p { margin: 0; font-size: 13px; line-height: 1.95; color: #c4c0b9; }
    .status-box p strong { color: var(--ink); }
    .skill-card, .platform-info, .status-box > *, .hero-copy, .hero-stage, .feature, .install-layout > * { min-width: 0; }
    .status-meta { white-space: normal; }
    @media (max-width: 790px) {
      .hero-layout { grid-template-columns: minmax(0,1fr); }
      .locale-layout { grid-template-columns: minmax(0,1fr); }
      .feature-grid { grid-template-columns: repeat(2,minmax(0,1fr)); }
    }
    @media (max-width: 560px) {
      html[lang="zh-Hant-TW"] .hero h1 { font-size: clamp(34px,9vw,50px); line-height: 1.38; }
      .locale-cards { grid-template-columns: minmax(0,1fr); }
      .header-nav { flex-wrap: wrap; overflow: visible; gap: 12px 18px; }
      .header-nav a { white-space: normal; }
    }
"""


def x(value):
    return escape(str(value), quote=True)


def canonical_css():
    layout = (ROOT / "_layouts" / "landing.html").read_text(encoding="utf-8")
    match = re.search(r"<style>([\s\S]*?)</style>", layout)
    if match is None:
        raise ValueError("Canonical KUMIHAN index stylesheet was not found")
    return "/* KUMIHAN｜字衡 index: canonical KUMIHAN index CSS + ZiHeng locale settings. */\n" \
        + match.group(1).strip("\n") + "\n" + OVERRIDES.lstrip("\n")


def render(lang, c):
    u = UI[lang]
    sfx = LANGS[lang]
    page = f"kumihan-zh-han{sfx}.html"
    gateway, gateway_label = FRAME.GATEWAYS[lang]
    alternates = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}kumihan-zh-han{v}.html">' for k, v in LANGS.items())
    langs = "".join(
        f'<a hreflang="{k}" lang="{k}" href="kumihan-zh-han{v}.html"' + (' aria-current="page"' if k == lang else "")
        + f'>{label}</a>' for (k, v), label in zip(LANGS.items(), ("繁體中文", "English", "日本語")))
    nav = "".join(f'<a href="#{a}">{x(t)}</a>' for a, t in zip(("concept", "features", "skills", "install"), c["nav"]))
    features = "".join(
        f'<article class="feature"><div class="feature-index">{x(f.get("idx", FEATURE_INDEX[i]))}</div>'
        f'<div class="feature-motif" aria-hidden="true">{x(f["mark"])}</div><h3>{x(f["h3"])}</h3><p>{x(f["p"])}</p></article>'
        for i, f in enumerate(c["features"]))
    locales = "".join(
        f'<article lang="{x(l["code"])}"><div class="locale-tag"><span lang="en">{x(l["tag"])}</span><strong lang="{lang}">{x(l["name"])}</strong></div>'
        f'<code lang="en">{x(l["code"])}</code><p lang="{lang}">{x(l["p"])}</p></article>'
        for l in c["locales"])
    skills = "".join(
        f'<a class="skill-card" href="{SOURCE}/skills/{x(s["name"])}" target="_blank" rel="noopener noreferrer">'
        f'<div class="card-top"><span class="skill-type">{SKILL_TYPES[i]}</span><span class="skill-symbol" aria-hidden="true">{x(s["motif"])}</span></div>'
        f'<div><h3 class="skill-name">{x(s["name"])}</h3><p class="skill-desc">{(x(s["role"].split(" / ", 1)[1]) + " — ") if "role" in s else ""}{x(s["p"])}</p>'
        f'<div class="skill-end"><span>{x(u["view"])}</span><span aria-hidden="true">↗</span></div></div></a>'
        for i, s in enumerate(c["skills"]))
    rows = "".join(
        f'<a class="platform-row" href="{href.format(sfx)}"><span class="platform-index">0{i + 1}</span>'
        f'<div class="platform-info"><div class="platform-name">{name}</div><div class="platform-note">{x(c["install_notes"][i])}</div></div>'
        f'<span class="platform-arrow" aria-hidden="true">↗</span></a>'
        for i, (name, href) in enumerate(HOSTS))
    def display(key):
        text, cut = c[key], PHRASE_BREAKS[lang].get(key)
        if isinstance(text, list):
            return "<br>".join(x(t) for t in text)
        if cut and text.startswith(cut) and len(text) > len(cut):
            return x(cut) + "<br>" + x(text[len(cut):])
        return x(text)
    feet = c["hero_foot"] if isinstance(c["hero_foot"], list) else ["OPEN SOURCE", "FOUR SKILLS", c["hero_foot"]]
    foot = '<span class="rule" aria-hidden="true"></span>'.join(f"<span>{x(t)}</span>" for t in feet)
    stage = c["stage_text"].replace("<small>", " — <span>").replace("</small>", "</span>")
    out = f"""<!doctype html>
<html lang="{lang}" data-product="zh-han">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f5f3ee">
<meta name="description" content="{x(c['description'])}">
<meta name="kumihan-product-route" content="zh-han">
<meta property="og:type" content="website">
<meta property="og:locale" content="{OG[lang]}">
<meta property="og:title" content="{x(c['og_title'])}">
<meta property="og:description" content="{x(c['description'])}">
<meta property="og:url" content="{BASE}{page}">
<meta property="og:image" content="{BASE}{LOGO}">
<link rel="canonical" href="{BASE}{page}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{BASE}kumihan-zh-han.html">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
<link rel="stylesheet" href="assets/ziheng-site.css">
<title>{x(c['title'])}</title>
{WEB_FONTS.head(lang)}
</head>
<body id="top">
<a class="skip-link" href="#main">{x(c['skip'])}</a>
<header class="site-header">
  <div class="shell header-content">
    <a class="brand" href="#top" aria-label="KUMIHAN ZiHeng — top"><span lang="zh-Hant-TW">{BRAND}</span></a>
    <nav class="header-nav" aria-label="{x(c['nav_label'])}">{nav}</nav>
    <div class="header-controls"><nav class="language-switch lang-picker" aria-label="{x(c['lang_label'])}">{langs}</nav></div>
  </div>
</header>
<main id="main" tabindex="-1">
<section class="hero" aria-labelledby="hero-title">
  <div class="shell hero-layout">
    <div class="hero-copy">
      <p class="eyebrow"><span class="line" aria-hidden="true"></span> {x(c['eyebrow'])}</p>
      <h1 id="hero-title">{"<br>".join(x(p) for p in c['h1'][:-1])}<br><span class="accent">{x(c['h1'][-1])}</span></h1>
      <p class="hero-desc">{x(c['lead'])}</p>
      <div class="hero-cta">
        <a class="button button-primary" href="#install">{x(c['cta'][0])}<span class="arrow" aria-hidden="true">↗</span></a>
        <a class="button" href="#concept">{x(c['cta'][1])}<span class="arrow" aria-hidden="true">↘</span></a>
      </div>
      <div class="hero-foot">{foot}</div>
    </div>
    <div class="hero-stage" aria-label="KUMIHAN official logo">
      <div class="logo-card"><img src="{LOGO}" width="1254" height="1254" alt="KUMIHAN official logo" fetchpriority="high"></div>
      <div class="stage-label">{stage}</div>
    </div>
  </div>
</section>
<section class="intro-strip" id="concept" aria-labelledby="concept-title">
  <div class="shell intro-layout">
    <div><span class="section-number">01 / THE IDEA</span></div>
    <div class="intro-text"><h2 id="concept-title">{x(c['concept_h2'][0])}<br><em>{x(c['concept_h2'][1])}</em></h2><p>{x(c['concept_body'])}</p></div>
  </div>
</section>
<section class="features" id="features" aria-labelledby="features-title">
  <div class="shell">
    <div class="section-heading"><div><div class="section-number">{u['features_idx']}</div><h2 id="features-title">{x(c['features_h2'])}</h2></div><p>{x(c['features_deck'])}</p></div>
    <div class="feature-grid">{features}</div>
  </div>
</section>
<section class="idea-band" id="regions" aria-labelledby="idea-title">
  <div class="shell idea-layout locale-layout">
    <div><p class="eyebrow"><span class="line" aria-hidden="true"></span> {u['regions']}</p><h2 id="idea-title">{display('locale_h2')}</h2><p>{x(c['locale_body'])}</p></div>
    <div class="locale-cards">{locales}</div>
  </div>
</section>
<section class="skills-section" id="skills" aria-labelledby="skills-title">
  <div class="shell">
    <div class="section-heading"><div><div class="section-number">03 / THE SKILLS</div><h2 id="skills-title">{display('skills_h2')}</h2></div><p>{x(c['skills_deck'])}</p></div>
    <div class="skills-grid">{skills}</div>
  </div>
</section>
<section class="install-section" id="install" aria-labelledby="install-title">
  <div class="shell install-layout">
    <div class="install-intro"><div class="section-number">04 / GET STARTED</div><h2 id="install-title">{display('install_h2')}</h2><p>{x(c['install_body'])}</p></div>
    <div><div class="install-links">{rows}</div><div class="install-extra">{c['install_extra']}</div></div>
  </div>
</section>
<section class="status-section" aria-labelledby="status-title">
  <div class="shell status-box">
    <div><div class="status-title" id="status-title">{x(c.get('status_title', 'PREVIEW / 0.1.0'))}</div><p><strong>{x(c['status_h'])}</strong></p><p>{x(c['status_body'])}</p></div>
    <div class="status-meta"><a href="{ZIP}" download>{x(c.get('status_link', u['zip'] + ' ↗'))}</a><br>OPEN SOURCE · APACHE 2.0</div>
  </div>
</section>
<section class="cta-section" aria-labelledby="cta-title">
  <div class="shell cta-layout">
    <div><h2 id="cta-title">{display('cta_h2')}</h2><p>{x(c['cta_body'])}</p></div>
    <a class="button" href="https://github.com/landco-llc/kumihan" target="_blank" rel="noopener noreferrer">{x(c['cta_button'])}<span class="arrow" aria-hidden="true">↗</span></a>
  </div>
</section>
</main>
{WEB_FONTS.FOOTER.footer(lang)}
</body>
</html>
"""
    kinds = tuple(re.findall(r'<section class="([^"]+)"', out))
    if kinds != SECTIONS:
        raise ValueError(f"ZiHeng index structure mismatch: {kinds}")
    return WEB_FONTS.SHARE.apply(out)


def outputs():
    copy = json.loads((ROOT / "assets" / "ziheng-site-copy.json").read_text(encoding="utf-8"))
    files = {f"kumihan-zh-han{sfx}.html": render(lang, copy[lang]) for lang, sfx in LANGS.items()}
    files["assets/ziheng-site.css"] = canonical_css()
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
        raise SystemExit("Stale ZiHeng site files: " + ", ".join(stale))
    print("ZiHeng site: 4 files " + ("verified" if args.check else "built"))


if __name__ == "__main__":
    main()
