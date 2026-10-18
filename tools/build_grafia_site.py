#!/usr/bin/env python3
"""Build the KUMIHAN｜Grafía site (es / en / ja); --check verifies committed output.

Landings follow the canonical KUMIHAN index (_layouts/landing.html) and install
guides use the shared install-guide frame (tools/install_frame.py). Copy lives
in assets/grafia-site-copy.json; its ja/en copy is the shared KUMIHAN copy
(tools/base_copy.py). Following kumihan-grafia-web, Spanish pages declare
lang="es", emit only es/en/ja alternates (no es-419), never hide overflow, and
do not rely on hyphens:auto or break-all; supplied text is reproduced byte for
byte. Japanese copy follows kumihan-web.
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
SOURCE = REPO + "/tree/main/plugins/kumihan-grafia"
VERSION = "0.1.0"
RELEASE = REPO + f"/releases/tag/kumihan-grafia-v{VERSION}"
# The release files are also committed with the plugin; guides link to those copies.
DOWNLOAD = "../plugins/kumihan-grafia/downloads/"
BRAND = 'KUMIHAN<span class="brand-sub">｜Grafía</span>'
LANGS = {"es": "", "en": ".en", "ja": ".ja"}
LABELS = {"es": "ES", "en": "EN", "ja": "日本語"}
OG = {"es": "es_ES", "en": "en_US", "ja": "ja_JP"}
SKILLS = ("kumihan-grafia", "kumihan-grafia-web", "kumihan-grafia-documents", "kumihan-grafia-review")
SKILL_TYPES = ("01 / ENTRY", "02 / WEB", "03 / DOCUMENTS", "04 / REVIEW")
SKILL_SYMBOLS = ("¿?", "↗", "¶", "◎")
HOSTS = {"chatgpt": "ChatGPT / Codex", "claude": "Claude / Claude Code", "gemini": "Gemini"}
# (plugin, skill) asset names per host; skill ZIPs are kumihan-grafia{-web,...}-{skill}-v0.1.0.zip.
ASSETS = {"chatgpt": ("GPT-Codex-plugin", "GPT-Codex-skill"), "claude": ("Claude-Code-plugin", "Claude-skill"),
          "gemini": ("Gemini-CLI-extension", "Gemini-Apps-skill")}
COMMANDS = {
    "chatgpt": ["mkdir -p .agents/skills"],
    "claude": ["claude plugin validate /absolute/path/kumihan-grafia",
               "claude --plugin-dir /absolute/path/kumihan-grafia"],
    "gemini": ["gemini extensions install /absolute/path/to/folder\ngemini extensions list"],
}
VERIFY = "sha256sum -c SHA256SUMS.txt"
CHECK = "python runtime/checks.py original.txt --locale es --candidate candidate.txt"
# Spanish has no KUMIHAN index of its own yet, so it returns to the Japanese index.
GATEWAY = {"es": "index.html", "en": "top-en.html", "ja": "index.html"}

_spec = spec_from_file_location("kumihan_install_frame", Path(__file__).with_name("install_frame.py"))
FRAME = module_from_spec(_spec)
_spec.loader.exec_module(FRAME)

OVERRIDES = r"""
    /* KUMIHAN｜Grafía (kumihan-grafia-web): lang="es"; no break-all, no reliance on
       hyphens:auto, no hidden overflow. Long words wrap only where they must. */
    html[lang="es"] body { line-break: auto; }
    html:is([lang="es"], [lang="en"]) .hero h1 { font-size: clamp(42px,4.9vw,72px); letter-spacing: -.05em; line-height: 1.12; text-wrap: balance; }
    html:is([lang="es"], [lang="en"]) :is(.intro-text h2, .section-heading h2, .idea-band h2, .install-intro h2, .cta-layout h2) { letter-spacing: -.045em; line-height: 1.25; }
    html:is([lang="es"], [lang="en"]) :is(h1, h2, h3, .eyebrow, .button, .feature p) { overflow-wrap: break-word; }
    html[lang="ja"] body { line-break: strict; }
    @supports (word-break: auto-phrase) {
      html[lang="ja"] :is(h2, h3) { word-break: auto-phrase; }
    }
    .brand .brand-sub { margin-inline-start: 2px; font-weight: 700; letter-spacing: -.02em; }
    .language-switch a { display: inline-flex; align-items: center; justify-content: center; min-height: 38px; min-width: 38px; border-radius: 40px; color: var(--muted); padding: 7px 10px; font-size: 11px; font-weight: 800; letter-spacing: .05em; }
    .language-switch a[aria-current="page"] { background: var(--ink); color: white; }
    .language-switch a:hover:not([aria-current="page"]) { color: var(--red-dark); background: #ebe7df; }
    .hero-stage::after { content: "KUMIHAN / ES"; }
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
      html:is([lang="es"], [lang="en"]) .hero h1 { font-size: clamp(34px,9.6vw,46px); line-height: 1.16; }
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
    return f"kumihan-es{LANGS[lang]}.html"


def guide_path(host, lang):
    return f"docs/install-grafia-{host}{LANGS[lang]}.html"


def landing(lang, c):
    page = landing_path(lang)
    alternates = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{landing_path(k)}">' for k in LANGS)
    head = (f"<title>{x(c['title'])}</title>\n<meta name=\"description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:type" content="website">\n<meta property="og:locale" content="{OG[lang]}">\n'
            f"<meta property=\"og:title\" content=\"{x(c['title'])}\">\n<meta property=\"og:description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:url" content="{BASE}{page}">\n<meta property="og:image" content="{BASE}{LOGO}">\n'
            f'<link rel="canonical" href="{BASE}{page}">\n{alternates}\n'
            f'<link rel="alternate" hreflang="x-default" href="{BASE}{landing_path("es")}">\n'
            f'<link rel="icon" href="assets/favicon-32x32.png" type="image/png">\n<link rel="stylesheet" href="assets/grafia-site.css">')
    return SITE.landing(dict(
        lang=lang, head=head, brand=f"<span>{BRAND}</span>", home_label="KUMIHAN｜Grafía",
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
            f'<link rel="canonical" href="{BASE}{path}">{alternates}<link rel="alternate" hreflang="x-default" href="{BASE}{guide_path(host, "es")}">\n'
            f'<meta property="og:type" content="website"><meta property="og:locale" content="{OG[lang]}"><meta property="og:title" content="{x(title)}">'
            f'<meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}{LOGO}">\n'
            f'<link rel="icon" href="../assets/favicon-32x32.png" type="image/png">')
    plugin, skill = ASSETS[host]
    assets = [f"kumihan-grafia-{plugin}"] + [f"{name}-{skill}" for name in SKILLS]
    downloads = "".join(
        f'<li><a href="{DOWNLOAD}{name}-v{VERSION}.zip">{x(g["plugin"] if i == 0 else g["skill"])}: {name}-v{VERSION}.zip</a></li>'
        for i, name in enumerate(assets))
    commands = "".join(f"<pre><code>{x(cmd)}</code></pre>" for cmd in COMMANDS[host])
    ids = ("format", "download", "steps", "test", "updates", "limits")
    bodies = (
        f'<p>{x(g["format"])}</p>',
        f'<p>{x(g["download"])}</p><pre><code>{x(VERIFY)}</code></pre><ul class="download-list">{downloads}</ul>'
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
        languages=[(k, LABELS[k] if k != "es" else "Español", guide_path(host, k).removeprefix("docs/"), k == lang) for k in LANGS],
        number=f"0{list(HOSTS).index(host) + 1}", title=x(title), description=x(g["lead"]),
        toc=list(zip(ids, g["sections"])), content=content, platform=HOSTS[host], ui=ui,
        footer_sub=x(c["footer_sub"]) + f"<br>v{VERSION} · Apache-2.0 · Developed by L&amp;Co. LLC",
        footer_links=[("GitHub", SOURCE, True), ("Apache-2.0", REPO + "/blob/main/LICENSE", True)],
        gateway=("../" + GATEWAY[lang], c["gateway_label"]))
    return FRAME.render(frame)


def outputs():
    """The twelve pages (three landings, nine guides)."""
    copy = json.loads((ROOT / "assets" / "grafia-site-copy.json").read_text(encoding="utf-8"))
    files = {landing_path(lang): landing(lang, copy[lang]) for lang in LANGS}
    files.update({guide_path(host, lang): guide(host, lang, copy[lang]) for host in HOSTS for lang in LANGS})
    return files


def all_outputs():
    files = outputs()
    files["assets/grafia-site.css"] = SITE.canonical_css("KUMIHAN｜Grafía index: canonical KUMIHAN index CSS + Grafía settings.", OVERRIDES)
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for name, content in all_outputs().items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale Grafía site files: " + ", ".join(stale))
    print(f"Grafía site: {len(all_outputs())} files " + ("verified" if args.check else "built"))


if __name__ == "__main__":
    main()
