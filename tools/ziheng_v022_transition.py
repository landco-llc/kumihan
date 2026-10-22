"""Bounded Ziheng v0.2.2 transition; frozen release baselines remain unchanged.

The record binds the original preservation expectation, the actual preimage at
BASE_COMMIT, and the reviewed candidate. Its byte hash is pinned independently
here, so editing an artifact and its recorded hash together does not admit it.
This source transition does not certify publication or change retained ZIPs.
"""
import hashlib
import json
from pathlib import Path

RECORD = "tests/contracts/ziheng-v022-transition.json"
RECORD_SHA256 = "c786053469510ec9cc11a5eb585ed95e0d9c0b7e829e043d83da14d55d121cee"
BASE_COMMIT = "677c9f69ffbb39ddeeaad8ebc7788719876ec5cf"
BASELINE = "tests/contracts/release-preservation.json"
BASELINE_SHA256 = "689cb61441ebd3e52634241ecadbc6c925a445f0b1570889e719d3f0d585a7f4"
LOCALE_BASELINE = "tests/thai/locale-baseline.json"
LOCALE_BASELINE_SHA256 = "b3d469885500095df27bf9afe9158aaa48e5468c910ca4475c520f8a95766029"
PREFIX = "plugins/kumihan-ziheng/"
SKILLS = ("kumihan-ziheng", "kumihan-ziheng-web",
          "kumihan-ziheng-documents", "kumihan-ziheng-review")
MEDIA = ("web-editorial", "web-marketing", "web-ui", "report-document",
         "presentation", "display-copy")
LOCALES = ("zh-Hant-TW", "zh-Hant-HK")
REFERENCES = ("documents", "review", "web", "workflow")
SITE_BODIES = frozenset(
    f"{stem}{suffix}.html"
    for stem in ("kumihan-zh-han", "docs/install-ziheng",
                 "docs/install-ziheng-claude", "docs/install-ziheng-gemini")
    for suffix in ("", ".en", ".ja")
)
_PRODUCT_PATHS = {
    ".claude-plugin/plugin.json", ".codex-plugin/plugin.json", "plugin.json",
    "gemini-extension.json", "INSTALL.md", "README.md", "UPDATES.md",
    "rules/zh-hant.json", "runtime/checks.py", "schemas/rule.schema.json",
    "sources.json",
} | {
    f"docs/installation-{host}.{locale}.md"
    for host in ("claude", "gemini") for locale in ("en", "ja", "zh-hant")
} | {
    f"{host}/{name}"
    for host in ("downloads", "downloads Claude", "downloads Gemini")
    for name in ("MANIFEST.json", "SHA256SUMS.txt")
} | {
    f"{host}/README.md" for host in ("downloads Claude", "downloads Gemini")
} | {
    f"entrypoints/{skill}.md" for skill in SKILLS
} | {
    f"references/{name}.md" for name in REFERENCES
}
_SKILL_PATHS = {
    "SKILL.md", "inventory.json", "rules/catalog.json",
    "schemas/rule.schema.json", "scripts/checks.py", "sources/public-sources.json",
} | {f"profiles/{medium}.json" for medium in MEDIA} | {
    f"references/{name}.md" for name in REFERENCES
}
PROTECTED_PATHS = frozenset({"README.md"} | {
    PREFIX + path for path in _PRODUCT_PATHS
} | {
    f"{PREFIX}skills/{skill}/{path}" for skill in SKILLS for path in _SKILL_PATHS
})


def _sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def allowed(path, family):
    """An exact path set, with no ZIP, history, or other-edition exception."""
    return ((family == "protected" and path in PROTECTED_PATHS) or
            (family == "bodies" and path in SITE_BODIES))


def _contract(root):
    """Fail closed on a missing, edited, or rebaselined contract."""
    root = Path(root)
    try:
        raw = (root / RECORD).read_bytes()
        if _sha256(raw) != RECORD_SHA256:
            return None
        data = json.loads(raw)
        if (data.get("schema_version") != 1 or
                data.get("scope") != "ziheng-v022-source-and-site" or
                data.get("version") != "0.2.2" or
                data.get("base_commit") != BASE_COMMIT or
                data.get("original_contract_sha256") != BASELINE_SHA256 or
                data.get("locale_baseline_sha256") != LOCALE_BASELINE_SHA256 or
                _sha256((root / BASELINE).read_bytes()) != BASELINE_SHA256 or
                _sha256((root / LOCALE_BASELINE).read_bytes()) != LOCALE_BASELINE_SHA256):
            return None
        if set(data.get("paths", {})) != PROTECTED_PATHS | SITE_BODIES:
            return None
        if set(data.get("locale_profiles", {})) != {
                f"{locale}|{medium}" for locale in LOCALES for medium in MEDIA}:
            return None
        return data
    except (OSError, ValueError, TypeError):
        return None


def admitted(root, path, before, raw, family):
    """Admit only the reviewed final bytes against the original frozen hash."""
    if not allowed(path, family):
        return False
    data = _contract(root)
    if data is None:
        return False
    row = data["paths"].get(path, {})
    if row.get("family") != family or row.get("before") != before:
        return False
    if _sha256(raw) != row.get("after"):
        return False
    if path == "README.md":
        change = data["readme_change"]
        after_line = change["after_line"].encode("utf-8")
        preimage_line = change["preimage_line"].encode("utf-8")
        # Only the ZH-HANT source-version row changes. Publication stays factual.
        if (raw.count(after_line) != 1 or
                _sha256(raw.replace(after_line, preimage_line, 1)) != row["preimage_sha256"]):
            return False
    return True


def admitted_locale(root, locale, medium, before, context_sha256, after_sha256):
    """Admit twelve explicit ZH profiles; all other locale baselines still apply."""
    if locale not in LOCALES or medium not in MEDIA:
        return False
    data = _contract(root)
    if data is None:
        return False
    row = data["locale_profiles"].get(f"{locale}|{medium}", {})
    return (row.get("locale") == locale and row.get("medium") == medium and
            row.get("before") == before and
            row.get("context_sha256") == context_sha256 and
            row.get("after") == after_sha256)
