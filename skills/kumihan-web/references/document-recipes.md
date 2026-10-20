# Document recipes for Japanese reports and slides

Concrete starting points for Japanese reports and presentations in Word, PowerPoint and HTML-to-PDF. Values are starting points to adjust for the actual font, page size and viewing conditions, not fixed requirements. Menu names vary by application version and language; check the actual application.

## 1. Fonts

- Set the **Japanese (East Asian) font** and the **Latin font** separately. Office applies them independently, and a missing Japanese font setting is one possible cause of wrong glyphs; also inspect resolved fonts, fallback, language and renderer.
- Use fonts that are installed on the machines that will open the file, or embed them where the license allows.
- Common choices: Yu Gothic / Yu Mincho (Windows and Office), Hiragino (macOS), Noto Sans JP / Noto Serif JP (free, cross-platform), Meiryo (older Windows).
- For projection, compare actual gothic and mincho faces, ink size, weight, contrast, viewing distance and reader task; classification alone guarantees no advantage.

### Generating Office files with code

If you create files with a library, set the East Asian font explicitly:

- **python-docx**: set `w:rFonts` with `w:eastAsia="Yu Gothic"` on the run or style, in addition to the normal font name.
- **python-pptx**: set the `a:ea` element with `typeface="Yu Gothic"` on the run properties, in addition to `a:latin`.
- Set the language of Japanese runs to `ja-JP`.

## 2. Line breaking and punctuation in Office

**Word** — Paragraph settings → Asian typography (体裁):

- Turn on line-breaking rules (禁則処理を行う).
- Choose standard or strict kinsoku consistently for the whole document.
- Hanging punctuation (句読点のぶら下げ) is optional; use it consistently.

**PowerPoint** — Paragraph settings → Asian typography (体裁):

- Turn on line-breaking rules (禁則処理を行う).
- Allow Latin text to wrap in the middle of a word only if the content needs it.

Check actual line starts and ends after the final font is applied. Do not insert manual line breaks or spaces into supplied text to fix a break, unless the user asks.

### Natural prosodic groups in Japanese titles (JA-TYPE-011)

For short Word, PDF and PowerPoint headings, first check ordinary wrapping and whether intentional breaks are needed. Compare modifier attachment, all lines and surrounding space; natural speech is an assisted interpretation, not a measured fact. `いつものAIツールから／はじめよう` is one conditional comparison, not a compulsory split or widening sequence. Check actual exported line ends and smaller/zoomed states. Preserve every original source character; never assume font or Office kinsoku alone proves a natural break. Document semantic judgments (assisted) and actual rendering (observed) separately.

## 3. Reports

| Element | Starting point |
| --- | --- |
| Body text | 10.5–11 pt (A4 print); line spacing about 1.5–1.8 lines |
| Line length | About 35–45 characters per line in a single-column A4 layout |
| Headings | Clear size or weight steps; keep with the next paragraph |
| Tables | Repeat headers; keep only short rows that fit a page together. Split oversized rows while retaining final cells and notes |
| Figures | Keep the figure, caption and source note together |
| Numbers | Align digits in tables; keep units with numbers |

Word settings that help:

- Heading styles: "Keep with next" (次の段落と分離しない).
- Table rows: disable splitting only for rows that fit the usable page height; allow and inspect continuation for longer rows.
- Table header: "Repeat as header row".

Check every page, not just the first few. Look for headings stranded at the bottom of a page, split table rows, separated captions, and wrong page numbers or cross-references.

## 4. Slides

| Element | Starting point (16:9 projection) |
| --- | --- |
| Body text | 18pt or 24pt can be comparison starts only; record smallest required role, projected dimensions and farthest seat |
| Titles | About 28–40 pt |
| Lines per slide | Keep text short; one main message per slide |
| Notes | Keep speaker notes complete and on the right slide |

When a slide overflows:

1. Split it into two slides, or
2. Regroup the content (table, diagram, fewer bullets with the same information), or
3. Move supporting detail to an appendix slide.

Do not shrink all text until it fits, and do not move required information into the speaker notes. Removing or rewording content needs the user's permission.

Check the slides at the real viewing size (or a realistic preview) and confirm the slide order follows the intended message.

## 5. HTML or Markdown to PDF

```css
@page { size: A4; margin: 20mm; }

body {
  font-size: 10.5pt;
  line-height: 1.7;
  line-break: strict;
}

h1, h2, h3 { break-after: avoid; }

figure, .short-row, .keep-together { break-inside: avoid; }
/* Apply keep only to units that fit a page. Oversized rows must continue. */

p { orphans: 2; widows: 2; }

thead { display: table-header-group; } /* Repeat table headers */
```

- Do not set `overflow-wrap: anywhere` or `word-break: break-all` on the whole body. Apply `overflow-wrap: anywhere` only to long URLs or IDs.
- Embed or install the Japanese font in the PDF renderer; otherwise text may fall back to a different font or show missing-glyph boxes.
- Check that text in the PDF can be selected and copied correctly.

## 6. After export

| Check | Why |
| --- | --- |
| Copy text out of the PDF/PPTX/DOCX and compare with the source | Checks exact supported extracted text only; does not prove glyphs, visibility, reading order or absence of clipping |
| Open the file in the target application (actual Office, not only a preview) | Previews and converters can render differently |
| Confirm fonts are the intended ones | Missing fonts are silently substituted |
| Confirm required editability | Text converted to images or outlines cannot be edited |

Record the application name and version, fonts and page size used. If you could only check a preview or a PDF, say that native Office rendering was not checked.

Projection remains not-checked when physical dimensions, farthest seat or environment are unknown. Inspect every rendered page for overlap, clipping, continuation headers, final cells, notes and reading order. PDF extraction and PDF preview are distinct observations, and neither establishes native Office acceptance. These recipes add no common document-generation service.
