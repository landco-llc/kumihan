#!/usr/bin/env python3
"""English landing for the Thai product in the canonical KUMIHAN index structure.

Uses shared layout CSS from _layouts/landing.html, the shared KUMIHAN copy in
tools/base_copy.py, and the Thai-specific English copy in
assets/thai-site-copy.json. The copy file is not changed.
"""
from __future__ import annotations

from pathlib import Path
import re

from importlib.util import spec_from_file_location, module_from_spec
_wf_spec = spec_from_file_location("kumihan_web_fonts", Path(__file__).with_name("web_fonts.py"))
WEB_FONTS = module_from_spec(_wf_spec)
_wf_spec.loader.exec_module(WEB_FONTS)
_ja_spec = spec_from_file_location("kumihan_th_reference", Path(__file__).with_name("build_th_ja_index.py"))
_ja = module_from_spec(_ja_spec)
_ja_spec.loader.exec_module(_ja)
BASE, BRAND, LOGO, RELEASE, SECTIONS, SOURCE = (
    _ja.BASE, _ja.BRAND, _ja.LOGO, _ja.RELEASE, _ja.SECTIONS, _ja.SOURCE
)
anchor, canonical_css, thai_name, x = _ja.anchor, _ja.canonical_css, _ja.thai_name, _ja.x

# Shared copy of the canonical KUMIHAN page (tools/base_copy.py) with only the
# product and language names swapped. Thai-specific text (feature 01, the
# fidelity detail, the entry skill and release status) stays in
# assets/thai-site-copy.json.
SHARED = _ja.base_copy.shared("en", "th")

ENGLISH_OVERRIDES = r"""
    html[lang="en"] body { line-height: 1.7; }
    html[lang="en"] .hero h1 { text-wrap: balance; }
    .intro-text h2, .section-heading h2, .idea-band h2, .install-intro h2, .cta-layout h2 {
      text-wrap: balance;
    }
    .hero-layout {
      grid-template-columns: minmax(0,1.18fr) minmax(0,.82fr);
      gap: clamp(42px,5vw,86px);
    }
    .header-nav a { white-space: normal; line-height: 1.5; }
    .language-switch a {
      display:inline-flex; min-height:38px; min-width:41px;
      align-items:center; justify-content:center;
      padding:8px 10px; border-radius:40px;
      font: 780 12px/1.35 "Noto Sans Thai", Arial, sans-serif;
      color:var(--muted);
      letter-spacing:0; text-decoration:none;
    }
    .language-switch a[aria-current="page"] { color:white; background:var(--ink); }
    .language-switch a:hover:not([aria-current="page"]) { background:var(--paper-2); }
    .hero .edition {
      display: inline-block; margin-top: 12px;
      color: var(--red-dark); font: 750 16px/1.65 "Noto Sans Thai", Thonburi, Arial, sans-serif;
      letter-spacing: 0;
    }
    .hero-stage::after { content:"KUMIHAN / TH"; }
    .feature-motif { font-family:"Noto Sans Thai",Thonburi,sans-serif; letter-spacing:0; }
    .feature:nth-child(2) .feature-motif { font-family:"Noto Sans Thai",Thonburi,sans-serif; }
    .feature:nth-child(3) .feature-motif { font-family:"Noto Sans Thai",Thonburi,sans-serif; font-size:31px; }
    .feature h3 { letter-spacing:-.02em; }
    .skill-name {
      font-size:clamp(22px,2vw,28px);
      letter-spacing:-.03em;
      overflow-wrap:anywhere;
    }
    .skill-desc,.platform-note,.footer-links a { overflow-wrap:break-word; }
    .skill-card,.platform-info { min-width:0; }
    .status-meta { white-space:normal; }
    .status-meta a { display:inline-block; line-height:1.7; color:var(--red-dark); }
    .status-meta a:hover { text-decoration:underline; text-underline-offset:5px; }
    /* Enlarged text at phone widths: wrap long English words rather than
       widening grid tracks past the viewport. */
    html[lang="en"] .hero h1, html[lang="en"] h2, html[lang="en"] h3,
    html[lang="en"] .eyebrow, html[lang="en"] .button, html[lang="en"] .feature-index,
    html[lang="en"] .hero-desc, html[lang="en"] .brand { overflow-wrap: anywhere; }
    .hero-foot { flex-wrap: wrap; }
    .hero-cta .button { max-width: 100%; }
    .hero-copy, .hero-stage, .feature, .install-layout > *, .header-content > * { min-width: 0; }
    @media (max-width:790px) {
      .hero-layout { grid-template-columns: minmax(0,1fr); gap: 46px; }
      .hero-stage { max-width:min(100%,575px); }
    }
    @media (max-width:560px) {
      html[lang="en"] .feature-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
      .language-switch a { padding:7px 9px; }
      .hero .edition { font-size: 15px; }
      .skill-name { font-size:24px; }
      .platform-row { gap:14px; }
      .footer-links { justify-content:flex-start; }
    }
    @media (max-width:365px) {
      html[lang="en"] .feature-grid { grid-template-columns:1fr; }
      .feature,.feature:not(:first-child),.feature:nth-child(3) {
        padding:22px 0;min-height:0;border-left:0;
        border-bottom:1px solid var(--line);
      }
      .feature:last-child { border-bottom:0; }
    }
"""


