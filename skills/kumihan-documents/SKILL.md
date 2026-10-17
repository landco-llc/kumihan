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

## 3. Build with these settings

Read [document recipes](references/document-recipes.md) for Word, PowerPoint and HTML-to-PDF settings. In short:

- Set the Japanese (East Asian) font separately from the Latin font.
- Turn on kinsoku (line-breaking rules) in the application.
- For short Japanese titles, apply JA-TYPE-011: compare natural speech groups, keep modifier and particle relationships together when feasible, adjust the text box/layout first, and check actual rendered/exported lines.
- Reports: keep headings with the content that follows; avoid splitting table rows, captions and footnotes across pages.
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
