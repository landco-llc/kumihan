#!/usr/bin/env python3
"""Build every language edition's installation guides from one template; --check verifies.

The Japanese guide (docs/installation*.ja.md, rendered by _layouts/installation.html) is
the standard. Its text is kept as a template per page language in
templates/install-guide/<lang>/{chatgpt,claude,gemini}.md with ui.json for the page frame;
English is templates/install-guide/en. Each edition fills the template with its own data:
brand, version, Release ZIPs (assets/edition-versions.json), plugin and skill names,
the top-level folder of each ZIP (templates/install-guide/zip-layout.json) and whether
its Claude Code plugin is in the KUMIHAN marketplace. Pages use the shared install
frame (tools/install_frame.py), which mirrors the Japanese layout.

A new edition needs: its landing pages, a release (or source ZIPs) and, for its own
language, a translated templates/install-guide/<code>/ (copy ja/ and keep every {{marker}}).

Template markers: {{name}} values; lines {{#if name}} / {{else}} / {{/if}}; list blocks
{{skills_list}}, {{skills_list_indented}}, {{claude_commands}}, {{gemini_paths}}.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_adapter import seo_outputs
from version_display import version_outputs
import argparse
import json
import re
from html import escape
from urllib.parse import quote
from importlib.util import module_from_spec, spec_from_file_location

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://landco-llc.github.io/kumihan/"
REPO = "https://github.com/landco-llc/kumihan"
TEMPLATES = ROOT / "templates" / "install-guide"
HOSTS = ("chatgpt", "claude", "gemini")
HOST_NAMES = {"chatgpt": "ChatGPT / Codex", "claude": "Claude", "gemini": "Gemini"}
SKILLS = ("base", "web", "documents", "review")
# Existing address prefix of each edition's guides (docs/install-<prefix>-<host>[.en|.ja].html;
# 字衡's ChatGPT guide has no host suffix).
PAGES = {
    "en": "measure",
    "ar": "kumihan-ar", "bn": "kumihan-bn", "fa": "kumihan-fa", "hi": "kumihan-hi", "th": "kumihan-th",
    "de": "satzbild", "es": "grafia", "fr": "accord", "id": "laras", "it": "equilibrio", "km": "lumnung",
    "ko": "ko", "pl": "szyk", "pt": "compasso", "ru": "lad", "sw": "mizani", "vi": "nhip-chu",
    "zh-hans": "zilu", "zh-hant": "ziheng", "zu": "hlela",
    "sa": "vinyasa", "my": "kumihan-my", "tl": "tugma", "fi": "rytmi", "sv": "samspel",
    "da": "samklang-da", "no": "samklang-no", "uk": "mira-uk",
    "tr": "ahenk", "ms": "jalin", "hu": "arany", "cs": "soulad", "la": "concinnitas", "he": "miktsav", "el": "metro", "nl": "zetwerk",
}
RTL = {"ar", "fa", "he"}

_load = lambda name, file: (lambda s: (s.loader.exec_module(m := module_from_spec(s)), m)[1])(
    spec_from_file_location(name, Path(__file__).with_name(file)))
FRAME = _load("kumihan_install_frame", "install_frame.py")
GATEWAYS = _load("kumihan_build_gateways", "build_gateways.py")
SZYK = _load("kumihan_build_szyk", "build_szyk_site.py")
import edition_versions as V  # noqa: E402


def x(value):
    return escape(str(value), quote=True)


# ---------------------------------------------------------------- edition data

def classify(name, slug):
    """(host, kind, skill) of a ZIP name; host None means ChatGPT/Codex (or shared skills)."""
    stem = re.sub(r"-v?\d+\.\d+\.\d+(?:-preview)?\.zip$", "", name.lower())
    host = ("chatgpt" if re.search(r"chatgpt|gpt-codex|openai-codex", stem) else
            "claude" if "claude" in stem else "gemini" if "gemini" in stem else None)
    kind = "plugin" if re.search(r"plugin|bundle|extension", stem) else "skill"
    rest = stem.replace(slug, "", 1)
    skill = next((s for s in ("documents", "review", "web") if re.search(rf"(^|-){s}(-|$)", rest)), "base")
    return host, kind, None if kind == "plugin" else skill


def guide_path(code, host, lang):
    prefix = PAGES[code]
    sfx = "" if lang == code else f".{lang}"
    name = (f"install-{prefix}{sfx}.html" if host == "chatgpt" else f"install-{prefix}-{host}{sfx}.html") \
        if code == "zh-hant" else f"install-{prefix}-{host}{sfx}.html"
    return "docs/" + name


def edition(code):
    spec = V.catalogue()[code]
    facts = V.load()["editions"][code]
    slug = spec["product"]
    plugin_dir = ROOT / "plugins" / slug
    product = GATEWAYS.PRODUCTS[code]
    layout = json.loads((TEMPLATES / "zip-layout.json").read_text(encoding="utf-8"))["archives"]
    if facts["release_status"] == "published":
        version = facts["published_version"]
        archives = [(a["name"], a["url"]) for a in facts["verified_assets"]]
        release = facts["release_url"]
        sums = next(m["url"] for m in facts["verified_metadata"] if m["name"] == "SHA256SUMS.txt")
    elif code in {"tr", "ms", "hu", "cs", "la", "he", "el", "nl",
                 "sa", "my", "tl", "fi", "sv", "da", "no", "uk"}:
        # Product-local 0.1.0 manifests are tracked as lowercase manifest.json.
        # OS/filesystem case sensitivity MUST NOT change the generated installation pages.
        version = facts["source_version"]
        manifest = json.loads((plugin_dir / "downloads" / "manifest.json").read_text(encoding="utf-8"))
        archives = [(row["file"], f"../plugins/{slug}/downloads/{row['file']}") for row in manifest["packages"]]
        release = f"{REPO}/tree/main/plugins/{slug}/downloads"
        if code in {"tr", "ms", "hu", "cs", "la", "he", "el", "nl"}:
            sums = f"../plugins/{slug}/downloads/SHA256SUMS"
        else:
            sums = {h: f"../plugins/{slug}/downloads/SHA256SUMS-{suffix}"
                    for h, suffix in (("chatgpt", "gpt-codex"), ("claude", "claude"), ("gemini", "gemini"))}
    elif (plugin_dir / "downloads" / "MANIFEST.json").exists():  # source packages in the repository (no GitHub Release yet)
        version = facts["source_version"]
        manifest = json.loads((plugin_dir / "downloads" / "MANIFEST.json").read_text(encoding="utf-8"))
        archives = [(Path(r["file"]).name, f"../plugins/{slug}/downloads/{r['file']}") for r in manifest.get("archives", manifest.get("packages", []))]
        release = f"{REPO}/tree/main/plugins/{slug}/downloads"
        sums = f"../plugins/{slug}/downloads/" + ("SHA256SUMS.txt" if (plugin_dir / "downloads" / "SHA256SUMS.txt").exists() else "SHA256SUMS")
    elif not (plugin_dir / "downloads").exists():  # packages in the shared downloads <Host>/ folders (English)
        version = facts["source_version"]
        folders = {"chatgpt": "downloads GPT-Codex", "claude": "downloads Claude", "gemini": "downloads Gemini"}
        archives = [(p.name, "../" + quote(f"{folder}/{p.name}")) for folder in folders.values()
                    for p in sorted((ROOT / folder).glob(f"{slug}-*.zip"))]
        release = f"{REPO}/tree/main/" + quote(folders["chatgpt"])
        sums = {h: "../" + quote(f"{folder}/{slug}-v{version}-SHA256SUMS.txt") for h, folder in folders.items()}
    else:  # offline consumer packages (downloads/manifest.json) with one checksum file per host
        version = facts["source_version"]
        manifest = json.loads((plugin_dir / "downloads" / "manifest.json").read_text(encoding="utf-8"))
        archives = [(r["file"], f"../plugins/{slug}/downloads/{r['file']}") for r in manifest["packages"]]
        release = f"{REPO}/tree/main/plugins/{slug}/downloads"
        sums = {h: f"../plugins/{slug}/downloads/SHA256SUMS-{f}" for h, f in
                (("chatgpt", "gpt-codex"), ("claude", "claude"), ("gemini", "gemini"))}
    hosts = {h: {"plugin": None, "skills": {}} for h in HOSTS}
    shared = {}
    for name, url in archives:
        host, kind, skill = classify(name, slug)
        entry = (name, url, layout.get(name, slug if kind == "plugin" else None))
        if host is None and kind == "skill":
            shared[skill] = entry
            continue
        target = hosts[host or "chatgpt"]
        if kind == "plugin":
            target["plugin"] = entry
        else:
            target["skills"][skill] = entry
    # Host-less skill ZIPs are ChatGPT/Codex's, or the only skill ZIPs for every host (bn).
    for h in HOSTS:
        if h == "chatgpt" or not hosts[h]["skills"]:
            for s, entry in shared.items():
                hosts[h]["skills"].setdefault(s, entry)
    skill_names = {s: f"{slug}-{s}" if s != "base" else slug for s in SKILLS}
    codex = json.loads((plugin_dir / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    marketplace = {p["name"] for p in json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())["plugins"]}
    return dict(code=code, slug=slug, brand=product["brand"], version=version, release=release, sums=sums,
                hosts=hosts, skills=skill_names, marketplace=slug in marketplace,
                display=codex.get("interface", {}).get("displayName") or codex.get("displayName") or product["brand"])


# ---------------------------------------------------------------- template

def fill(text, values, flags):
    """Resolve {{#if}} blocks, then {{markers}}."""
    out, stack = [], []
    for line in text.split("\n"):
        s = line.strip()
        if m := re.fullmatch(r"\{\{#if (\w+)\}\}", s):
            stack.append(bool(flags.get(m.group(1))))
            continue
        if s == "{{else}}":
            stack[-1] = not stack[-1]
            continue
        if s == "{{/if}}":
            stack.pop()
            continue
        if all(stack):
            out.append(line)
    text = "\n".join(out)

    def value(m):
        key = m.group(1)
        if key not in values:
            raise KeyError(f"Unknown template marker: {key}")
        return values[key]
    return re.sub(r"\{\{(\w+)\}\}", value, text)


def inline(text):
    """Escape, then `code`, **bold** and [text](url) (code spans are kept literal)."""
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            out.append(f"<code>{x(part[1:-1])}</code>")
            continue
        s = x(part)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: link(m.group(1), m.group(2)), s)
        out.append(s)
    return "".join(out)


def link(label, href):
    href = href.replace("&amp;", "&")
    external = href.startswith("http")
    attrs = ' target="_blank" rel="noopener noreferrer"' if external and "releases/download" not in href else ""
    return f'<a href="{x(href)}"{attrs}>{label}</a>'


def heading_id(text, n):
    m = re.match(r"([A-Z])\.", text)
    if m:
        return m.group(1).lower()
    m = re.match(r"(\d+)\.", text)
    return f"step-{m.group(1)}" if m else f"section-{n}"


def render_md(md):
    """Markdown subset used by the guides -> (HTML, [(id, heading)])."""
    lines = md.split("\n")
    html, toc, i = [], [], 0

    def block(lines, base_indent=0):
        out, j = [], 0
        while j < len(lines):
            line = lines[j]
            s = line.strip()
            ind = len(line) - len(line.lstrip())
            if not s:
                j += 1
                continue
            if s.startswith("```"):
                lang = s[3:].strip()
                code, j = [], j + 1
                while not lines[j].strip().startswith("```"):
                    code.append(lines[j][ind:] if lines[j][:ind].strip() == "" else lines[j])
                    j += 1
                j += 1
                cls = f' class="language-{x(lang)}"' if lang else ""
                out.append(f"<pre><code{cls}>{x(chr(10).join(code))}</code></pre>")
                continue
            if s.startswith(">"):
                quote = []
                while j < len(lines) and lines[j].strip().startswith(">"):
                    quote.append(lines[j].strip()[1:].strip())
                    j += 1
                out.append("<blockquote><p>" + "\n".join(inline(q) for q in quote) + "</p></blockquote>")
                continue
            if s.startswith("|"):
                rows = []
                while j < len(lines) and lines[j].strip().startswith("|"):
                    rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                    j += 1
                head, body = rows[0], [r for r in rows[2:]]
                out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
                           + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
                           + "</tbody></table>")
                continue
            m = re.match(r"(\s*)(\d+\.|-) (.*)", line)
            if m:
                ordered = m.group(2) != "-"
                items, k = [], j
                while k < len(lines):
                    mm = re.match(r"(\s*)(\d+\.|-) (.*)", lines[k])
                    if mm and len(mm.group(1)) == ind and (mm.group(2) != "-") == ordered:
                        body, k = [mm.group(3)], k + 1
                        while k < len(lines) and (not lines[k].strip() or len(lines[k]) - len(lines[k].lstrip()) > ind):
                            body.append(lines[k])
                            k += 1
                        items.append(body)
                        continue
                    break
                j = k
                tag = "ol" if ordered else "ul"
                parts = []
                for body in items:
                    first, rest = body[0], body[1:]
                    while rest and not rest[-1].strip():
                        rest.pop()
                    inner = block(rest) if rest else ""
                    parts.append(f"<li>{inline(first)}{inner}</li>")
                out.append(f"<{tag}>" + "".join(parts) + f"</{tag}>")
                continue
            if s == "---":
                out.append("<hr>")
                j += 1
                continue
            para = [s]
            j += 1
            while j < len(lines) and lines[j].strip() and not re.match(r"\s*(\d+\.|-) |\s*[>|#`]", lines[j]) \
                    and lines[j].strip() != "---":
                para.append(lines[j].strip())
                j += 1
            out.append("<p>" + inline(" ".join(para)) + "</p>")
        return "".join(out)

    chunk, n = [], 0
    for line in lines + ["## "]:
        if line.startswith("## "):
            if chunk:
                html.append(block(chunk))
            chunk = []
            title = line[3:].strip()
            if title:
                n += 1
                hid = heading_id(title, n)
                toc.append((hid, re.sub(r"\*\*|`", "", title)))
                html.append(f'<h2 id="{hid}">{inline(title)}</h2>')
            continue
        chunk.append(line)
    return "".join(html), toc


