"""Deterministic consumer data packaging; development-only builder."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import stat
import sys
import zipfile

try:
    from .validate_catalog import load_catalog, rule_profile_data, read_bytes, safe_name, VERSION, SCHEMA_HASHES, emit, ResultParser, InputContentError
    from .verify_bundle import SKILLS, MAX_MEMBERS, MAX_TOTAL, verify_skill_files, local_targets
except ImportError:
    from validate_catalog import load_catalog, rule_profile_data, read_bytes, safe_name, VERSION, SCHEMA_HASHES, emit, ResultParser, InputContentError
    from verify_bundle import SKILLS, MAX_MEMBERS, MAX_TOTAL, verify_skill_files, local_targets


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def build_arguments(root, output_dir, version, source_epoch):
    if not isinstance(version, str) or not VERSION.fullmatch(version):
        raise ValueError("builder: invalid version")
    # ZIP's representable UTC range. Odd seconds are deterministically truncated
    # by the ZIP DOS timestamp, while the exact epoch is preserved in provenance.
    if type(source_epoch) is not int or not 0 <= source_epoch <= 4354819198:
        raise ValueError("builder: epoch outside supported ZIP UTC range")
    root = Path(root).absolute(); output = Path(output_dir).absolute()
    for component in [*reversed(output.parents), output]:
        if component.is_symlink():
            raise ValueError("builder: symlink output rejected")
    if output.exists():
        raise ValueError("builder: output directory already exists")
    if not root.is_dir() or root.is_symlink():
        raise ValueError("builder: invalid source root")
    if any(output.resolve().is_relative_to((root / name).resolve()) for name in ("rules", "profiles", "sources", "schemas", "skill-src")):
        raise ValueError("builder: output directory overlaps consumer inputs")
    if not output.parent.is_dir():
        raise ValueError("builder: output parent directory missing")
    return root, output, datetime.fromtimestamp(max(source_epoch, 315532800), timezone.utc).timetuple()[:6]


def _package_validated_inputs(root, output_dir, version, source_epoch):
    """Internal packaging core; callers must first establish full catalog admission.

    Uses only consumer-safe enumerated resources; not a release approval or a
    standalone replacement for the public build_skills callable.
    """
    root, output, timestamp = build_arguments(root, output_dir, version, source_epoch)
    rules, profiles = rule_profile_data(root)
    common = {"LICENSE": read_bytes(root / "LICENSE"), "rules/catalog.json": canonical(rules),
              "sources/public-sources.json": read_bytes(root / "sources/public-sources.json")}
    for name in SCHEMA_HASHES:
        common[f"schemas/{name}.schema.json"] = read_bytes(root / f"schemas/{name}.schema.json")
    for profile in profiles:
        common[f"profiles/{profile['id']}.json"] = canonical(profile)
    common["references/provenance.json"] = canonical({"builder_version": "0.1.0", "version": version,
        "source_epoch": source_epoch, "license": "LICENSE", "sources": "sources/public-sources.json",
        "limitations": ["Structural packaging does not authenticate approvals, source authority or Japanese visual quality."]})
    source = root / "skill-src"
    if not source.is_dir() or source.is_symlink() or {p.name for p in source.iterdir()} != set(SKILLS):
        raise ValueError("builder: missing or unlisted skill source directory")
    archive_files = {"bundle.json": canonical({"format": "kumihan-bundle-1", "version": version, "skills": list(SKILLS)})}
    for skill in SKILLS:
        directory = source / skill
        if directory.is_symlink() or not directory.is_dir():
            raise ValueError("builder: unsafe skill directory")
        files = dict(common); source_files = set(); aliases = set()
        for path in sorted(directory.rglob("*")):
            if path.is_symlink():
                raise ValueError("builder: symlink input rejected")
            if path.is_dir():
                continue
            name = path.relative_to(directory).as_posix(); safe_name(name)
            if (name != "SKILL.md" and not (name.startswith("references/") and path.suffix in {".md", ".json"})):
                raise InputContentError("builder: unlisted or forbidden skill source file")
            if name in files or name.casefold() in aliases or name.casefold() in {n.casefold() for n in files}:
                raise InputContentError("builder: ambiguous or colliding source resource")
            aliases.add(name.casefold()); source_files.add(name)
            files[name] = read_bytes(path)
            if len(files) > MAX_MEMBERS:
                raise InputContentError("builder: excessive source inventory")
        reached = {"SKILL.md"}; pending = ["SKILL.md"]
        try:
            while pending:
                name = pending.pop()
                if name.endswith(".md") and name in files:
                    for target in local_targets(name, files[name]):
                        if target not in reached:
                            reached.add(target); pending.append(target)
        except (ValueError, UnicodeError):
            raise InputContentError("builder: unsafe local reference") from None
        if source_files - reached:
            raise InputContentError("builder: unreferenced skill source file")
        # Local reference checks ensure closure; all declared skill-src/reference
        # data is explicit consumer material, rather than recursive repository copy.
        files["inventory.json"] = canonical({"format": "kumihan-skill-1", "version": version,
            "files": {name: "sha256:" + hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}})
        errors = verify_skill_files(files, version)
        if errors:
            raise InputContentError("builder: " + "; ".join(errors))
        archive_files.update({f"{skill}/{name}": data for name, data in files.items()})
    if len(archive_files) > MAX_MEMBERS or sum(map(len, archive_files.values())) > MAX_TOTAL:
        raise InputContentError("builder: excessive output inventory/size")
    # All input validation precedes output creation; exclusive mkdir prevents
    # overwrite even if another writer creates the directory during validation.
    output.mkdir()
    archive = output / f"kumihan-{version}.zip"
    with archive.open("xb") as handle:
        with zipfile.ZipFile(handle, "w", compression=zipfile.ZIP_STORED, allowZip64=False) as bundle:
            for name, data in sorted(archive_files.items()):
                info = zipfile.ZipInfo(name, timestamp)
                info.create_system = 3; info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.compress_type = zipfile.ZIP_STORED
                bundle.writestr(info, data)
    return archive


def build_skills(root: Path, output_dir: Path, version: str, source_epoch: int) -> Path:
    build_arguments(root, output_dir, version, source_epoch)
    load_catalog(root)
    return _package_validated_inputs(root, output_dir, version, source_epoch)


def main():
    parser = ResultParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--source-epoch", required=True, type=int)
    args = parser.parse_args()
    try:
        archive = build_skills(args.root, args.output_dir, args.version, args.source_epoch)
        emit("passed", [], archive=archive.name, digest="sha256:" + hashlib.sha256(read_bytes(archive, MAX_TOTAL)).hexdigest())
        return 0
    except InputContentError:
        emit("failed", ["builder: verified input-content failure"])
        print("Build rejected; input content violates a verified invariant.", file=sys.stderr)
        return 1
    except (ValueError, OSError):
        emit("incomplete", ["builder: invalid arguments, conflicting output, I/O or unavailable/invalid input content"])
        print("Build rejected; see sanitized diagnostics.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
