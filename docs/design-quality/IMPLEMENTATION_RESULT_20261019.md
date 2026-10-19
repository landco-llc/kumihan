# KUMIHAN Design Quality & Use-case Routing — Implementation Candidate

**Date:** 2026-10-19 (JST)
**Decision IDs:** KUMI-DESIGN-QUALITY-ENHANCEMENT-20261019-01 / KUMI-USECASE-ADAPTER-SELECTION-20261019-01
**Reference design:** [v0.1](https://docs.google.com/document/d/1sSFEm1YnyBo9hrpsQDQFuELWwSx5LSZrYE2L9oOrbhE/edit) / [v0.1a](https://docs.google.com/document/d/1o4gmykikAVc55atdhHX2mVyaGhbKwVAlPYdcXpKyuiU/edit)
**Status:** candidate source and ZIPs on a feature branch only. Not a GitHub Release; native host integration and visual detector are not claimed.

## Decision mapping and source inventory

- Auto-choice as default / manual compatible override / ask only for consequential ambiguity: `skills/kumihan/references/use-case-selection.md`, `references/use-case-adapters.json`, optional `scripts/use_case_selector.py`. The latter is conservative JA/EN routing by explicit surface terms, not general multilingual intent AI.
- Keep the existing six primary media profiles and all 39 rule IDs. No `graphic-design` profile. The six named adapters attach guidance only; they do not add rules or grant authorization.
- Standard design review is default; Strict requires explicit user selection. No auto Strict from “AI-looking” copy and no retroactive `DESIGN-002` strict error. See `design-review-modes.md`.
- Contextual text/picture/whitespace/brand checks: `visual-relationship-guidance.md`; evidence categories remain actual static, rendered, assisted or manual.
- Four Japanese KUMIHAN Skills share references and optional script via existing deterministic `tools/build_dist.py`. Independent language packages under `plugins/` are unchanged.
- Existing `design-contract.schema.json`, `report.schema.json`, `rule.schema.json` and their versioned IDs are unchanged; route output is outside their public schema.
- Corrected historical “38 rules” description in canonical architecture to match current 39 and JA-TYPE-011; no rules added or removed.

## Usage examples (from standalone skill folder)

```sh
python3 scripts/use_case_selector.py --brief 'Instagram用の広告画像を作って'
python3 scripts/use_case_selector.py --brief '新製品のランディングページを作って'
python3 scripts/use_case_selector.py --brief 'バナーを作って'
python3 scripts/use_case_selector.py --brief 'ポスターをレビュー' --mode audit --strict --stage after-production
```

The tool returns `selected` with medium/adapter/source/reason or `needs-clarification` with one question. Follow-up review added conservative handling for explicit Japanese `XではなくY` corrections and `LPの見出しコピーだけ` (copy-only), and allows compatible same-medium manual adapter overrides without an unnecessary question. It does not create or change any production asset. Host and human reasoning are still needed for complex intents, permissions, mixed locale boundaries and actual visual inspection.

## Verification (performed in local workspace)

| Check | Observed result |
|---|---|
| UCA-01..10 and additional router/contract tests | 34 unit tests PASS |
| Existing rule/schema/distribution contract tests | 5 tests PASS |
| JA-TYPE-011 source fixture consistency | 11 spec fixtures PASS; no renderer invoked |
| Four standalone Skills + distribution archives regenerated | 15 ZIPs candidate for v0.1.8-preview |
| Deterministic pack builder | `build_dist.py --check`: 148 generated files up to date; Python caches explicitly excluded |
| Existing six media profiles + 39 catalog IDs | unchanged; verified by unit tests |
| Other independent language modules | no changes made under `plugins/` |
| Complete root `unittest discover -s tests` | 55 tests PASS after follow-up review corrections and rebasing on main `329cced` (all scope tests); the earlier base `051a34e` had 19 independent font CSS order failures, reproduced unchanged in a separate baseline worktree. They were resolved upstream before rebase and are not attributed to this feature |
| Browser/Office/rendered visual checks | NOT CHECKED; this change adds guidance and routing, not a renderer |
| Native ChatGPT/Claude/Gemini plugin invocation | NOT CHECKED |
| GitHub CI, merge, Release, Pages | To be read back after PR creation; no publication authorized |

## Acceptance and limitation notes

- Evidence from a script selecting `poster` is **not** evidence the resulting poster reads well.
- A user-selected `poster` adapter for a stated Instagram delivery surface differs from its stated use; the conservative selector asks rather than silently changing required delivery checks.
- No automated “AI-like design detector”, generic aesthetic score, glyph-shaping test, font installer or licensed asset fetch was created.
- Strict comparison requires an actual earlier recorded policy and comparison evidence. The CLI always returns `prior_strict_policy_verified: false` as a guard; host authorization and historic evidence must be verified separately.
- A `needs-clarification` result does not grant permissions and asks no more than one question.
- Preserving upstream language plugins and existing SEO Draft PR #93 is a delivery constraint.
- An implementation PR is not authorization for main merge or GitHub Release. Review the candidate version and decide publication separately.

## Follow-up phases (not included here)

True native host interaction validation; broader locale-specific integration with independently versioned language plugins; true renderer-based QA of actual posters, PNGs, Office/PDF and website outputs; dataset-backed error/recall evaluation for the text-only selector. These need scoped cases, tools and actual evidence. The existing design v0.1/v0.1a remains the source of what is authorized.
