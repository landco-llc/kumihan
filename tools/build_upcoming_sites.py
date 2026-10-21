#!/usr/bin/env python3
"""Build the landings of the newer language editions; --check verifies committed output.

KUMIHAN｜Μέτρο (el), Zetwerk (nl), Jalin (ms), Ahenk (tr), מקצב (he), विन्यास (sa),
Soulad (cs), Arány (hu), ဟန်ချက် (my), Concinnitas (la), Tugma (tl), Rytmi (fi),
Samspel (sv) and Samklang (da) each get a
landing in their own language, English and Japanese (kumihan-<code>[.en|.ja].html);
Measure (en) has an English and a Japanese landing (kumihan-en[.ja].html),
in the canonical KUMIHAN index structure (tools/product_site.py). Copy lives in
assets/upcoming-site-copy.json.

An edition whose packages are in the version catalogue (tools/edition_versions.py) is
released: skill cards link to its source, AI tools to its installation guides
(tools/build_install_guides.py) and the version panel shows its packages. The others
have no package yet, so their pages say "coming soon": skill cards and AI tools are
shown without links and the status names v0.1.0 as in preparation.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_adapter import seo_outputs
from version_display import version_outputs
import edition_versions as V
import argparse
import json
from importlib.util import module_from_spec, spec_from_file_location

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://landco-llc.github.io/kumihan/"
LOGO = "assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"
REPO = "https://github.com/landco-llc/kumihan"
# code -> (sub-brand, package slug, edition label, language-switch label, og:locale, skill symbols)
EDITIONS = {
    "el": ("Μέτρο", "metro", "EL", "ΕΛ", "el_GR", ("ς", "↗", "¶", "◎")),
    "nl": ("Zetwerk", "zetwerk", "NL", "NL", "nl_NL", ("IJ", "↗", "¶", "◎")),
    "ms": ("Jalin", "jalin", "MS", "MS", "ms_MY", ("ng", "↗", "¶", "◎")),
    "tr": ("Ahenk", "ahenk", "TR", "TR", "tr_TR", ("İı", "↗", "¶", "◎")),
    "he": ("מקצב", "miktsav", "HE", "עב", "he_IL", ("ך", "↗", "¶", "◎")),
    "sa": ("विन्यास", "vinyasa", "SA", "सं", "sa_IN", ("क्ष", "↗", "¶", "◎")),
    "cs": ("Soulad", "soulad", "CS", "CS", "cs_CZ", ("Řů", "↗", "¶", "◎")),
    "hu": ("Arány", "arany", "HU", "HU", "hu_HU", ("Őű", "↗", "¶", "◎")),
    "my": ("ဟန်ချက်", "my", "MY", "မြ", "my_MM", ("င်္ဂ", "↗", "¶", "◎")),
    "la": ("Concinnitas", "concinnitas", "LA", "LA", "la_VA", ("ā æ", "↗", "¶", "◎")),
    "tl": ("Tugma", "tugma", "TL", "TL", "tl_PH", ("â ñ", "↗", "¶", "◎")),
    "en": ("Measure", "measure", "EN", "EN", "en_US", ("&", "↗", "¶", "◎")),
    "fi": ("Rytmi", "rytmi", "FI", "FI", "fi_FI", ("Ää", "↗", "¶", "◎")),
    "sv": ("Samspel", "samspel", "SV", "SV", "sv_SE", ("Åö", "↗", "¶", "◎")),
    "da": ("Samklang", "samklang-da", "DA", "DA", "da_DK", ("Æøå", "↗", "¶", "◎")),
}
RTL = {"he"}
HOSTS = ("ChatGPT / Codex", "Claude / Claude Code", "Gemini")
OG = {"en": "en_US", "ja": "ja_JP"}

_ps_spec = spec_from_file_location("kumihan_product_site", Path(__file__).with_name("product_site.py"))
SITE = module_from_spec(_ps_spec)
_ps_spec.loader.exec_module(SITE)
x = SITE.x


def langs(code):
    """Page languages and file suffixes; English (Measure) is its own language, so it has two."""
    return {code: "", **{lang: "." + lang for lang in ("en", "ja") if lang != code}}


def landing_path(code, lang):
    return f"kumihan-{code}{langs(code)[lang]}.html"


def released(code):
    """True when the edition's packages are in the version catalogue."""
    return code in V.catalogue()


