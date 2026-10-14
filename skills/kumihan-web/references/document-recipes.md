# Document recipes for Japanese reports and slides

Concrete starting points for Japanese reports and presentations in Word, PowerPoint and HTML-to-PDF. Values are starting points to adjust for the actual font, page size and viewing conditions, not fixed requirements. Menu names vary by application version and language; check the actual application.

## 1. Fonts

- Set the **Japanese (East Asian) font** and the **Latin font** separately. Office applies them independently, and a missing Japanese font setting is the most common cause of wrong glyphs.
- Use fonts that are installed on the machines that will open the file, or embed them where the license allows.
- Common choices: Yu Gothic / Yu Mincho (Windows and Office), Hiragino (macOS), Noto Sans JP / Noto Serif JP (free, cross-platform), Meiryo (older Windows).
- For projected slides, a gothic (sans-serif) face is usually easier to read than mincho.

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

## 3. Reports

| Element | Starting point |
| --- | --- |
| Body text | 10.5–11 pt (A4 print); line spacing about 1.5–1.8 lines |
| Line length | About 35–45 characters per line in a single-column A4 layout |
| Headings | Clear size or weight steps; keep with the next paragraph |
| Tables | Repeat the header row on each page; do not let a row split across pages |
| Figures | Keep the figure, caption and source note together |
| Numbers | Align digits in tables; keep units with numbers |

Word settings that help:

- Heading styles: "Keep with next" (次の段落と分離しない).
- Table rows: turn off "Allow row to break across pages".
- Table header: "Repeat as header row".

Check every page, not just the first few. Look for headings stranded at the bottom of a page, split table rows, separated captions, and wrong page numbers or cross-references.

## 4. Slides

| Element | Starting point (16:9 projection) |
| --- | --- |
| Body text | About 18 pt or larger for a typical meeting room |
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

figure, table, .keep-together { break-inside: avoid; }

p { orphans: 2; widows: 2; }

thead { display: table-header-group; } /* Repeat table headers */
```

- Embed or install the Japanese font in the PDF renderer; otherwise text may fall back to a different font or show missing-glyph boxes.
- Check that text in the PDF can be selected and copied correctly.

## 6. After export

| Check | Why |
| --- | --- |
| Copy text out of the PDF/PPTX/DOCX and compare with the source | Confirms no characters were lost or changed |
| Open the file in the target application (actual Office, not only a preview) | Previews and converters can render differently |
| Confirm fonts are the intended ones | Missing fonts are silently substituted |
| Confirm required editability | Text converted to images or outlines cannot be edited |

Record the application name and version, fonts and page size used. If you could only check a preview or a PDF, say that native Office rendering was not checked.
