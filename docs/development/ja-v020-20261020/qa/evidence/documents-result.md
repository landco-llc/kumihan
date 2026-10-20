# W03 — actual report and PPTX artifact evidence

State: **VERIFIED within the named visual preview scopes; PARTIALLY_VERIFIED overall; P1 FAILED for LibreOffice-export PDF exact extraction/copy fidelity; native Microsoft Office and real projection NOT-CHECKED.** No global G2 exact-export PASS is supported. No native AI-host installation or invocation is established.

Inputs were read from the four candidate `skills/kumihan*/SKILL.md` entries, document recipes, typography context, conditional task recipes, Japanese writing/type, routing, Standard review and visual-relationship guidance. Profiles: report-document + report and presentation + slide-deck. A pre-production brief, role sizes, fictional data provenance and protected strings are in [documents/brief.json](documents/brief.json) and [documents/source.json](documents/source.json). This is a standalone artifact test authored under source-read guidance, not a new document-generation product or installed-skill runtime test.

Reproduce: `python tools/qa_documents_v020.py`. Actual renderers: Chromium 154.0.8037.57, LibreOfficeDev 26.8.0.0.alpha0 (`2c87e51eeaa2b413ff4ae097b2705eea1995d8e5`), PyMuPDF rasterization at 1.25x. `soffice` exists through the runtime override; there is no need to install another renderer. Report A4, 20mm margins; deck 13.333 × 7.5in. Noto Sans CJK JP was available; embedded PDF font inventory is recorded in measurements.json. Font-family declaration alone is not glyph certification.

## Deliverables and exact text

- [Report source](documents/report.html), [six-page PDF](documents/report.pdf), [PDF extraction](documents/report-extracted.txt).
- [Eight-slide editable PPTX](documents/presentation.pptx), [LibreOffice PDF export](documents/presentation.pdf), [PPTX text](documents/pptx-extracted.txt), [PDF extraction](documents/presentation-extracted.txt), [conversion log](documents/conversion.log).
- [Measured results and file sizes/SHA-256](documents/measurements.json). PPTX ZIP CRC is clean. Saved PPTX XML retains all three protected strings exactly, including 髙, 﨑, fullwidth digits and decomposed か + combining dakuten. All three strings also occur exactly in the Chromium report PDF extraction.
- **P1 / FAILED — LibreOffice PDF exact extraction/copy fidelity:** all three exact-substring checks are false, because the PDF extraction inserts spaces between Latin/numeric and Japanese runs (`2026 年`, `１, ２００`). The PPTX XML source remains exact. No normalization or space-stripping was used to turn this into a pass. This converter-export scope must not receive exact-export acceptance or a global G2 PASS. The observation does not establish changed PPTX source. Native Office copy/paste is not-checked.

## All-page visual audit

Every image below was opened with view_image. Judgments about readability and grouping are assisted observations of these specific images, not reader-performance measurements. No sampled-page claim is used. Rendered observations: no clipped mandatory text, missing glyph boxes, text occluded by shapes, stray line-head punctuation, orphaned heading, lost final table cells or lost final note was observed. Fullwidth price and decomposed source are preserved in source/extraction but variant-glyph correctness is not independently certified from image appearance.

| Page | Image | Observed region / result |
| --- | --- | --- |
| Report 1 | [image](documents/report-01.png) | Title/body hierarchy; date/place/price/name visible; mixed English paragraph wraps; introductory note visible. |
| Report 2 | [image](documents/report-02.png) | Table starts, legend precedes it; rows 01–12 visible with whole short rows. |
| Report 3 | [image](documents/report-03.png) | Header repeats; rows 13–26 continue, all columns visible. |
| Report 4 | [image](documents/report-04.png) | Header repeats; rows 27–40 continue, last row not clipped. |
| Report 5 | [image](documents/report-05.png) | Header repeats; rows 41–44 and final note visible on same page. Sparse remainder is intentional flow, not hidden content. |
| Report 6 | [image](documents/report-06.png) | Protected cancellation label intact, no オ／ンライン split, explanatory sections and closing legend visible. |
| Slide 1 | [image](documents/presentation-01.png) | Title, subtitle and mandatory date/place/name/price visible. |
| Slide 2 | [image](documents/presentation-02.png) | Three-step diagram and arrows; explanatory sentence below shapes. |
| Slide 3 | [image](documents/presentation-03.png) | Comparison columns align after bounded layout correction; no joined row labels. |
| Slide 4 | [image](documents/presentation-04.png) | Four bars and values 4/3/2/1 match source; legend explicitly says fictional QA input. |
| Slide 5 | [image](documents/presentation-05.png) | Background shape is behind all caution text; required information not occluded. |
| Slide 6 | [image](documents/presentation-06.png) | Long cancellation label fully visible; complete caption wraps below without collision. |
| Slide 7 | [image](documents/presentation-07.png) | Three limitations plus supporting note readable in preview; notes are also captured separately. |
| Slide 8 | [image](documents/presentation-08.png) | Summary order and Owner Gate visible; footer/page number remain visible. |

An initial slide 3 used whitespace in a single text run as pseudo-columns. In the actual converter output, its last row visually joined method and scope. Root cause was proportional whitespace used for layout. Replaced only that comparison region with separate aligned text boxes, preserving cell wording. [Before image](documents/presentation-03-before.png) and [after image](documents/presentation-03.png) are retained. No global font shrink or deletion of notes was used. All other slides were inspected before this local change; final slide 3 was inspected again. Each final slide has corresponding text and notes in measurements.json.

PV-027 historical clipped negative remains unchanged and failed. This new report's crossing table is a separate positive observation for DOC-002. PV-028 gains actual six-page report PDF preview and eight-slide PPTX/LibreOffice-export scope for DOC-004; this does not pass native Office. PV-023/024 projection and PV-025/026 physical signage/reader studies remain not-checked; no equipment or participants were invented. Actual printing, native editing, accessibility reading order in PowerPoint, and native host discovery/invocation require authorized operator evidence.