def guide(code, host, lang):
    from build_install_guides import guide_path
    return guide_path(code, host, lang)


def gateway(code, lang):
    return {"en": "index.html", "ja": "top-ja.html"}.get(lang, f"top-{code}.html")


def brand(code):
    return f'<bdi dir="ltr">KUMIHAN<span class="brand-sub">｜{x(EDITIONS[code][0])}</span></bdi>'


def landing(code, lang, c):
    sub, slug, label, switch, og, symbols = EDITIONS[code]
    page = landing_path(code, lang)
    alternates = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{landing_path(code, k)}">' for k in langs(code))
    head = (f"<title>{x(c['title'])}</title>\n<meta name=\"description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:type" content="website">\n<meta property="og:locale" content="{OG.get(lang, og)}">\n'
            f"<meta property=\"og:title\" content=\"{x(c['title'])}\">\n<meta property=\"og:description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:url" content="{BASE}{page}">\n<meta property="og:image" content="{BASE}{LOGO}">\n'
            f'<link rel="canonical" href="{BASE}{page}">\n{alternates}\n'
            f'<link rel="alternate" hreflang="x-default" href="{BASE}{landing_path(code, code)}">\n'
            f'<link rel="icon" href="assets/favicon-32x32.png" type="image/png">\n<link rel="stylesheet" href="assets/{slug}-site.css">')
    names = [f"kumihan-{slug}"] + [f"kumihan-{slug}-{s}" for s in ("web", "documents", "review")]
    switches = {code: switch, "en": "EN", "ja": "日本語"}
    if released(code):
        source = f"{REPO}/tree/main/plugins/kumihan-{slug}"
        skills = [(name, f"{source}/skills/{name}", symbols[i]) for i, name in enumerate(names)]
        hosts = [(name, guide(code, host, lang)) for host, name in zip(("chatgpt", "claude", "gemini"), HOSTS)]
        from build_install_guides import edition
        release = edition(code)["release"]
    else:
        skills, hosts, release = [(name, None, symbols[i]) for i, name in enumerate(names)], [(name, None) for name in HOSTS], REPO
    return SITE.landing(dict(
        lang=lang, dir="rtl" if lang in RTL else None, head=head, brand=brand(code), home_label=f"KUMIHAN｜{sub}",
        languages=[(k, switches[k], landing_path(code, k), k == lang) for k in langs(code)],
        logo=LOGO, repo=REPO, release=release, license=REPO + "/blob/main/LICENSE",
        skills=skills,
        hosts=hosts,
        gateway=(gateway(code, lang), c["gateway_label"]), family=c["family"]), c)


def css(code):
    sub, slug, label, *_ = EDITIONS[code]
    rtl = {"he": RTL_CSS, "sa": DEVANAGARI_CSS, "my": MYANMAR_CSS}.get(code, "")
    return SITE.canonical_css(f"KUMIHAN｜{sub} index: canonical KUMIHAN index CSS + edition settings (tools/build_upcoming_sites.py).",
                              OVERRIDES.replace("@LABEL@", label).replace("@LANG@", code) + rtl)