# ---------------------------------------------------------------- pages

def page_lang_attr(code, lang):
    if lang != code:
        return lang
    landing = (ROOT / GATEWAYS.PRODUCTS[code]["pages"][code]).read_text(encoding="utf-8")
    # 글짜임's landing is a Jekyll source: its language is in the front matter.
    return (re.search(r'<html lang="([^"]+)"', landing) or re.search(r"^lang: (\S+)", landing, re.M)).group(1)


# Brand markup of editions whose landing header shows only "KUMIHAN", is a Jekyll source,
# or uses landing-only classes (字律).
BRANDS = {"th": 'KUMIHAN<span class="brand-sub" lang="th">｜ดุลอักษร</span>',
          "zh-hans": 'KUMIHAN<span class="brand-sub" lang="zh-Hans-CN">｜字律</span>',
          "ko": 'KUMIHAN<span class="brand-sub" lang="ko-KR">｜글짜임</span>'}


def brand_html(code, name):
    """The edition's approved header brand: the one on its landing page."""
    if code in BRANDS:
        return BRANDS[code]
    landing = (ROOT / GATEWAYS.PRODUCTS[code]["pages"][code]).read_text(encoding="utf-8")
    m = re.search(r'<a class="brand"[^>]*>(.*?)</a>', landing, re.S)
    inner = re.sub(r"<img\b[^>]*>", "", m.group(1)).strip() if m else ""
    return inner if "｜" in inner else x(name)


