"""The one footer every KUMIHAN page shares; generators call footer(lang, root).

KUMIHAN
Open-source typography & design guidance by L&Co. LLC.
Links: KUMIHAN (the top page in the page's language), the language-edition
menu (rounded, "choose a language" in the page's language, the page's own
language first and the rest by code), GitHub, Apache 2.0, and the privacy
policy (labelled in the page's language, opening that language's section of
privacy.html).

The styles are part of assets/kumihan-fonts.css (tools/web_fonts.py), which
every page already loads after its own stylesheet. Jekyll layouts and the
Nhịp Chữ builder read _data/site_footer.json, where ROOT marks the path to
the site root.
"""
import json
from html import escape
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

REPO = "https://github.com/landco-llc/kumihan"
ROOT_MARK = "@ROOT@"
# "Privacy Policy" in each gateway language (tools/build_privacy.py builds privacy.html).
PRIVACY = {"en": "Privacy Policy", "ja": "プライバシーポリシー", "ar": "سياسة الخصوصية", "bn": "গোপনীয়তা নীতি",
           "de": "Datenschutzerklärung", "es": "Política de privacidad", "fa": "سیاست حفظ حریم خصوصی",
           "fr": "Politique de confidentialité", "hi": "गोपनीयता नीति", "id": "Kebijakan Privasi",
           "it": "Informativa sulla privacy", "km": "គោលការណ៍ឯកជនភាព", "ko": "개인정보 처리방침",
           "pl": "Polityka prywatności", "pt": "Política de Privacidade", "ru": "Политика конфиденциальности",
           "sw": "Sera ya Faragha", "th": "นโยบายความเป็นส่วนตัว", "vi": "Chính sách quyền riêng tư",
           "zh-hans": "隐私政策", "zh-hant": "隱私權政策", "zu": "Inqubomgomo Yobumfihlo"}
# Editions with pages but no package yet carry their label in assets/upcoming-editions.json.
PRIVACY.update({k: v["privacy"] for k, v in json.loads(
    (Path(__file__).resolve().parents[1] / "assets" / "upcoming-editions.json").read_text(encoding="utf-8")).items()
    if "privacy" in v})
# html lang values that differ from the gateway keys
KEYS = {"ko-KR": "ko", "th-TH": "th", "zh-Hans-CN": "zh-hans", "zh-Hant-TW": "zh-hant", "zh-Hant-HK": "zh-hant"}

CSS = """/* Shared footer (tools/site_footer.py): the same on every page. */
.kumihan-footer { background: #23221f; color: #e6e1d7; padding: 36px 0 40px; font-size: 13px; line-height: 1.7; }
.kumihan-footer .kf-inner { box-sizing: border-box; width: min(1184px, calc(100% - 40px)); margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 18px 28px; flex-wrap: wrap; }
.kumihan-footer .kf-brand { min-width: 0; }
.kumihan-footer .kf-mark { font: 800 18px/1.4 Arial, Helvetica, sans-serif; letter-spacing: -.05em; color: #f3eee4; }
.kumihan-footer .kf-note { margin: 4px 0 0; font: 500 11px/1.8 Arial, Helvetica, sans-serif; letter-spacing: .01em; color: #aaa69f; }
.kumihan-footer a { color: #e6e1d7; text-underline-offset: 4px; }
.kumihan-footer .kf-note a { color: inherit; }
.kumihan-footer .kf-links { display: flex; flex-wrap: wrap; align-items: center; gap: 12px 22px; min-width: 0; }
.kumihan-footer .kf-links > a { font-size: 12px; font-weight: 700; min-width: 0; overflow-wrap: anywhere; }
.kumihan-footer .kf-menu { position: relative; }
.kumihan-footer .kf-menu summary { list-style: none; display: flex; align-items: center; justify-content: space-between; gap: 12px; min-width: min(220px, 100%); min-height: 40px; box-sizing: border-box; padding: 8px 16px; border: 1px solid #5d5953; border-radius: 12px; background: #2d2b28; color: #aaa69f; cursor: pointer; font-size: 12px; font-weight: 600; }
.kumihan-footer .kf-menu summary::-webkit-details-marker { display: none; }
.kumihan-footer .kf-menu summary::after { content: ""; width: 6px; height: 6px; border-right: 2px solid currentColor; border-bottom: 2px solid currentColor; transform: translateY(2px) rotate(225deg); transition: transform .15s ease; }
.kumihan-footer .kf-menu[open] summary::after { transform: translateY(-2px) rotate(45deg); }
.kumihan-footer .kf-menu summary:focus-visible { outline: 3px solid #c84b4b; outline-offset: 3px; }
.kumihan-footer .kf-menu:not([open]) ul { display: none; }
.kumihan-footer .kf-menu ul { position: absolute; inset-inline-start: 0; bottom: calc(100% + 6px); z-index: 30; box-sizing: border-box; min-width: 100%; width: max-content; max-width: min(320px, calc(100vw - 32px)); max-height: min(50vh, 360px); overflow-y: auto; overscroll-behavior: contain; margin: 0; padding: 6px 0; list-style: none; background: #fbf9f4; border: 1px solid #d8d2c6; border-radius: 12px; box-shadow: 0 18px 40px rgba(0,0,0,.25); }
.kumihan-footer .kf-menu li a { display: block; padding: 9px 16px; color: #3b3935; text-decoration: none; font-size: 13px; font-weight: 700; line-height: 1.5; }
.kumihan-footer .kf-menu li a .code { color: #726d65; font: 800 12px/1.5 Arial, Helvetica, sans-serif; letter-spacing: .04em; }
.kumihan-footer .kf-menu li a:hover, .kumihan-footer .kf-menu li a:focus-visible { background: #ede8de; color: #252421; }
.kumihan-footer .kf-menu li a.current, .kumihan-footer .kf-menu li a.current .code { color: #8f2525; }
@media (max-width: 640px) { .kumihan-footer .kf-inner { flex-direction: column; align-items: flex-start; } }
"""