OVERRIDES = r"""
    /* No unverified automatic hyphenation; long words break only when they cannot fit. */
    html[lang="@LANG@"] :is(.hero-desc, .intro-text p, .feature p, .idea-band p, .skill-desc, .install-intro p, .status-box p, .cta-layout p) { hyphens: manual; word-break: normal; overflow-wrap: break-word; }
    html:is([lang="@LANG@"], [lang="en"]) .hero h1 { font-size: clamp(40px,4.7vw,70px); letter-spacing: -.04em; line-height: 1.14; text-wrap: balance; }
    html:is([lang="@LANG@"], [lang="en"]) :is(.intro-text h2, .section-heading h2, .idea-band h2, .install-intro h2, .cta-layout h2) { letter-spacing: -.035em; line-height: 1.25; }
    html:is([lang="@LANG@"], [lang="en"]) :is(h1, h2, h3, .eyebrow, .button, .feature p) { overflow-wrap: break-word; }
    html[lang="ja"] body { line-break: strict; }
    @supports (word-break: auto-phrase) {
      html[lang="ja"] :is(h2, h3, .hero-desc) { word-break: auto-phrase; }
    }
    /* Japanese heading: its three lines stay whole; long language names (サンスクリット語の)
       get smaller type instead of a fourth line, sized to the column, not the window. */
    html[lang="ja"] .hero-copy { container-type: inline-size; }
    html[lang="ja"] .hero h1 { font-size: min(clamp(44px, 5.2vw, 77px), 10.4cqi); word-break: keep-all; }
    .brand .brand-sub { margin-inline-start: 2px; font-weight: 700; letter-spacing: -.02em; }
    .language-switch a { display: inline-flex; align-items: center; justify-content: center; min-height: 38px; min-width: 38px; border-radius: 40px; color: var(--muted); padding: 7px 10px; font-size: 11px; font-weight: 800; letter-spacing: .05em; }
    .language-switch a[aria-current="page"] { background: var(--ink); color: white; }
    .language-switch a:hover:not([aria-current="page"]) { color: var(--red-dark); background: #ebe7df; }
    .hero-stage::after { content: "KUMIHAN / @LABEL@"; }
    .hero-foot { flex-wrap: wrap; }
    .hero-cta .button { max-width: 100%; }
    .feature-motif { font-family: Georgia, "Times New Roman", serif !important; letter-spacing: 0 !important; font-weight: 400 !important; }
    .skill-symbol { font-family: Georgia, "Times New Roman", serif; letter-spacing: 0; }
    /* Not yet distributed: skill cards and AI tools are shown without links. */
    div.skill-card, div.skill-card:hover { cursor: default; transform: none; }
    div.platform-row, div.platform-row:hover { cursor: default; padding-left: 4px; padding-right: 4px; }
    .status-meta { white-space: normal; }
    .header-content { flex-wrap: wrap; row-gap: 10px; }
    .header-nav { flex-wrap: wrap; min-width: 0; row-gap: 8px; }
    .brand { min-width: 0; flex: 0 1 auto; }
    .brand > bdi { white-space: normal; overflow-wrap: anywhere; }
    .idea-layout > *, .card-top > *, .cta-layout > * { min-width: 0; }
    .feature-index, .skill-type { overflow-wrap: anywhere; }
    .cta-layout .button { flex: 0 1 auto; max-width: 100%; }
    .status-meta a { color: var(--red-dark); }
    .skill-card, .platform-info, .status-box > *, .hero-copy, .hero-stage, .feature, .install-layout > * { min-width: 0; }
    @media (max-width: 560px) {
      html:is([lang="@LANG@"], [lang="en"]) .hero h1 { font-size: clamp(33px,9vw,45px); line-height: 1.18; }
      html[lang="ja"] .hero h1 { font-size: min(clamp(38px,9.7vw,56px), 10.4cqi); }
      .header-nav { flex-wrap: wrap; overflow: visible; gap: 12px 18px; }
      .header-nav a { white-space: normal; }
      .idea-layout { grid-template-columns: minmax(0,1fr); }
    }
"""

# Devanagari (as the Hindi edition): no tracking, which would break the headline
# (shirorekha) and conjuncts, and taller lines for vowel signs above and below.
DEVANAGARI_CSS = r"""
    html[lang="sa"] :is(h1, h2, h3, p, .eyebrow, .feature-index, .section-number, .skill-desc, .feature p) { letter-spacing: normal; }
    html[lang="sa"] .hero h1 { font-size: clamp(32px,4.4vw,64px); line-height: 1.5; }
    html[lang="sa"] :is(.intro-text h2, .section-heading h2, .idea-band h2, .install-intro h2, .cta-layout h2) { line-height: 1.55; }
    html[lang="sa"] body { line-height: 1.9; }
    html[lang="sa"] .skill-end { letter-spacing: 0; font-size: 12px; }
"""

