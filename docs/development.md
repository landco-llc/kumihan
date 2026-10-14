# Development and read-only verification

The v0.1 candidate uses four checked-in source folders under `skills/`. Canonical rules, profiles, sources, schemas and `skill-src/` remain the authored inputs; inventories identify exact source snapshots and explicit entry-point adaptations. Do not edit standalone copies independently of reviewed canonical inputs. The [architecture addendum](architecture.md) takes precedence over historical archive provisions for this delivery. The excluded legacy ZIP builder is neither required nor repaired by this scope.

Consumers need no Python dependencies. Development checks use Python 3.12 and the following exact dependencies, matching the [workflow](../.github/workflows/verify.yml). For a disposable environment outside tracked product files:

```sh
python3 -m venv /tmp/kumihan-verifier
/tmp/kumihan-verifier/bin/python -m pip --isolated install --index-url https://pypi.org/simple --only-binary=:all: --no-deps jsonschema==4.26.0 attrs==26.1.0 jsonschema-specifications==2025.9.1 referencing==0.37.0 rpds-py==2026.6.3 typing-extensions==4.16.0
/tmp/kumihan-verifier/bin/python -m pip check
```

Use a fresh unused environment path; do not reuse an unknown environment. Dependency versions are pinned without wheel hashes. Package download is a development setup operation; the checks below are offline. Hosted `ubuntu-24.04` images are mutable; this is not a fully immutable build environment.

From the repository root, record tracked file hashes before and after the approved checks:

```sh
git ls-files -z | xargs -0 sha256sum > /tmp/kumihan-before.sha256
/tmp/kumihan-verifier/bin/python -B scripts/check_standalone.py --root .
/tmp/kumihan-verifier/bin/python -B scripts/check_public_boundary.py --root .
/tmp/kumihan-verifier/bin/python -B -m unittest discover -s tests -v
/tmp/kumihan-verifier/bin/python -B scripts/check_standalone.py --root .
/tmp/kumihan-verifier/bin/python -B scripts/check_public_boundary.py --root .
git ls-files -z | xargs -0 sha256sum > /tmp/kumihan-after.sha256
cmp /tmp/kumihan-before.sha256 /tmp/kumihan-after.sha256
git diff --exit-code
```

Preserve exit codes and original failures; run commands individually or in a fail-fast shell. The public-boundary checker uses Git's tracked set, so newly authored documentation must be staged or committed before checking. Static grammar and disclosure checks are bounded, not runtime, rights or exhaustive security assurance. The 19 tests are verifier negative controls, not automatic checks for every guidance rule.

Documentation changes also require bilingual feature/limitation parity, local-link checks, command/source-path validation, owned-path review and exact LICENSE byte preservation. An isolated filesystem copy can validate the proposed copy command without establishing host discovery. A documentation candidate needs its own hosted PR check result; prior producer CI is source evidence only. The workflow's push trigger is limited to the checker branch prefix; pull requests trigger verification.
