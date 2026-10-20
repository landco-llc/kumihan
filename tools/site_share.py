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
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://landco-llc.github.io/kumihan/"
IMAGE = SITE + "assets/kumihan-share.png"
LOCALES = {"ja": "ja_JP", "en": "en_US", "ko": "ko_KR", "zh-hans": "zh_CN", "zh-hant": "zh_TW", "th": "th_TH",
           "vi": "vi_VN", "ar": "ar_AR", "fa": "fa_IR", "hi": "hi_IN", "bn": "bn_BD", "fr": "fr_FR", "es": "es_ES",
           "pt": "pt_PT", "de": "de_DE", "it": "it_IT", "pl": "pl_PL", "id": "id_ID", "ru": "ru_RU", "sw": "sw_TZ",
           "zu": "zu_ZA", "km": "km_KH", "el": "el_GR", "nl": "nl_NL", "ms": "ms_MY", "tr": "tr_TR", "he": "he_IL"}
# A single tag, attributes in any order.
TAG = re.compile(r'[ \t]*<meta\b(?:\s+[\w:-]+="[^"]*")*\s*/?>\n?')
SHARED = re.compile(r'\s(?:property="og:|name="twitter:)')

_spec = spec_from_file_location("kumihan_site_footer", Path(__file__).with_name("site_footer.py"))
FOOTER = module_from_spec(_spec)
_spec.loader.exec_module(FOOTER)
ABOUT = {k: v["description"] for k, v in
         json.loads((ROOT / "assets/gateway-copy.json").read_text(encoding="utf-8")).items()}


def key(lang):
    normalized = lang.lower()
    # FOOTER deliberately falls back to JA for presentation; SEO must fail closed.
    if normalized.split('-')[0] not in {k.split('-')[0] for k in LOCALES}:
        raise ValueError(f'Unregistered share language: {lang}')
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
    class Head(HTMLParser):
        def __init__(self):
            super().__init__(); self.lang = ''; self.title = ''; self.page = ''; self.url = ''; self.in_title = False
        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            if tag == 'html': self.lang = a.get('lang', '')
            if tag == 'title': self.in_title = True
            if tag == 'meta' and a.get('name', '').lower() == 'description': self.page = a.get('content', '')
            if tag == 'link' and a.get('rel') == 'canonical': self.url = a.get('href', '')
        def handle_data(self, data):
            if self.in_title: self.title += data
        def handle_endtag(self, tag):
            if tag == 'title': self.in_title = False
    head = Head(); head.feed(html.split('</head>', 1)[0])
    def remove(match):
        class Attributes(HTMLParser):
            def handle_starttag(self, tag, attrs): self.attrs = dict(attrs)
        parser = Attributes(); parser.feed(match[0])
        key = (parser.attrs.get('property') or parser.attrs.get('name') or '').lower()
        return '' if key.startswith(('og:', 'twitter:')) else match[0]
    html = re.sub(r'[ \t]*<meta\b[^>]*>\n?', remove, html, flags=re.I)
    return html.replace('</head>', tags(head.lang, head.title.strip(), description(head.lang, head.page), head.url) + '\n</head>', 1)


def data():
    """Per page language for the Jekyll layouts: KUMIHAN's description and the og:locale."""
    langs = sorted(set(LOCALES) | {"ko-KR", "zh-Hant-TW", "zh-Hans-CN"})
    return {lang: {"about": ABOUT[key(lang)], "separator": separator(ABOUT[key(lang)]), "locale": locale(lang)}
            for lang in langs}

