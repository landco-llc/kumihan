#!/usr/bin/env python3
"""Typefaces per page language for every KUMIHAN site page; --check never writes.

Each language uses the fonts already on the reader's system first and falls
back to the Google Fonts family made for its script only when none of them is
installed (a web font is downloaded only when a character actually needs it).
Names of other languages and products (日本語, 한국어, 字衡, نضيد ...) use a
small subset limited to those characters. The font files are served from this
site (assets/fonts/google, copied by tools/fetch_fonts.py); pages make no
requests to Google.

Outputs: assets/kumihan-fonts.css (loaded after each page's own stylesheet; it
also carries the shared footer styles of tools/site_footer.py),
_data/web_fonts.yml (the font links for the Jekyll layouts and Nhịp Chữ) and
_data/site_footer.json (the shared footer for the Jekyll layouts and Nhịp Chữ).
Generators call head(lang, asset_root) to place the links in <head>; the
hand-maintained pages in STATIC have their links rewritten here.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
_spec = spec_from_file_location("kumihan_site_footer", Path(__file__).with_name("site_footer.py"))
FOOTER = module_from_spec(_spec)
_spec.loader.exec_module(FOOTER)
_spec = spec_from_file_location("kumihan_site_share", Path(__file__).with_name("site_share.py"))
SHARE = module_from_spec(_spec)
_spec.loader.exec_module(SHARE)
GOOGLE = "https://fonts.googleapis.com/css2?"

# script key -> (system sans stack, system serif stack, Google sans family, Google serif family)
SCRIPTS = {
    "km": ('"Khmer Sangam MN", "DaunPenh", "Khmer OS"', '"Khmer Sangam MN", "Khmer OS"', "Noto Sans Khmer", "Noto Serif Khmer"),
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
    # Persian: Vazirmatn is drawn for Persian (Arabic script, Persian letters and digits).
    "fa": ('"Geeza Pro", "Segoe UI", Tahoma', '"Geeza Pro", "Segoe UI"', "Vazirmatn", "Noto Naskh Arabic"),
    # Bangla: Kohinoor Bangla (macOS/iOS), Nirmala UI and Vrinda (Windows), then Noto Bengali.
    "bn": ('"Kohinoor Bangla", "Bangla Sangam MN", "Nirmala UI", Vrinda', '"Bangla Sangam MN", "Nirmala UI", Vrinda',
           "Noto Sans Bengali", "Noto Serif Bengali"),
    # Russian Cyrillic: system fonts first, Noto fallback for full script coverage.
    "ru": ('"PT Sans", "Segoe UI", Arial', '"PT Serif", Georgia', "Noto Sans", "Noto Serif"),
    # Vietnamese: Be Vietnam Pro is drawn for Vietnamese stacked diacritics.
    "vi": ('"Helvetica Neue", "Segoe UI", Roboto', "Georgia", "Be Vietnam Pro", "Noto Serif"),
    # Greek: system fonts with Greek (tonos, dialytika) first, Noto for full coverage.
    "el": ('"Helvetica Neue", "Segoe UI", Roboto', "Georgia", "Noto Sans", "Noto Serif"),
    # Hebrew: Arial Hebrew (macOS/iOS) and Segoe UI (Windows), then Noto Hebrew.
    "he": ('"Arial Hebrew", "Segoe UI", Arial', '"Times New Roman"', "Noto Sans Hebrew", "Noto Serif Hebrew"),
}
# After the Google family, before the generic family (Latin system fallbacks
# that exist almost everywhere; Arial/Times only for Latin text).
LATIN_TAIL = {"latin": ("Arial", '"Times New Roman"'), "vi": ("Arial", '"Times New Roman"'), "el": ("Arial", '"Times New Roman"')}
AXES = {"Be Vietnam Pro": "wght@400;500;600;700;800", "Noto Serif": "wght@100..900",
        "Inter": "wght@100..900", "Source Serif 4": "wght@200..900", "Noto Naskh Arabic": "wght@400..700",
        "Noto Sans Thai": "wght@100..900", "Noto Serif Thai": "wght@100..900",
        "Vazirmatn": "wght@100..900"}
# Page language (html lang attribute) -> script key
LANGS = {"km": "km", "km-KH": "km", "it": "latin", "ru": "ru", "de": "latin", "ja": "ja", "en": "latin", "es": "latin", "fr": "latin", "pt": "latin", "ar": "ar",
         "ko": "ko", "ko-KR": "ko", "th": "th", "th-TH": "th", "zh-Hans-CN": "zh-hans",
         "zh-Hant-TW": "zh-hant", "zh-Hant-HK": "zh-hk", "hi": "hi", "vi": "vi",
         "pl": "latin", "id": "latin", "bn": "bn", "sw": "latin", "zu": "latin", "fa": "fa",
         "el": "el", "nl": "latin", "ms": "latin", "tr": "latin", "he": "he", "sa": "hi"}
# Characters of language and product names shown on pages of other languages.
NAMES = ("日本語 한국어 ไทย 简体中文 繁體中文 繁体中文 العربية हिंदी 字衡 字律 글짜임 ดุลอักษร نضيد "
         "अक्षर-संगति বাংলা অক্ষরসজ্জা فارسی تراز ភាសាខ្មែរ លំនឹង ក あ 한 ก 汉 漢 ع अ 臺灣 香港 台灣 中文 "
         "Ελληνικά Μέτρο ΕΛ ς עברית מקצב עב ך संस्कृतम् विन्यास सं क्ष")
# Subset families for those names, in the order they are tried.
SUBSET = ("Noto Sans JP", "Noto Sans KR", "Noto Sans SC", "Noto Sans TC", "Noto Sans Thai", "Noto Naskh Arabic",
          "Noto Sans Devanagari", "Noto Sans Bengali", "Noto Sans Khmer", "Vazirmatn", "Noto Sans Hebrew", "Noto Sans")


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


# Display typefaces for the large letters on the top-page cards (one character per
# edition), chosen to show each script's own letterforms rather than a Gothic/sans
# face: page language (html lang of the character) -> Google Fonts family.
GLYPH_LATIN = "Cormorant Garamond"
GLYPH_FAMILIES = {
    "ja": "Shippori Mincho", "ko": "Nanum Myeongjo", "zh-Hans-CN": "Noto Serif SC", "zh-Hant-TW": "Noto Serif TC",
    "th": "Noto Serif Thai", "km": "Noto Serif Khmer", "ar": "Amiri", "fa": "Noto Nastaliq Urdu",
    "he": "Frank Ruhl Libre", "hi": "Tiro Devanagari Hindi", "sa": "Tiro Devanagari Sanskrit",
    "bn": "Tiro Bangla", "el": "GFS Didot",
}
# The card characters; the stylesheet carries only these glyphs.
GLYPHS = "Ä Ñ Ç È Ł Ã Ж İ Ắ IJ Ng Aa -lah ng’ Ω あ 한 汉 漢 ก ក ع ژ א अ क्ष অ"


def glyph_url():
    names = sorted(set(GLYPH_FAMILIES.values()) | {GLYPH_LATIN})
    chars = "".join(sorted(set(GLYPHS.replace(" ", ""))))
    return (GOOGLE + "&".join("family=" + quote(n).replace("%20", "+") + (":wght@500" if n == GLYPH_LATIN else "")
                              for n in names) + "&text=" + quote(chars) + "&display=swap")


def glyph_css():
    """Rules for the card characters; Latin, Cyrillic and Vietnamese letters use GLYPH_LATIN."""
    out = [f'.type-art .glyph .character {{ font-family: "{GLYPH_LATIN}", var(--serif); font-weight: 500; }}']
    for lang, family in GLYPH_FAMILIES.items():
        out.append(f'.type-art .glyph .character[lang="{lang}"] {{ font-family: "{family}", var(--serif); font-weight: 400; }}')
    # Amiri's ع has a deep descending tail: lift it so it clears the label.
    out.append('.type-art .glyph .character[lang="ar"] { line-height: 1; transform: translateY(-.32em); }')
    return out


def google_urls():
    """Every Google Fonts stylesheet the pages use; tools/fetch_fonts.py copies them to this site."""
    return [u for key in SCRIPTS for u in (own_url(key), subset_url(key))] + [glyph_url()]


def stacks(key):
    local_sans, local_serif, sans, serif = SCRIPTS[key]
    tail_sans, tail_serif = LATIN_TAIL.get(key, ("", ""))
    others = ", ".join(f'"{f}"' for f in subset_families(key))
    s = ", ".join(p for p in (local_sans, f'"{sans}"', tail_sans, others, "system-ui, sans-serif") if p)
    r = ", ".join(p for p in (local_serif, f'"{serif}"', tail_serif, others, "serif") if p)
    return s, r


def local_id(url):
    """Name of this site's copy of a Google Fonts stylesheet (tools/fetch_fonts.py)."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]


