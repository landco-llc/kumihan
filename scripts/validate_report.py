"""Report structure and local bindings; external authenticity needs trusted host evidence."""
import hashlib
from pathlib import Path
import sys

try:
    from .validate_catalog import validators, schema_errors, read_json, read_bytes, safe_name, emit, ResultParser
except ImportError:
    from validate_catalog import validators, schema_errors, read_json, read_bytes, safe_name, emit, ResultParser


def validate_report(report: dict, catalog: list[dict]) -> list[str]:
    try:
        checks = validators()
        errors = schema_errors(checks["report"], report, "report")
        if not isinstance(catalog, list):
            return sorted(errors + ["catalog: invalid input"])
        index = {}
        for item in catalog:
            invalid = schema_errors(checks["rule"], item, "catalog rule")
            errors.extend(invalid)
            if invalid:
                continue
            if item["id"] in index:
                errors.append("catalog: duplicate rule ID")
            index[item["id"]] = item
        if errors:
            return sorted(set(errors))
        keys = set()
        for check in report["checks"]:
            key = (check["rule_id"], check["scope"])
            if key in keys:
                errors.append("report: duplicate check key")
            keys.add(key)
            item = index.get(check["rule_id"])
            if item is None:
                errors.append("report: unresolved catalog rule")
                continue
            if report["profile"] not in item["media"]:
                errors.append("report: rule outside profile")
            if check["method"] != item["verification"]["method"]:
                errors.append("report: method differs from catalog")
            if check["status"] == "passed" and check["method"] == "static" and item["verification"]["coverage"] != "implemented":
                errors.append("report: static pass without implemented detector coverage")
            if check["status"] == "passed" and check["method"] == "rendered" and not report["environment"]["renderers"]:
                errors.append("report: rendered pass without renderer")
            if check["status"] == "waived":
                waiver = check["waiver"]
                if not item["exception_policy"]["allowed"]:
                    errors.append("report: rule exception disallowed")
                if waiver["scope"] != check["scope"]:
                    errors.append("report: waiver scope mismatch")
                if waiver["artifact_digest"] != report["artifact_digest"]:
                    errors.append("report: waiver artifact mismatch")
        return sorted(set(errors))
    except (ValueError, OSError, TypeError, RecursionError):
        return ["report: missing, invalid or unsupported input"]


def local_evidence_errors(root, report):
    """Resolve exact local artifact/evidence paths; presence cannot prove relevance."""
    errors = []
    try:
        artifact = read_bytes(root / safe_name(report["artifact_ref"]))
        if "sha256:" + hashlib.sha256(artifact).hexdigest() != report["artifact_digest"]:
            errors.append("report: local artifact digest mismatch")
        for check in report["checks"]:
            for reference in check["evidence_refs"]:
                read_bytes(root / safe_name(reference))
    except (ValueError, OSError):
        errors.append("report: missing or unsafe local artifact/evidence")
    if any(check["status"] == "waived" for check in report["checks"]):
        errors.append("report: trusted approval lookup/authority/time/latest-state context unavailable")
    if any(check["status"] == "passed" for check in report["checks"]):
        errors.append("report: evidence relevance and observed method authentication unavailable")
    return sorted(set(errors))


def main():
    parser = ResultParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    try:
        try:
            from .validate_catalog import load_catalog
        except ImportError:
            from validate_catalog import load_catalog
        report = read_json(args.report)
        errors = validate_report(report, load_catalog(args.root))
        if not errors:
            errors = local_evidence_errors(args.root, report)
        code = 2 if errors else (1 if any(c["status"] == "failed" for c in report["checks"]) else 0)
        # A catalog-disallowed exception is substantive failure, not missing approval.
        if "report: rule exception disallowed" in errors:
            code = 1
        emit("incomplete" if code == 2 else "failed" if code == 1 else "passed", errors,
             limitations=["Structural/local fixture validation does not authenticate external approvals or Japanese visual quality."])
        if errors:
            print("Report admission rejected; see sanitized diagnostics.", file=sys.stderr)
        return code
    except (ValueError, OSError):
        emit("incomplete", ["report: missing, invalid or unsupported context"])
        return 2


if __name__ == "__main__":
    sys.exit(main())