def sums(ed, host):
    """Checksum file for a host's guide: one SHA256SUMS for the edition, or one per host."""
    return ed["sums"][host] if isinstance(ed["sums"], dict) else ed["sums"]


def render(code, host, lang, ed):
    tdir = TEMPLATES / (lang if lang in ("en", "ja") else code)
    ui = json.loads((tdir / "ui.json").read_text(encoding="utf-8"))
    if lang == "pl":  # Szyk keeps one-letter words off line ends (the templates already do)
        ui = SZYK.bind_one_letter_words(ui)
    roles = ui["roles"]
    h = ed["hosts"][host]
    plugin_name, plugin_url, plugin_folder = h["plugin"]
    skills = [(ed["skills"][s], h["skills"][s][1]) for s in SKILLS if s in h["skills"]]

    def listing(indent):
        return "\n".join(f"{indent}- [{n}]({u}) — {roles[s]}" for (n, u), s in zip(skills, [s for s in SKILLS if s in h["skills"]]))
    letters = ("B", "C") if ed["marketplace"] else ("A", "B")
    page = lambda other: guide_path(code, other, lang).removeprefix("docs/")
    values = dict(
        brand=ed["brand"], version=ed["version"], release=ed["release"], sums=sums(ed, host), display=ed["display"],
        lang=GATEWAYS.EDITION_NAMES[lang][code],
        first=ed["skills"]["base"], plugin=ed["slug"], plugin_url=plugin_url, plugin_folder=plugin_folder or "",
        plugin_dir=plugin_folder or ed["slug"], plugin_link=f"[{plugin_name}]({plugin_url})",
        skills_list=listing(""), skills_list_indented=listing("   "),
        claude_commands="\n".join(f"- `/{ed['slug']}:{ed['skills'][s]}`" for s in SKILLS),
        gemini_paths="\n".join(f"- `plugins/{ed['slug']}/skills/{ed['skills'][s]}` — {roles[s]}" for s in SKILLS[1:]),
        skills_path=f"plugins/{ed['slug']}/skills",
        L_zip=letters[0], l_zip=letters[0].lower(), L_chat=letters[1], l_chat=letters[1].lower(),
        page_chatgpt=page("chatgpt"), page_claude=page("claude"), page_gemini=page("gemini"))
    md = fill((tdir / f"{host}.md").read_text(encoding="utf-8"), values,
              {"marketplace": ed["marketplace"], "plugin_folder": bool(plugin_folder)})
    # Gemini Help opens in the page language whatever the template's link says.
    hl = {"en": "", "zh-hans": "zh-CN", "zh-hant": "zh-TW"}.get(lang, lang)
    md = re.sub(r"(support\.google\.com/gemini/answer/\d+)(\?hl=[\w-]+)?", lambda m: m[1] + (f"?hl={hl}" if hl else ""), md)
    content, toc = render_md(md)
    langs = list(dict.fromkeys((code, "en", "ja")))
    attr = page_lang_attr(code, lang)
    title = ui["titles"][host]
    path = guide_path(code, host, lang)
    alternates = "".join(f'<link rel="alternate" hreflang="{page_lang_attr(code, k)}" href="{BASE}{guide_path(code, host, k)}">'
                         for k in langs)
    head = (f"<title>{x(title)} | {x(ed['brand'])}</title>\n<meta name=\"description\" content=\"{x(ui['leads'][host])}\">\n"
            f'<link rel="canonical" href="{BASE}{path}">\n{alternates}\n'
            f'<link rel="alternate" hreflang="x-default" href="{BASE}{guide_path(code, host, code)}">\n'
            f'<link rel="icon" href="../assets/favicon-32x32.png" type="image/png">')
    native_label = GATEWAYS.GATEWAYS[code][3] if code in GATEWAYS.GATEWAYS else code.upper()
    labels = {code: native_label, "en": "English", "ja": "日本語"}
    gateway_file = {"en": "index.html", "ja": "top-ja.html"}.get(lang, GATEWAYS.GATEWAYS[code][0])
    brand = brand_html(code, ed["brand"])
    frame = FRAME.Frame(
        lang=attr, dir="rtl" if lang == code and code in RTL else "", head=head,
        css="../assets/kumihan-install.css", asset_root="../", brand=brand,
        home="../" + GATEWAYS.PRODUCTS[code]["pages"][lang],
        hosts=[(HOST_NAMES[hh], page(hh), hh == host) for hh in HOSTS],
        languages=[(page_lang_attr(code, k), labels[k], guide_path(code, host, k).removeprefix("docs/"), k == lang) for k in langs],
        number=f"0{HOSTS.index(host) + 1}", title=x(title), description=x(ui["leads"][host]),
        toc=toc, content=content, platform=HOST_NAMES[host],
        ui=dict(ui, source_href=f"{REPO}/blob/main/plugins/{ed['slug']}/INSTALL.md"),
        gateway=("../" + gateway_file, ui["home"]))
    return FRAME.render(frame)


def editions():
    return [c for c in V.catalogue() if c != "ja"]


@version_outputs
@seo_outputs
def outputs():
    files = {}
    for code in editions():
        ed = edition(code)
        for host in HOSTS:
            for lang in (code, "en", "ja"):
                files[guide_path(code, host, lang)] = render(code, host, lang, ed)
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    files = outputs()
    for name, content in files.items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale installation guides: " + ", ".join(stale))
    print(f"Installation guides: {len(files)} pages " + ("verified" if args.check else "built"))


if __name__ == "__main__":
    main()
