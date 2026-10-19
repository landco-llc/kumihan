#!/usr/bin/env python3
"""Build the KUMIHAN｜Mizani site (fr / en / ja); --check verifies committed output.

Landings follow the canonical KUMIHAN index (_layouts/landing.html) and install
guides use the shared install-guide frame (tools/install_frame.py). Copy lives
in assets/mizani-site-copy.json. Following kumihan-mizani-web, Swahili pages
declare lang="sw" and new Swahili copy uses the explicitly selected
id-standard house style; supplied text is reproduced byte for byte and
never normalized. Japanese copy follows kumihan-web.
"""
import argparse
import json
from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://landco-llc.github.io/kumihan/"
LOGO = "assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"
REPO = "https://github.com/landco-llc/kumihan"
SOURCE = REPO + "/tree/main/plugins/kumihan-mizani"
VERSION = "0.1.0"
RELEASE = REPO + f"/releases/tag/kumihan-sw-v{VERSION}"
DOWNLOAD = REPO + f"/releases/download/kumihan-sw-v{VERSION}/"
BRAND = 'KUMIHAN<span class="brand-sub">｜Mizani</span>'
LANGS = {"sw": "", "en": ".en", "ja": ".ja"}
LABELS = {"sw": "SW", "en": "EN", "ja": "日本語"}
OG = {"sw": "sw_TZ", "en": "en_US", "ja": "ja_JP"}
SKILLS = ("kumihan-mizani", "kumihan-mizani-web", "kumihan-mizani-documents", "kumihan-mizani-review")
SKILL_TYPES = ("01 / ENTRY", "02 / WEB", "03 / DOCUMENTS", "04 / REVIEW")
SKILL_SYMBOLS = ("ng’", "↗", "¶", "◎")
HOSTS = {"chatgpt": "ChatGPT / Codex", "claude": "Claude / Claude Code", "gemini": "Gemini"}
PLUGIN = {"chatgpt": "kumihan-mizani-chatgpt-codex-plugin", "claude": "kumihan-mizani-claude-code-plugin",
          "gemini": "kumihan-mizani-gemini-cli-extension"}
COMMANDS = {
    "chatgpt": [],
    "claude": ["claude --plugin-dir /absolute/path/kumihan-mizani",
               "claude plugin validate /absolute/path/kumihan-mizani",
               "/plugin marketplace add landco-llc/kumihan\n/plugin install kumihan-mizani@kumihan-marketplace"],
    "gemini": ["gemini extensions install /absolute/path/kumihan-mizani\ngemini extensions list"],
}
CHECK = "python runtime/checks.py input.txt --locale sw-TZ"
GATEWAY = {"sw": "top-sw.html", "en": "top-en.html", "ja": "index.html"}

_spec = spec_from_file_location("kumihan_install_frame", Path(__file__).with_name("install_frame.py"))
FRAME = module_from_spec(_spec)
_spec.loader.exec_module(FRAME)