def render(root: Path, copy: dict) -> str:
    c = copy
    s = SHARED
    css = canonical_css(root)
    head = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#f5f3ee">
  <title>{x(s["title"])}</title>
  <meta name="description" content="{x(s["description"])}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{x(s["title"])}">
  <meta property="og:description" content="{x(s["description"])}">
  <meta property="og:url" content="{BASE}kumihan-th-en.html">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{BASE}{LOGO}">
  <meta property="og:image:alt" content="{BRAND}">
  <link rel="canonical" href="{BASE}kumihan-th-en.html">
  <link rel="alternate" hreflang="th-TH" href="{BASE}kumihan-th.html">
  <link rel="alternate" hreflang="en" href="{BASE}kumihan-th-en.html">
  <link rel="alternate" hreflang="ja" href="{BASE}kumihan-th-ja.html">
  <link rel="alternate" hreflang="x-default" href="{BASE}kumihan-th.html">
  <link rel="icon" href="favicon.ico">
  <style>{css}
{ENGLISH_OVERRIDES}
  </style>
  <script src="assets/thai-site.js" defer></script>
  {WEB_FONTS.head("en")}
</head>
<body id="top">
<a class="skip-link" href="#main">Skip to content</a>
"""
    languages = [
        ("th", "ไทย", "kumihan-th.html"),
        ("en", "EN", "kumihan-th-en.html"),
        ("ja", "日本語", "kumihan-th-ja.html"),
    ]
    language_nav = '<div class="header-controls"><nav class="language-switch" aria-label="Language">'
    for code, label, dest in languages:
        current = ' aria-current="page"' if code == "en" else ""
        language_nav += anchor(dest, label, extra='data-language lang="' + code +
                               '" hreflang="' + code + '"' + current)
    language_nav += "</nav></div>"
    hero_markup = x(s["h1"][0]) + '<br><span class="accent">' + x(s["h1"][1]) + '</span>'
    out = head + f"""
<header class="site-header">
  <div class="shell header-content">
    {anchor("#top", "KUMIHAN", "brand", 'aria-label="Back to top"')}
    <nav class="header-nav" aria-label="Primary navigation">
      {anchor("#concept", x(s["nav"][0]))}
      {anchor("#features", x(s["nav"][1]))}
      {anchor("#skills", x(s["nav"][2]))}
      {anchor("#install", x(s["nav"][3]))}
    </nav>
    {language_nav}
  </div>
