#!/usr/bin/env python3
"""Build the Thai product's Japanese landing page using the canonical index visual structure.

Canonical reference: _layouts/landing.html (the existing Japanese KUMIHAN index).
Only Japanese landing HTML is generated here; Thai/English pages and installation
guides retain their own language-specific sources and layouts.
"""
from __future__ import annotations

from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import re
_wf_spec = spec_from_file_location("kumihan_web_fonts", Path(__file__).with_name("web_fonts.py"))
WEB_FONTS = module_from_spec(_wf_spec)
_wf_spec.loader.exec_module(WEB_FONTS)

_base_spec = spec_from_file_location("kumihan_base_copy", Path(__file__).with_name("base_copy.py"))
base_copy = module_from_spec(_base_spec)
_base_spec.loader.exec_module(base_copy)


SECTIONS = (
    "hero",
    "intro-strip",
    "features",
    "idea-band",
    "skills-section",
    "install-section",
    "status-section",
    "cta-section",
)
BRAND = "KUMIHAN｜ดุลอักษร"
RELEASE = "https://github.com/landco-llc/kumihan/releases/tag/kumihan-th-v0.1.1"
SOURCE = "https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-th"
BASE = "https://landco-llc.github.io/kumihan/"
LOGO = "assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"

# Shared copy of the canonical Japanese KUMIHAN page (tools/base_copy.py) with
# only the product and language names swapped. Thai-specific text (feature 01,
# the fidelity detail, the entry skill and release status) stays in
# assets/thai-site-copy.json.
SHARED = base_copy.shared("ja", "th")
SHORT = base_copy.EDITIONS["th"][1]

# Display headings are free of Japanese comma/period.
DISPLAY = {
    "hero": "".join(SHARED["h1"]),
    "concept": "".join(SHARED["concept_h2"]),
    "features": SHARED["features_h2"],
    "idea": "".join(SHARED["idea_h2"]),
    "skills": "".join(SHARED["skills_h2"]),
    "install": "".join(SHARED["install_h2"]),
    "cta": "".join(SHARED["cta_h2"]),
}


def thai_name(text: str) -> str:
    """Escape text and mark the Thai product name for Thai font and line breaking."""
    return x(text).replace(SHORT, '<span lang="th">' + SHORT + '</span>')


def x(value: str) -> str:
    return escape(str(value), quote=True)


def anchor(href: str, label: str, css: str = "", extra: str = "") -> str:
    attrs = (' class="' + x(css) + '"') if css else ""
    return '<a href="' + x(href) + '"' + attrs + (' ' + extra if extra else '') + '>' + label + '</a>'


def canonical_css(root: Path) -> str:
    reference = (root / "_layouts" / "landing.html").read_text(encoding="utf-8")
    match = re.search(r"<style>([\s\S]*?)</style>", reference)
    if match is None:
        raise ValueError("Canonical KUMIHAN index stylesheet was not found")
    required = [".hero-layout", ".feature-grid", ".skill-card", ".install-layout", ".cta-layout"]
    if any(selector not in match.group(1) for selector in required):
        raise ValueError("Canonical index layout is missing a required style")
    return "\n".join(line.rstrip() for line in match.group(1).splitlines())


