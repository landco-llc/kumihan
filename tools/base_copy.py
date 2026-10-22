"""Shared Japanese and English copy for every KUMIHAN language edition.

The Japanese KUMIHAN page (kumihan.html / _layouts/landing.html) is the source.
Every edition shares its philosophy and concept, so the Japanese and English
pages of an edition reuse this copy with only the language and product names
swapped. What is genuinely specific to an edition (feature 01, the entry
skill, release status, install extras, fidelity details) stays in that
edition's copy file: feature 01, the entry skill, the fidelity details
(feature 03 text) and the release status. A shared sentence that an edition
extends with script-specific detail is kept as written.

Usage: python tools/base_copy.py [--check]
Rewrites the shared keys of assets/*-site-copy.json and assets/upcoming-site-copy.json.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# key: (brand, short name, Japanese language name, English language name, version)
EDITIONS = {
    "it": ("KUMIHAN｜Equilibrio", "Equilibrio", "イタリア語", "Italian", "0.1.0"),
    "de": ("KUMIHAN｜Satzbild", "Satzbild", "ドイツ語", "German", "0.1.0"),
    "hi": ("KUMIHAN｜अक्षर-संगति", "अक्षर-संगति", "ヒンディー語", "Hindi", "0.1.0"),
    "fr": ("KUMIHAN｜Accord", "Accord", "フランス語", "French", "0.1.1"),
    "ar": ("KUMIHAN｜نضيد", "نضيد", "アラビア語", "Arabic", "0.1.0"),
    "ru": ("KUMIHAN｜Лад", "Лад", "ロシア語", "Russian", "0.1.0"),
    "pt": ("KUMIHAN｜Compasso", "Compasso", "ポルトガル語", "Portuguese", "0.1.0"),
    "es": ("KUMIHAN｜Grafía", "Grafía", "スペイン語", "Spanish", "0.1.0"),
    "ko": ("KUMIHAN｜글짜임", "글짜임", "韓国語", "Korean", "0.1.0"),
    "th": ("KUMIHAN｜ดุลอักษร", "ดุลอักษร", "タイ語", "Thai", "0.1.1"),
    "zh-hans": ("KUMIHAN｜字律", "字律", "簡体中国語", "Simplified Chinese", "0.1.0"),
    "zh-hant": ("KUMIHAN｜字衡", "字衡", "繁体中国語", "Traditional Chinese", "0.1.0"),
    "vi": ("KUMIHAN｜Nhịp Chữ", "Nhịp Chữ", "ベトナム語", "Vietnamese", "0.1.0"),
    "pl": ("KUMIHAN｜Szyk", "Szyk", "ポーランド語", "Polish", "0.1.0"),
    "id": ("KUMIHAN｜Laras", "Laras", "インドネシア語", "Indonesian", "0.1.0"),
    "bn": ("KUMIHAN｜অক্ষরসজ্জা", "অক্ষরসজ্জা", "ベンガル語", "Bangla", "0.1.0"),
    "sw": ("KUMIHAN｜Mizani", "Mizani", "スワヒリ語", "Swahili", "0.1.0"),
    "zu": ("KUMIHAN｜Hlela", "Hlela", "ズールー語", "isiZulu", "0.1.0"),
    "km": ("KUMIHAN｜លំនឹង", "លំនឹង", "クメール語", "Khmer", "0.1.0"),
    "fa": ("KUMIHAN｜تراز", "تراز", "ペルシア語", "Persian", "0.1.0"),
    "el": ("KUMIHAN｜Μέτρο", "Μέτρο", "ギリシャ語", "Greek", "0.1.0"),
    "nl": ("KUMIHAN｜Zetwerk", "Zetwerk", "オランダ語", "Dutch", "0.1.0"),
    "ms": ("KUMIHAN｜Jalin", "Jalin", "マレー語", "Malay", "0.1.0"),
    "tr": ("KUMIHAN｜Ahenk", "Ahenk", "トルコ語", "Turkish", "0.1.0"),
    "he": ("KUMIHAN｜מקצב", "מקצב", "ヘブライ語", "Hebrew", "0.1.0"),
    "sa": ("KUMIHAN｜विन्यास", "विन्यास", "サンスクリット語", "Sanskrit", "0.1.0"),
    "no": ("KUMIHAN｜Samklang", "Samklang", "ノルウェー語", "Norwegian", "0.1.0"),
    "uk": ("KUMIHAN｜Міра", "Міра", "ウクライナ語", "Ukrainian", "0.1.0"),
    "cs": ("KUMIHAN｜Soulad", "Soulad", "チェコ語", "Czech", "0.1.0"),
    "hu": ("KUMIHAN｜Arány", "Arány", "ハンガリー語", "Hungarian", "0.1.0"),
    "my": ("KUMIHAN｜ဟန်ချက်", "ဟန်ချက်", "ビルマ語", "Burmese", "0.1.0"),
    "la": ("KUMIHAN｜Concinnitas", "Concinnitas", "ラテン語", "Latin", "0.1.0"),
    "tl": ("KUMIHAN｜Tugma", "Tugma", "タガログ語", "Tagalog", "0.1.0"),
    "en": ("KUMIHAN｜Measure", "Measure", "英語", "English", "0.1.0"),
    "fi": ("KUMIHAN｜Rytmi", "Rytmi", "フィンランド語", "Finnish", "0.1.0"),
    "sv": ("KUMIHAN｜Samspel", "Samspel", "スウェーデン語", "Swedish", "0.1.0"),
    "da": ("KUMIHAN｜Samklang", "Samklang", "デンマーク語", "Danish", "0.1.0"),
}
# Editions with pages but no package or Release yet: their copy lives together in
# assets/upcoming-site-copy.json and the release wording below replaces the shared one.
UPCOMING = ("el", "nl", "ms", "tr", "he", "sa", "cs", "hu", "my", "la", "tl", "en", "fi", "sv", "da", "no", "uk")


def released(edition):
    """An edition whose packages are in the version catalogue uses the released wording."""
    sys.path.insert(0, str(ROOT / "tools"))
    import edition_versions
    return edition in edition_versions.catalogue()

COPY_FILES = {"it": "equilibrio", "de": "satzbild", "hi": "hi", "fr": "accord", "ar": "ar", "pt": "compasso", "es": "grafia",
              "pl": "szyk", "id": "laras", "ru": "lad", "sw": "mizani", "zu": "hlela",
              "km": "lumnung", "fa": "fa"}

JA = {
    "title": "{B} — {L}のデザインをもっと自然に",
    "description": "{B}は、AIによる{L}のWebサイト・文書・プレゼン資料の制作とレビューを支援する、オープンソースのスキル集です。",
    "nav": ["{S}とは", "できること", "4つのスキル", "導入方法"],
    "eyebrow": "OPEN-SOURCE SKILLS / {LU} TYPOGRAPHY",
    "h1": ["{L}の", "デザインを", "もっと自然に"],
    "lead": "AIとつくる{L}のWebサイト、記事、報告書、プレゼンテーション。読みやすさも、伝わりやすさも、内容を大切にすることも。{B}は、{L}のための制作・レビュースキル集です。",
    "cta": ["使いはじめる", "{S}について"],
    "hero_foot": ["OPEN SOURCE", "FOUR SKILLS", "{LU} FIRST"],
    "concept_h2": ["「見た目をそろえる」より", "「伝わる形を考える」"],
    "concept_body": "目的も読み手も違うのに、同じ構成を繰り返さない。文章の意味や情報の優先順位を踏まえて、文字組み・余白・レイアウトを考える。{B}は、デザインを画一化するためではなく、一つひとつの制作物をよりよくするための指針を提供します。",
    "features_h2": "伝えるための4つの視点",
    "features_deck": "制作と見直しに共通する、{B}が大切にする考え方。",
    "features": [None,
                 {"idx": "02 / STRUCTURE", "mark": "▮▮▯", "h3": "内容に合う構成", "p": "伝える順番と情報の重要度を整理し、目的に合ったレイアウトを考えます。"},
                 {"idx": "03 / FIDELITY", "h3": "原稿を大切に"},
                 {"idx": "04 / REVIEW", "mark": "◌", "h3": "制作後の見直し", "p": "完成物の気になる点を、対象を変更せずに確認・整理するための指針です。"}],
    "idea_eyebrow": "DESIGNED FOR THE MESSAGE",
    "idea_h2": ["文字を並べるだけでなく", "読む体験を組み立てる"],
    "idea_body": "{B}は完成デザインを一律に指定しません。使う媒体や条件に合わせて考えるための知識を提供します。",
    "skills_h2": ["4つのスキル", "ひとつの考え方"],
    "skills_deck": "制作の入口から、Web・資料制作・レビューまで。",
    "skills": [None,
               ["Web", "{L}のWebサイト、記事、LP、UIの文字組みとデザインを支援。"],
               ["Documents", "報告書、資料、プレゼンテーションの構成と読みやすさを支援。"],
               ["Review", "制作物を変更せず、組版・情報・デザインの見直しを支援。"]],
    "skill_view": "スキルを見る",
    "install_h2": ["いつものAIツールから", "はじめよう"],
    "install_body": "導入方法は利用環境によって異なります。お使いのツールのガイドから、必要なスキルを選んでください。",
    "install_notes": ["スキルの追加・プラグイン登録・ローカル導入のガイド", "Claude Code・チャット向けの導入ガイド", "Gemini CLI・Geminiアプリ向けの導入ガイド"],
    "status_title": "RELEASED / v{V}",
    "status_link": "最新版のダウンロード ↗",
    "cta_h2": ["{L}のデザインに", "もうひとつの選択肢を"],
    "cta_body": "{B}はオープンソース。ソースコード、配布ファイル、変更履歴はGitHubで公開しています。",
    "cta_button": "GitHubで見る",
    "footer_sub": "{LE} typography skills for AI-assisted design.",
}

EN = {
    "title": "{B} — Natural {LE} typography, made with AI",
    "description": "{B} is a set of open-source AI skills for creating and reviewing {LE} websites, articles, reports, and presentations—with care for readability, layout, and the integrity of your original content.",
    "nav": ["About", "Principles", "Skills", "Get started"],
    "eyebrow": "OPEN-SOURCE SKILLS / {LU} TYPOGRAPHY",
    "h1": ["Natural {LE} typography,", "made with AI"],
    "lead": "{B} is a set of open-source AI skills for creating and reviewing {LE} websites, articles, reports, and presentations—with care for readability, layout, and the integrity of your original content.",
    "cta": ["Get started", "Learn more"],
    "hero_foot": ["OPEN SOURCE", "FOUR SKILLS", "{LU} FIRST"],
    "concept_h2": ["Not a uniform look—", "the right form for each message"],
    "concept_body": "Every brief, audience, and message is different. {B} helps AI shape typography, spacing, and hierarchy around the meaning and priorities of each piece—rather than applying one template to everything.",
    "features_h2": "Four things worth getting right",
    "features_deck": "Practical priorities for creating and reviewing {LE} content.",
    "features": [None,
                 {"idx": "02 / STRUCTURE", "mark": "▮▮▯", "h3": "Purposeful structure", "p": "Shape the layout around the information, its priority, and the reader’s goal."},
                 {"idx": "03 / FIDELITY", "h3": "Source fidelity"},
                 {"idx": "04 / REVIEW", "mark": "◌", "h3": "Read-only review", "p": "Check finished work and organize issues—without touching the files."}],
    "idea_eyebrow": "DESIGNED FOR THE MESSAGE",
    "idea_h2": ["Beyond arranging type", "Design the reading experience"],
    "idea_body": "{B} doesn't dictate a finished look. It gives AI the knowledge to adapt to each medium and brief.",
    "skills_h2": ["Four skills", "One approach"],
    "skills_deck": "From scoping the work to web, documents, and review.",
    "skills": [None,
               ["Web", "Typography and design for {LE} websites, articles, landing pages, and UI."],
               ["Documents", "Structure and readability for reports, business documents, and slide decks."],
               ["Review", "Review typography, information, and layout without editing source files."]],
    "skill_view": "View skill",
    "install_h2": ["Start with the AI tools", "you already use"],
    "install_body": "Setup varies by tool. Pick the guide for yours, then choose the skills you need.",
    "install_notes": ["Guides for adding skills, registering plugins, and local installation", "Setup guide for Claude Code and Claude chat", "Setup guide for Gemini CLI and the Gemini app"],
    "status_title": "RELEASED / v{V}",
    "status_link": "Download latest ↗",
    "cta_h2": ["Another way to design", "in {LE}"],
    "cta_body": "{B} is open source. The skills, releases, and full change history are on GitHub.",
    "cta_button": "View on GitHub",
    "footer_sub": "{LE} typography skills for AI-assisted design.",
}

# Not yet distributed: no "RELEASED", download or installation guide (KUMIHAN_07, rule 5).
JA_UPCOMING = {
    "cta": ["準備状況を見る", "{S}について"],
    "hero_foot": ["OPEN SOURCE", "FOUR SKILLS", "COMING SOON"],
    "skill_view": "近日公開",
    "install_h2": ["導入ガイドは", "準備中です"],
    "install_body": "配布ファイルと導入ガイドは準備中です。公開時にこのページでご案内します。",
    "install_notes": ["ChatGPT・Codex向けの導入ガイドを準備中", "Claude・Claude Code向けの導入ガイドを準備中", "Gemini向けの導入ガイドを準備中"],
    "status_title": "COMING SOON / v{V}",
    "status_link": "GitHubでKUMIHANを見る ↗",
    "cta_body": "{B}はオープンソースで開発しています。準備が整い次第、スキルと配布ファイルをGitHubで公開します。",
}

EN_UPCOMING = {
    "cta": ["See status", "Learn more"],
    "hero_foot": ["OPEN SOURCE", "FOUR SKILLS", "COMING SOON"],
    "skill_view": "Coming soon",
    "install_h2": ["Installation guides", "are in preparation"],
    "install_body": "Distribution files and installation guides are in preparation. They will be published on this page when ready.",
    "install_notes": ["Installation guide for ChatGPT and Codex in preparation", "Installation guide for Claude and Claude Code in preparation", "Installation guide for Gemini in preparation"],
    "status_title": "COMING SOON / v{V}",
    "status_link": "View KUMIHAN on GitHub ↗",
    "cta_body": "{B} is developed as open source. The skills and distribution files will be published on GitHub once ready.",
}

BASE = {"ja": JA, "en": EN}
UPCOMING_BASE = {"ja": dict(JA, **JA_UPCOMING), "en": dict(EN, **EN_UPCOMING)}


def fill(value, edition):
    brand, short, ja_name, en_name, version = EDITIONS[edition]
    if isinstance(value, str):
        return (value.replace("{B}", brand).replace("{S}", short).replace("{LU}", en_name.upper())
                .replace("{LE}", en_name).replace("{L}", ja_name).replace("{V}", version))
    if isinstance(value, list):
        return [fill(v, edition) for v in value]
    if isinstance(value, dict):
        return {k: fill(v, edition) for k, v in value.items()}
    return value


def shared(lang, edition):
    """Shared copy for one edition; None entries are edition-specific."""
    return fill((UPCOMING_BASE if edition in UPCOMING and not released(edition) else BASE)[lang], edition)


def extends(current, base):
    """True when an edition keeps the shared sentence and adds its own detail."""
    if not isinstance(current, str) or len(current) <= len(base):
        return False
    common = 0
    for a, b in zip(current, base):
        if a != b:
            break
        common += 1
    return common >= 0.7 * len(base)


# Release-specific wording belongs to each edition, not shared generic copy.
# English Measure joined the released editions after its independent package QA.
RELEASED_COPY_OVERRIDES = frozenset(("tr", "ms", "hu", "cs", "la", "he", "el", "nl", "en"))
EDITION_RELEASE_FIELDS = frozenset((
    "description", "cta", "hero_foot", "skill_view", "install_h2",
    "install_body", "install_notes", "status_title", "status_body", "status_link", "cta_body"
))


def apply(copy, lang, edition):
    """Return copy with every shared key set from the base; keeps edition specifics.

    A shared sentence that an edition extends with language-specific detail
    (the base text followed by more) is kept as written.
    """
    out = dict(copy)
    for key, value in shared(lang, edition).items():
        if edition in RELEASED_COPY_OVERRIDES and key in EDITION_RELEASE_FIELDS:
            out[key] = copy[key]
        elif key == "features":
            feats = [dict(f) for f in copy["features"]]
            for i, base in enumerate(value):
                if base is not None:
                    feats[i] = dict(feats[i], **{k: feats[i][k] if extends(feats[i].get(k), v) else v
                                                 for k, v in base.items()})
            out[key] = feats
        elif key == "skills":
            out[key] = [list(copy["skills"][i]) if base is None else
                        [copy["skills"][i][0], copy["skills"][i][1] if extends(copy["skills"][i][1], base[1]) else base[1]]
                        for i, base in enumerate(value)]
        else:
            out[key] = copy[key] if extends(copy.get(key), value) else value
    return out


def main():
    check = "--check" in sys.argv
    stale = []
    for edition, name in COPY_FILES.items():
        path = ROOT / "assets" / f"{name}-site-copy.json"
        if not path.exists():
            continue
        source = path.read_text(encoding="utf-8")
        data = json.loads(source)
        second = source.split("\n", 2)[1]
        indent = len(second) - len(second.lstrip(" "))
        for lang in ("ja", "en"):
            if lang in data:
                data[lang] = apply(data[lang], lang, edition)
        text = json.dumps(data, ensure_ascii=False, indent=indent) + ("\n" if source.endswith("\n") else "")
        if source != text:
            stale.append(path.relative_to(ROOT))
            if not check:
                path.write_text(text, encoding="utf-8")
    path = ROOT / "assets" / "upcoming-site-copy.json"
    source = path.read_text(encoding="utf-8")
    data = json.loads(source)
    for edition in (e for e in UPCOMING if e in data):
        for lang in ("ja", "en"):
            data[edition][lang] = apply(data[edition][lang], lang, edition)
    text = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    if source != text:
        stale.append(path.relative_to(ROOT))
        if not check:
            path.write_text(text, encoding="utf-8")
    if check and stale:
        sys.exit("shared ja/en copy out of date: " + ", ".join(map(str, stale)))
    print(("stale: " if stale else "ok: ") + ", ".join(map(str, stale)))


if __name__ == "__main__":
    main()