</header>
<main id="main">
<section class="hero" aria-labelledby="hero-title">
  <div class="shell hero-layout">
    <div class="hero-copy">
      <p class="eyebrow"><span class="line" aria-hidden="true"></span> {x(s["eyebrow"])}</p>
      <h1 id="hero-title">{hero_markup}</h1>
      <p class="edition" lang="th">{BRAND}</p>
      <p class="hero-desc">{thai_name(s["lead"])}</p>
      <div class="hero-cta">
        {anchor("#install", x(s["cta"][0])+'<span class="arrow" aria-hidden="true">↗</span>', "button button-primary")}
        {anchor("#concept", x(s["cta"][1])+'<span class="arrow" aria-hidden="true">↘</span>', "button")}
      </div>
      <div class="hero-foot" aria-label="Open-source, four skills, Thai-first">
        <span>{x(s["hero_foot"][0])}</span><span class="rule" aria-hidden="true"></span>
        <span>{x(s["hero_foot"][1])}</span><span class="rule" aria-hidden="true"></span>
        <span>{x(s["hero_foot"][2])}</span>
      </div>
    </div>
    <div class="hero-stage" aria-label="KUMIHAN identity">
      <div class="logo-card"><img src="{LOGO}" width="1254" height="1254"
        alt="Official KUMIHAN logo: a black typographic grid, a red horizontal bar, and the KUMIHAN wordmark." fetchpriority="high"></div>
      <div class="stage-label">WORDS · SPACE · PURPOSE</div>
    </div>
  </div>
</section>
<section class="intro-strip" id="concept" aria-labelledby="concept-title">
  <div class="shell intro-layout">
    <div><span class="section-number">01 / THE IDEA</span></div>
    <div class="intro-text">
      <h2 id="concept-title">{x(s["concept_h2"][0])}<br><em>{x(s["concept_h2"][1])}</em></h2>
      <p>{thai_name(s["concept_body"])}</p>
    </div>
  </div>
</section>
<section class="features" id="features" aria-labelledby="features-title">
  <div class="shell">
    <div class="section-heading">
      <div><div class="section-number">02 / WHAT MATTERS</div>
        <h2 id="features-title">{x(s["features_h2"])}</h2></div>
      <p>{x(s["features_deck"])}</p>
    </div>
    <div class="feature-grid">
"""
    def split(item: str) -> tuple[str, str]:
        title, sep, detail = item.partition(" — ")
        if not sep:
            raise ValueError("English feature text is missing title separator")
        return title, detail

    # Feature 01 is Thai-specific; it also carries the vowel and tone mark
    # rendering point, since feature 02 is the shared STRUCTURE principle.
    breaks, breaks_detail = split(c["feature 1"])
    _, shaping_detail = split(c["feature 2"])
    breaks_detail = (breaks_detail.removesuffix(".") + ", and "
                     + shaping_detail.replace("stacked signs", "stacked vowels and tone marks"))
    shared = s["features"]
    features = [
        ("01 / BREAKS", "ก", breaks, breaks_detail),
        (shared[1]["idx"], shared[1]["mark"], shared[1]["h3"], shared[1]["p"]),
        (shared[2]["idx"], "Aa/ก", shared[2]["h3"], split(c["feature 3"])[1]),
        (shared[3]["idx"], shared[3]["mark"], shared[3]["h3"], shared[3]["p"]),
    ]
    for num, motif, title, detail in features:
        out += f"""<article class="feature">
  <div class="feature-index">{x(num)}</div>
  <div class="feature-motif" aria-hidden="true">{x(motif)}</div>
  <h3>{x(title)}</h3><p>{x(detail[:1].upper() + detail[1:])}</p>
</article>
"""
    out += f"""</div></div></section>
<section class="idea-band" aria-labelledby="idea-title">
  <div class="shell idea-layout">
    <div><p class="eyebrow"><span class="line" aria-hidden="true"></span> DESIGNED FOR THE MESSAGE</p>
      <h2 id="idea-title">{x(s["idea_h2"][0])}<br><strong>{x(s["idea_h2"][1])}</strong></h2>
      <p>{thai_name(s["idea_body"])}</p>
    </div>
    <div class="idea-art" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span>
      <small>FORM FOLLOWS MEANING</small></div>
  </div>
</section>
<section class="skills-section" id="skills" aria-labelledby="skills-title">
  <div class="shell">
    <div class="section-heading">
      <div><div class="section-number">03 / THE SKILLS</div>
        <h2 id="skills-title">{x(s["skills_h2"][0])}<br>{x(s["skills_h2"][1])}</h2></div>
      <p>{x(s["skills_deck"])}</p>
    </div>
    <div class="skills-grid">
