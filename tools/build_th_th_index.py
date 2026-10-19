#!/usr/bin/env python3
"""Thai landing in the canonical KUMIHAN index visual structure.

Uses shared layout CSS from _layouts/landing.html, Thai-specific typesetting
settings, and the already approved Thai copy in assets/thai-site-copy.json.
It does not apply Japanese kinsoku or enforce preset Thai line breaks.
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
anchor, canonical_css, x = _ja.anchor, _ja.canonical_css, _ja.x

THAI_OVERRIDES = r"""
    html[lang="th"] {
      scroll-padding-top: 116px;
      word-break: normal;
    }
    html[lang="th"] body {
      font-family: "Noto Sans Thai", Thonburi, "Leelawadee UI",
                   Tahoma, system-ui, sans-serif;
      font-size: 16px;
      line-height: 1.95;
    }
    html[lang="th"] h1,
    html[lang="th"] h2,
    html[lang="th"] h3,
    html[lang="th"] .hero-desc,
    html[lang="th"] .skill-desc,
    html[lang="th"] .platform-note,
    html[lang="th"] .button {
      letter-spacing: 0;
      word-break: normal;
    }
    html[lang="th"] h1 { line-height: 1.55; }
    html[lang="th"] h2 { line-height: 1.55; }
    html[lang="th"] h3 { line-height: 1.65; }
    html[lang="th"] .hero-desc { line-height: 2.05; }
    html[lang="th"] .intro-text p { line-height: 2.06; }
    html[lang="th"] .feature p { line-height: 1.96; }
    html[lang="th"] .idea-band p:not(.eyebrow) { line-height: 2.0; }
    html[lang="th"] .hero h1 {
      font-size: clamp(40px,4.7vw,66px);
      font-weight: 730;
      letter-spacing: 0;
      line-height: 1.43;
      word-break: normal;
      text-wrap: balance;
    }
    html[lang="th"] .hero h1 .accent { color: var(--red-dark); }
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
    .hero-stage::after { content:"KUMIHAN / TH"; }
    .hero-stage .logo-card img { display:block; }
    .feature-motif { font-family:"Noto Sans Thai",Thonburi,sans-serif; letter-spacing:0; }
    .feature:nth-child(2) .feature-motif { font-family:"Noto Sans Thai",Thonburi,sans-serif; }
    .feature:nth-child(3) .feature-motif { font-family:"Noto Sans Thai",Thonburi,sans-serif; font-size:31px; }
    .feature h3 { letter-spacing:0; }
    .skill-name {
      font-size:clamp(22px,2vw,28px);
      font-family:Arial,Helvetica,sans-serif;
      letter-spacing:-.03em;
      overflow-wrap:anywhere;
    }
    .skill-desc,.platform-note,.footer-links a { overflow-wrap:break-word; }
    .skill-card,.platform-info { min-width:0; }
    .status-meta { white-space:normal; }
    .status-meta a { display:inline-block; line-height:1.7; color:var(--red-dark); }
    .status-meta a:hover { text-decoration:underline; text-underline-offset:5px; }
    @media (max-width:790px) {
      .hero-layout { grid-template-columns: 1fr; gap: 46px; }
      .hero h1 { font-size:clamp(39px,8vw,56px); line-height:1.5; }
      .hero-stage { max-width:min(100%,575px); }
    }
    @media (max-width:560px) {
      html[lang="th"] .hero h1 { font-size:clamp(34px,8.6vw,47px); line-height:1.56; }
      html[lang="th"] .hero-desc { font-size:15px; line-height:1.95; }
      html[lang="th"] .feature-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
      .language-switch a { padding:7px 9px; }
      .skill-name { font-size:24px; }
      .platform-row { gap:14px; }
      .footer-links { justify-content:flex-start; }
    }
    @media (max-width:365px) {
      html[lang="th"] .feature-grid { grid-template-columns:1fr; }
      .feature,.feature:not(:first-child),.feature:nth-child(3) {
        padding:22px 0;min-height:0;border-left:0;
        border-bottom:1px solid var(--line);
      }
      .feature:last-child { border-bottom:0; }
    }
"""


def render(root: Path, copy: dict) -> str:
    c = copy
    # Metadata is not rewritten; labels and links are derived from the canonical copy.
    css = canonical_css(root)
    head = f"""<!doctype html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#f5f3ee">
  <title>{x(c["meta title"])}</title>
  <meta name="description" content="{x(c["meta description"])}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{x(c["meta title"])}">
  <meta property="og:description" content="{x(c["meta description"])}">
  <meta property="og:url" content="{BASE}kumihan-th.html">
  <meta property="og:locale" content="th_TH">
  <meta property="og:image" content="{BASE}{LOGO}">
  <meta property="og:image:alt" content="{BRAND}">
  <link rel="canonical" href="{BASE}kumihan-th.html">
  <link rel="alternate" hreflang="th-TH" href="{BASE}kumihan-th.html">
  <link rel="alternate" hreflang="en" href="{BASE}kumihan-th-en.html">
  <link rel="alternate" hreflang="ja" href="{BASE}kumihan-th-ja.html">
  <link rel="alternate" hreflang="x-default" href="{BASE}kumihan-th.html">
  <link rel="icon" href="favicon.ico">
  <style>{css}
{THAI_OVERRIDES}
  </style>
  <script src="assets/thai-site.js" defer></script>
  {WEB_FONTS.head("th")}
