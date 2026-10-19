#!/usr/bin/env python3
"""Build a deterministic, self-contained KUMIHAN language registry from existing Skills."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LANGUAGE_TAG = re.compile(r"^[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")
MAX_FILE_BYTES = 256_000


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def collect_rule_data(source: Path) -> tuple[list[dict], list[dict]]:
    normalized = []
    files = []
    for path in sorted((source / "rules").rglob("*.json")):
        if path.stat().st_size > MAX_FILE_BYTES:
            raise ValueError("Rule file too large: " + str(path))
        raw = path.read_bytes()
        obj = json.loads(raw)
        files.append({"path": str(path.relative_to(PROJECT_ROOT)), "sha256": sha256(raw)})
        records = obj if isinstance(obj, list) else obj.get("rules", []) if isinstance(obj, dict) else []
        for item in records:
            if not isinstance(item, dict):
                continue
            rule_id = item.get("id")
            if not isinstance(rule_id, str) or not rule_id:
                continue
            title = next((item[k] for k in ("title", "requirement_en", "description_en", "policy_ja", "description") if isinstance(item.get(k), str)), "")
            normalized.append({
                "id": rule_id,
                "title": title,
                "verification": item.get("verification", "guidance-only"),
                "source_file": str(path.relative_to(PROJECT_ROOT)),
                "details": item,
            })
    return normalized, files


def build_one(module_id: str, entry: dict) -> dict:
    if not LANGUAGE_TAG.fullmatch(module_id):
        raise ValueError("Invalid module id " + module_id)
    source_value = entry["source"]
    if not isinstance(source_value, str) or source_value.startswith("/") or ".." in Path(source_value).parts:
        raise ValueError("Unsafe source path")
    source = (PROJECT_ROOT / source_value).resolve()
    if not source.is_relative_to(PROJECT_ROOT.resolve()) or not source.is_dir():
        raise ValueError("Missing or escaping source: " + source_value)
    if module_id == "ja":
        plugin_path = PROJECT_ROOT / "plugin.json"
        skill_path = source / "SKILL.md"
    else:
        plugin_path = source / "plugin.json"
        slug = source.name
        skill_path = source / "skills" / slug / "SKILL.md"
        if not skill_path.exists():
            candidates = sorted((source / "skills").glob("*/SKILL.md"))
            if not candidates:
                raise ValueError("Missing entry Skill: " + source_value)
            skill_path = candidates[0]
    plugin = load_json(plugin_path)
    skill_raw = skill_path.read_bytes()
    rules, rule_files = collect_rule_data(source)
    if not rules:
        raise ValueError("No eligible structured rules: " + module_id)
    locale_dir = source / "locales"
    locales = []
    if locale_dir.exists():
        for p in sorted(locale_dir.glob("*.json")):
            stem = p.stem
            if LANGUAGE_TAG.fullmatch(stem) and (stem == module_id or stem.startswith(module_id + "-")):
                locales.append(stem)
    files = [
        {"path": str(plugin_path.relative_to(PROJECT_ROOT)), "sha256": sha256(plugin_path.read_bytes())},
        {"path": str(skill_path.relative_to(PROJECT_ROOT)), "sha256": sha256(skill_raw)},
        *rule_files,
    ]
    # This hash is scoped to ONE module and remains stable when other modules change.
    digest = sha256(json.dumps(files, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    label = plugin.get("extensions", {}).get("com.openai", {}).get("interface", {}).get("displayName")
    return {
        "id": module_id,
        "name": label or entry.get("label") or plugin.get("name", module_id),
        "version": plugin.get("version", "unversioned"),
        "source": source_value,
        "status": "preview_unverified",
        "capabilities": ["reference_guidance", "source_preserving_review"],
        "locales": sorted(set(locales + [module_id])),
        "description": plugin.get("description", ""),
        "entry_skill_path": str(skill_path.relative_to(PROJECT_ROOT)),
        "entry_skill_text": skill_raw.decode("utf-8"),
        "rules": rules,
        "files": files,
        "module_sha256": digest,
    }


def build() -> dict:
    conf = load_json(PROJECT_ROOT / "universal" / "languages.json")
    modules = conf.get("modules")
    if not isinstance(modules, dict) or not modules:
        raise ValueError("Language inventory is empty")
    built = {module_id: build_one(module_id, modules[module_id]) for module_id in sorted(modules)}
    return {
        "schema_version": "1.0",
        "engine": "KUMIHAN Universal MCP",
        "modules": built,
        "module_count": len(built),
        "source_integrity": "per_module_sha256",
        "validation": "guidance-only until host/render/static checks independently proven",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "universal" / "server" / "runtime" / "registry.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        data = build()
        content = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        if args.check:
            if not args.output.exists() or args.output.read_text(encoding="utf-8") != content:
                raise ValueError("Outdated registry artifact")
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(content, encoding="utf-8")
        print(f"validated modules: {data['module_count']}, registry bytes: {len(content.encode('utf-8'))}")
        return 0
    except (ValueError, OSError, KeyError, json.JSONDecodeError, UnicodeError) as exc:
        print(f"build registry failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
