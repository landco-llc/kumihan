#!/usr/bin/env python3
"""Typefaces per page language for every KUMIHAN site page; --check never writes.

Each language uses the fonts already on the reader's system first and falls
back to the Google Fonts family made for its script only when none of them is
installed (a web font is downloaded only when a character actually needs it).
Names of other languages and products (日本語, 한국어, 字衡, نضيد ...) use a
small Google Fonts subset limited to those characters.

Outputs: assets/kumihan-fonts.css (loaded after each page's own stylesheet)
and _data/web_fonts.yml (the Google Fonts links for the Jekyll layouts).
Generators call head(lang, asset_root) to place the links in <head>; the
hand-maintained pages in STATIC have their links rewritten here.
"""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
GOOGLE = "https://fonts.googleapis.com/css2?"

# script key -> (system sans stack, system serif stack, Google sans family, Google serif family)
SCRIPTS = {
    "ja": ('"Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic", Meiryo',
           '"Hiragino Mincho ProN", "Yu Mincho"', "Noto Sans JP", "Noto Serif JP"),
    "latin": ('"Helvetica Neue", Helvetica, "Segoe UI", Roboto',
              "Georgia", "Inter", "Source Serif 4"),
    "ar": ('"Geeza Pro", "Segoe UI"', '"Geeza Pro"', "Noto Naskh Arabic", "Noto Naskh Arabic"),
    "ko": ('"Apple SD Gothic Neo", "Malgun Gothic"', 'AppleMyungjo, Batang', "Noto Sans KR", "Noto Serif KR"),
    "th": ('Thonburi, "Leelawadee UI"', 'Thonburi, "Leelawadee UI"', "Noto Sans Thai", "Noto Serif Thai"),
    "zh-hans": ('"PingFang SC", "Hiragino Sans GB", "Microsoft YaHei"', '"Songti SC", STSong, SimSun',
                "Noto Sans SC", "Noto Serif SC"),
    "zh-hant": ('"PingFang TC", "Microsoft JhengHei"', '"Songti TC", PMingLiU', "Noto Sans TC", "Noto Serif TC"),
    "zh-hk": ('"PingFang HK", "Microsoft JhengHei"', '"Songti TC", PMingLiU', "Noto Sans HK", "Noto Serif HK"),
    # Hindi keeps the edition's self-hosted Noto Sans Devanagari ("Kumihan Devanagari",
    # assets/fonts) ahead of the Google copy, so pages that define it never fetch twice.
    "hi": ('"Kohinoor Devanagari", "Nirmala UI", "Kumihan Devanagari"', '"Kohinoor Devanagari", "Nirmala UI"',
           "Noto Sans Devanagari", "Noto Serif Devanagari"),
    # Vietnamese: Be Vietnam Pro is drawn for Vietnamese stacked diacritics.
    "vi": ('"Helvetica Neue", "Segoe UI", Roboto', "Georgia", "Be Vietnam Pro", "Noto Serif"),
}
# After the Google family, before the generic family (Latin system fallbacks
# that exist almost everywhere; Arial/Times only for Latin text).
LATIN_TAIL = {"latin": ("Arial", '"Times New Roman"'), "vi": ("Arial", '"Times New Roman"')}
AXES = {"Be Vietnam Pro": "wght@400;500;600;700;800", "Noto Serif": "wght@100..900",
        "Inter": "wght@100..900", "Source Serif 4": "wght@200..900", "Noto Naskh Arabic": "wght@400..700",
        "Noto Sans Thai": "wght@100..900", "Noto Serif Thai": "wght@100..900"}
# Page language (html lang attribute) -> script key
LANGS = {"de": "latin", "ja": "ja", "en": "latin", "es": "latin", "fr": "latin", "pt": "latin", "ar": "ar",
         "ko": "ko", "ko-KR": "ko", "th": "th", "th-TH": "th", "zh-Hans-CN": "zh-hans",
         "zh-Hant-TW": "zh-hant", "zh-Hant-HK": "zh-hk", "hi": "hi", "vi": "vi",
         "de": "latin", "pl": "latin", "id": "latin"}
# Characters of language and product names shown on pages of other languages.
NAMES = ("日本語 한국어 ไทย 简体中文 繁體中文 繁体中文 العربية हिंदी 字衡 字律 글짜임 ดุลอักษร نضيد "
         "अक्षर-संगति あ 한 ก 汉 漢 ع अ 臺灣 香港 台灣 中文")
# Subset families for those names, in the order they are tried.
SUBSET = ("Noto Sans JP", "Noto Sans KR", "Noto Sans SC", "Noto Sans TC", "Noto Sans Thai", "Noto Naskh Arabic",
          "Noto Sans Devanagari")


