# KUMIHAN architecture and contracts

KUMIHAN is an independent Apache-2.0 skill package for Japanese typography
and deliberate design. Its six stages are brief and permissions, rule
resolution, compact generation instructions, production with existing host
tools, separate content/static/render/style checks, and an evidence-based
report. The package defines data and workflow contracts; it does not provide
an AI scheduler, a renderer, a hosted auditing service, or a visual-quality
score. The existing license is preserved.

## Contract boundary

The five schemas use JSON Schema Draft 2020-12. Every record rejects unknown
fields. Required fields have no inferred defaults, and descriptive strings
must contain a non-whitespace character. Development validators use Python
3.12 or newer, `unittest`, and a pinned, tested `jsonschema` dependency.
The producer acceptance was exercised with `jsonschema==4.26.0`. Consumer
skills require neither Python nor development dependencies.

Schemas have versioned identifiers of the form
`urn:kumihan:schema:<name>:0.1.0`. Rule IDs, media profile IDs and verification
methods are defined once in `rule.schema.json` and referenced by the profile,
design and report schemas. Validators must register all five local schema
resources by their exact `$id` before validation, using an offline registry
with no network retrieval. Missing resources or unsupported schema versions
are validation errors. Do not resolve arbitrary instance-supplied schemas.
The Draft 2020-12 specification defines structural validation; external
authenticity and cross-record invariants are not implemented by these schemas.