def local_css(url, root=""):
    """Path of this site's copy of a Google Fonts stylesheet, versioned by its content."""
    path = f"assets/fonts/google/{local_id(url)}.css"
    version = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:10]
    return f"{root}{path}?v={version}"


def font_links(lang, root=""):
    """The script's own families and the language-name subset, served from this site."""
    key = script(lang)
    return "".join(f'<link rel="stylesheet" href="{local_css(u, root)}">' for u in (own_url(key), subset_url(key)))


def fonts_css_path():
    """Shared stylesheet path with a content version, so browsers never keep a stale copy."""
    return "assets/kumihan-fonts.css?v=" + hashlib.sha256(css().encode("utf-8")).hexdigest()[:10]


def head(lang, asset_root=""):
    """Font links plus the shared typeface stylesheet; place after the page CSS."""
    return font_links(lang, asset_root) + f'<link rel="stylesheet" href="{asset_root}{fonts_css_path()}">'


def css():
    out = ["/* KUMIHAN typefaces per page language. Generated by tools/web_fonts.py; do not edit.",
           "   System fonts come first; the Google Fonts family for the script (served from this site)",
           "   is used only when none is installed. Other scripts' names use a small subset. */"]
    for key in SCRIPTS:
        langs = [l for l, k in LANGS.items() if k == key]
        s, r = stacks(key)
        html = ", ".join(f'html[lang="{l}"]' for l in langs)
        body = ", ".join(f'html[lang="{l}"] body' for l in langs)
        out.append(f"{html} {{ --display: {s}; --sans: {s}; --font-jp: {s}; --serif: {r}; }}")
        out.append(f"{body} {{ font-family: {s}; }}")
    out.append("/* Text marked as another non-Latin language inside a page uses that script's fonts. */")
    for key in ("fa", "km", "ja", "ko", "th", "zh-hans", "zh-hant", "zh-hk", "ar", "hi", "bn", "ru", "el", "he"):
        langs = [l for l, k in LANGS.items() if k == key]
        sel = ", ".join(f'body [lang="{l}"]' for l in langs)
        out.append(f"{sel} {{ font-family: {stacks(key)[0]}; }}")
    out.append("/* Top-page cards: each edition's character in a typeface that shows its script (GLYPH_FAMILIES). */")
    out += glyph_css()
    out.append("/* Decorative symbol motifs (▮▮▯, « », ◌) take whichever font has the glyph; when that")
    out.append("   font is wide, let them wrap between symbols instead of widening the page. */")
    out.append(":is(.feature-motif, .skill-symbol) { overflow-wrap: anywhere; min-width: 0; }")
    out.append("/* Long German compounds (and brand names such as KUMIHAN｜Satzbild) at enlarged text on")
    out.append("   narrow screens: break inside a word only when it cannot fit, where no hyphenation")
    out.append("   dictionary is available. */")
    out.append('html[lang="de"] :is(.cta-layout p, .toc-details summary) { overflow-wrap: anywhere; }')
    out.append("/* Khmer (no spaces between words) and isiZulu (long agglutinated words): the same, for")
    out.append("   headings and paragraphs. */")
    out.append('html:is([lang="km"], [lang="zu"]) :is(h1, h2, h3, p, li, summary) { overflow-wrap: anywhere; }')
    return "\n".join(out) + "\n" + FOOTER.CSS