def script(lang):
    return LANGS.get(lang) or LANGS.get(lang.split("-")[0], "latin")


def family_param(name):
    axes = AXES.get(name, "wght@100..900" if name.startswith("Noto Sans") else "wght@200..900")
    return "family=" + quote(name).replace("%20", "+") + ":" + axes


def own_url(key):
    _, _, sans, serif = SCRIPTS[key]
    names = [sans] + ([serif] if serif != sans else [])
    return GOOGLE + "&".join(family_param(n) for n in names) + "&display=swap"


def subset_families(key):
    return [f for f in SUBSET if f != SCRIPTS[key][2]]


def subset_url(key):
    chars = "".join(sorted(set(NAMES.replace(" ", ""))))
    return (GOOGLE + "&".join("family=" + quote(f).replace("%20", "+") for f in subset_families(key))
            + "&text=" + quote(chars) + "&display=swap")


def stacks(key):
    local_sans, local_serif, sans, serif = SCRIPTS[key]
    tail_sans, tail_serif = LATIN_TAIL.get(key, ("", ""))
    others = ", ".join(f'"{f}"' for f in subset_families(key))
    s = ", ".join(p for p in (local_sans, f'"{sans}"', tail_sans, others, "system-ui, sans-serif") if p)
    r = ", ".join(p for p in (local_serif, f'"{serif}"', tail_serif, others, "serif") if p)
    return s, r


def google_links(lang):
    key = script(lang)
    return ('<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="{own_url(key).replace("&", "&amp;")}">'
            f'<link rel="stylesheet" href="{subset_url(key).replace("&", "&amp;")}">')


def head(lang, asset_root=""):
    """Google Fonts links plus the shared typeface stylesheet; place after the page CSS."""
    return google_links(lang) + f'<link rel="stylesheet" href="{asset_root}assets/kumihan-fonts.css">'


def css():
    out = ["/* KUMIHAN typefaces per page language. Generated by tools/web_fonts.py; do not edit.",
           "   System fonts come first; the Google Fonts family for the script is used only",
           "   when none is installed. Other scripts' names use a small Google Fonts subset. */"]
    for key in SCRIPTS:
        langs = [l for l, k in LANGS.items() if k == key]
        s, r = stacks(key)
        html = ", ".join(f'html[lang="{l}"]' for l in langs)
        body = ", ".join(f'html[lang="{l}"] body' for l in langs)
        out.append(f"{html} {{ --display: {s}; --sans: {s}; --font-jp: {s}; --serif: {r}; }}")
        out.append(f"{body} {{ font-family: {s}; }}")
    out.append("/* Text marked as another non-Latin language inside a page uses that script's fonts. */")
    for key in ("ja", "ko", "th", "zh-hans", "zh-hant", "zh-hk", "ar", "hi"):
        langs = [l for l, k in LANGS.items() if k == key]
        sel = ", ".join(f'body [lang="{l}"]' for l in langs)
        out.append(f"{sel} {{ font-family: {stacks(key)[0]}; }}")
    out.append("/* Decorative symbol motifs (▮▮▯, « », ◌) take whichever font has the glyph; when that")
    out.append("   font is wide, let them wrap between symbols instead of widening the page. */")
    out.append(":is(.feature-motif, .skill-symbol) { overflow-wrap: anywhere; min-width: 0; }")
    return "\n".join(out) + "\n"


def data_yml():
    lines = ["# Google Fonts links per page language for the Jekyll layouts. Generated by tools/web_fonts.py."]
    for lang in LANGS:
        lines.append(f"{json.dumps(lang)}: {json.dumps(google_links(lang), ensure_ascii=False)}")
    return "\n".join(lines) + "\n"


# Pages without a generator of their own (ZiLu landings are copied from templates/).
STATIC = ("docs/install-ziheng*.html", "templates/zilu-*-landing.html")
LINKS = re.compile(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?assets/kumihan-fonts\.css">', re.S)


def static_pages():
    out = {}
    for pattern in STATIC:
        for path in sorted(ROOT.glob(pattern)):
            text = path.read_text(encoding="utf-8")
            lang = re.search(r'<html lang="([^"]+)"', text).group(1)
            root = "../" if path.parent.name == "docs" else ""
            new = head(lang, root)
            out[str(path.relative_to(ROOT))] = (LINKS.sub(lambda _: new, text) if LINKS.search(text)
                                                else text.replace("</head>", new + "\n</head>", 1))
    return out


def outputs():
    return {"assets/kumihan-fonts.css": css(), "_data/web_fonts.yml": data_yml(), **static_pages()}


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
        raise SystemExit("Stale web font files: " + ", ".join(stale))
    print("Web fonts: " + ("verified" if args.check else "built"))


if __name__ == "__main__":
    main()
