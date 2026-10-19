# Design quality review: Standard and Strict

**Design lineage:** DESIGN-001..006, existing content and evidence checks, review-protocol.md, design-contract.md. This is a *review procedure and evidence taxonomy*, not a universal visual quality detector. It does not replace substantive checks or change their existing strength/conditional impact.

## Universal decision sequence

1. Obtain the trusted brief: purpose, audience, actual output, brand constraints, protected source, content priorities and authorization. Confirm intended reader action (if any).
2. Resolve the existing medium profile, use-case adapter and language scope. Apply only applicable rules. The adapter never edits `rules/catalog.json`, 39 IDs, or six media profile definitions.
3. Separate observations: **static** (markup/strings), **rendered** (actual screen/document/image and fonts), **assisted** (contextual AI critique), **manual** (human judgment). Record methods and scope accurately.
4. Evaluate hierarchy, layout justification, visual treatment, brand consistency and reading performance against the actual brief and visible evidence. Do not infer authorship or aesthetic quality from motif counts.
5. In `audit`, make recommendations keyed to existing rule ID + scope in a **separate human-readable proposal**. Do not mutate the target. Use the unchanged `report.schema.json`.
6. If separately authorized `refine`, protect supplied bytes, edit only approved regions and rerun impacted checks. Absence of a renderer is `not-checked` (or `unsupported` when proven unavailable), not a pass.

## Standard — default

- Apply all relevant DESIGN-001..006 and profile-specific CONTENT/JA-TYPE/WEB/DOC/EVIDENCE checks.
- Ask whether structure follows real information, colors/fonts/whitespace have roles, text can be read, actions are real and data/assets have provenance.
- Respect intentional cards, gradients and symmetry when they fit the purpose and authorized brand. An unrelated design's visual similarity alone is neither `failed` nor “AI-made.”
- Record `needs-review` for contextual uncertainty; do not turn preferences into mandatory violations.

## Strict — *only* if explicitly selected by the user

All Standard checks still apply. Additionally compare relevant designs against the **actual briefs** and any safely available approved brand or prior layouts. Ask for purpose-specific reasons for reused motifs, repetitive hero/cards/CTA structures, ornamental data and unexplained hierarchy. When no comparison reference was supplied or inspected, **do not invent one**: mark that comparison `not-checked` or `needs-review`.

`DESIGN-002` has an existing conditional **error** boundary. Apply it only if evidence establishes *all* of these: (a) a strict comparison policy was selected **before production**, (b) materially different briefs produced repeated structure and (c) a purpose-specific rationale is absent. A late Strict request cannot recreate the historical decision. Do not raise severity by fiat or count cards/gradients to simulate proof.

A user's “Strict” request is neither evidence of actual rendered inspection nor authority to waive original brand or content restrictions. Record selected intensity separately from whether its pre-production contract/chronology was independently validated.

## Specific review prompts by existing rule

| Rule | Observable question | Avoid |
|---|---|---|
| DESIGN-001 | Was the purpose/audience/information order **recorded before production** with actual permission? | Retroactive justifications |
| DESIGN-002 | Is the structure suited to this brief and, where comparable, genuinely different briefs? | Hero/card counts as quality scores |
| DESIGN-003 | Does every claim, decorative element and control correspond to real information/function? | Invented metrics and fake controls |
| DESIGN-004 | Are protected brand conventions consistent without blindly importing irrelevant layouts? | Novelty for novelty's sake |
| DESIGN-005 | Can roles of palette, typefaces and spacing be explained and verified in rendered output? | Unverified fonts and token-only PASS |
| DESIGN-006 | Does a familiar motif *actually* serve the purpose and readable access? | Blanket prohibitions of cards, gradients, symmetry |

## Proposal output (outside the frozen JSON report)

For each issue include `rule_id`, `artifact_region`, observed evidence and method, why it conflicts with the brief, a bounded suggestion, protected-content and brand risks, and the tests needed after an authorized change. Label *proposal only*. Never write `confidence`, `design_score` or `review_intensity` into the existing report schema.

## Negative examples

- “The design has three cards, therefore AI-like and failed”: **invalid**.
- “All five screens passed because CSS contains `overflow-wrap`”: **invalid**; rendering not observed.
- “There is no brand manual in the input, so no brand issues exist”: **invalid**; unknown is not proved absent.
- “The redesign suggestion authorizes changing the user's deck”: **invalid**; review is read-only.
- “Strict was requested after the page was made; therefore prior strict conditions are met”: **invalid**.
