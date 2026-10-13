"""Bounded data-only ZIP inspection. Does not execute content or fetch references."""
import hashlib
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat
import sys
import zipfile
import zlib

try:
    from .validate_catalog import MAX_FILE, VERSION, safe_name, read_bytes, parse_json, emit, SCHEMA_HASHES, validators_from_bytes, schema_errors, ResultParser, source_errors
except ImportError:
    from validate_catalog import MAX_FILE, VERSION, safe_name, read_bytes, parse_json, emit, SCHEMA_HASHES, validators_from_bytes, schema_errors, ResultParser, source_errors

SKILLS = ("kumihan", "kumihan-web", "kumihan-documents", "kumihan-review")
MAX_MEMBERS = 2048
MAX_TOTAL = 64 * 1024 * 1024
MAX_ARCHIVE = 64 * 1024 * 1024
DIGEST = re.compile(r"sha256:[0-9a-f]{64}")


def allowed_file(name):
    safe_name(name)
    parts = name.split("/")
    if any(re.search(r"(?:^|[-_.])(?:raw-log|command-log|transcript|maintainer-routing|approvals|credentials|secrets)(?:[-_.]|$)", part, re.I) for part in parts):
        return False
    if name in {"SKILL.md", "LICENSE", "inventory.json"}:
        return True
    if parts[0] == "schemas":
        return name in {f"schemas/{schema}.schema.json" for schema in SCHEMA_HASHES}
    if parts[0] == "rules":
        return name == "rules/catalog.json"
    if parts[0] == "sources":
        return name == "sources/public-sources.json"
    if parts[0] == "profiles":
        return len(parts) == 2 and PurePosixPath(name).suffix == ".json"
    return len(parts) >= 2 and parts[0] == "references" and PurePosixPath(name).suffix in {".md", ".json"}


def local_targets(name, data):
    text = data.decode("utf-8")
    targets = re.findall(r"\]\(\s*([^\s)]+)", text)
    targets += re.findall(r"(?m)^\s*\[[^\]]+\]:\s*(\S+)", text)
    targets += re.findall(r"`((?:references|rules|profiles|schemas|sources)/[^`\s]+)`", text)
    resolved = []
    for target in targets:
        target = target.strip("<>")
        if target.startswith(("https://", "http://", "#", "mailto:")):
            continue
        target = target.split("#", 1)[0]
        if not target or target.startswith("/") or "\\" in target or ":" in target or "%" in target or "?" in target:
            raise ValueError("unsafe reference")
        result = posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
        resolved.append(safe_name(result))
    return resolved


def reference_errors(files):
    """Check Markdown links, definitions and quoted local resource paths offline."""
    errors = []
    for name, data in sorted(files.items()):
        if not name.endswith(".md"):
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeError:
            errors.append("bundle: invalid UTF-8 guidance")
            continue
        # Active HTML dependencies would evade ordinary Markdown links.
        if re.search(r"<(?:script|iframe|object)\b|\b(?:import|require)\s*\(", text, re.I):
            errors.append("bundle: unsupported active dependency")
        try:
            if any(target not in files for target in local_targets(name, data)):
                raise ValueError("missing reference")
        except ValueError:
            errors.append("bundle: missing, stale or unsafe local reference")
    return sorted(set(errors))


def reference_closure(files):
    reached = {"SKILL.md", "references/provenance.json"}; pending = ["SKILL.md"]
    while pending:
        name = pending.pop()
        if name not in files:
            raise ValueError("missing local reference")
        if name.endswith(".md"):
            for target in local_targets(name, files[name]):
                if target not in reached:
                    reached.add(target); pending.append(target)
    return reached


def verify_skill_files(files, expected_version):
    errors = []
    if not {"SKILL.md", "LICENSE", "inventory.json"} <= files.keys():
        return ["bundle: missing skill entry, license or inventory"]
    try:
        inv = parse_json(files["inventory.json"])
        if (not isinstance(inv, dict) or set(inv) != {"format", "version", "files"} or
                inv["format"] != "kumihan-skill-1" or inv["version"] != expected_version or
                not isinstance(inv["files"], dict)):
            return ["bundle: invalid skill inventory"]
        if set(inv["files"]) != set(files) - {"inventory.json"}:
            errors.append("bundle: unlisted or missing skill file")
        names = set()
        for name, data in sorted(files.items()):
            if not allowed_file(name):
                errors.append("bundle: forbidden skill file")
            if name.casefold() in names:
                errors.append("bundle: case-colliding skill names")
            names.add(name.casefold())
            if len(data) > MAX_FILE:
                errors.append("bundle: skill file size limit exceeded")
            if b'"approver_ref"' in data or re.search(rb"(?:sk-proj-[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)", data):
                errors.append("bundle: restricted approval/credential material")
            if name != "inventory.json":
                digest = inv["files"].get(name)
                if not isinstance(digest, str) or not DIGEST.fullmatch(digest) or digest != "sha256:" + hashlib.sha256(data).hexdigest():
                    errors.append("bundle: skill digest mismatch")
        errors.extend(reference_errors(files))
        try:
            reached = reference_closure(files)
            if any(name.startswith("references/") and name not in reached for name in files):
                errors.append("bundle: unreferenced skill file")
        except (ValueError, UnicodeError):
            errors.append("bundle: missing, stale or unsafe local reference")
        errors.extend(resource_errors(files))
        return sorted(set(errors))
    except (ValueError, TypeError, KeyError, RecursionError):
        return ["bundle: invalid skill data"]