"""
    skills = [
        ("kumihan-th", "01 / ENTRY", "組"),
        ("kumihan-th-web", "02 / WEB", "↗"),
        ("kumihan-th-documents", "03 / DOCUMENTS", "文"),
        ("kumihan-th-review", "04 / REVIEW", "◎"),
    ]
    for i, (slug, category, motif) in enumerate(skills, 1):
        label, sep, description = c[f"skill {i}"].partition(" — ")
        if label != slug or not sep:
            raise ValueError("Unexpected English skill naming")
        if s["skills"][i - 1] is not None:
            description = s["skills"][i - 1][1]  # shared; only the entry skill is Thai-specific
        out += f"""<a class="skill-card" href="{SOURCE}/skills/{slug}"
    target="_blank" rel="noopener noreferrer">
  <div class="card-top"><span class="skill-type">{category}</span>
    <span class="skill-symbol" aria-hidden="true">{x(motif)}</span></div>
  <div><h3 class="skill-name">{slug}</h3>
    <p class="skill-desc">{x(description[:1].upper() + description[1:])}</p>
    <div class="skill-end"><span>{x(s["skill_view"])}</span><span aria-hidden="true">↗</span></div>
  </div></a>
"""
    out += f"""</div></div></section>
<section class="install-section" id="install" aria-labelledby="install-title">
  <div class="shell install-layout">
    <div class="install-intro">
      <div class="section-number">04 / GET STARTED</div>
      <h2 id="install-title">{x(s["install_h2"][0])}<br>{x(s["install_h2"][1])}</h2>
      <p>{x(s["install_body"])}</p>
    </div>
    <div><div class="install-links">
"""
    hosts = [
        ("01", "ChatGPT / Codex", "docs/install-kumihan-th-chatgpt.en.html", s["install_notes"][0]),
        ("02", "Claude / Claude Code", "docs/install-kumihan-th-claude.en.html", s["install_notes"][1]),
        ("03", "Gemini", "docs/install-kumihan-th-gemini.en.html", s["install_notes"][2]),
    ]
    for number, name, href, note in hosts:
        out += f"""<a class="platform-row" href="{href}">
  <span class="platform-index">{number}</span>
  <div class="platform-info"><div class="platform-name">{x(name)}</div>
    <div class="platform-note">{x(note)}</div></div>
  <span class="platform-arrow" aria-hidden="true">↗</span>
</a>
"""
    out += f"""</div>
      <div class="install-extra">Download from {anchor(RELEASE, "GitHub Release", extra='target="_blank" rel="noopener noreferrer"')} and verify SHA256SUMS before installing.</div>
    </div>
  </div>
</section>
<section class="status-section" aria-labelledby="status-title">
  <div class="shell status-box">
    <div>
      <div class="status-title" id="status-title">{x(s["status_title"])}</div>
      <p>{x(c["status body"])}</p>
      <p>Native installation and invocation on ChatGPT / Codex / Claude / Gemini: not-checked.</p>
    </div>
    <div class="status-meta">{anchor(RELEASE, x(s["status_link"]), extra='target="_blank" rel="noopener noreferrer"')}
      <br>OPEN SOURCE · APACHE 2.0</div>
  </div>
</section>
<section class="cta-section" aria-labelledby="cta-title">
  <div class="shell cta-layout">
    <div><h2 id="cta-title">{x(s["cta_h2"][0])}<br>{x(s["cta_h2"][1])}</h2>
      <p>{thai_name(s["cta_body"])}</p></div>
    {anchor(SOURCE, x(s["cta_button"]) + '<span class="arrow" aria-hidden="true">↗</span>',
            "button", 'target="_blank" rel="noopener noreferrer"')}
  </div>
</section>
</main>
{WEB_FONTS.FOOTER.footer("en")}
</body></html>
"""
    kinds = tuple(re.findall(r'<section class="([^"]+)"', out))
    if kinds != SECTIONS:
        raise ValueError(f"English page index structure mismatch: {kinds}")
    return out