# The canonical index CSS is reused rather than approximated with new generic cards.
# The below overrides only cover the independent product's language links,
# mixed Japanese/Thai type and narrow-screen reflow.
OVERRIDES = r"""
    html[lang="ja"] { line-break: strict; }
    html[lang="ja"] body {
      font-family: "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic",
                   "Noto Sans JP", Meiryo, sans-serif;
      line-height: 1.8;
    }
    .hero-layout {
      grid-template-columns: minmax(0,1.18fr) minmax(0,.82fr);
      gap: clamp(42px,5vw,86px);
    }
    .header-nav { min-width: 0; }
    .header-nav a { white-space: normal; text-wrap: balance; }
    .language-switch a {
      display: inline-flex; min-height: 38px; min-width: 40px;
      align-items: center; justify-content: center;
      padding: 8px 10px; border-radius: 40px;
      font: 800 11px/1.35 Arial, sans-serif; letter-spacing: .04em;
      color: var(--muted); text-decoration: none;
    }
    .language-switch a[aria-current="page"] { background: var(--ink); color: white; }
    .language-switch a:hover:not([aria-current="page"]) { background: var(--paper-2); }
    .hero h1 {
      letter-spacing: -.045em; text-wrap: wrap;
      word-break: normal; overflow-wrap: normal;
    }
    @supports (word-break: auto-phrase) {
      /* Real Chrome 155 / 1280 + 320 measurement preferred larger speech groups. */
      .hero h1 { word-break: auto-phrase; text-wrap: balance; }
    }
    .intro-text h2, .section-heading h2, .idea-band h2, .install-intro h2, .cta-layout h2 {
      text-wrap: balance; word-break: normal;
    }
    .hero .edition {
      display: inline-block; margin-top: 10px;
      color: var(--red-dark); font: 750 16px/1.65 "Noto Sans Thai", Thonburi,
            "Hiragino Sans", sans-serif;
      letter-spacing: 0; overflow-wrap: anywhere;
    }
    .feature-motif { font-family: "Noto Sans Thai", Thonburi, "Hiragino Sans", sans-serif; }
    .feature:nth-child(2) .feature-motif { letter-spacing: -.12em; }
    .feature:nth-child(3) .feature-motif { font-size: 31px; }
    .hero-stage::after { content: "KUMIHAN / TH"; }
    .skill-name { font-size: clamp(23px,2.0vw,29px); overflow-wrap: anywhere; }
    .skill-desc { overflow-wrap: break-word; }
    .skill-card { min-width: 0; }
    .platform-info { min-width: 0; }
    .platform-name, .platform-note { overflow-wrap: break-word; }
    .status-meta { white-space: normal; overflow-wrap: break-word; }
    .status-box > * { min-width: 0; }
    .card-top > * { min-width: 0; }
    .skill-type { overflow-wrap: anywhere; }
    .status-meta a { display: inline-block; padding-block: 5px; color: var(--red-dark); }
    .status-meta a:hover { text-decoration: underline; text-underline-offset: 4px; }
    .footer-links a { overflow-wrap: break-word; }
    @media (max-width: 790px) {
      .hero-layout { grid-template-columns: 1fr; gap: 46px; }
      .header-nav { gap: 12px; }
      .language-switch a { min-height: 40px; }
      .hero-stage { max-width: min(100%, 575px); }
    }
    @media (max-width: 560px) {
      .hero h1 { font-size: clamp(36px, 9vw, 50px); letter-spacing: -.04em; }
      .language-switch a { padding: 7px 9px; }
      .hero .edition { font-size: 15px; }
      .hero-stage::after { right: 8px; }
      .feature-grid { grid-template-columns: repeat(2,minmax(0,1fr)); }
      .skill-name { font-size: 25px; }
      .platform-row { gap: 13px; }
      .footer-links { justify-content: flex-start; }
    }
    @media (max-width: 365px) {
      .feature-grid { grid-template-columns: 1fr; }
      .feature,.feature:not(:first-child),.feature:nth-child(3) {
        padding: 23px 0; min-height: 0; border-left: 0;
        border-bottom: 1px solid var(--line);
      }
      .feature:last-child { border-bottom: 0; }
    }
    /* These selectors target actual external URLs, not Japanese reading copy. */
    .external-id { overflow-wrap: anywhere; }
"""


def render(root: Path, copy: dict) -> str:
    c = copy
    s = SHARED
    styles = canonical_css(root)
    title = s["title"]
    description = s["description"]
    head = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#f5f3ee">
  <title>{x(title)}</title>
  <meta name="description" content="{x(description)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{x(title)}">
  <meta property="og:description" content="{x(description)}">
  <meta property="og:url" content="{BASE}kumihan-th-ja.html">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:image" content="{BASE}{LOGO}">
  <meta property="og:image:alt" content="{BRAND}">
  <link rel="canonical" href="{BASE}kumihan-th-ja.html">
  <link rel="alternate" hreflang="th-TH" href="{BASE}kumihan-th.html">
  <link rel="alternate" hreflang="en" href="{BASE}kumihan-th-en.html">
  <link rel="alternate" hreflang="ja" href="{BASE}kumihan-th-ja.html">
  <link rel="alternate" hreflang="x-default" href="{BASE}kumihan-th.html">
  <link rel="icon" href="favicon.ico">
  <style>{styles}
{OVERRIDES}
  </style>
  <script src="assets/thai-site.js" defer></script>
  {WEB_FONTS.head("ja")}
