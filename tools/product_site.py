"""Shared renderer for product landings in the canonical KUMIHAN index structure.

Used by product builders (Accord, Arabic) so every language edition keeps the
sections of _layouts/landing.html: hero, idea strip, four principles, band,
skills, install rows, release status and closing call to action. Callers pass
already-resolved paths and copy; this module only lays them out.
"""
import re
from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_wf_spec = spec_from_file_location("kumihan_web_fonts", Path(__file__).with_name("web_fonts.py"))
WEB_FONTS = module_from_spec(_wf_spec)
_wf_spec.loader.exec_module(WEB_FONTS)
SECTIONS = ("hero", "intro-strip", "features", "idea-band", "skills-section",
            "install-section", "status-section", "cta-section")


def x(value):
    return escape(str(value), quote=True)


# The regional band (copy "regions"), as on KUMIHAN｜字衡: it takes the dark band's place.
REGION_CSS = """
    .locale-layout { grid-template-columns: minmax(0,1fr) minmax(0,1.1fr); }
    .locale-cards { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 14px; align-self: center; }
    .locale-cards article { padding: 24px 22px; border: 1px solid rgba(250,246,238,.22); background: rgba(250,246,238,.04); min-width: 0; }
    .locale-tag { display: flex; align-items: baseline; gap: 10px; }
    .locale-tag span { font: 800 11px/1 Arial, sans-serif; letter-spacing: .14em; color: #ff8b85; }
    .locale-tag strong { font-size: 18px; }
    .locale-cards code { display: block; margin: 10px 0 8px; font: 600 12px/1.5 ui-monospace, Menlo, Consolas, monospace; color: #c4c0b9; }
    .idea-band .locale-cards p { margin: 0; font-size: 13px; line-height: 1.95; color: #c4c0b9; }
    @media (max-width: 790px) { .locale-layout { grid-template-columns: minmax(0,1fr); } }
    @media (max-width: 560px) { .locale-cards { grid-template-columns: minmax(0,1fr); } }
"""


def canonical_css(header, overrides):
    """Canonical index CSS from _layouts/landing.html plus the regional band and product overrides."""
    layout = (ROOT / "_layouts" / "landing.html").read_text(encoding="utf-8")
    match = re.search(r"<style>([\s\S]*?)</style>", layout)
    if match is None:
        raise ValueError("Canonical KUMIHAN index stylesheet was not found")
    return f"/* {header} */\n" + match.group(1).strip("\n") + REGION_CSS + overrides.lstrip("\n")


def band(p, c):
    """The dark band: the shared idea copy, or the edition's regional variants when it has them."""
    r = c.get("regions")
    if not r:
        return f"""<section class="idea-band" aria-labelledby="idea-title">
  <div class="shell idea-layout">
    <div><p class="eyebrow"><span class="line" aria-hidden="true"></span> {x(c['idea_eyebrow'])}</p><h2 id="idea-title">{two(c['idea_h2'], 'strong', '')}</h2><p>{x(c['idea_body'])}</p></div>
    <div class="idea-art" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span><small>FORM FOLLOWS MEANING</small></div>
  </div>
</section>"""
    cards = "".join(
        f'<article lang="{x(card["code"])}"><div class="locale-tag"><span lang="en" dir="ltr">{x(card["tag"])}</span>'
        f'<strong lang="{x(p["lang"])}">{x(card["name"])}</strong></div>'
        f'<code lang="en" dir="ltr">{x(card["code"])}</code><p lang="{x(p["lang"])}">{x(card["p"])}</p></article>'
        for card in r["cards"])
    return f"""<section class="idea-band" id="regions" aria-labelledby="idea-title">
  <div class="shell idea-layout locale-layout">
    <div><p class="eyebrow" dir="ltr"><span class="line" aria-hidden="true"></span> {x(r['eyebrow'])}</p><h2 id="idea-title">{"<br>".join(x(t) for t in r['h2'])}</h2><p>{x(r['body'])}</p></div>
    <div class="locale-cards">{cards}</div>
  </div>
</section>"""


