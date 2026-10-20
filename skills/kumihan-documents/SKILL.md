---
name: kumihan-documents
description: Use when producing or refining Japanese reports or presentations, including pagination, chart data, footnotes, speaker notes, and Office export review.
---

# Japanese reports and presentations

Shape readable pages and slides while keeping every piece of source content intact.

## Always

- Keep names, prices, numbers, units, table cells, chart data, captions, footnotes and speaker notes exactly as supplied, including their original characters.
- Never delete notes, invent data or move required content into speaker notes to make a layout fit.
- Keep each figure with its caption and source, and each slide with its notes.
- Change only what the user asked for. A review never edits the target.
- Say plainly what you did not check.

## 1. Choose the profile

- Reports and paginated documents: [report-document](profiles/report-document.json)
- Slide decks: [presentation](profiles/presentation.json)

Look up rule details in the [catalog](rules/catalog.json) only when you need a rule's conditions or exceptions.

## 2. Before building, write a short brief

Purpose, audience, viewing conditions (print, screen, projection), the most important message, why this structure or slide order fits, and type roles (body, headings, captions, tables). Confirm which fonts are actually available in the target application.

## Shared design quality and selection

Read [the routing guide](references/use-case-selection.md), [design review modes](references/design-review-modes.md), and [visual relationship guidance](references/visual-relationship-guidance.md). A slide deck generally uses existing `presentation` plus `slide-deck`; a paginated report uses `report-document` plus `report`. A short poster or static-image headline is `display-copy`, not a seventh graphics profile. Honor compatible manual adapter overrides and clarify only important output/permission ambiguity. Standard is the default; Strict requires explicit selection. Image/PDF preview is not proof of native Office or print production.

## 3. Build with these settings

Read [document recipes](references/document-recipes.md) for Word, PowerPoint and HTML-to-PDF settings. In short:

- Set the Japanese (East Asian) font separately from the Latin font.
- Turn on kinsoku (line-breaking rules) in the application.
- For short Japanese titles, apply JA-TYPE-011: first check ordinary wrapping and whether intentional breaks are needed, then compare whole-line composition and meaning in actual rendered/exported lines; no compulsory widening or speech-group sequence.
- Reports: keep headings with the content that follows; keep short rows/captions/notes together only when they fit a page; allow oversized-row continuation while checking headers, final cells and notes.
- Slides: when content overflows, split the slide or regroup it. Do not shrink all text to fit.

## 4. Check before delivery

- Every relevant page or slide, not just a sample.
- No heading left alone at the bottom of a page.
- Table rows, figures, captions, footnotes and page numbers stay together and correct.
- Slide text is readable in the stated viewing conditions, and notes are complete.
- After export (PDF, PPTX, DOCX), the text, fonts and required editability survive. A PDF preview does not prove how the file looks in native Office.

Record the application, version and fonts used. If you could not render, say which checks were not done.

## Review and refine

For a read-only review, use `kumihan-review`. To apply its findings, get explicit permission for the exact part to change, then recheck what the change affects.

If the user asks for a formal design record, an exception or a waiver, use the [design contract](references/design-contract.md) and [architecture](references/architecture.md).

If a referenced file is missing, say so and continue with what is available.

## Context and evidence by region (v0.2.0)

Use [typography context](references/typography-context.md) for role, readingTask, attributed intent, prose/display/hybrid and required-information mapping. Keep the brief proportional to the task. Use [Japanese writing and type](references/japanese-writing-and-type.md) and [task recipes](references/typography-recipes-by-task.md) only for relevant decisions. Ordinary wrapping comes first unless intentional breaks are needed; JA-TYPE-002 kinsoku, 003 indivisible ranges, 004 meaning and 011 whole-line composition remain separate. Compare actual fonts, widths and surrounding layout without a mandatory speech-group or widening sequence.
