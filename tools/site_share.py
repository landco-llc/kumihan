"""Link-preview (Open Graph / X card) tags every KUMIHAN page shares; generators call apply().

When a page is shared, the preview shows the page title, a description made of
what KUMIHAN is (in the page's language, the top page's description from
assets/gateway-copy.json) followed by the page's own meta description, and the
KUMIHAN logo (assets/kumihan-share.png: the official logo on a 1200x630 white
canvas). apply() reads the page's lang, <title>, meta description and canonical
link, drops any og:/twitter: tags and adds the shared set before </head>, so it
is idempotent.

tools/web_fonts.py applies it to the hand-kept pages and writes
_data/site_share.json for the Jekyll layouts (_includes/share.html).
"""
import json
import re
from html import escape, unescape
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://landco-llc.github.io/kumihan/"
IMAGE = SITE + "assets/kumihan-share.png"
LOCALES = {"ja": "ja_JP", "en": "en_US", "ko": "ko_KR", "zh-hans": "zh_CN", "zh-hant": "zh_TW", "th": "th_TH",
           "vi": "vi_VN", "ar": "ar_AR", "fa": "fa_IR", "hi": "hi_IN", "bn": "bn_BD", "fr": "fr_FR", "es": "es_ES",
           "pt": "pt_PT", "de": "de_DE", "it": "it_IT", "pl": "pl_PL", "id": "id_ID", "ru": "ru_RU", "sw": "sw_TZ",
           "zu": "zu_ZA", "km": "km_KH"}
# A single tag, attributes in any order.
TAG = re.compile(r'[ \t]*<meta\b(?:\s+[\w:-]+="[^"]*")*\s*/?>\n?')
SHARED = re.compile(r'\s(?:property="og:|name="twitter:)')

_spec = spec_from_file_location("kumihan_site_footer", Path(__file__).with_name("site_footer.py"))
FOOTER = module_from_spec(_spec)
_spec.loader.exec_module(FOOTER)
ABOUT = {k: v["description"] for k, v in
         json.loads((ROOT / "assets/gateway-copy.json").read_text(encoding="utf-8")).items()}


def key(lang):
    return FOOTER.key(lang)


def locale(lang):
    return "zh_HK" if lang.endswith("-HK") else LOCALES[key(lang)]


def separator(about):
    """No space after a Japanese or Chinese full stop."""
    return "" if about.endswith("。") else " "


def description(lang, page):
    """What KUMIHAN is, in the page's language, then the page's own description."""
    about = ABOUT[key(lang)]
    return page if about in page else (about + separator(about) + page).strip()


def tags(lang, title, desc, url):
    """Share tags for one page; `desc` already combined by description()."""
    t, d = escape(title), escape(desc)
    return "\n".join([
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="KUMIHAN">',
        f'<meta property="og:title" content="{t}">',
        f'<meta property="og:description" content="{d}">',
        f'<meta property="og:url" content="{escape(url)}">',
        f'<meta property="og:locale" content="{locale(lang)}">',
        f'<meta property="og:image" content="{IMAGE}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="KUMIHAN">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{t}">',
        f'<meta name="twitter:description" content="{d}">',
        f'<meta name="twitter:image" content="{IMAGE}">',
    ])


def apply(html):
    """`html` with the shared tags; the page's canonical link is its address."""
    lang = re.search(r'<html\b[^>]*\slang="([^"]+)"', html).group(1)
    title = unescape(re.search(r"<title>(.*?)</title>", html, re.S).group(1).strip())
    meta = re.search(r'<meta\b(?=[^>]*\sname="description")[^>]*\scontent="([^"]*)"', html)
    page = unescape(meta.group(1)) if meta else ""
    url = unescape(re.search(r'<link\b(?=[^>]*\srel="canonical")[^>]*\shref="([^"]*)"', html).group(1))
    html = TAG.sub(lambda m: "" if SHARED.search(m.group(0)) else m.group(0), html)
    return html.replace("</head>", tags(lang, title, description(lang, page), url) + "\n</head>", 1)


def data():
    """Per page language for the Jekyll layouts: KUMIHAN's description and the og:locale."""
    langs = ["ja", "en", "ko-KR", "zh-Hant-TW", "zh-Hans-CN", "vi", "sw"]
    return {lang: {"about": ABOUT[key(lang)], "separator": separator(ABOUT[key(lang)]), "locale": locale(lang)}
            for lang in langs}