def _gateways():
    spec = spec_from_file_location("kumihan_build_gateways", Path(__file__).with_name("build_gateways.py"))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_G = None


def gateways():
    global _G
    if _G is None:
        _G = _gateways()
    return _G


def key(lang, g=None):
    g = g or gateways()
    k = KEYS.get(lang, lang)
    return k if k in g.GATEWAYS else (k.split("-")[0] if k.split("-")[0] in g.GATEWAYS else "en")


def footer(lang, root="", g=None):
    """Footer HTML for a page in `lang`; `root` is the relative path to the site root.

    `g` is the loaded tools/build_gateways.py (the gateway builder passes itself)."""
    g = g or gateways()
    k = key(lang, g)
    order = ([k] if k in g.PRODUCTS else []) + sorted(c for c in g.PRODUCTS if c != k)
    items = "".join(
        f'<li><a href="{root}{g.PRODUCTS[c]["pages"].get(k) or g.PRODUCTS[c]["pages"]["en"]}"'
        + (' class="current"' if c == k else "")
        + f'><span class="code">{c.upper()}</span> - {escape(g.EDITION_NAMES[k][c])}</a></li>'
        for c in order)
    return (f'<footer class="kumihan-footer"><div class="kf-inner">'
            f'<div class="kf-brand"><div class="kf-mark">KUMIHAN</div>'
            f'<p class="kf-note">Open-source typography &amp; design guidance by '
            f'<a href="https://landco.co.jp/" target="_blank" rel="noopener noreferrer">L&amp;Co. LLC</a>.</p></div>'
            f'<nav class="kf-links" aria-label="KUMIHAN">'
            f'<a href="{root}{g.GATEWAYS[k][0]}">KUMIHAN</a>'
            f'<details class="kf-menu"><summary>{escape(g.PICK[k])}</summary><ul>{items}</ul></details>'
            f'<a href="{REPO}" target="_blank" rel="noopener noreferrer">GitHub</a>'
            f'<a href="{REPO}/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">Apache 2.0</a>'
            f'<a href="{root}privacy.html#{k}">{escape(PRIVACY[k])}</a>'
            f'</nav></div></footer>')


def data():
    """Footer per page language for Jekyll and Nhịp Chữ, with ROOT_MARK for the site root."""
    langs = ["ja", "en", "ko-KR", "zh-Hant-TW", "zh-Hans-CN", "vi", "sw"]
    return {lang: footer(lang, ROOT_MARK) for lang in langs}
