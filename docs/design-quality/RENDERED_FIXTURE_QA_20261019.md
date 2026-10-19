# KUMIHAN v0.1.8-preview — bounded rendered-artifact QA (2026-10-19)

**Status:** synthetic fixture validation completed; preview release still requires an owner decision. This document adds **no product runtime changes**.

- Verified source baseline: `main` commit `73d2b01d2f604608360beabe364f59af72b8b66c` (merged PR #100).
- Design inputs: owner-adopted KUMIHAN design-quality v0.1 and use-case selection v0.1a.
- Complete QA package (HTML/PPTX/PDF/images/JSON): private project Drive, `30_EXECUTION/KUMIHAN_DESIGN_QUALITY_RENDERED_QA_20261019/`.
- Package: `KUMIHAN_Design_Quality_Validation_20261019.zip`, SHA-256 `68b7d11850f72d4c385b63a9d68d0facfd33cc826125ae49b22cb06fb5f25da5`, 47 manifest-listed evidence/source files plus manifest. This private Drive package is not a public plugin release.

## Production tasks and observed outcomes

| Synthetic task | Actual profile and optional adapter | Render or extraction evidence | Bounded outcome |
|---|---|---|---|
| Text-led poster | `display-copy × poster` | Original 900 × 1272 PNG, typography + vector illustration | Rendered and reviewed, printing/CMYK/bleed not tested |
| SNS static image | `display-copy × social-static` | Original 1080 × 1080 PNG | Flat text/bg contrast computed 11.774:1, no HTML carrier horizontal overflow |
| Landing page | `web-marketing × landing-page` | Chromium 144, widths 320 / 390 / 768 / 1440 and CSS root/body 200% simulation | 8/8 bounded viewport states had no document horizontal overflow; page-local CTA destinations exist, keyboard skip link focus visible |
| Three-slide deck | `presentation × slide-deck` | Editable PPTX, presenter notes, LibreOffice→PDF, PDF rendered at 130dpi | All three pages inspected; expected text fragments extracted; native Microsoft PowerPoint/Keynote was **not** tested |

A bare “バナーを作って” request returns one clarification for static image vs interactive HTML rather than inventing the delivery medium. All four named use cases selected the existing media profiles with `standard` review.

### Meaning-preserving Japanese line breaks

A draft landing-page headline at width 390px and simulated text 200% left one final Japanese character 「る」 on its own line. The synthetic HTML was refined by grouping authored phrase spans rather than changing protected content. After rerendering, 320px/390px both showed no one-character visual lines under the tested simulated enlargement. The observation is Chromium-specific; semantic correctness in untested target environments is not implied.

### Deliberately defective comparison fixtures

| Negative fixture | Observation | Limitation |
|---|---|---|
| Static image with low text contrast | Calculated flat text/bg contrast **1.108:1**, versus positive 11.774:1 | Flat CSS-region measurement, not full-image perceptual quality |
| Social static-image HTML carrier without a clip boundary | Document width **1135px** at 1080px viewport (55px overflow) | A fixed output PNG's intentional artwork crop is a different assertion |
| Web page with missing CTA and fabricated claim | Primary CTA points to absent `#missing-catalog`; explicitly ungrounded “99%” string appears | Automated link test possible; semantic evidence/claim truth needs a trusted external source or human review |

These defects were deliberately introduced and are **not** proof that KUMIHAN itself implements a general visual detector. The observer executed Playwright, static checks, font/color calculations and guided human/assisted review separately.

## Methods, evidence and limits

- `static` covered the link target, source text, file digest and editable PPTX structures.
- `rendered` covered Chromium screenshots (13 HTML render states), page scroll widths, actual character boxes, and LibreOffice-rendered PDF pages.
- `assisted` covered justification for a three-column peer comparison and visual hierarchy. A three-card structure or gradient alone is never an automatic failure.
- `manual` was required for design intent/approval provenance and the meaning of the composition. Synthetic local brief files do not substitute for independently authenticated permission or pre-production Strict evidence.
- Read-only QA integrity: HTML/PPTX SHA-256 before and after the audit matched. Negative fixtures were made independently rather than modifying targets during an audit.
- Missing and clearly separated as `not-checked`: native browser text-only zoom, user typography spacing overrides, Safari/Firefox, physical printing and ICC/CMYK/bleed, PowerPoint/Keynote native viewing, actual Instagram crops/compression, other-language native shaping, native AI-host plugin invocation and real customer assets/rights.
- Strict DESIGN-002 conditional severity is **not** asserted; this synthetic test did not independently verify pre-production Strict policy selection for materially different briefs.
- This work does not produce an “AI-authorship score”, an image-generation engine, an autonomous aesthetic correctness verdict or blanket bans on cards/gradients.

## Regression checks already confirmed

- Existing main-source unit tests: **59/59 PASS** at `73d2b01d`.
- Existing distribution determinism: `python3 tools/build_dist.py --check` — **148 generated files current**.
- Japanese type source-fixture consistency: **11 spec fixtures**, not a renderer.
- Browser checks: **13** states, and 3 PDF pages inspected (separate host).
- The full private QA ZIP passed a file-size and SHA-256 verification against its manifest.

## Proposed next gate (not automatically approved by this report)

The candidate `v0.1.8-preview` may be described as *guided, use-case-aware typography/design review with conservative routing* if the preview documentation lists its limits prominently. It should **not** be called a universal automated AI-style blocker, a native host-verified release, a print-ready solution or a production visual-quality certification.

Leave any GitHub Release/tag publication to a distinct owner decision. Do not modify pending multilingual SEO PR #93 or the independent language-plugin distributions as part of this QA documentation.

Reproducible original fixtures, PNGs, editable PPTX, exported PDF, screenshot metadata, report statuses and SHA-256 inventory are maintained in the bounded QA package in the project's private Drive.