</head>
<body id="top">
<a class="skip-link" href="#main">本文へ移動</a>
"""
    # No JS is needed to navigate between languages; links work with JS off.
    language = [
        ("th", "ไทย", "kumihan-th.html"),
        ("en", "EN", "kumihan-th-en.html"),
        ("ja", "日本語", "kumihan-th-ja.html"),
    ]
    lang_nav = '<div class="header-controls"><nav class="language-switch" aria-label="表示言語を選ぶ">'
    for code, label, url in language:
        current = ' aria-current="page"' if code == "ja" else ""
        lang_nav += anchor(url, label, extra='data-language lang="' + code +
                           '" hreflang="' + code + '"' + current)
    lang_nav += "</nav></div>"
    out = head + f"""
<header class="site-header">
  <div class="shell header-content">
    {anchor("#top", "KUMIHAN", "brand", 'aria-label="ページ上部へ戻る"')}
    <nav class="header-nav" aria-label="メインナビゲーション">
      {anchor("#concept", thai_name(s["nav"][0]))}
      {anchor("#features", x(s["nav"][1]))}
      {anchor("#skills", x(s["nav"][2]))}
      {anchor("#install", x(s["nav"][3]))}
    </nav>
    {lang_nav}
  </div>
</header>
<main id="main">
<section class="hero" aria-labelledby="hero-title">
  <div class="shell hero-layout">
    <div class="hero-copy">
      <p class="eyebrow"><span class="line" aria-hidden="true"></span> {x(s["eyebrow"])}</p>
      <div class="edition" lang="th">{BRAND}</div>
      <h1 id="hero-title">{"<br>".join(x(p) for p in s["h1"][:-1])}<br><span class="accent">{x(s["h1"][-1])}</span></h1>
      <p class="hero-desc">{thai_name(s["lead"])}</p>
      <div class="hero-cta">
        {anchor("#install", x(s["cta"][0]) + '<span class="arrow" aria-hidden="true">↗</span>', "button button-primary")}
        {anchor("#concept", thai_name(s["cta"][1]) + '<span class="arrow" aria-hidden="true">↘</span>', "button")}
      </div>
      <div class="hero-foot" aria-label="オープンソース タイ語版 4つのスキル">
        <span>{x(s["hero_foot"][0])}</span><span class="rule" aria-hidden="true"></span>
        <span>{x(s["hero_foot"][1])}</span><span class="rule" aria-hidden="true"></span>
        <span>{x(s["hero_foot"][2])}</span>
      </div>
    </div>
    <div class="hero-stage" aria-label="KUMIHAN公式ビジュアル">
      <div class="logo-card"><img src="{LOGO}" width="1254" height="1254"
        alt="KUMIHANの公式ロゴ" fetchpriority="high"></div>
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
      <p>{thai_name(s["features_deck"])}</p>
    </div>
    <div class="feature-grid">