</head>
<body id="top">
<a class="skip-link" href="#main">ข้ามไปยังเนื้อหา</a>
"""
    languages = [
        ("th", "ไทย", "kumihan-th.html"),
        ("en", "EN", "kumihan-th-en.html"),
        ("ja", "日本語", "kumihan-th-ja.html"),
    ]
    language_nav = '<div class="header-controls"><nav class="language-switch" aria-label="เลือกภาษา">'
    for code, label, dest in languages:
        current = ' aria-current="page"' if code == "th" else ""
        language_nav += anchor(dest, label, extra='data-language lang="' + code +
                               '" hreflang="' + code + '"' + current)
    language_nav += "</nav></div>"
    hero = c["hero H1"]
    first, sep, second = hero.partition(" ")
    if not sep or not first or not second:
        raise ValueError("Thai headline is missing its approved phrase separator")
    hero_markup = x(first + sep) + '<span class="accent">' + x(second) + '</span>'
    out = head + f"""
<header class="site-header">
  <div class="shell header-content">
    {anchor("#top", "KUMIHAN", "brand", 'aria-label="กลับด้านบน"')}
    <nav class="header-nav" aria-label="เมนูหลัก">
      {anchor("#concept", x(c["nav concept"]))}
      {anchor("#features", x(c["nav features"]))}
      {anchor("#skills", x(c["nav skills"]))}
      {anchor("#install", x(c["nav install"]))}
    </nav>
    {language_nav}
  </div>
</header>
<main id="main">
<section class="hero" aria-labelledby="hero-title">
  <div class="shell hero-layout">
    <div class="hero-copy">
      <p class="eyebrow"><span class="line" aria-hidden="true"></span> OPEN-SOURCE SKILLS / THAI TYPOGRAPHY</p>
      <h1 id="hero-title">{hero_markup}</h1>
      <p class="hero-desc">{x(c["hero lead"])}</p>
      <div class="hero-cta">
        {anchor("#install", x(c["CTA 1"])+'<span class="arrow" aria-hidden="true">↗</span>', "button button-primary")}
        {anchor("#concept", 'อ่านแนวคิด<span class="arrow" aria-hidden="true">↘</span>', "button")}
      </div>
      <div class="hero-foot" aria-label="โอเพนซอร์ส สี่ทักษะ ออกแบบเพื่อภาษาไทย">
        <span>OPEN SOURCE</span><span class="rule" aria-hidden="true"></span>
        <span>FOUR SKILLS</span><span class="rule" aria-hidden="true"></span>
        <span>THAI FIRST</span>
      </div>
    </div>
    <div class="hero-stage" aria-label="ตราสัญลักษณ์ทางการของ KUMIHAN">
      <div class="logo-card"><img src="{LOGO}" width="1254" height="1254"
        alt="โลโก้ KUMIHAN" fetchpriority="high"></div>
      <div class="stage-label">WORDS · SPACE · PURPOSE</div>
    </div>
  </div>
</section>
<section class="intro-strip" id="concept" aria-labelledby="concept-title">
  <div class="shell intro-layout">
    <div><span class="section-number">01 / THE IDEA</span></div>
    <div class="intro-text">
      <h2 id="concept-title">{x(c["concept heading"])}</h2>
      <p>{x(c["concept body"])}</p>
    </div>
  </div>
</section>
<section class="features" id="features" aria-labelledby="features-title">
  <div class="shell">
    <div class="section-heading">
      <div><div class="section-number">02 / WHAT MATTERS</div>
        <h2 id="features-title">{x(c["features title"])}</h2></div>
      <p>หลักคิดสำคัญสำหรับการออกแบบและตรวจทานข้อความภาษาไทย</p>
    </div>
    <div class="feature-grid">
"""
    features = [
        ("01 / BREAKS", "ก", c["feature 1"]),
        ("02 / SHAPING", "◌", c["feature 2"]),
        ("03 / FIDELITY", "Aa/ก", c["feature 3"]),
        ("04 / REVIEW", "◎", c["feature 4"]),
    ]
    for num, motif, copy_item in features:
        title, sep, detail = copy_item.partition(" — ")
        if not sep:
            raise ValueError("Thai feature text is missing title separator")
        out += f"""<article class="feature">
  <div class="feature-index">{x(num)}</div>
  <div class="feature-motif" aria-hidden="true">{x(motif)}</div>
  <h3>{x(title)}</h3><p>{x(detail)}</p>
</article>
"""
    out += f"""</div></div></section>
