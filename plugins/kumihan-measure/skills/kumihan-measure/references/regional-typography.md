# Regional typography, number display and mixed scripts

Use this reference with [workflow.md](workflow.md), the selected locale and explicit house style. Regional labels describe context; they do not establish a universal font, scale, line length, tracking value or beauty score. Preserve exact supplied text and metadata. Propose layout or editorial alternatives separately, with the user's permission and applicable source scope.

## Roles and media

| Role | Conditional advice | Evidence still needed |
| --- | --- | --- |
| Body | Choose a readable rhythm for the actual typeface, language, reader and medium. Compare line length and line height together. | Actual viewport or page, computed styles, font load and long content. |
| Heading | Keep semantic hierarchy separate from visual size. Check proper names and house style before suggesting capitalization. | Font, content role, wrap points and the selected design-system version. |
| UI | Check action meaning, recovery, label length, focus and keyboard order. Short fragments can be intentional. | Actual interaction, narrow reflow, user spacing and assistive technology. |
| Display/marketing | Preserve deliberate fragments and fixed copy. Offer spacing and line-break alternatives as design choices. | Viewing distance, intended emphasis, actual font and permission for copy edits. |
| Data | Choose lining/tabular features only for the comparison task. Keep numerical value, currency code, date schema and timezone distinct from display locale. | Available font features and actual Intl/renderer output. |

Published system tokens belong to the specified system, role and version. GOV.UK Frontend v6+ body and mobile scale guidance must not be merged with older mobile values (REG-S50/REG-S51). SGDS v1 Lato and current Inter describe different versions (REG-S25/REG-S26); unresolved versions need review. MYDS general headings and rich-text headings have different font contexts; inspect the applicable role rather than applying Poppins to every heading (REG-S27). GOV.UK, USWDS, NSW, SGDS, MYDS and Canada.ca examples do not grant font distribution rights or prescribe a national font. Obtain valid rights separately; no font files are included here.

## Text spacing and rendering

WCAG text-spacing override conditions include line height 1.5 times font size, paragraph spacing 2 times font size, letter spacing 0.12em and word spacing 0.16em (REG-S61). They test content/function loss when applicable user overrides are applied. They are not compulsory design defaults and must not be used as a universal aesthetic grade. Check the actual layout with long words, mixed scripts, fixed copy and controls; hidden overflow or nowrap is a static review signal, not proof of rendered clipping.

For web output inspect 320 CSS px-equivalent reflow, 200% text resize and applicable user spacing. Record the browser, viewport, zoom/resize method, font files and font-load status. A screenshot or CSS emulation must be described as such. Without the target renderer and fonts, glyph coverage, shaping, width, line breaks, clipping and visual quality are `not-checked`. Metadata and successful UTF-8 preservation cannot establish them. Browser or PDF checks do not establish native Office or PowerPoint acceptance; reopen each actual target format independently.

## Number and date display

Treat Intl output as a formatted display of a separately supplied value. Never infer currency from locale, convert USD to SGD, guess a timezone, or parse an ambiguous numeric date such as `03/04/2026` into a calendar value. Keep currency codes, input date schema, timezone and fraction-digit options explicit. Retain original code points, including NBSP or narrow NBSP; ASCII-only grouping assumptions can change meaning or break parsing.

Record runtime, Intl implementation, ICU version, CLDR version, resolved locale, rounding/fraction options and timezone for any measured comparison (REG-S58/REG-S59/REG-S60). The bounded reference observation on Node 22.16.0 / ICU 77.1 / CLDR 47.0 produced `12,34,567.89` for en-IN and `1 234 567,89` for en-ZA with two fraction digits. Those are reference-environment observations, not portable expected strings for every runtime or proof that this product ran Intl. Newer CLDR documentation does not change the older probe's recorded CLDR version. Run the actual target environment and inspect output code points independently.

## Inserted languages and names

Keep base locale separate from each span's language. Preserve `te reo Māori`, macrons, decomposed combining sequences, names, punctuation, identifiers and all joiners or direction controls. Do not strip accents or normalize the stored original to compensate for missing glyphs. English locale does not authorize dictionary correction of a Swahili span. Treat `Green Tea（煎茶）`, Japanese, Simplified and Traditional Chinese, Korean, Arabic and Hebrew as distinct coverage and layout requirements.

Keep logical source order in RTL/LTR mixtures; do not reverse source characters or digits to imitate a screenshot. For dynamic inserted spans, consider `bdi`/`dir=auto` in the intended document structure and inspect punctuation, parentheses, selection, copy/paste and reading order in the actual renderer. English font success alone does not prove CJK, Māori or RTL support. Keep missing-font, fallback, ligature, grapheme and joining checks `not-checked` until measured.

## Acceptance and evidence

[../fixtures/regional-acceptance.json](../fixtures/regional-acceptance.json) maps all 32 regional acceptance candidates into the existing `cases` fixture pattern. Each entry preserves a distinct ID, source context, expected boundary and remaining check. `execution_status: not-run` and `actual_result: null` describe the proposed editorial/rendering/runtime acceptance, not the separate static regression tests. Source IDs use the `REG-Sxx` namespace in sources.json.

`test_regional_rendering.py` exercises exact bytes and metadata with changed-candidate negative cases, including Māori/CJK/RTL/combining marks and number/date text. A passing integrity comparison means only the supplied source was retained. Language and contextual meaning remain `needs-review`; actual font/renderer, native Office, accessibility, house-style editing and release/package checks require their own evidence. Do not convert all 32 candidates to passed because the static test succeeded.
