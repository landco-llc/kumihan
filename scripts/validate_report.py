"""Report structure and local bindings; external authenticity needs trusted host evidence."""
import hashlib
from pathlib import Path
import sys

try:
    from .validate_catalog import validators, schema_errors, read_json, safe_name, emit, ResultParser, HostAuthority, StableInputs
except ImportError:
    from validate_catalog import validators, schema_errors, read_json, safe_name, emit, ResultParser, HostAuthority, StableInputs


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



def admission_errors(root, report, catalog):
    """Trust-aware local admission; protected host writers remain required."""
    with StableInputs() as inputs:
        errors=[]; root=Path(root); index={item['id']:item for item in catalog}
        try:
            artifact=inputs.read(root/safe_name(report['artifact_ref']))
            if 'sha256:'+hashlib.sha256(artifact).hexdigest()!=report['artifact_digest']:
                errors.append('report: local artifact digest mismatch')
            evidence={}
            for check in report['checks']:
                for reference in check['evidence_refs']:
                    evidence[reference]=inputs.read(root/safe_name(reference))
        except (ValueError,OSError): return ['report: missing or unsafe local artifact/evidence']
        if report['ruleset_version']!='0.1.0': errors.append('report: unsupported ruleset version binding')
        required=[check for check in report['checks'] if check['status'] in ('passed','waived')]
        if required:
            try:
                authority=HostAuthority(root)
                for check in required:
                    if check['rule_id']=='DESIGN-001' and not check['evidence_refs']:
                        raise ValueError('missing required design-contract evidence')
                    if check['status']=='passed':
                        for reference in check['evidence_refs']:
                            authority.observation(report,check,reference,evidence[reference],index[check['rule_id']])
                    else:
                        subject={key:report[key] for key in ('report_id','artifact_ref','artifact_digest')}; subject['rule_id']=check['rule_id']
                        authority.approval(check['waiver'],'report-waiver',subject,index[check['rule_id']])
                        for reference in check['evidence_refs']:
                            value=authority.design_evidence(evidence[reference],index[check['rule_id']])
                            if value is not None:
                                authority.design_chronology(value,evidence[reference],report,check,index[check['rule_id']])
                authority.finish()
            except (ValueError,OSError,KeyError,TypeError,MemoryError):
                errors.append('report: trusted host identity/authority/current-state/binding evidence unavailable or invalid')
        try: inputs.check()
        except (ValueError,OSError): errors.append('report: artifact/evidence changed during admission')
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
        catalog = load_catalog(args.root)
        errors = validate_report(report, catalog)
        if not errors:
            errors = admission_errors(args.root, report, catalog)
        code = 2 if errors else (1 if any(c["status"] == "failed" for c in report["checks"]) else 0)
        # A catalog-disallowed exception is substantive failure, not missing approval.
        if errors == ["report: rule exception disallowed"]:
            code = 1
        emit("incomplete" if code == 2 else "failed" if code == 1 else "passed", errors,
             limitations=["Semantic admission depends on an independently trusted host capability; this does not establish Japanese visual quality."])
        if errors:
            print("Report admission rejected; see sanitized diagnostics.", file=sys.stderr)
        return code
    except (ValueError, OSError, MemoryError):
        emit("incomplete", ["report: missing, invalid or unsupported context"])
        return 2


if __name__ == "__main__":
    sys.exit(main())