# Burmese: no tracking or forced breaks inside syllable clusters (kinzi, stacked
# consonants, medials), lines broken at the phrase spaces, and tall lines so marks
# above and below are never clipped.
MYANMAR_CSS = r"""
    html[lang="my"] :is(h1, h2, h3, p, li, .eyebrow, .feature-index, .section-number, .skill-desc, .feature p, .button) { letter-spacing: normal; }
    html[lang="my"] :is(h1, h2, h3, p, li) { word-break: normal; overflow-wrap: normal; text-wrap: wrap; }
    html[lang="my"] .hero h1 { font-size: clamp(30px,4vw,58px); line-height: 1.7; }
    html[lang="my"] :is(.intro-text h2, .section-heading h2, .idea-band h2, .install-intro h2, .cta-layout h2) { line-height: 1.75; }
    html[lang="my"] :is(h3, .button, .skill-name, .platform-name) { line-height: 1.7; }
    html[lang="my"] body { line-height: 1.95; }
    html[lang="my"] .skill-end { letter-spacing: 0; font-size: 12px; }
    /* The header brand is set in Arial with negative tracking, which splits Burmese clusters. */
    .brand .brand-sub { letter-spacing: 0; font-family: "Myanmar Sangam MN", "Myanmar Text", "Noto Sans Myanmar", sans-serif; }
    @media (max-width: 560px) {
      html[lang="my"] .hero h1 { font-size: clamp(26px,7.4vw,38px); line-height: 1.7; }
    }
"""

# Right-to-left (as the Arabic and Persian editions): the canonical index CSS uses
# physical edges, so they are mirrored for dir="rtl"; Latin labels keep their order.
RTL_CSS = r"""
    html[lang="he"] :is(h1, h2, h3, p, .eyebrow, .feature-index, .section-number) { letter-spacing: 0; }
    html[lang="he"] .hero h1 { line-height: 1.3; }
    bdi { unicode-bidi: isolate; }
    .skill-name, .platform-name { direction: ltr; text-align: start; }
    html[dir="rtl"] :is(.feature-index, .skill-type, .platform-index, .status-title) { direction: ltr; unicode-bidi: isolate; text-align: right; }
    html[dir="rtl"] .header-nav { margin-left: 0; margin-right: auto; }
    html[dir="rtl"] .header-controls { margin-left: 0; margin-right: 16px; }
    html[dir="rtl"] .eyebrow .line { margin-right: 0; margin-left: 9px; }
    html[dir="rtl"] .arrow { margin-left: 0; margin-right: 12px; }
    html[dir="rtl"] :is(.arrow, .platform-arrow, .skill-end > span[aria-hidden]) { display: inline-block; transform: scaleX(-1); }
    html[lang="he"] .skill-end { letter-spacing: 0; font-size: 12px; }
    html[dir="rtl"] .feature { padding: 32px 0 36px 24px; }
    html[dir="rtl"] .feature:not(:first-child) { padding-left: 24px; padding-right: 25px; border-left: 0; border-right: 1px solid var(--line); }
    html[dir="rtl"] .status-meta { text-align: left; }
    html[dir="rtl"] .hero-stage::after { right: auto; left: -18px; }
    html[dir="rtl"] .stage-label { left: auto; right: 27px; }
    @media (max-width: 1080px) {
      html[dir="rtl"] .header-controls { margin-right: 0; }
      html[dir="rtl"] .feature { padding-left: 18px; }
      html[dir="rtl"] .feature:not(:first-child) { padding-right: 18px; }
    }
    @media (max-width: 790px) {
      html[dir="rtl"] .header-nav { margin: 0; }
      html[dir="rtl"] .header-controls { margin-right: auto; margin-left: 0; }
      html[dir="rtl"] .feature:nth-child(3) { border-right: 0; padding-right: 0; }
      html[dir="rtl"] .hero-stage::after { left: 10px; right: auto; }
    }
    @media (max-width: 560px) {
      html[dir="rtl"] .feature:not(:first-child) { padding-right: 14px; }
      html[dir="rtl"] .feature:nth-child(3) { padding-right: 0; }
      html[dir="rtl"] .status-meta { text-align: right; }
      html[dir="rtl"] .stage-label { right: 15px; }
    }
"""


@version_outputs
@seo_outputs
def outputs():
    copy = json.loads((ROOT / "assets" / "upcoming-site-copy.json").read_text(encoding="utf-8"))
    files = {}
    for code in EDITIONS:
        files.update({landing_path(code, lang): landing(code, lang, copy[code][lang]) for lang in langs(code)})
        files[f"assets/{EDITIONS[code][1]}-site.css"] = css(code)
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
        raise SystemExit("Stale upcoming edition pages: " + ", ".join(stale))
    print(f"Upcoming editions: {len(outputs())} files " + ("verified" if args.check else "built"))


if __name__ == "__main__":
    main()