OVERRIDES = r"""
    /* KUMIHAN｜Mizani (kumihan-mizani-web): lang="sw" with source protection
       avoids unverified automatic hyphenation; headings and identifiers are protected. */
    html[lang="sw"] body { line-break: auto; word-break: normal; }
    html[lang="sw"] :is(.hero-desc, .intro-text p, .feature p, .idea-band p, .skill-desc, .install-intro p, .status-box p, .cta-layout p) { hyphens: manual; word-break: normal; }
    html[lang="sw"] :is(h1, h2, h3, .brand, .skill-name, .platform-name, a) { hyphens: manual; }
    html:is([lang="sw"], [lang="en"]) .hero h1 { font-size: clamp(42px,4.9vw,72px); letter-spacing: -.05em; line-height: 1.12; text-wrap: balance; }
    html:is([lang="sw"], [lang="en"]) :is(.intro-text h2, .section-heading h2, .idea-band h2, .install-intro h2, .cta-layout h2) { letter-spacing: -.045em; line-height: 1.25; }
    html:is([lang="sw"], [lang="en"]) :is(h1, h2, h3, .eyebrow, .button, .feature p) { overflow-wrap: break-word; }
    html[lang="ja"] body { line-break: strict; }
    @supports (word-break: auto-phrase) {
      html[lang="ja"] :is(h2, h3) { word-break: auto-phrase; }
    }
    .brand .brand-sub { margin-inline-start: 2px; font-weight: 700; letter-spacing: -.02em; }
    .language-switch a { display: inline-flex; align-items: center; justify-content: center; min-height: 38px; min-width: 38px; border-radius: 40px; color: var(--muted); padding: 7px 10px; font-size: 11px; font-weight: 800; letter-spacing: .05em; }
    .language-switch a[aria-current="page"] { background: var(--ink); color: white; }
    .language-switch a:hover:not([aria-current="page"]) { color: var(--red-dark); background: #ebe7df; }
    .hero-stage::after { content: "KUMIHAN / SW"; }
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
      html:is([lang="sw"], [lang="en"]) .hero h1 { font-size: clamp(34px,9.6vw,46px); line-height: 1.16; }
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
    return f"kumihan-sw{LANGS[lang]}.html"


def guide_path(host, lang):
    return f"docs/install-mizani-{host}{LANGS[lang]}.html"


def landing(lang, c):
    page = landing_path(lang)
    alternates = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{landing_path(k)}">' for k in LANGS)
    head = (f"<title>{x(c['title'])}</title>\n<meta name=\"description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:type" content="website">\n<meta property="og:locale" content="{OG[lang]}">\n'
            f"<meta property=\"og:title\" content=\"{x(c['title'])}\">\n<meta property=\"og:description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:url" content="{BASE}{page}">\n<meta property="og:image" content="{BASE}{LOGO}">\n'
            f'<link rel="canonical" href="{BASE}{page}">\n{alternates}\n'
            f'<link rel="alternate" hreflang="x-default" href="{BASE}{landing_path("sw")}">\n'
            f'<link rel="icon" href="assets/favicon-32x32.png" type="image/png">\n<link rel="stylesheet" href="assets/mizani-site.css">')
    return SITE.landing(dict(
        lang=lang, head=head, brand=f"<span>{BRAND}</span>", home_label="KUMIHAN｜Mizani",
        languages=[(k, LABELS[k], landing_path(k), k == lang) for k in LANGS],
        logo=LOGO, repo=REPO, release=RELEASE, license=REPO + "/blob/main/LICENSE",
        skills=[(name, f"{SOURCE}/skills/{name}", SKILL_SYMBOLS[i]) for i, name in enumerate(SKILLS)],
        hosts=[(name, guide_path(host, lang)) for host, name in HOSTS.items()],
        gateway=(GATEWAY[lang], c["gateway_label"]), family=c["family"]), c)


def guide(host, lang, c):
    g = c["guide"]
    path = guide_path(host, lang)
    title = g["title"].format(host=HOSTS[host])
    alternates = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{guide_path(host, k)}">' for k in LANGS)
    head = (f'<title>{x(title)}</title>\n<meta name="description" content="{x(g["lead"])}">\n'
            f'<link rel="canonical" href="{BASE}{path}">{alternates}<link rel="alternate" hreflang="x-default" href="{BASE}{guide_path(host, "sw")}">\n'
            f'<meta property="og:type" content="website"><meta property="og:locale" content="{OG[lang]}"><meta property="og:title" content="{x(title)}">'
            f'<meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}{LOGO}">\n'
            f'<link rel="icon" href="../assets/favicon-32x32.png" type="image/png">')
    assets = [PLUGIN[host]] + [f"{name}-{host}-skill" for name in SKILLS]
    downloads = "".join(
        f'<li><a href="{DOWNLOAD}{name}-v{VERSION}.zip">{x(g["plugin"] if i == 0 else g["skill"])}: {name}-v{VERSION}.zip</a></li>'
        for i, name in enumerate(assets))
    commands = "".join(f"<pre><code>{x(cmd)}</code></pre>" for cmd in COMMANDS[host])
    ids = ("format", "download", "steps", "test", "updates", "limits")
    bodies = (
        f'<p>{x(g["format"])}</p>',
        f'<p>{x(g["download"])}</p><ul class="download-list">{downloads}</ul>'
        f'<p><a href="{DOWNLOAD}SHA256SUMS.txt">SHA256SUMS.txt</a> · <a href="{DOWNLOAD}MANIFEST.json">MANIFEST.json</a> · <a href="{RELEASE}">GitHub Release v{VERSION}</a></p>',
        f'<p>{x(g[host])}</p>{commands}<p><a href="{SOURCE}/INSTALL.md">INSTALL.md</a></p>',
        f'<p>{x(g["test"])}</p><blockquote><p>{x(g["prompt"])}</p></blockquote><p>{x(g["check"])}</p><pre><code>{x(CHECK)}</code></pre>',
        f'<p>{x(g["update"])}</p>',
        f'<p class="note">{x(g["limits"])}</p>',
    )
    content = "".join(f'<section id="{i}"><h2>{n + 1:02d} / {x(s)}</h2>{b}</section>'
                      for n, (i, s, b) in enumerate(zip(ids, g["sections"], bodies)))
    ui = dict(g, skip=c["skip"], language=c["lang_label"], source_href=SOURCE + "/INSTALL.md")
    frame = FRAME.Frame(
        lang=lang, head=head, css="../assets/kumihan-install.css", asset_root="../", brand=BRAND,
        home="../" + landing_path(lang),
        hosts=[(name.split(" / ")[0] if h == "claude" else name, guide_path(h, lang).removeprefix("docs/"), h == host)
               for h, name in HOSTS.items()],
        languages=[(k, LABELS[k] if k != "sw" else "Kiswahili", guide_path(host, k).removeprefix("docs/"), k == lang) for k in LANGS],
        number=f"0{list(HOSTS).index(host) + 1}", title=x(title), description=x(g["lead"]),
        toc=list(zip(ids, g["sections"])), content=content, platform=HOSTS[host], ui=ui,
        footer_sub=x(c["footer_sub"]) + f"<br>v{VERSION} · Apache-2.0 · Developed by L&amp;Co. LLC",
        footer_links=[("GitHub", SOURCE, True), ("Apache-2.0", REPO + "/blob/main/LICENSE", True)],
        gateway=("../" + GATEWAY[lang], c["gateway_label"]))
    return FRAME.render(frame)


def outputs():
    copy = json.loads((ROOT / "assets" / "mizani-site-copy.json").read_text(encoding="utf-8"))
    files = {landing_path(lang): landing(lang, copy[lang]) for lang in LANGS}
    files.update({guide_path(host, lang): guide(host, lang, copy[lang]) for host in HOSTS for lang in LANGS})
    files["assets/mizani-site.css"] = SITE.canonical_css("KUMIHAN｜Mizani index: canonical KUMIHAN index CSS + Mizani settings.", OVERRIDES)
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
        raise SystemExit("Stale Mizani site files: " + ", ".join(stale))
    print(f"Mizani site: {len(outputs())} files " + ("verified" if args.check else "built"))


if __name__ == "__main__":
    main()
