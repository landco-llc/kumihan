#!/usr/bin/env python3
"""Hindi site: canonical product_site/install_frame, editable hi-site-copy, master JA/EN parity."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_adapter import seo_outputs
import argparse
import json
from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://landco-llc.github.io/kumihan/"
LOGO = "assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"
REPO = "https://github.com/landco-llc/kumihan"
SOURCE = REPO + "/tree/main/plugins/kumihan-hi"
VERSION = "0.1.0"
RELEASE = REPO + f"/releases/tag/kumihan-hi-v{VERSION}"
DOWNLOAD = REPO + f"/releases/download/kumihan-hi-v{VERSION}/"
BRAND = 'KUMIHAN<span class="brand-sub">｜अक्षर-संगति</span>'
LANGS = {"hi": "", "en": ".en", "ja": ".ja"}
LABELS = {"hi": "हिन्दी", "en": "EN", "ja": "日本語"}
OG = {"hi": "hi_IN", "en": "en_US", "ja": "ja_JP"}
SKILLS = ("kumihan-hi", "kumihan-hi-web", "kumihan-hi-documents", "kumihan-hi-review")
SKILL_TYPES = ("01 / ENTRY", "02 / WEB", "03 / DOCUMENTS", "04 / REVIEW")
SKILL_SYMBOLS = ("«»", "↗", "¶", "◎")
HOSTS = {"chatgpt": "ChatGPT / Codex", "claude": "Claude / Claude Code", "gemini": "Gemini"}
PLUGIN = {"chatgpt": "kumihan-hi-chatgpt-codex-plugin", "claude": "kumihan-hi-claude-code-plugin",
          "gemini": "kumihan-hi-gemini-cli-extension"}
COMMANDS = {
    "chatgpt": [],
    "claude": ["claude plugin validate /absolute/path/kumihan-hi", "claude --plugin-dir /absolute/path/kumihan-hi"],
    "gemini": ["gemini extensions install /absolute/path/kumihan-hi\ngemini extensions list"],
}
CHECK = "python runtime/checks.py original.txt --candidate candidate.txt"
GATEWAY = {"hi": "top-hi.html", "en": "top-en.html", "ja": "index.html"}

_spec = spec_from_file_location("kumihan_install_frame", Path(__file__).with_name("install_frame.py"))
FRAME = module_from_spec(_spec)
_spec.loader.exec_module(FRAME)

OVERRIDES = r"""
@font-face { font-family: "Kumihan Devanagari"; src: url("fonts/NotoSansDevanagari.ttf") format("truetype"); font-weight: 100 900; font-style: normal; font-display: swap; }
body { font-family: "Kumihan Devanagari", "Noto Sans Devanagari", "Noto Sans JP", sans-serif; }
:lang(hi), .brand, .brand-sub, .footer-mark { letter-spacing: normal !important; word-break: normal; overflow-wrap: normal; line-height: 1.65; }
html[lang="hi"] :is(h1,h2,h3) { letter-spacing: normal; line-height: 1.5; }
html[lang="hi"] .hero h1 { font-size: clamp(32px,4.4vw,64px); }
.brand .brand-sub { display: inline-block; font-weight: 700; }
.brand { min-width: 0; max-width: 100%; white-space: normal; }
.header-content, .header-nav { flex-wrap: wrap; row-gap: 12px; }
.hero-foot { flex-wrap: wrap; }
.hero-stage::after { content: "KUMIHAN / HI"; }
.hero-copy, .hero-stage, .feature, .skill-card, .platform-info, .install-layout > *, .idea-layout > *, .cta-layout > * { min-width: 0; }
.skill-name, .skill-name bdi { overflow-wrap: anywhere !important; }
.feature-motif { font-family: "Kumihan Devanagari", "Noto Sans Devanagari", sans-serif !important; line-height: 1.8; height: auto; min-height: 80px; padding-block: .2em; letter-spacing: normal !important; }
.language-switch a { display: inline-flex; min-height: 38px; padding: 7px 10px; }
.language-switch a[aria-current="page"] { background: var(--ink); color: white; border-radius: 30px; }
.status-meta { white-space: normal; }
.status-meta a { color: var(--red-dark); }
html[lang="ja"] body { line-break: strict; }
html[lang="en"] .hero h1 { font-size: clamp(34px,4.4vw,64px); line-height: 1.25; }
@media(max-width:560px) { .header-nav { gap: 12px; } .header-nav a { white-space: normal; } .idea-layout { grid-template-columns: minmax(0,1fr); } .brand { font-size: 20px; } .hero h1 { font-size: 34px; } }
"""


_ps_spec = spec_from_file_location("kumihan_product_site", Path(__file__).with_name("product_site.py"))
SITE = module_from_spec(_ps_spec)
_ps_spec.loader.exec_module(SITE)
x = SITE.x


def landing_path(lang):
    return f"kumihan-hi{LANGS[lang]}.html"


def guide_path(host, lang):
    return f"docs/install-kumihan-hi-{host}{LANGS[lang]}.html"


def landing(lang, c):
    page = landing_path(lang)
    alternates = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{landing_path(k)}">' for k in LANGS)
    head = (f"<title>{x(c['title'])}</title>\n<meta name=\"description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:type" content="website">\n<meta property="og:locale" content="{OG[lang]}">\n'
            f"<meta property=\"og:title\" content=\"{x(c['title'])}\">\n<meta property=\"og:description\" content=\"{x(c['description'])}\">\n"
            f'<meta property="og:url" content="{BASE}{page}">\n<meta property="og:image" content="{BASE}{LOGO}">\n'
            f'<link rel="canonical" href="{BASE}{page}">\n{alternates}\n'
            f'<link rel="alternate" hreflang="x-default" href="{BASE}{landing_path("hi")}">\n'
            f'<link rel="icon" href="assets/favicon-32x32.png" type="image/png">\n<link rel="stylesheet" href="assets/hi-site.css">')
    return SITE.landing(dict(
        lang=lang, dir="ltr", head=head, brand=f"<span>{BRAND}</span>", home_label="KUMIHAN｜अक्षर-संगति",
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
            f'<link rel="canonical" href="{BASE}{path}">{alternates}<link rel="alternate" hreflang="x-default" href="{BASE}{guide_path(host, "hi")}">\n'
            f'<meta property="og:type" content="website"><meta property="og:locale" content="{OG[lang]}"><meta property="og:title" content="{x(title)}">'
            f'<meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}{LOGO}">\n'
            f'<link rel="icon" href="../assets/favicon-32x32.png" type="image/png"><link rel="stylesheet" href="../assets/hi-install.css">')
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
        lang=lang, dir="ltr", head=head, css="../assets/kumihan-install.css", asset_root="../", brand=BRAND,
        home="../" + landing_path(lang),
        hosts=[(name.split(" / ")[0] if h == "claude" else name, guide_path(h, lang).removeprefix("docs/"), h == host)
               for h, name in HOSTS.items()],
        languages=[(k, LABELS[k] if k != "hi" else "हिंदी", guide_path(host, k).removeprefix("docs/"), k == lang) for k in LANGS],
        number=f"0{list(HOSTS).index(host) + 1}", title=x(title), description=x(g["lead"]),
        toc=list(zip(ids, g["sections"])), content=content, platform=HOSTS[host], ui=ui,
        footer_sub=x(c["footer_sub"]) + f"<br>v{VERSION} · Apache-2.0 · Developed by L&amp;Co. LLC",
        footer_links=[("GitHub", SOURCE, True), ("Apache-2.0", REPO + "/blob/main/LICENSE", True)],
        gateway=("../" + GATEWAY[lang], c["gateway_label"]))
    return FRAME.render(frame)


@seo_outputs
def outputs():
    copy = json.loads((ROOT / "assets" / "hi-site-copy.json").read_text(encoding="utf-8"))
    files = {landing_path(lang): landing(lang, copy[lang]) for lang in LANGS}
    files.update({guide_path(host, lang): guide(host, lang, copy[lang]) for host in HOSTS for lang in LANGS})
    files["assets/hi-site.css"] = SITE.canonical_css("KUMIHAN｜अक्षर-संगति index: canonical KUMIHAN index CSS + अक्षर-संगति settings.", OVERRIDES)
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
        raise SystemExit("Stale अक्षर-संगति site files: " + ", ".join(stale))
    print(f"अक्षर-संगति site: {len(outputs())} files " + ("verified" if args.check else "built"))


if __name__ == "__main__":
    main()
