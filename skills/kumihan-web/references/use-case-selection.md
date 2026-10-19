# Use-case routing: automatic by default, manual override, ask only if necessary

**Status:** implemented guidance + optional conservative reference router.
**Decision:** KUMI-USECASE-ADAPTER-SELECTION-20261019-01. Applies to all six *existing* media profiles; never introduce a seventh `graphic-design` profile.

## What the user experiences

1. Start from the actual brief and authorized material. Determine the actual deliverable, platform, display/print/projection conditions, and protected text/assets.
2. **Auto by default:** infer the primary medium from the output artifact (not merely the marketing purpose). Add a supported use-case adapter only if the brief provides affirmative evidence. Otherwise use the normal medium profile with **no adapter**.
3. **Manual override:** if the user explicitly names an adapter, use it when compatible with the actual deliverable and permissions. It overrides the automatic recommendation. Never silently change the requested medium or pretend an incompatible adapter applies.
4. **Clarify only if consequential:** when image versus interactive HTML, or competing delivery formats, would change the output, material verification or permission, ask **one short question**. Do not ask about cosmetic uncertainty that a safe default can resolve.
5. Make the effective medium, adapter (or none), language/region, intensity and rationale accessible when relevant. These are **routing context**, not a new field in the frozen `design-contract:0.1.0` or `report:0.1.0` schemas.
6. Use the independent language product's typography for each protected segment. Do not normalize Unicode, perform Chinese script conversion, translate, or change names, prices, units, or brand copy without a separate request.
7. Only an existing host's authorized build tools create assets. This skill neither installs design software nor provides rendering.

## Adapter table

The canonical adapter definitions and limits are in `use-case-adapters.json`. Their IDs **are not rule IDs or profiles**.

| Requested artifact | Primary medium | Optional adapter | Why |
|---|---|---|---|
| Poster or print headline with visuals | `display-copy` | `poster` | Print scale, copy-image relation, output constraints |
| Instagram/SNS **static image** | `display-copy` | `social-static` | Viewing size, safe area, legible text/imagery |
| **Static** digital banner image | `display-copy` | `digital-banner` | Actual pixel dimensions and crop |
| Presentation or slides | `presentation` | `slide-deck` | Slide hierarchy, figure labels, notes and projection |
| LP / campaign Web landing page | `web-marketing` | `landing-page` | Real CTA and claims, responsive layout |
| Paginated report / distributed document | `report-document` | `report` | Pagination, figures, headings, protected data |
| General article | `web-editorial` | *none* | Existing editorial profile suffices |
| UI or form | `web-ui` | *none* | Existing UI profile suffices |
| Generic short headline/copy | `display-copy` | *none* | No reason to impose a poster/SNS adapter |
| Banner without stated output type | *unresolved* | *unresolved* | Ask whether static image or interactive HTML |

A static SNS ad is **not** automatically `web-marketing` simply because it advertises a product. Use the *actual medium*. An interactive HTML banner may use `web-marketing` without pretending to be a `digital-banner` static-image adapter.

## Optional helper (no dependency)

From any standalone skill root:

```sh
python3 scripts/use_case_selector.py --brief 'Instagram用の広告画像を作って'
python3 scripts/use_case_selector.py --brief 'Instagram用の広告画像を作って' --adapter poster
python3 scripts/use_case_selector.py --brief '新商品のランディングページを作って' --strict
python3 scripts/use_case_selector.py --brief 'バナーを作って'
```

The helper performs conservative, rule-based surface recognition for common JA/EN briefs. It returns a transparent suggestion with `selected` or `needs-clarification`, at most one question and the selected source. It is **not** a multilingual general-purpose intent model or a design detector. Host judgment must resolve other languages or complex requests; no selection is treated as verified authority or as a quality pass. No file is mutated and no approval is granted.

In combined work, name one primary medium and mark distinct regions/scopes for separately reviewed elements. A result outside the scope of the chosen profile is not passed simply because another profile was selected.

## Intensity and authority are independent axes

- `study`, `build`, `audit`, `refine` remain the permission-related workflow modes.
- `standard` is the **default review intensity**, regardless of adapter or subject.
- `strict` is used only when the user explicitly requests it. A selection made *after* production cannot retroactively establish a prior Strict policy or design contract for `DESIGN-002`.
- `audit` is always read-only. A useful fix recommendation does **not** authorize changing source files.
- New tool use, uploads, rights, source edits, publishing and exceptions require their own permission under the existing host contracts.

See `design-review-modes.md` for evidence and acceptance requirements and `visual-relationship-guidance.md` for cross-medium visual composition.

The published schema fields are frozen; `report.schema.json` cannot silently gain `adapter`, `intensity`, `design_score` or `confidence`. Selection metadata may be recorded in a host-managed context with attributable source and genuine chronology, but its permanent sidecar schema is **not yet specified**.

## Examples to keep

- If one decision would lead to PNG and another to an interactive Web implementation, ask which deliverable the user needs.
- If the user says “short catchphrase” and not “poster,” return `display-copy` + no adapter, not an unrequested media change.
- A supplied `poster` adapter overrides an inferred `social-static` only when both target an actually compatible text-led static image; if the brief actually requires an interactive Web UI, ask rather than quietly pretending.
- Never conclude “AI-made,” “AI-free,” “brand-compliant,” “approved,” or “rendering passed” from a routed adapter.