def data_yml():
    lines = ["# Font links per page language for the Jekyll layouts and Nhịp Chữ; @ROOT@ is the site root.",
             "# Generated by tools/web_fonts.py."]
    for lang in LANGS:
        lines.append(f"{json.dumps(lang)}: {json.dumps(font_links(lang, FOOTER.ROOT_MARK), ensure_ascii=False)}")
    return "\n".join(lines) + "\n"


# Pages without a generator of their own (ZiLu landings are copied from templates/;
# the Bangla pages are maintained by hand).
STATIC = ("docs/install-ziheng*.html", "templates/zilu-*-landing.html", "kumihan-bn*.html",
          "docs/install-kumihan-bn-*.html")
FOOTER_TAG = re.compile(r"<footer\b.*?</footer>", re.S)
LINKS = re.compile(r'<link rel="(?:preconnect|stylesheet)" href="[^"]*(?:fonts\.googleapis\.com|assets/fonts/google/)[^"]*"[^>]*>'
                   r'.*?assets/kumihan-fonts\.css[^"]*">', re.S)


def format_static(text, relative):
            path = Path(relative)
            lang = re.search(r'<html lang="([^"]+)"', text).group(1)
            root = "../" if path.parent.name == "docs" else ""
            new = head(lang, root)
            # Replace each legacy Google or local font link independently.
            # Metadata enrichment can split a contiguous original font block.
            # Keep the shared stylesheet last so per-script rules take precedence.
            font_link = re.compile(r'<link\b[^>]*\bhref="[^"]*(?:fonts\.(?:googleapis|gstatic)\.com|assets/fonts/google/|assets/kumihan-fonts\.css)[^"]*"[^>]*>', re.I)
            text = font_link.sub('', text)
            text = text.replace("</head>", new + "\n</head>", 1)
            footer = FOOTER.footer(lang, root)
            text = (FOOTER_TAG.sub(lambda _: footer, text, count=1) if FOOTER_TAG.search(text)
                    else text.replace("</body>", footer + "\n</body>", 1))
            from seo_metadata import enrich_html
            from version_display import apply_html
            return apply_html(enrich_html(SHARE.apply(text), relative), relative)


def static_pages():
    out = {}
    for pattern in STATIC:
        for path in sorted(ROOT.glob(pattern)):
            relative = str(path.relative_to(ROOT))
            out[relative] = format_static(path.read_text(encoding="utf-8"), relative)
    return out


def outputs():
    return {"assets/kumihan-fonts.css": css(), "_data/web_fonts.yml": data_yml(),
            "_data/kumihan_assets.json": json.dumps({"fonts_css": fonts_css_path()}) + "\n",
            "_data/site_footer.json": json.dumps(FOOTER.data(), ensure_ascii=False, indent=1) + "\n",
            "_data/site_share.json": json.dumps(SHARE.data(), ensure_ascii=False, indent=1) + "\n", **static_pages()}


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