def resource_errors(files):
    try:
        checks = validators_from_bytes({name: files.get(f"schemas/{name}.schema.json") for name in SCHEMA_HASHES})
        values = parse_json(files.get("rules/catalog.json", b"null"))
        if not isinstance(values, list):
            return ["bundle: missing or invalid local catalog"]
        ids = []
        for value in values:
            if schema_errors(checks["rule"], value, "rule"):
                return ["bundle: invalid local rule"]
            ids.append(value["id"])
        expected = checks["rule"].schema["$defs"]["rule_id"]["enum"]
        if len(ids) != len(set(ids)) or set(ids) != set(expected):
            return ["bundle: incomplete or duplicate local rule IDs"]
        index = {value["id"]: value for value in values}
        profile_ids = checks["rule"].schema["$defs"]["media_profile"]["enum"]
        if {name for name in files if name.startswith("profiles/")} != {f"profiles/{identity}.json" for identity in profile_ids}:
            return ["bundle: missing or unlisted local profiles"]
        for identity in profile_ids:
            profile = parse_json(files.get(f"profiles/{identity}.json", b"null"))
            if schema_errors(checks["profile"], profile, "profile") or profile["id"] != identity:
                return ["bundle: missing or invalid local profile"]
            if any(rule_id not in index or identity not in index[rule_id]["media"] for rule_id in profile["rule_ids"]):
                return ["bundle: unresolved local profile rule"]
        if "sources/public-sources.json" not in files:
            return ["bundle: missing local provenance registry"]
        return source_errors(parse_json(files["sources/public-sources.json"]), values, checks)
    except (ValueError, TypeError, KeyError, RecursionError):
        return ["bundle: missing, invalid or unsupported local resources"]


def verify_skill_directory(directory, expected_version):
    """Same inventory validation on a copied skill, with no repository lookup."""
    try:
        files = {}
        for path in sorted(Path(directory).rglob("*")):
            if path.is_symlink():
                return ["bundle: symlink rejected"]
            if path.is_dir():
                continue
            name = path.relative_to(directory).as_posix()
            safe_name(name)
            files[name] = read_bytes(path)
            if len(files) > MAX_MEMBERS or sum(map(len, files.values())) > MAX_TOTAL:
                return ["bundle: directory size/inventory limit exceeded"]
        return verify_skill_files(files, expected_version)
    except (OSError, ValueError):
        return ["bundle: missing or invalid skill directory"]


def verify_bundle(archive: Path, expected_version: str) -> list[str]:
    if not isinstance(expected_version, str) or not VERSION.fullmatch(expected_version):
        return ["bundle: invalid expected version"]
    try:
        # Verify the actual opened archive is regular and bound its compressed bytes.
        data = read_bytes(archive, MAX_ARCHIVE)
        import io
        with zipfile.ZipFile(io.BytesIO(data)) as bundle:
            members = bundle.infolist()
            if not members or len(members) > MAX_MEMBERS:
                return ["bundle: unsafe member inventory"]
            names = set(); aliases = set(); total = 0
            for member in members:
                safe_name(member.filename)
                # NUL names can be truncated by ZipInfo; reject original spelling too.
                if member.orig_filename != member.filename:
                    return ["bundle: ambiguous member name"]
                if member.filename in names or member.filename.casefold() in aliases:
                    return ["bundle: duplicate or case-colliding entry"]
                names.add(member.filename); aliases.add(member.filename.casefold())
                kind = stat.S_IFMT(member.external_attr >> 16)
                if member.is_dir() or kind not in (0, stat.S_IFREG) or member.flag_bits & 1:
                    return ["bundle: nonregular or encrypted member rejected"]
                if member.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                    return ["bundle: unsupported compression"]
                total += member.file_size
                if (member.file_size > MAX_FILE or total > MAX_TOTAL or
                        member.file_size > max(member.compress_size, 1) * 200):
                    return ["bundle: unsafe archive sizes"]
                if member.filename != "bundle.json":
                    parts = member.filename.split("/", 1)
                    if len(parts) != 2 or parts[0] not in SKILLS or not allowed_file(parts[1]):
                        return ["bundle: unlisted or forbidden archive entry"]
            # Read only after the complete central-directory inventory is admitted.
            files = {}
            for member in members:
                with bundle.open(member) as handle:
                    item = handle.read(MAX_FILE + 1)
                if len(item) != member.file_size or len(item) > MAX_FILE:
                    return ["bundle: inconsistent member size"]
                files[member.filename] = item
            metadata = parse_json(files.get("bundle.json", b"null"))
            if metadata != {"format": "kumihan-bundle-1", "version": expected_version, "skills": list(SKILLS)}:
                return ["bundle: missing or invalid bundle metadata"]
            errors = []
            for skill in SKILLS:
                prefix = skill + "/"
                errors.extend(verify_skill_files({name[len(prefix):]: item for name, item in files.items()
                                                 if name.startswith(prefix)}, expected_version))
            return sorted(set(errors))
    except (OSError, ValueError, TypeError, zipfile.BadZipFile, zlib.error, EOFError, RuntimeError, NotImplementedError, RecursionError):
        return ["bundle: missing, invalid or unsafe archive"]


def main():
    parser = ResultParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--expected-version", required=True)
    args = parser.parse_args()
    errors = verify_bundle(args.archive, args.expected_version)
    emit("incomplete" if errors else "passed", errors,
         limitations=["Inventory/digest/reference validation is not authenticity, Japanese visual quality or release approval."])
    if errors:
        print("Bundle rejected; see sanitized diagnostics.", file=sys.stderr)
    return 2 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
