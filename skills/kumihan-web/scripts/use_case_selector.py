#!/usr/bin/env python3
"""Optional, dependency-free routing aide for KUMIHAN.

This is a conservative surface/intent router, not a natural-language
understanding model or an image/visual-quality detector. Host judgment must
resolve unrecognized cases. It never modifies input or reports a quality pass.
The user-approved policy lives in references/use-case-selection.md.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ADAPTERS = HERE.parent / "references" / "use-case-adapters.json"
MODES = ("study", "build", "audit", "refine")
STAGES = ("before-production", "after-production")
MEDIUMS = (
    "web-editorial", "web-marketing", "web-ui",
    "report-document", "presentation", "display-copy",
)

# Only affirmative signals for deliverable surfaces. Never treat absence of a
# pattern as proof of any other deliverable type.
SIGNALS = {
    "social": re.compile(r"SNS|Instagram|インスタ|ソーシャルメディア|social[- ]?media", re.I),
    "static": re.compile(r"静止|画像|イメージ|PNG|JPE?G|WEBP|static|image|graphic", re.I),
    "motion": re.compile(r"動画|映像|アニメーション|video|motion|reel", re.I),
    "poster": re.compile(r"ポスター|poster", re.I),
    "banner": re.compile(r"バナー|banner", re.I),
    "interactive": re.compile(r"HTML|動的|クリック|インタラクティブ|interactive|clickable", re.I),
    "landing": re.compile(r"ランディングページ|ランディング|(?<![a-z])LP(?![a-z])|landing[- ]page", re.I),
    "slides": re.compile(r"プレゼン|スライド|PowerPoint|\.pptx|pitch deck|slide[- ]deck|presentation", re.I),
    "report": re.compile(r"報告書|調査報告|配布資料|(?<![a-z])report(?![a-z])|\.docx", re.I),
    "ui": re.compile(r"アプリ画面|入力フォーム|(?<![a-z])UI(?![a-z])|app screen|user interface|web form", re.I),
    "article": re.compile(r"記事|ブログ|特集ページ|blog post|(?<![a-z])article(?![a-z])|editorial page", re.I),
    "website": re.compile(r"Webサイト|ウェブサイト|Webページ|website|web page", re.I),
    "copy": re.compile(r"キャッチコピー|短いコピー|見出し|スローガン|コピーライティング|tagline|headline|short copy", re.I),
}
LANG_SIGNALS = {
    "ja": re.compile(r"日本語|Japanese", re.I),
    "zh-Hant": re.compile(r"繁体|繁體|Traditional Chinese", re.I),
    "zh-Hans": re.compile(r"簡体|简体|簡體|Simplified Chinese", re.I),
    "ko": re.compile(r"韓国語|한국어|Korean", re.I),
    "th": re.compile(r"タイ語|ภาษาไทย|Thai", re.I),
    "en": re.compile(r"英語|English", re.I),
}


def _spec() -> dict:
    data = json.loads(ADAPTERS.read_text(encoding="utf-8"))
    if data["default_review_intensity"] != "standard":
        raise ValueError("Unsupported routing default")
    allowed = set(MEDIUMS)
    if set(data["primary_profiles"]) != allowed:
        raise ValueError("Profile catalog differs from six supported media")
    adapters = data["adapters"]
    if len(adapters) != len({a["id"] for a in adapters}):
        raise ValueError("Duplicate use-case adapter identifiers")
    for item in adapters:
        if item["primary_profile"] not in allowed:
            raise ValueError("Unsupported medium in adapter: " + item["id"])
    return data


def _detect(brief: str) -> tuple[list[tuple[str, str | None, str]], str | None]:
    """Bounded candidates; never generate a visual/quality verdict."""
    # In an explicit "X ではなく Y" contrast, evaluate the positively
    # requested deliverable Y instead of treating rejected X as another task.
    # Do not discard X when Y contains no deliverable (e.g. style advice).
    positive = brief
    if "ではなく" in brief:
        tail = brief.rsplit("ではなく", 1)[1].lstrip(" 、，,")
        if any(p.search(tail) for p in SIGNALS.values()):
            positive = tail
    has = {key: bool(pattern.search(positive)) for key, pattern in SIGNALS.items()}
    # A headline/copy *only* for a wider website or LP is display-copy,
    # not a request to build the entire website or landing page.
    limited_copy = (
        re.search(r"(?:見出しコピー|キャッチコピー|短いコピー|スローガン|見出し)\s*(?:だけ|のみ)", positive)
        or re.search(r"\b(?:only|just)\b.{0,25}\b(?:headline|tagline|copy)\b", positive, re.I)
    )
    if has["copy"] and limited_copy:
        return [("display-copy", None, "explicitly limited to copy/headline")], None
    result: list[tuple[str, str | None, str]] = []
    question = None

    if has["landing"]:
        result.append(("web-marketing", "landing-page", "landing-page deliverable"))
    if has["slides"]:
        result.append(("presentation", "slide-deck", "presentation deliverable"))
    if has["report"]:
        result.append(("report-document", "report", "report deliverable"))
    if has["poster"]:
        result.append(("display-copy", "poster", "poster deliverable"))
    if has["banner"]:
        if has["interactive"] and has["static"]:
            question = "バナーの納品物は静止画像ですか、それともHTML／操作可能なWebバナーですか？"
        elif has["interactive"]:
            result.append(("web-marketing", None, "interactive Web banner; not a static image"))
        elif has["static"]:
            result.append(("display-copy", "digital-banner", "static image banner"))
        else:
            question = "バナーの納品物は静止画像ですか、それともHTML／操作可能なWebバナーですか？"
    if has["social"] and has["static"] and not has["motion"]:
        result.append(("display-copy", "social-static", "static social-media image"))
    if has["social"] and has["motion"]:
        question = "SNSの納品物は静止画像ですか、動画ですか？"
    if has["ui"]:
        result.append(("web-ui", None, "interactive app/UI screen"))
    if has["article"]:
        result.append(("web-editorial", None, "editorial web article"))
    if has["website"] and not has["landing"] and not has["ui"] and not has["article"]:
        result.append(("web-editorial", None, "generic website content"))
    if has["copy"] and not result:
        result.append(("display-copy", None, "short display copy"))

    # Social image is more specific than a generic static banner, but we cannot
    # assume a deliverable when independently different media are requested.
    unique: list[tuple[str, str | None, str]] = []
    seen: set[tuple[str, str | None]] = set()
    for medium, adapter, reason in result:
        if (medium, adapter) not in seen:
            unique.append((medium, adapter, reason))
            seen.add((medium, adapter))
    if ("display-copy", "social-static") in seen and ("display-copy", "digital-banner") in seen:
        unique = [r for r in unique if r[1] != "digital-banner"]
    return unique, question


def route(
    brief: str,
    *,
    manual_adapter: str | None = None,
    manual_medium: str | None = None,
    locale: str | None = None,
    strict_explicit: bool = False,
    mode: str = "build",
    stage: str = "before-production",
) -> dict:
    """Return a transparent recommendation, not production authorization."""
    if not isinstance(brief, str) or not brief.strip():
        raise ValueError("A nonempty brief is required")
    if mode not in MODES or stage not in STAGES:
        raise ValueError("Unrecognized workflow mode or production stage")
    spec = _spec()
    adapters = {a["id"]: a for a in spec["adapters"]}
    if manual_adapter is not None and manual_adapter not in adapters:
        raise ValueError("Unknown adapter: " + manual_adapter)
    if manual_medium is not None and manual_medium not in MEDIUMS:
        raise ValueError("Unknown medium: " + manual_medium)
    if locale is not None and (not locale.strip() or any(c.isspace() for c in locale)):
        raise ValueError("Locale must be a nonempty language tag without spaces")

    candidates, question = _detect(brief)
    suggested_mediums = {c[0] for c in candidates}
    detected_locales = [lang for lang, pattern in LANG_SIGNALS.items() if pattern.search(brief)]
    language = locale or (detected_locales[0] if len(detected_locales) == 1 else None)
    context = {
        "status": "selected",
        "medium": None,
        "adapter": None,
        "locale": language,
        "locale_resolution": "explicit" if locale else ("brief-indicated" if language else "requires-host-evidence"),
        "review_intensity": "strict" if strict_explicit else "standard",
        "workflow_mode": mode,
        "selection_source": "manual" if manual_adapter or manual_medium else "auto",
        "selection_reason": "",
        "needs_confirmation": False,
        "confirmation_question": None,
        "focus": [],
        "limitations": [
            "Selection is guidance only; it grants no editing, approval, asset usage, or publishing permission.",
            "Actual rendering, design quality and protected-source checks are not performed by this router.",
            "Strict DESIGN-002 conditional error needs independently verified selection before production and real comparison evidence.",
        ],
        "prior_strict_policy_verified": False,
        "source_decision": spec["source_decision"],
    }

    def clarify(q: str, reason: str) -> dict:
        context["status"] = "needs-clarification"
        context["needs_confirmation"] = True
        context["confirmation_question"] = q
        context["selection_reason"] = reason
        return context

    # A manual choice is given precedence where it is consistent with the
    # actual output surface. A conflict is never silently rewritten or waived.
    if manual_adapter:
        chosen = adapters[manual_adapter]
        medium = chosen["primary_profile"]
        if manual_medium and manual_medium != medium:
            return clarify("指定した媒体と用途アダプターのどちらを優先しますか？", "manual medium/adapter conflict")
        if suggested_mediums and medium not in suggested_mediums:
            return clarify("ご指定の用途と制作物の形式が異なります。どちらの納品形式ですか？", "manual adapter/output conflict")
        if question and not suggested_mediums:
            return clarify(question, "delivery format materially ambiguous despite manual adapter")
        context["medium"], context["adapter"] = medium, manual_adapter
        context["selection_reason"] = "compatible explicit manual adapter override"
        if any(c[1] is not None and c[1] != manual_adapter for c in candidates):
            context["limitations"].append("Manual adapter overrides an inferred same-medium use case; preserve the actual delivery platform and its checks.")
    elif manual_medium:
        if suggested_mediums and manual_medium not in suggested_mediums:
            return clarify("ご指定の媒体と制作物の形式が異なります。どちらの形式を制作しますか？", "manual medium/output conflict")
        same_medium = [c for c in candidates if c[0] == manual_medium]
        if len({c[1] for c in same_medium}) > 1:
            return clarify("主な制作物の用途を一つ確認してください。", "multiple adapters under manual medium")
        if question and not same_medium:
            return clarify(question, "ambiguous delivery format")
        context["medium"] = manual_medium
        context["adapter"] = same_medium[0][1] if same_medium else None
        context["selection_reason"] = "explicit medium; applicable adapter inferred only when supported"
    else:
        if question:
            return clarify(question, "ambiguous delivery format")
        if len(suggested_mediums) > 1:
            return clarify("主に制作・納品するのはどの形式ですか？", "multiple materially different output media")
        if not candidates:
            return clarify("制作するものはWebページ、画像、資料、スライドなどのどれですか？", "primary medium not specified")
        if len({c[1] for c in candidates}) > 1:
            return clarify("制作するものの主な用途は何ですか？", "multiple equally plausible adapters")
        context["medium"], context["adapter"], reason = candidates[0]
        context["selection_reason"] = "explicit deliverable evidence: " + reason

    if context["adapter"] is not None:
        chosen = adapters[context["adapter"]]
        assert context["medium"] == chosen["primary_profile"]
        context["focus"] = chosen["focus"]
        context["limitations"].extend(chosen["limits"])
    if len(detected_locales) > 1 and not locale:
        context["limitations"].append("Mixed/ambiguous locale: resolve each text segment in the host; never translate automatically.")
    if stage == "after-production" and strict_explicit:
        context["limitations"].append("Post-production strict request is not retroactive pre-production strict evidence.")
    if mode == "audit":
        context["limitations"].append("Audit is strictly read-only; this result must not trigger refinements.")
    return context


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief", required=True, help="Short trusted summary of the requested deliverable")
    parser.add_argument("--adapter", help="Explicit manual use-case adapter override")
    parser.add_argument("--medium", choices=MEDIUMS, help="Explicit primary medium")
    parser.add_argument("--locale", help="Explicit locale; no automatic translation")
    parser.add_argument("--strict", action="store_true", help="Explicit user request for strict review")
    parser.add_argument("--mode", choices=MODES, default="build")
    parser.add_argument("--stage", choices=STAGES, default="before-production")
    args = parser.parse_args()
    result = route(
        args.brief, manual_adapter=args.adapter, manual_medium=args.medium,
        locale=args.locale, strict_explicit=args.strict, mode=args.mode, stage=args.stage
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
