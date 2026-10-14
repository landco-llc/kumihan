# Intentional design before production

Record the actual brief and structure decision before production begins.
Identify who must understand what, which action matters, and how the proposed
information order serves that purpose. A familiar template is a candidate to
evaluate, not a substitute for those choices. Do not invent metrics or testimonials
to make an otherwise empty section appear credible.

Use the frozen `schemas/design-contract.schema.json` fields. The example below is a
synthetic, schema-valid starting point, not an approval record or an observed
rendering result. Replace its decisions with the actual brief before use;
do not treat its font size, three-card structure or wording as universal defaults.

```json
{
  "brief_id": "synthetic-archive-choice",
  "medium": "web-editorial",
  "audience": "Readers choosing one of three independent archive collections",
  "objective": "Help readers identify the collection relevant to their question",
  "primary_information": ["川辺の写真記録", "港の地図記録", "町の聞き書き"],
  "primary_action": "Open the relevant collection guide",
  "structure_rationale": "Three peer collection summaries support comparison; each has a real guide link. Visiting instructions follow the comparison, rather than a generic conversion CTA.",
  "type_roles": [
    {
      "role": "body",
      "family": "host-available system font",
      "size": "1rem",
      "rationale": "Readable collection summaries; confirm actual glyphs and reflow."
    }
  ],
  "asset_provenance": [],
  "brand_constraints": ["Retain the approved three-card collection component when it serves this comparison."],
  "rejected_defaults": ["Do not add an invented visitor metric or testimonial to fill a hero."],
  "exceptions": [],
  "created_before_generation": true
}
```

## Establish a usable decision

Before production, the host must establish current attributable authorization
for the exact brief, immutable contract and planned generation/refine scope.
Resolve the authorized owner and the applicable permission evidence; do not
infer permission from a model's draft, an old brand approval or a schema-valid
record. Preserve the exact contract bytes/digest, the recorded decision time
and the production boundary. The boolean is a declaration, not chronology proof.

Keep authorization evidence outside the frozen public JSON shape. Use the
existing host brief/permissions workflow; do not add undocumented schema keys
or invent a new approval kind. Approval references must resolve to attributable
authorized decisions with current scope and subject binding. Applicable issue,
finite-expiry and revocation bounds must be verified before use, using trusted
UTC time and `issued_at <= evaluated_at < expires_at`; equality at expiry rejects
approval. An unknown, expired, revoked or unverifiable decision cannot authorize
production. The producer does not authenticate its own permission by assertion.

For each exception, record `scope`, `reason` and `approval_ref` in `exceptions`.
The host resolves the referenced `design-exception` record under the approval
contract in `references/architecture.md`: authorized approver, issue/expiry, latest
state and exact `brief_id`/`design_contract_digest` binding. Recheck at use;
the public reference string cannot supply authority. A report waiver later
requires its separate report/check/artifact binding and stays `waived`.
No exception permits fabricated claims, silent protected-content changes,
missing production permission or retroactive justification.

The recorded rationale must explain information relationships: why peers are
compared, why a sequence is chronological, why a summary precedes detail, or
why an actual action belongs beside particular information. An empty statement
such as “this looks modern” is not a purpose-specific structure decision.
Record rejected defaults and meaningful alternatives rather than manufacture
a reason after seeing a generated layout.

If production happened first, retain that failure. A later explanation is
not retroactive justification. Only a new explicit refine authorization
permits a new pass: record its contract before that pass and distinguish it
from the earlier artifact. Never backdate the contract or relabel the earlier
generation as approved.

## Protect brand continuity and readable access

Three cards can be correct when three real peer items need comparable summaries
and actual links or actions. A current approved brand system can legitimately
reuse that component across related pages. It does not need a waiver simply
because the same motif appears elsewhere, and approval alone does not prove
that it fits this brief or renders readably.

By contrast, blindly repeating Hero → three cards → CTA for an emergency
location task and a scholarly evidence comparison leaves the actual purposes
unresolved. Changing accent colors does not resolve that mismatch. A stricter
comparison policy must be explicit in the host review context before production;
it is not an extra design-contract schema field or a default ban on repetition.

Compare both protected brand conventions and the particular information task.
Do not replace familiar navigation merely to appear novel. Cards, gradients
and symmetry are neither automatic failures nor automatic passes. Examine
readable hierarchy, actual text/control access and whether each element has
a real informational or operational purpose. A clearly labeled original
noninteractive explanatory diagram differs from a fake live control.

Define color, typography and spacing roles rather than scatter unexplained
values. Summarize brand/token obligations in `brand_constraints` and structure
decisions; `type_roles` keeps its frozen role/family/size/rationale keys. Keep
the actual implementation token map with the authorized product assets or
styles. Confirm the fonts and assets actually available, their rights and
fallback behavior; no external font import is implied. An empty asset list
means none are declared, not that unknown assets have been cleared.

## Review without overstating evidence

Inspect the actual output against the recorded choices and protected source.
Role definitions and approved brand patterns cannot substitute for rendered
readability checks. If no renderer or target application is available, retain
`not-checked` or `unsupported`; do not declare a visual pass. Contextual design
judgment remains `assisted` or `manual`, while actual render review is labeled
`rendered`. Keep `passed`, `failed`, `needs-review`, `not-checked`, `unsupported`,
`waived` and `not-applicable` distinct, with relevant evidence and limitations.
Review is read-only until a separate bounded refine authorization permits edits.

The six design rules are guidance, not an automated visual-quality detector.
Resolve them and their policy references from the complete installed catalog.
Source/profile integration and package-local resource paths must be verified
by standalone folder inventory and catalog checks before claiming complete local resources.
