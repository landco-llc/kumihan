# KUMIHAN architecture and contracts

KUMIHAN is an independent Apache-2.0 skill package for Japanese typography
and deliberate design. Its six stages are brief and permissions, rule
resolution, compact generation instructions, production with existing host
tools, separate content/static/render/style checks, and an evidence-based
report. The package defines data and workflow contracts; it does not provide
an AI scheduler, a renderer, a hosted auditing service, or a visual-quality
score. The existing license is preserved.

## Contract boundary

The four consumer schemas use JSON Schema Draft 2020-12. Every record rejects unknown
fields. Required fields have no inferred defaults, and descriptive strings
must contain a non-whitespace character. Development validators use Python
3.12 or newer, `unittest`, and a pinned, tested `jsonschema` dependency.
The producer acceptance was exercised with `jsonschema==4.26.0`. Consumer
skills require neither Python nor development dependencies.

Schemas have versioned identifiers of the form
`urn:kumihan:schema:<name>:0.1.0`. Rule IDs, media profile IDs and verification
methods are defined once in `schemas/rule.schema.json` and referenced by the profile,
design and report schemas. Validators must register all four local schema
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

### Reports

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
The trusted host report-admission workflow owns report-waiver lookup and
validation, including catalog exception bounds and exact report/check/artifact
binding. Structural schema validation cannot authenticate external records.
The host independently rechecks required approvals at each use and admission.
Missing, invalid, stale or unverifiable evidence rejects admission; disallowed
exceptions fail. Neither outcome converts a waiver into a pass or permits
editing the reviewed target. Further edits require refine authorization.

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

## Standalone folder delivery — v0.1.0

This complete folder is a Git-tracked standalone Agent Skill. Copy the whole
folder, including LICENSE and inventory.json. All consumer paths in guidance
are relative to this folder root, even inside references or JSON records.
The local rules/catalog.json is the complete 38-rule catalog; its six family
snapshots retain canonical bytes. All six profiles remain available for mixed
media and rule resolution. The public registry retains 57 source records.
Four consumer schemas resolve their versioned URNs locally; source URLs and
JSON Schema dialect URLs identify provenance, not network requirements.

Two practical references, `references/web-recipes.md` and
`references/document-recipes.md`, give concrete starting settings for web,
Office and PDF output. They are guidance to adjust and verify, not rules.

inventory.json lists every other file in this folder with its size and SHA-256
digest. Its own hash is recorded in the distribution checksums to avoid a
recursive self-digest. The repository build script regenerates inventories,
archives and checksums from the canonical `skills/kumihan` shared files; do not
maintain independent rule copies.

No builder, runtime validator, detector, renderer, Python/npm package, private
resource or sibling is required to use this folder. Existing authorized host
tools perform production and evidence review. Folder closure and byte stability
do not establish host discovery or invocation, rendering, native Office
acceptance, source truth or approval authenticity.