"""
    def split(item: str) -> tuple[str, str]:
        label, sep, detail = item.partition(" — ")
        if not sep:
            raise ValueError("Expected a Japanese feature title and description")
        return label, detail

    # Feature 01 is Thai-specific; it also carries the vowel and tone mark
    # rendering point, since feature 02 is the shared STRUCTURE principle.
    breaks, breaks_detail = split(c["feature 1"])
    _, shaping_detail = split(c["feature 2"])
    shaping_detail = shaping_detail.replace("記号の重なり、欠け、", "母音・声調記号の重なりや欠け、")
    shared = s["features"]
    features = [
        ("01 / BREAKS", "ก", breaks, breaks_detail + shaping_detail),
        (shared[1]["idx"], shared[1]["mark"], shared[1]["h3"], shared[1]["p"]),
        (shared[2]["idx"], "Aa/ก", shared[2]["h3"], split(c["feature 3"])[1]),
        (shared[3]["idx"], shared[3]["mark"], shared[3]["h3"], shared[3]["p"]),
    ]
    for index, motif, label, detail in features:
        out += f"""<article class="feature">
  <div class="feature-index">{x(index)}</div>
  <div class="feature-motif" aria-hidden="true">{x(motif)}</div>
  <h3>{x(label)}</h3><p>{x(detail)}</p>
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
    for i, (slug, typ, motif) in enumerate(skills, 1):
        label, sep, text = c[f"skill {i}"].partition(" — ")
        if not sep or label != slug:
            raise ValueError("Unexpected skill name in Japanese copy")
        if s["skills"][i - 1] is not None:
            text = s["skills"][i - 1][1]  # shared; only the entry skill is Thai-specific
        url = SOURCE + "/skills/" + slug
        out += f"""<a class="skill-card" href="{x(url)}" target="_blank" rel="noopener noreferrer">
  <div class="card-top"><span class="skill-type">{x(typ)}</span>
    <span class="skill-symbol" aria-hidden="true">{x(motif)}</span></div>
  <div><h3 class="skill-name">{slug}</h3>
    <p class="skill-desc">{x(text)}</p>
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
    installations = [
        ("01", "ChatGPT / Codex", "docs/install-kumihan-th-chatgpt.ja.html", s["install_notes"][0]),
        ("02", "Claude / Claude Code", "docs/install-kumihan-th-claude.ja.html", s["install_notes"][1]),
        ("03", "Gemini", "docs/install-kumihan-th-gemini.ja.html", s["install_notes"][2]),
    ]
    for num, name, href, note in installations:
        out += f"""<a class="platform-row" href="{href}">
  <span class="platform-index">{num}</span>
  <div class="platform-info"><div class="platform-name">{x(name)}</div>
    <div class="platform-note">{x(note)}</div></div>
  <span class="platform-arrow" aria-hidden="true">↗</span>
</a>
"""
    out += f"""</div>
      <div class="install-extra">配布ファイルは {anchor(RELEASE, "GitHub Release", extra='target="_blank" rel="noopener noreferrer"')} で確認できます</div>
    </div>
  </div>
</section>
<section class="status-section" aria-labelledby="status-title">
  <div class="shell status-box">
    <div>
      <div class="status-title" id="status-title">{x(s["status_title"])}</div>
      <p>{x(c["status body"])}</p>
      <p>ChatGPT・Codex・Claude・Geminiでの実ホスト導入と呼び出しは未検証（not-checked）です</p>
    </div>
    <div class="status-meta">{anchor(RELEASE, x(s["status_link"]), extra='target="_blank" rel="noopener noreferrer"')}
      <br>OPEN SOURCE · APACHE 2.0</div>
  </div>
</section>
<section class="cta-section" aria-labelledby="cta-title">
  <div class="shell cta-layout">
    <div><h2 id="cta-title">{x(s["cta_h2"][0])}<br>{x(s["cta_h2"][1])}</h2>
      <p>{thai_name(s["cta_body"])}</p></div>
    {anchor(SOURCE, x(s["cta_button"]) + '<span class="arrow" aria-hidden="true">↗</span>', "button", 'target="_blank" rel="noopener noreferrer"')}
  </div>
</section>
</main>
{WEB_FONTS.FOOTER.footer("ja")}
</body></html>
"""
    # Assertions are source-level guardrails, not a rendered typography claim.
    elements = re.findall(r'<section class="([^"]+)"', out)
    if tuple(elements) != SECTIONS:
        raise ValueError(f"Japanese landing diverged from canonical index structure: {elements}")
    for phrase in DISPLAY.values():
        if any(mark in phrase for mark in "、。！？"):
            raise ValueError("Display headline contains prohibited Japanese punctuation")
    for heading in re.findall(r"<h([123])\b[^>]*>(.*?)</h\1>", out, re.S):
        if any(mark in re.sub("<[^>]*>", "", heading[1]) for mark in "、。"):
            raise ValueError("Heading contains Japanese comma or period")
    if any(section not in out for section in (
        'id="hero-title"', 'id="concept-title"', 'id="features-title"',
        'id="skills-title"', 'id="install-title"', 'id="status-title"', 'id="cta-title"',
    )):
        raise ValueError("Missing canonical landmark")
    return WEB_FONTS.SHARE.apply(out)


if __name__ == "__main__":
    import json
    root = Path(__file__).resolve().parents[1]
    copy = json.loads((root / "assets/thai-site-copy.json").read_text())["ja"]
    print(render(root, copy))