References: [Draft 2020-12 validation specification](https://json-schema.org/draft/2020-12/json-schema-validation)
and [jsonschema validation API](https://python-jsonschema.readthedocs.io/en/stable/validate/).

### Rules and profiles

The complete catalog has exactly these 38 IDs, in family order and ascending
numeric order within a family:

| Family | IDs | Count |
| --- | --- | ---: |
| Content | `CONTENT-001` through `CONTENT-005` | 5 |
| Japanese typography | `JA-TYPE-001` through `JA-TYPE-010` | 10 |
| Web | `WEB-001` through `WEB-008` | 8 |
| Documents | `DOC-001` through `DOC-004` | 4 |
| Design | `DESIGN-001` through `DESIGN-006` | 6 |
| Evidence | `EVIDENCE-001` through `EVIDENCE-005` | 5 |

Rule revisions are positive integers. Each rule states its independent
requirement, normative kind, strength, impact, media scope, provenance through
source references, conditions, verification method and coverage, fix policy,
exception policy and case IDs. `case_ids` may be empty while coverage remains
honestly planned, unsupported or guidance-only. Conditional impact is an
explicit condition containing `when`, `impact` and `scope`; it is never an
additional severity value. `implemented` must refer to a real detector or
documented review procedure with relevant tests; the schema cannot verify it.
The methods are `static`, `rendered`, `assisted`, and `manual`; coverage is
`implemented`, `guidance-only`, `planned`, or `unsupported`.

Source references are stable identifiers, not instructions to fetch or execute
anything. Public references resolve against `sources/public-sources.json`.
References beginning `policy:` resolve to explicit, independently authored
policy statements in that same source registry. A source entry must identify
its type, public URL or authored policy location, and attributable statement.
No reference may depend on an inaccessible private source. Reference presence
does not establish that a source supports the requirement.

Profiles have `id`, integer `revision`, `title`, `description`, `rule_ids` and
`guidance`. The six IDs are `web-editorial`, `web-marketing`, `web-ui`,
`report-document`, `presentation`, and `display-copy`. Rule `media` and design
`medium` use those same precise profile IDs. Profile rule references must
resolve in the complete catalog; selection does not delete other catalog rules.

### Intentional design

A design contract records the brief, audience, objective, primary information
and action, structure rationale, typography roles, asset provenance, brand
constraints, rejected defaults and bounded exceptions before generation.
`created_before_generation` must be `true`; an independently recorded brief
and generation boundary must substantiate that declaration. A post-generation
explanation cannot substitute for it. Asset records identify the asset,
origin, source reference, license and intended use. An empty asset list means
no declared assets, not verified rights. Typography roles state `role`,
`family`, `size` and `rationale`; actual font availability remains a host check.
Existing brand patterns, including cards, gradients and symmetry, are judged
against purpose and constraints rather than prohibited unconditionally.
Exceptions require `scope`, `reason` and `approval_ref`.
The referenced record must satisfy the approval contract below; an opaque
reference alone does not authorize the exception.

The host must establish authorized mode, editable scope, protected content and
permission to refine in the brief workflow. Those permissions are not granted
by schema validity. Review is read-only. A new explicit refine authorization
is required before modifying a reviewed target.

### Reports and release metadata

Reports identify one artifact using `artifact_ref` and `artifact_digest`,
the ruleset version, profile, checks, environment, limitations and content
change summary. Digests use `sha256:` followed by 64 lowercase hexadecimal
characters. Each check has `rule_id`, `status`, `method`, `evidence_refs`,
`scope` and `reason`. Scope is a stable identifier for a bounded region or
whole artifact; `(rule_id, scope)` is the unique check key within a report.

The seven statuses are exactly `passed`, `failed`, `needs-review`,
`not-checked`, `unsupported`, `waived`, and `not-applicable`. `passed` needs
at least one nonblank evidence reference and a named method. A `waived` check
requires a `waiver` with `approval_ref`, `scope`, `reason` and
`artifact_digest`; other statuses cannot carry a waiver. A waiver remains
distinct from a pass and must match the report artifact and check scope.
Its referenced approval must also satisfy the approval contract below.
The environment names the actual host, tools and available renderers without
private operating details. Missing rendering becomes `not-checked` or
`unsupported`. A language-model judgment is assisted/manual, not deterministic
static verification. References must resolve to relevant observed evidence
about the exact artifact; strings alone are not proof.

Release manifests contain `version`, `source_commit`, `source_tree`,
`artifacts`, `build_environment`, `included_skills`, `schema_version`,
`ruleset_version`, `check_refs`, `independent_review_ref` and
`known_limitations`. Commit and tree identities are full 40-character
lowercase Git object IDs for this repository. Each artifact has a basename
`name`, prefixed SHA-256 `digest` and positive byte `size`. Artifact names
must also be unique under semantic validation. The environment records Python,
platform, builder version, fixed source epoch and exact dependency versions.
Versions use three numeric components with optional prerelease text; no build
metadata is accepted in this contract. All four skill names occur exactly once.

Publication approval is a separate, restricted record, not a manifest field.
It must bind `source_commit`, `source_tree`, the complete artifact name/digest
set, the independent review reference, approved stage and a current approval
state. Changing any bound value invalidates it. Only sanitized product check
and review references belong in public release metadata. Neither schema
validity nor a nonblank review reference establishes independent review.

### Referenced exception and waiver approvals

Design exceptions and report waivers retain their existing public schema
shapes. Their `approval_ref` resolves to a separate, restricted approval
record; approver identity and approval records are not public package content.
JSON Schema does not authenticate these external records.
Every field in the following record is required.

| Field | Required meaning |
| --- | --- |
| `approval_ref` | Unique, nonblank opaque identifier matching the requesting record; ambiguous or duplicate lookup results are rejected. |
| `purpose` | Exactly `design-exception` or `report-waiver`; approval for one purpose cannot authorize the other. |
| `approver_ref` | Nonblank stable principal identifier resolvable to an identifiable approver through the host's trusted identity and authorization evidence. A display name or unresolved identifier is insufficient. |
| `issued_at` | Valid UTC issue timestamp in the exact representation specified below. |
| `expires_at` | Required finite UTC expiry timestamp in that representation; no null, omitted or indefinite expiry. |
| `scope` | Nonblank stable identifier for the exact authorized region or whole subject; no inferred wildcard expansion. |
| `reason` | Nonblank explanation of the bounded exception being authorized. |
| `subject` | Exact purpose-specific binding specified below, independently compared with the requesting subject. |
| `state` | Latest authoritative state: `current`, `revoked` or `superseded`; unknown states are invalid. The field alone is not evidence of currency. |

Missing or blank approver identity or expiry is rejected.
Identifiable does not mean authorized.
The approver must be authorized for that purpose and scope at issue and evaluation.
The host verifies that authority against its independently trusted policy and
identity evidence; an approval record cannot grant its own signer authority.
Scope and reason must exactly match the requesting exception or waiver.
Rule exceptions must also be allowed by the catalog rule and stay within its bounds.
Applicable brief permissions and protected-content restrictions remain binding.

For `design-exception`, `subject` requires `brief_id` and
`design_contract_digest`: the prefixed SHA-256 digest of the exact immutable
UTF-8 design-contract bytes retained by the host before generation. The
approval must match that brief and digest before generation begins or an
authorized refine action uses the exception. Changing those bytes requires
a new bound approval. The reference may be allocated before issuance so the
design contract can include it without embedding the external approval record.
This pre-generation binding authorizes design intent for that contract, not
a blanket waiver for future output artifacts.

For `report-waiver`, `subject` requires `report_id`, `rule_id`, `artifact_ref`
and `artifact_digest`. They must match the actual report, check and output
artifact. Its `scope` must equal both the check scope and waiver scope, its
`reason` must equal the waiver reason, and its artifact digest must equal
both report and waiver digests. Subject digests use the existing
`sha256:` plus 64 lowercase hexadecimal characters convention.
The full applicable subject binding must match.
An altered artifact, design contract, scope, reason or purpose cannot reuse
the approval. A valid report waiver stays `waived`; waived remains distinct from passed.

All approval timestamps use `YYYY-MM-DDTHH:MM:SSZ`: Gregorian calendar dates,
24-hour time, whole seconds and a literal uppercase `Z` for UTC. Parse the
complete string and reject invalid calendar dates or trailing characters.
Offsets, local times, fractional seconds and leap seconds are rejected.
issued_at must be strictly earlier than expires_at.
The decision clock is trusted UTC host time, not an instance-supplied time.
Evaluate the half-open interval `issued_at <= evaluated_at < expires_at` at
the actual decision instant without rounding or a grace period. A host clock
with finer precision must retain it when comparing against whole-second bounds.
At evaluated_at == expires_at the approval is expired and rejected.
A decision before issuance or after expiry is also rejected. If trusted
decision time cannot be established, validation is incomplete and must reject
use of the exception or waiver.

Only an authoritatively verified current record may be accepted.
Revoked, superseded, missing, mismatched or unverifiable records are rejected.
A cached declaration of current is insufficient.
The host-owned resolver must establish the latest state for the exact approval
at the decision instant, using trusted records and authorization evidence.
It must not resurrect an older revision after revocation or supersession.
Unavailable lookup, ambiguous results or inability to establish current state
fail closed. Recheck immediately before each generation/refine use or report
admission and at subsequent release admission; previous acceptance is not
permanent authorization. A trusted local resolution mechanism is sufficient;
this contract adds no service or network-at-use requirement. If the available
local evidence cannot establish current state, the decision remains rejected.

The brief/permissions host workflow owns design-exception lookup and validation
before generation/refine, including identity, authority, time, revocation,
brief permissions and exact design binding. It must not pass an unresolved
exception downstream as authorized.
The report CLI owns report-waiver lookup and validation
using trusted approval context supplied by its host, plus catalog exception
allowance/bounds and exact report/check/artifact binding. The frozen
two-argument `validate_report` callable cannot authenticate external records;
its structural result alone cannot complete waiver admission. The CLI must
perform the lookup checks before treating the report as semantically admitted.
The release adapter independently rechecks both kinds
whenever required by submitted design/report evidence. Missing, invalid,
unverifiable or stale approval evidence produces an incomplete admission
(exit 2); a disallowed exception produces substantive failure (exit 1).
Neither path silently converts a rejected approval into a pass or changes
the reviewed target. Any further edit still requires refine authorization.

The following case expectations apply independently to both approval purposes.
These are contract acceptance cases, not an implemented semantic validator.
Later semantic tests must exercise actual trusted lookup and authorization
against original synthetic records; prose checks alone cannot establish it.

| Case | Expected | Condition |
| --- | --- | --- |
| `valid` | accept | All required fields, authorized principal, verified latest current state, matching scope/reason/subject, permitted rule bounds and a decision strictly before expiry. |
| `missing-approver` | reject | The approver identifier is absent or blank. |
| `missing-expiry` | reject | Expiry is absent, blank, null or indefinite. |
| `expiry-boundary` | reject | Decision time equals expiry exactly. |
| `expired` | reject | Decision time is later than expiry. |
| `not-yet-issued` | reject | Decision time precedes issuance. |
| `revoked` | reject | Latest authoritative state is revoked, even within the time interval. |
| `superseded` | reject | The referenced approval has been replaced. |
| `wrong-scope` | reject | Approval scope differs from the requesting scope. |
| `wrong-subject` | reject | Design brief/digest or report/check/artifact binding differs. |
| `wrong-reason` | reject | Approval authorizes a different bounded exception. |
| `unauthorized` | reject | Identity resolves but lacks authority for this purpose and scope. |
| `unverifiable` | reject | Lookup, identity, authority, latest state or trusted decision time cannot be verified. |
| `offset-timestamp` | reject | Timestamp uses an offset or another noncanonical representation. |

## Module and CLI ownership

These are contracts for subsequent implementations; the schemas and this
document do not implement the modules, CLIs, detectors or release gate.
Keep each public callable in the named script, import-safe and free of CLI
side effects. CLI parsing belongs under a main guard. Inputs are local JSON
and files. Never execute artifact content or code copied from a research page.

| Owner module | Frozen callable | Responsibility |
| --- | --- | --- |
| `scripts/validate_catalog.py` | `load_catalog(root: Path) -> list[dict]` | Schema and semantic catalog/profile/source/fixture validation; reject invalid or duplicate rules. |
| `scripts/validate_report.py` | `validate_report(report: dict, catalog: list[dict]) -> list[str]` | Validate report and catalog relationships without coercion, editing or generating proof. |
| `scripts/build_skills.py` | `build_skills(root: Path, output_dir: Path, version: str, source_epoch: int) -> Path` | Produce a deterministic archive in a new authorized output directory. |
| `scripts/verify_bundle.py` | `verify_bundle(archive: Path, expected_version: str) -> list[str]` | Inspect the archive safely; never execute its contents. |
| `scripts/check_release.py` | `evaluate_release(stage: str, evidence: dict, expected_head: str) -> tuple[int, dict]` | Evaluate `candidate`, `reviewed` or `published` evidence against exact identities. |
| `scripts/render_report.py` | `render_report(report: dict) -> str` | Render observed facts, distinctions and limitations with appropriate output escaping. |

`load_catalog` returns deterministic family/numeric ID order, not raw filename
order or lexicographic family order. It raises `ValueError` with sanitized,
deterministically ordered diagnostics for invalid data, missing input or
unsupported contracts. `validate_report` and `verify_bundle` return an empty
list on success and ordered diagnostic strings on invalid, missing or
unsupported input. Expected validation failures must not escape as tracebacks.
`build_skills` raises `ValueError` for invalid inputs or an existing output
directory; it never overwrites that directory. Environmental I/O failure can
raise `OSError`; the CLI converts it into a sanitized exit-2 diagnostic.
`render_report` raises `ValueError` for structurally invalid input; it produces
UTF-8 Markdown, escapes untrusted markup and never upgrades a status.

The release callable receives a JSON-compatible `evidence` object with
`manifest`, `catalog_check`, `report_checks`, `bundle_check`, `host_checks`,
`public_boundary_check`, `independent_review`, `publication_approval` and
`publication` keys. Unavailable evidence is represented by `null`, never a
fabricated pass. Each check/review result contains `status`, `source_commit`,
`source_tree`, `artifact_digests` (an artifact-name to digest map), `reference`
and `limitations`. `status` is `passed`, `failed`, `missing`, `invalid`,
`unsupported` or `stale`; references and declarations require verification
against their actual records. Independent review also names `reviewer_ref`
and confirms independence from the producer. Publication approval also
contains `approved_stage` and `current`; publication evidence identifies the
tag and release references and the observed published asset digest map.

`candidate` requires the valid manifest and all catalog, report, bundle, host
and public-boundary checks. `reviewed` additionally requires an independent
review of the exact candidate. `published` additionally requires current human
publication approval bound to that reviewed candidate and observed published
tag/release/assets matching its identities. Approval to publish must be checked
before any separate publication action; a gate result never performs one.
Every required record must match the expected commit, manifest tree and exact
artifact set. Contradictory/unknown states are invalid, not passed.

The release result dictionary contains `stage`, `status`, `expected_head`,
`source_tree`, `artifact_digests`, `failures` and `limitations`. Status is
`passed`, `failed` or `incomplete`. Return code 0 means all required evidence
passed; 1 means substantive failure; 2 means missing, invalid, unsupported or
stale evidence or an unknown stage. Incomplete evidence takes precedence over
substantive failure when both occur; diagnostics retain both facts. No evidence
is silently generated by the gate.

All CLIs run as `python scripts/<module>.py` and write one JSON result to stdout
except `render_report.py`, which writes Markdown. Diagnostics go to stderr.
Validation CLIs use exits 0/1/2 for valid/substantive failure/missing-invalid-
unsupported input. The builder uses 0 on success, 1 for verified input-content
failure, and 2 for invalid arguments, output-directory conflicts or I/O failure.

| Script | Frozen arguments |
| --- | --- |
| `validate_catalog.py` | `--root PATH` |
| `validate_report.py` | `--root PATH --report PATH` |
| `build_skills.py` | `--root PATH --output-dir PATH --version VERSION --source-epoch INTEGER` |
| `verify_bundle.py` | `--archive PATH --expected-version VERSION` |
| `check_release.py` | `--stage {candidate,reviewed,published} --evidence PATH --expected-head FULL_COMMIT` |
| `render_report.py` | `--report PATH` |

The report renderer uses a locally registered schema before rendering; it
cannot establish catalog/source resolution through its one-argument callable.
The report validator can establish catalog membership but its two-argument
callable cannot authenticate external evidence. The report CLI resolves local
evidence, using `--root` as context. Evidence authentication, chronology and
approval freshness at release admission belong to the release adapter, which
must load independently verified records and compare them with the supplied
summaries. The earlier design and report approval decisions belong to the
host workflow and report CLI as specified above. In-memory summaries alone
cannot satisfy publication admission.

## Cross-record invariants and tests

The later validators own the following checks. Their tests must use synthetic
original content and offline resources and must fail when each invariant is
violated; these are future implementation obligations, not current test claims.

| Invariant | Owner and required rejection |
| --- | --- |
| Duplicate rule IDs | Catalog loader rejects repeated IDs even when the two rule objects differ; compares the complete ID set with all 38 expected IDs and rejects missing or additional IDs. |
| Unresolved source references | Catalog loader resolves every public/policy identifier against the source registry, verifies its declared kind and authored statement, and rejects missing or unsupported references. |
| Profile and fixture consistency | Catalog loader resolves profile rules, rule media, and case IDs; retains all rules with honest coverage. The fifteen priority IDs each require original positive, negative and exception cases, totaling at least 45 records. |
| Duplicate report keys | Report validator rejects repeated `(rule_id, scope)` pairs even if evidence or reasons differ. Separate scopes remain separate checks. |
| Passed without relevant evidence | Report schema rejects empty/missing evidence. Report CLI and release adapter reject unresolved, irrelevant or wrong-artifact evidence and false method classifications. |
| Stale release approval | Release adapter rejects an approval for another commit, tree, artifact set, review reference or publication stage, or an approval that is no longer current. A schema-valid digest is not proof of binding. |
| Exception and waiver approval bounds | Host workflow/report CLI and release adapter verify the required referenced record, authorized approver, UTC half-open expiry interval, latest revocation state, rule allowance/bounds and exact scope/reason/subject binding. No waiver is converted to passed. |
| Build integrity | Builder and verifier reject path escapes, absolute paths, symlinks, unlisted files, stale references and forbidden dependency imports. Repeated builds with fixed inputs must produce identical archive bytes and ordering. |
| Public boundary | Boundary checker rejects secrets, private operating references, transcripts and personal/customer data before public commit or publication. |

The priority IDs are `CONTENT-001`, `CONTENT-002`, `CONTENT-004`,
`JA-TYPE-002`, `JA-TYPE-004`, `JA-TYPE-005`, `JA-TYPE-006`, `JA-TYPE-008`,
`JA-TYPE-009`, `WEB-001`, `WEB-004`, `WEB-005`, `DESIGN-001`, `DESIGN-002`,
and `EVIDENCE-001`. The other 23 remain visible. This is not a promise of
38 automatic detectors. Source-content assertions are automatic only when a
supported fixture/extractor supplies exact text. Other judgments retain
assisted, rendered or manual labels and explicit limitations.

Schema tests must include positive records, each missing required field,
unknown fields, invalid enums, all 38 valid IDs, all seven statuses, missing
artifact digests, passed records without evidence, incomplete waivers,
post-generation design declarations and incomplete skill sets. They must
also demonstrate that shape-valid unresolved references, duplicate check keys
and stale bindings still need the semantic layer.

## Packaging, content and host ownership

`rules/` is the authored rule source; `profiles/` selects those rules;
`sources/` records public references and authored policies. `skill-src/`
owns the four entry workflows and shared guidance. `examples/` and
`tests/fixtures/` own original synthetic material. Schema definitions own
record shapes; validators must not invent parallel enums or silently coerce
records. Committed acceptance tests belong under `tests/` when the validator
implementation is added; producer scratch tests are not package content.

`dist/` is generated. Each installed skill folder includes its required local
references, profiles and schema resources and works after copying that folder
to an unrelated workspace. The builder may duplicate generated resources;
independent hand-maintained rule copies are prohibited. Bundles have no
network-at-use requirement, sibling-repository dependency or symlink. The
archive verifier inspects names, sizes, inventories and digests before any
bounded extraction, and never executes package content. It must also reject
duplicate entries and platform-specific path escapes.

Codex Cloud is the required production host for this release. Other consumer
hosts may be documented as untested; a compatibility pointer does not establish
validation. Host results must separately record what was actually exercised.
The demo expectation is three original web fixtures at 320, 768 and 1280 CSS
pixels, plus one synthetic report and one synthetic presentation in available
output environments. Text zoom, spacing changes, native document rendering
and alternate browser engines are separate tested/not-tested checks. Viewport
resizing cannot establish those results. No font files are bundled.

All product rules, examples and assets must be independently authored. Do not
import third-party skill implementations, prose or assets into this package.
The package includes no payment/authentication service, remote control, general
rendering engine, universal Japanese line-breaking detector, semantic-truth
detector or cross-application compatibility guarantee. Public files and
release metadata contain sanitized product facts; private operating state,
approvals and transcripts remain outside the repository.