def lines(parts, cls="accent"):
    """Heading lines separated by <br>; the last line carries the accent."""
    return "<br>".join(x(p) for p in parts[:-1]) + f'<br><span class="{cls}">{x(parts[-1])}</span>'


def two(parts, tag="span", cls="accent"):
    attr = f' class="{cls}"' if cls else ""
    return f"{x(parts[0])}<br><{tag}{attr}>{x(parts[1])}</{tag}>"


def landing(p, c):
    """Render one landing.

    p: lang, dir, head (meta/link HTML), brand (HTML), home_label, languages
       [(code, label, href, current)], logo, source, repo, release,
       skills [(name, href, symbol)], hosts [(name_html, href)], gateway
       (href, label), family (label, href), license
    c: copy for this language (see assets/*-site-copy.json)
    """
    langs = "".join(f'<a href="{x(href)}" lang="{code}" hreflang="{code}"'
                    + (' aria-current="page"' if current else "") + f">{x(label)}</a>"
                    for code, label, href, current in p["languages"])
    nav = "".join(f'<a href="#{a}">{x(t)}</a>' for a, t in zip(("concept", "features", "skills", "install"), c["nav"]))
    features = "".join(
        f'<article class="feature"><div class="feature-index">{x(f["idx"])}</div>'
        f'<div class="feature-motif" aria-hidden="true">{x(f["mark"])}</div><h3>{x(f["h3"])}</h3><p>{x(f["p"])}</p></article>'
        for f in c["features"])
    types = ("01 / ENTRY", "02 / WEB", "03 / DOCUMENTS", "04 / REVIEW")
    # A skill or host without an address (an edition not yet distributed) is shown, not linked.
    skills = "".join(
        (f'<a class="skill-card" href="{x(href)}" target="_blank" rel="noopener noreferrer">' if href else '<div class="skill-card">')
        + f'<div class="card-top"><span class="skill-type">{types[i]}</span><span class="skill-symbol" aria-hidden="true">{x(symbol)}</span></div>'
        f'<div><h3 class="skill-name"><bdi dir="ltr">{x(name)}</bdi></h3><p class="skill-desc">{x(c["skills"][i][1])}</p>'
        f'<div class="skill-end"><span>{x(c["skill_view"])}</span>' + ('<span aria-hidden="true">↗</span>' if href else "")
        + "</div></div>" + ("</a>" if href else "</div>")
        for i, (name, href, symbol) in enumerate(p["skills"]))
    rows = "".join(
        (f'<a class="platform-row" href="{x(href)}">' if href else '<div class="platform-row">')
        + f'<span class="platform-index">0{i + 1}</span>'
        f'<div class="platform-info"><div class="platform-name"><bdi dir="ltr">{x(name)}</bdi></div><div class="platform-note">{x(c["install_notes"][i])}</div></div>'
        + ('<span class="platform-arrow" aria-hidden="true">↗</span></a>' if href else "</div>")
        for i, (name, href) in enumerate(p["hosts"]))
    extra = (f'<div class="install-extra"><a href="{x(p["release"])}" target="_blank" rel="noopener noreferrer">{x(c["install_extra"])}</a></div>'
             if c.get("install_extra") else "")
    foot = '<span class="rule" aria-hidden="true"></span>'.join(f"<span>{x(t)}</span>" for t in c["hero_foot"])
    direction = f' dir="{p["dir"]}"' if p.get("dir") else ""
    out = f"""<!doctype html>
<html lang="{p['lang']}"{direction}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f5f3ee">
{p['head']}
{WEB_FONTS.head(p['lang'], p.get('asset_root', ''))}
</head>
<body id="top">
<a class="skip-link" href="#main">{x(c['skip'])}</a>
<header class="site-header">
  <div class="shell header-content">
    <a class="brand" href="#top" aria-label="{x(p['home_label'])}">{p['brand']}</a>
    <nav class="header-nav" aria-label="{x(c['nav_label'])}">{nav}</nav>
    <div class="header-controls"><nav class="language-switch" aria-label="{x(c['lang_label'])}">{langs}</nav></div>
  </div>
</header>
<main id="main" tabindex="-1">
<section class="hero" aria-labelledby="hero-title">
  <div class="shell hero-layout">
    <div class="hero-copy">
      <p class="eyebrow"><span class="line" aria-hidden="true"></span> {x(c['eyebrow'])}</p>
      <h1 id="hero-title">{lines(c['h1'])}</h1>
      <p class="hero-desc">{x(c['lead'])}</p>
      <div class="hero-cta">
        <a class="button button-primary" href="#install">{x(c['cta'][0])}<span class="arrow" aria-hidden="true">↗</span></a>
        <a class="button" href="#concept">{x(c['cta'][1])}<span class="arrow" aria-hidden="true">↘</span></a>
      </div>
      <div class="hero-foot" dir="ltr">{foot}</div>
    </div>
    <div class="hero-stage" aria-label="KUMIHAN">
      <div class="logo-card"><img src="{x(p['logo'])}" width="1254" height="1254" alt="KUMIHAN" fetchpriority="high"></div>
      <div class="stage-label" dir="ltr">WORDS · SPACE · PURPOSE</div>
    </div>
  </div>
</section>
<section class="intro-strip" id="concept" aria-labelledby="concept-title">
  <div class="shell intro-layout">
    <div><span class="section-number" dir="ltr">01 / THE IDEA</span></div>
    <div class="intro-text"><h2 id="concept-title">{two(c['concept_h2'], 'em', '')}</h2><p>{x(c['concept_body'])}</p></div>
  </div>
</section>
<section class="features" id="features" aria-labelledby="features-title">
  <div class="shell">
    <div class="section-heading"><div><div class="section-number" dir="ltr">02 / WHAT MATTERS</div><h2 id="features-title">{x(c['features_h2'])}</h2></div><p>{x(c['features_deck'])}</p></div>
    <div class="feature-grid">{features}</div>
  </div>
</section>
{band(p, c)}
<section class="skills-section" id="skills" aria-labelledby="skills-title">
  <div class="shell">
    <div class="section-heading"><div><div class="section-number" dir="ltr">03 / THE SKILLS</div><h2 id="skills-title">{x(c['skills_h2'][0])}<br>{x(c['skills_h2'][1])}</h2></div><p>{x(c['skills_deck'])}</p></div>
    <div class="skills-grid">{skills}</div>
  </div>
</section>
<section class="install-section" id="install" aria-labelledby="install-title">
  <div class="shell install-layout">
    <div class="install-intro"><div class="section-number" dir="ltr">04 / GET STARTED</div><h2 id="install-title">{x(c['install_h2'][0])}<br>{x(c['install_h2'][1])}</h2><p>{x(c['install_body'])}</p></div>
    <div><div class="install-links">{rows}</div>{extra}</div>
  </div>
</section>
<section class="status-section" aria-labelledby="status-title">
  <div class="shell status-box">
    <div><div class="status-title" id="status-title" dir="ltr">{x(c['status_title'])}</div><p>{x(c['status_body'])}</p></div>
    <div class="status-meta"><a href="{x(p['release'])}" target="_blank" rel="noopener noreferrer">{x(c['status_link'])}</a><br><span dir="ltr">OPEN SOURCE · APACHE 2.0</span></div>
  </div>
</section>
<section class="cta-section" aria-labelledby="cta-title">
  <div class="shell cta-layout">
    <div><h2 id="cta-title">{x(c['cta_h2'][0])}<br>{x(c['cta_h2'][1])}</h2><p>{x(c['cta_body'])}</p></div>
    <a class="button" href="{x(p['repo'])}" target="_blank" rel="noopener noreferrer">{x(c['cta_button'])}<span class="arrow" aria-hidden="true">↗</span></a>
  </div>
</section>
</main>
{WEB_FONTS.FOOTER.footer(p['lang'], p.get('asset_root', ''))}
</body>
</html>
"""
    kinds = tuple(re.findall(r'<section class="([^"]+)"', out))
    if kinds != SECTIONS:
        raise ValueError(f"Landing index structure mismatch: {kinds}")
    return WEB_FONTS.SHARE.apply(out)