<section class="idea-band" aria-labelledby="idea-title">
  <div class="shell idea-layout">
    <div><p class="eyebrow"><span class="line" aria-hidden="true"></span> DESIGNED FOR THE MESSAGE</p>
      <h2 id="idea-title">{x(c["philosophy H2"])}</h2>
      <p>{x(c["philosophy body"])}</p>
    </div>
    <div class="idea-art" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span>
      <small>FORM FOLLOWS MEANING</small></div>
  </div>
</section>
<section class="skills-section" id="skills" aria-labelledby="skills-title">
  <div class="shell">
    <div class="section-heading">
      <div><div class="section-number">03 / THE SKILLS</div>
        <h2 id="skills-title">{x(c["skills title"])}</h2></div>
      <p>เริ่มต้นจากแนวทางที่เหมาะกับงานและสื่อของคุณ</p>
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
            raise ValueError("Unexpected Thai skill naming")
        out += f"""<a class="skill-card" href="{SOURCE}/skills/{slug}"
    target="_blank" rel="noopener noreferrer">
  <div class="card-top"><span class="skill-type">{category}</span>
    <span class="skill-symbol" aria-hidden="true">{x(motif)}</span></div>
  <div><h3 class="skill-name">{slug}</h3>
    <p class="skill-desc">{x(description)}</p>
    <div class="skill-end"><span>ดูรายละเอียด Skill</span><span aria-hidden="true">↗</span></div>
  </div></a>
"""
    out += f"""</div></div></section>
<section class="install-section" id="install" aria-labelledby="install-title">
  <div class="shell install-layout">
    <div class="install-intro">
      <div class="section-number">04 / GET STARTED</div>
      <h2 id="install-title">{x(c["install heading"])}</h2>
      <p>{x(c["install lead"])}</p>
    </div>
    <div><div class="install-links">
"""
    hosts = [
        ("01", "ChatGPT / Codex", "docs/install-kumihan-th-chatgpt.html",
         "ทักษะแยกและปลั๊กอินสำหรับ ChatGPT / Codex"),
        ("02", "Claude / Claude Code", "docs/install-kumihan-th-claude.html",
         "ปลั๊กอิน Claude Code และ Skill แยก"),
        ("03", "Gemini", "docs/install-kumihan-th-gemini.html",
         "ส่วนขยาย Gemini CLI และการใช้ Skill"),
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
      <div class="install-extra">ดาวน์โหลดจาก {anchor(RELEASE, "GitHub Release", extra='target="_blank" rel="noopener noreferrer"')} และตรวจ SHA256SUMS ก่อนติดตั้ง</div>
    </div>
  </div>
</section>
<section class="status-section" aria-labelledby="status-title">
  <div class="shell status-box">
    <div>
      <div class="status-title" id="status-title">KUMIHAN / THAI v0.1.1</div>
      <p>{x(c["release status body"])}</p>
      <p>การติดตั้งและเรียกใช้จริงบน ChatGPT / Codex / Claude / Gemini ยังไม่ได้ทดสอบ (not-checked)</p>
    </div>
    <div class="status-meta">{anchor(RELEASE, "ดาวน์โหลดเวอร์ชันล่าสุด ↗", extra='target="_blank" rel="noopener noreferrer"')}
      <br>OPEN SOURCE · APACHE 2.0</div>
  </div>
</section>
<section class="cta-section" aria-labelledby="cta-title">
  <div class="shell cta-layout">
    <div><h2 id="cta-title">{x(c["final CTA"])}</h2>
      <p>เปิดเผยซอร์สโค้ดและแพ็กเกจ เพื่อให้คุณตรวจสอบและนำไปใช้ตามความเหมาะสม</p></div>
    {anchor(SOURCE, 'ดูซอร์สโค้ด<span class="arrow" aria-hidden="true">↗</span>',
            "button", 'target="_blank" rel="noopener noreferrer"')}
  </div>
</section>
</main>
<footer class="footer">
  <div class="shell footer-layout">
    <div><div class="footer-mark" lang="th">{BRAND}</div>
      <div class="footer-sub">Thai typography skills for AI-assisted design<br>
      Developed by L&amp;Co. LLC</div></div>
    <div class="footer-links">
      {anchor("top-th.html", "หน้าแรก KUMIHAN")}
      {anchor("kumihan.html", "KUMIHAN 日本語")}
      {anchor("kumihan-th-en.html", "English")}
      {anchor("kumihan-th-ja.html", "日本語")}
      {anchor(SOURCE, "GitHub", extra='target="_blank" rel="noopener noreferrer"')}
      {anchor("LICENSE", "Apache License 2.0")}
      {anchor("#top", "กลับด้านบน ↑")}
    </div>
  </div>
</footer>
</body></html>
"""
    kinds = tuple(re.findall(r'<section class="([^"]+)"', out))
    if kinds != SECTIONS:
        raise ValueError(f"Thai page index structure mismatch: {kinds}")
    return out
