# Cross-medium text and visual relationships

These are *application guides for existing DESIGN and media-specific rules*, not a new graphic-design profile or an automated image-analysis guarantee. They serve posters, banners, presentations, documents and websites alike.

## Check at the actual target size

- **Information order:** Which element will be seen first, second and last? Does the reading path match the stated objective and actual audience?
- **Text on imagery:** Can the headline be read against the observed background? Is the placement intentional, and do crop variants, font substitution or responsive wrapping obscure it?
- **Negative space:** Does whitespace group information, provide legibility and support the intended mood? Blank space is not automatically waste; filled space is not automatically better.
- **Figure/text binding:** Is a photo, chart or illustration tied to its actual caption, label, footnote or explanatory text? Is a decorative visual mistaken for evidence?
- **Type and color roles:** Are hierarchy and contrast intentional and actually observable with the available licensed fonts/assets? Avoid assuming a font was available just because it appears in CSS.
- **Scale and cropping:** Test the real banner pixel dimensions, projected slide view, print size or device width where the host can render them. Do not infer quality from a desktop screenshot alone.
- **Brand continuity:** Honor licensed logos, type and color constraints. A visually ordinary brand component may be the *right* design.
- **Claims and actions:** Never create fake statistics, invented reviews, mock controls disguised as working UI, nonfunctional CTAs or inaccurate rights assertions.

## Adapter emphasis (not automatic eligibility)

| Adapter | Inspect | Unverified concerns |
|---|---|---|
| poster | Headline-image visual mass, type distance, physical format | Printer proof/bleed/CMYK/ICC when no authorized print workflow exists |
| social-static | Mobile-sized reading, text safe areas, source/claims | Platform previews and uploads |
| digital-banner | Legibility at requested pixels, crop and text balance | Click tracking or interactivity in an image |
| slide-deck | Projected hierarchy, figure provenance, titles, notes | Native PPTX editing from screenshots |
| landing-page | Real CTA, evidence and layout at narrow widths/zoom | Analytics or conversion results |
| report | Captions, table integrity, paragraph/page edges | Unchecked native Office and print appearance |

For multilingual work, compare copy lengths and script-specific shaping **without** automatically changing, translating or normalizing the supplied content. Determine type role per locale and check real glyph coverage and fallback. For RTL scripts test reading order, punctuation and mixed-script direction separately. The shared design guidance never replaces the independently maintained locale typography pack.

Use `static` for exact byte/text and available document structure comparisons, `rendered` only after observing the actual output, `assisted` for layout critique and `manual` for human verification. Preserve `needs-review`, `not-checked`, `unsupported` and `failed` as distinct states. Never produce an absolute design score or claim the work's origin can be inferred from appearance.
