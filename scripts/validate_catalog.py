"""Offline frozen schema support and catalog validation (development only)."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource

SCHEMA_HASHES = {
    "design-contract": "a38b3720b0b1a113a53bba4552bcc866f44f900db94b8187962038fe7a7555b9",
    "profile": "dc2e9397d380f3260b0a69f6dd8b72980e3eb2b326a02ba343537f744b6ccbce",
    "release-manifest": "1bda6b026d34932a66060c8435d8d5e31a20791c410971acc063192581ab1b36",
    "report": "4396bcbc1f709f6d451319ad93dbd891436ab367865969bcd958c1cdad998d7a",
    "rule": "132eda194cd883d32dd833714b75fee5da0d6a254c5d30459cccb1528538afb5",
}
MAX_FILE = 2 * 1024 * 1024
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?", re.ASCII)


def safe_name(name):
    """Portable relative data path; avoid platform aliases and Unicode ambiguity."""
    if not isinstance(name, str) or not name or not re.fullmatch(r"[A-Za-z0-9_./-]+", name):
        raise ValueError("invalid portable path")
    for part in name.split("/"):
        if (part in ("", ".", "..") or part.endswith(".") or
                part.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}):
            raise ValueError("invalid portable path")
    return name


def read_bytes(path, limit=MAX_FILE):
    """Reject symlinks in every component and nonregular inputs, bound reads."""
    path = Path(path).absolute()
    for component in [*reversed(path.parents), path]:
        if component.is_symlink():
            raise ValueError("symlink input rejected")
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError("nonregular input rejected")
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
    with os.fdopen(os.open(path, flags), "rb") as handle:
        if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
            raise ValueError("nonregular input rejected")
        data = handle.read(limit + 1)
    if len(data) > limit:
        raise ValueError("input exceeds size limit")
    return data


def _pairs(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON key")
        value[key] = item
    return value


def parse_json(data):
    try:
        return json.loads(data, object_pairs_hook=_pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")))
    except (UnicodeError, json.JSONDecodeError, RecursionError):
        raise ValueError("invalid UTF-8 JSON") from None


def read_json(path):
    return parse_json(read_bytes(path))


def _offline(uri):
    raise NoSuchResource(ref=uri)


def validators(root=None):
    root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    try:
        return validators_from_bytes({name: read_bytes(root / "schemas" / (name + ".schema.json"))
                                      for name in SCHEMA_HASHES})
    except (OSError, ValueError) as error:
        raise ValueError("missing, invalid or unsupported local schemas") from error


def validators_from_bytes(resources):
    """Register exact frozen resources without any repository or network lookup."""
    schemas = {}
    for name, digest in SCHEMA_HASHES.items():
        data = resources.get(name)
        if data is None or hashlib.sha256(data).hexdigest() != digest:
            raise ValueError("missing or unsupported frozen schema")
        schema = parse_json(data)
        Draft202012Validator.check_schema(schema)
        schemas[name] = schema
    registry = Registry(retrieve=_offline).with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas.values())
    return {name: Draft202012Validator(schema, registry=registry) for name, schema in schemas.items()}


def schema_errors(validator, value, label):
    # Do not echo untrusted instance values, schema messages or operating paths.
    # Dynamic map keys (e.g. environment.tools) are instance content too.
    return sorted({f"{label}: schema violation ({error.validator})"
                   for error in validator.iter_errors(value)})


def emit(status, errors, **details):
    print(json.dumps({"status": status, "errors": sorted(set(errors)), **details}, sort_keys=True))


class ResultParser(argparse.ArgumentParser):
    def error(self, message):
        # argparse includes untrusted argument values in its default diagnostics.
        emit("incomplete", ["CLI: missing or invalid arguments"])
        self.exit(2, "Invalid arguments; use --help for the contract.\n")


class InputContentError(ValueError):
    """Readable local product input violates a verified data invariant."""


def json_inputs(directory):
    """Flat, explicit JSON input directory; no recursive or extension-based surprises."""
    directory = Path(directory)
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError("catalog: missing or unsafe input directory")
    paths = sorted(directory.iterdir())
    if not paths or len(paths) > 128:
        raise ValueError("catalog: missing or excessive input inventory")
    aliases = set()
    for path in paths:
        safe_name(path.name)
        if path.name.casefold() in aliases:
            raise ValueError("catalog: case-colliding input names")
        aliases.add(path.name.casefold())
        if path.suffix != ".json" or path.is_symlink() or not path.is_file():
            raise ValueError("catalog: symlink, unlisted or non-JSON input")
    return paths


def rule_profile_data(root):
    """Frozen rule/profile structure only; not source/fixture catalog admission."""
    root = Path(root)
    checks = validators(root)
    expected = checks["rule"].schema["$defs"]["rule_id"]["enum"]
    profile_ids = checks["rule"].schema["$defs"]["media_profile"]["enum"]
    errors = []; index = {}
    for path in json_inputs(root / "rules"):
        values = read_json(path)
        if not isinstance(values, list):
            errors.append("catalog: rule files must be JSON arrays")
            continue
        if len(values) > 256:
            errors.append("catalog: excessive rule inventory")
            continue
        for value in values:
            invalid = schema_errors(checks["rule"], value, "catalog rule")
            errors.extend(invalid)
            if invalid:
                continue
            if value["id"] in index:
                errors.append("catalog: duplicate rule ID")
            index[value["id"]] = value
            if value["verification"]["coverage"] == "implemented":
                # Notes and case strings are declarations, not verified detector evidence.
                errors.append("catalog: implemented coverage lacks verified procedure/tests")
    if set(expected) - index.keys():
        errors.append("catalog: missing rule IDs")
    profiles = {}
    for path in json_inputs(root / "profiles"):
        value = read_json(path)
        invalid = schema_errors(checks["profile"], value, "catalog profile")
        errors.extend(invalid)
        if invalid:
            continue
        if value["id"] in profiles:
            errors.append("catalog: duplicate profile ID")
        profiles[value["id"]] = value
        for identity in value["rule_ids"]:
            if identity not in index:
                errors.append("catalog: unresolved profile rule")
            elif value["id"] not in index[identity]["media"]:
                errors.append("catalog: profile rule media mismatch")
    if set(profile_ids) - profiles.keys():
        errors.append("catalog: missing profile IDs")
    if errors:
        raise InputContentError("; ".join(sorted(set(errors))))
    return [index[identity] for identity in expected], [profiles[identity] for identity in profile_ids]


def source_errors(registry, rules, checks):
    """Coordinated W02 registry shape; declarations are not source authority."""
    from datetime import date
    import ipaddress
    from urllib.parse import urlsplit
    text = {"type": "string", "pattern": r"\S", "minLength": 1}
    nullable = {"anyOf": [text, {"type": "null"}]}
    properties = {"id": text, "type": {"enum": checks["rule"].schema["properties"]["kind"]["enum"]},
        "classification": {"enum": ["adopted", "comparison-only", "deferred"]},
        "title": text, "url": nullable, "version": nullable, "accessed_at": nullable,
        "context": text, "adopted_principle": nullable, "limits": text, "statement": nullable,
        "rule_ids": {"type": "array", "uniqueItems": True, "items": checks["rule"].schema["$defs"]["rule_id"]}}
    shape = {"type": "object", "properties": {"registry_version": {"const": "0.1.0"},
        "sources": {"type": "array", "maxItems": 256, "items": {"type": "object", "properties": properties,
        "required": list(properties), "additionalProperties": False}}},
        "required": ["registry_version", "sources"], "additionalProperties": False}
    if schema_errors(Draft202012Validator(shape), registry, "source schema"):
        return ["catalog: source schema violation"]
    errors = []; sources = {}; index = {rule["id"]: rule for rule in rules}
    for source in registry["sources"]:
        identity = source["id"]
        if identity in sources:
            errors.append("catalog: duplicate source ID")
        sources[identity] = source
        if identity.startswith("policy:"):
            if source["type"] != "project-policy":
                errors.append("catalog: declared source kind mismatch")
            if source["url"] is not None or not isinstance(source["statement"], str) or not source["statement"].strip():
                errors.append("catalog: source schema missing authored policy statement/location")
        else:
            try:
                url = urlsplit(source["url"] or "")
                public = (url.scheme in ("http", "https") and url.hostname and not url.username and not url.password
                          and url.hostname not in {"localhost", "127.0.0.1", "::1"}
                          and not re.search(r"\s", source["url"] or ""))
                if public:
                    try:
                        public = ipaddress.ip_address(url.hostname).is_global
                    except ValueError:
                        public = not url.hostname.lower().endswith((".internal", ".local", ".localhost"))
            except ValueError:
                public = False
            if not public:
                errors.append("catalog: missing or unsupported public source URL")
            if source["type"] == "project-policy" or source["statement"] is not None:
                errors.append("catalog: declared source kind mismatch")
        if source["classification"] == "adopted":
            if any(not isinstance(source[field], str) or not source[field].strip() for field in ("version", "accessed_at", "adopted_principle")):
                errors.append("catalog: source schema missing adopted attribution")
            try:
                stamp = source["accessed_at"]
                if not isinstance(stamp, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", stamp):
                    raise ValueError("invalid date")
                date.fromisoformat(stamp)
            except ValueError:
                errors.append("catalog: invalid source access date")
        elif source["rule_ids"] or source["adopted_principle"] is not None or source["statement"] is not None:
            errors.append("catalog: non-adopted source claims adopted coverage")
        for identity_rule in source["rule_ids"]:
            if identity_rule not in index or identity not in index[identity_rule]["source_refs"]:
                errors.append("catalog: unresolved or inconsistent source rule reference")
    for rule in rules:
        resolved = []
        for identity in rule["source_refs"]:
            source = sources.get(identity)
            if source is None:
                errors.append("catalog: unresolved source reference")
                continue
            if source["classification"] != "adopted":
                errors.append("catalog: non-adopted source reference")
            if rule["id"] not in source["rule_ids"]:
                errors.append("catalog: inconsistent source rule coverage")
            resolved.append(source)
        if resolved and not any(source["type"] == rule["kind"] for source in resolved):
            errors.append("catalog: declared source kind mismatch")
    return sorted(set(errors))



PRIORITY_IDS = ("CONTENT-001", "CONTENT-002", "CONTENT-004", "JA-TYPE-002", "JA-TYPE-004", "JA-TYPE-005", "JA-TYPE-006", "JA-TYPE-008", "JA-TYPE-009", "WEB-001", "WEB-004", "WEB-005", "DESIGN-001", "DESIGN-002", "EVIDENCE-001")


def case_errors(dataset, rules, profiles, checks):
    """Check fixture declarations/relationships; never run or upgrade assertions."""
    text = {"type": "string", "pattern": r"\S", "minLength": 1}
    properties = {"id": text, "rule_id": checks["rule"].schema["$defs"]["rule_id"],
        "kind": {"enum": ["positive", "negative", "exception"]},
        "profile": checks["rule"].schema["$defs"]["media_profile"],
        "input": {"type": "object", "minProperties": 1},
        "expected_status": checks["report"].schema["$defs"]["status"],
        "method": checks["rule"].schema["$defs"]["method"],
        "assertions": {"type": "array", "minItems": 1, "items": text},
        "assertion_type": {"enum": ["schema", "fixture-content", "assisted", "manual-render"]},
        "limitations": {"type": "array", "items": text}}
    shape = {"type": "object", "properties": {"fixture_version": {"const": "0.1.0"},
        "cases": {"type": "array", "maxItems": 1024, "items": {"type": "object", "properties": properties,
        "required": list(properties), "additionalProperties": False}}},
        "required": ["fixture_version", "cases"], "additionalProperties": False}
    if schema_errors(Draft202012Validator(shape), dataset, "case schema"):
        return ["catalog: case schema violation"]
    errors = []; cases = {}; triads = {identity: set() for identity in PRIORITY_IDS}
    index = {rule["id"]: rule for rule in rules}; profile_index = {p["id"]: p for p in profiles}
    for case in dataset["cases"]:
        if case["id"] in cases:
            errors.append("catalog: duplicate case ID")
        cases[case["id"]] = case
        rule = index.get(case["rule_id"])
        if rule is None or case["id"] not in rule["case_ids"]:
            errors.append("catalog: case rule binding mismatch")
            continue
        if case["method"] != rule["verification"]["method"]:
            errors.append("catalog: case method mismatch")
        if (case["profile"] not in rule["media"] or case["profile"] not in profile_index or
                case["rule_id"] not in profile_index[case["profile"]]["rule_ids"]):
            errors.append("catalog: case profile mismatch")
        if case["rule_id"] in triads:
            triads[case["rule_id"]].add(case["kind"])
    for rule in rules:
        for identity in rule["case_ids"]:
            if identity not in cases:
                errors.append("catalog: unresolved case reference")
            elif cases[identity]["rule_id"] != rule["id"]:
                errors.append("catalog: case rule binding mismatch")
    if any(kinds != {"positive", "negative", "exception"} for kinds in triads.values()):
        errors.append("catalog: incomplete priority triad")
    return sorted(set(errors))


def load_catalog(root: Path) -> list[dict]:
    """Admit coordinated local catalog/source/profile/fixture declarations.

    This does not execute fixture assertions, authenticate approvals or assess
    Japanese visual quality. Implemented detector/procedure evidence currently
    has no supported verifier and is explicitly rejected rather than fabricated.
    """
    try:
        rules, profiles = rule_profile_data(root)
        checks = validators(root)
        registry = Path(root) / "sources" / "public-sources.json"
        if not registry.exists():
            raise ValueError("catalog: missing source registry")
        errors = source_errors(read_json(registry), rules, checks)
        cases = Path(root) / "tests" / "fixtures" / "priority-cases.json"
        if not cases.exists():
            raise ValueError("catalog: missing priority cases")
        errors.extend(case_errors(read_json(cases), rules, profiles, checks))
        if errors:
            raise InputContentError("; ".join(sorted(set(errors))))
        return rules
    except OSError:
        raise ValueError("catalog: missing or unreadable local input") from None


def main():
    import sys
    parser = ResultParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    try:
        catalog = load_catalog(args.root)
        emit("passed", [], rule_count=len(catalog))
        return 0
    except ValueError as error:
        # Every diagnostic above is producer-authored, never raw source values.
        emit("incomplete", [str(error)])
        print("Catalog admission rejected; see sanitized diagnostics.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    __import__("sys").exit(main())
