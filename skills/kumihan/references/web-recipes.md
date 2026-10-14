# Web recipes for Japanese text

Concrete starting points for Japanese web typography. Apply them by text role, then check the result in a real browser. Values are starting points to adjust for the actual font, column and audience, not fixed requirements.

Browser support changes. The support notes below follow MDN browser-compat-data as of October 2026 and were confirmed with `CSS.supports()` in Chromium 141. Check MDN again before relying on a newer property. Every property here degrades safely: an unsupported property is ignored and the browser default applies.

## 1. Page setup

```html
<html lang="ja">
```

- `lang="ja"` lets the browser pick Japanese glyphs and apply Japanese line breaking. Mark embedded English with `lang="en"` where it matters.
- Never fix layout problems by editing the text itself (inserting spaces, `<br>` inside names, replacing characters).

### Font stacks

```css
/* Sans-serif (gothic) */
font-family: "Noto Sans JP", "Hiragino Sans", "Hiragino Kaku Gothic ProN",
  "Yu Gothic", YuGothic, Meiryo, sans-serif;

/* Serif (mincho) */
font-family: "Noto Serif JP", "Hiragino Mincho ProN", "Yu Mincho", YuMincho, serif;
```

- Use only fonts that are actually available and licensed for the project.
- Yu Gothic on Windows can look thin at weight 400. If it is in the stack, test it; `font-weight: 500` for body is a common adjustment.
- A web font can be large. Subset it or use a hosted service, and check the page before the font finishes loading.

## 2. Settings by text role

| Role | Starting settings | Notes |
| --- | --- | --- |
| Body text | `font-size: 16px`; `line-height: 1.7–2.0`; `line-break: strict`; `letter-spacing: 0` | Aim for roughly 30–40 characters per line on desktop; narrower on phones is fine. |
| Headings | `line-height: 1.3–1.5`; `word-break: auto-phrase`; `text-wrap: balance` | `palt` and slight negative tracking only if the font supports it and you check the result. |
| Display copy (hero, banners) | Same as headings; tighter spacing allowed | Keep the tightening on this element only. |
| Captions, notes | `font-size: 0.875em` or larger; `line-height: 1.6–1.8` | Must stay readable; do not shrink to hide overlap. |
| UI labels, buttons | `line-height: 1.4–1.5`; allow wrapping | Two-line labels are fine. Do not force `white-space: nowrap` on long labels. |
| Tables and numbers | `font-variant-numeric: tabular-nums` | Aligns digits in columns. |

### Example

```css
body {
  font-size: 16px;
  line-height: 1.8;
  line-break: strict;
  overflow-wrap: break-word;
}

h1, h2, h3 {
  line-height: 1.4;
  word-break: auto-phrase;
  text-wrap: balance;
}

.display {
  font-feature-settings: "palt" 1;
  letter-spacing: 0.02em;
}

.url, .code-id {
  overflow-wrap: anywhere;
}
```

## 3. Line breaking

| Goal | Property | Support | Use |
| --- | --- | --- | --- |
| Strict kinsoku (no small kana `ゃゅょっ` or `ー` at a line start) | `line-break: strict` | Chrome, Firefox 69+, Safari | Body text and articles |
| Break headings at phrase boundaries | `word-break: auto-phrase` | Chrome 119+ only (Safari in preview); requires `lang="ja"` | Headings, short display text. Not needed for long body text. |
| Even line lengths in headings | `text-wrap: balance` | Chrome 114+, Firefox 121+, Safari 17.5+ | Headings up to a few lines |
| Avoid a single short last line | `text-wrap: pretty` | Chrome 117+, Safari 26+; not Firefox | Body paragraphs, as an enhancement |
| Break long URLs and IDs | `overflow-wrap: anywhere` | All major browsers | Only on the element that holds them |

- Rendering check (Chromium 141, IPAGothic, 16px): across ten column widths, `line-break: normal` put a small kana or `ー` at a line start at nine widths; `line-break: strict` at none. `word-break: auto-phrase` broke a heading as 日本語の／文字組みからAIの／デザインをもっと／自然に.
- For phrase breaks in browsers without `auto-phrase`, insert `<wbr>` at phrase boundaries in headings, or use a phrase-splitting library such as BudouX at build time. Do not insert visible spaces.
- Avoid `word-break: keep-all` on Japanese body text; it removes normal break opportunities.
- Avoid `word-break: break-all` and page-wide `overflow-wrap: anywhere`; they break Latin words and numbers badly.
- Do not set `white-space: nowrap` on headings, paragraphs or long buttons.

## 4. Punctuation and spacing

| Goal | Property | Support | Use |
| --- | --- | --- | --- |
| Trim the extra space of brackets and punctuation | `text-spacing-trim` | Chrome 123+ only | `trim-start` trims at line starts; `space-all` keeps full-width spacing. The default varies; check the output. Needs a font with the relevant OpenType features. |
| Proportional punctuation and kana in headings | `font-feature-settings: "palt" 1` | All major browsers, if the font supports `palt` | Headings and display copy only. Not for body text. |
| Space between Japanese and Latin/numerals | `text-autospace: normal` | Chrome 140+, Firefox 145+, Safari 18.4+ | Adds a small gap automatically. Never type spaces into the source for this. |
| Hanging punctuation | `hanging-punctuation: allow-end` | Safari only | Optional enhancement. |

- `text-spacing-trim` had no visible effect with IPAGothic, which lacks the needed OpenType features. Check it with the actual project font.
- Keep one punctuation style per role. Do not mix trimmed and untrimmed punctuation in the same body text.
- When Latin text or numerals look too large or small next to Japanese, adjust the font stack or size of that span with CSS. Do not change the characters.

## 5. Vertical text

```css
.tategaki {
  writing-mode: vertical-rl;
  text-orientation: mixed;
}

.tcy {
  text-combine-upright: all; /* Two-digit numbers set horizontally inside vertical text */
}
```

- Check scrolling direction. Vertical text usually scrolls horizontally, so reflow is checked at 256 CSS px height instead of 320 px width.

## 6. Ruby and notes

```html
<ruby>組版<rt>くみはん</rt></ruby>
```

- Check that ruby does not collide with the line above, and increase `line-height` if it does.
- Keep footnote markers and their notes linked and in reading order.

## 7. Accessibility checks

Check these in a real browser:

| Check | How |
| --- | --- |
| Reflow | Set the viewport to 320 CSS px wide. Content and controls must work without horizontal scrolling (except genuine 2D content such as maps or wide data tables). |
| Text zoom | Zoom text to 200%. Nothing is cut off or overlapping. |
| Spacing overrides | Apply line height 1.5×, paragraph spacing 2×, letter spacing 0.12× and word spacing 0.16× the font size. Nothing is cut off. |
| Long content | Test with the longest real label, name and URL. |
| Fonts | Check the page with the web font loaded and with the fallback font. |
| States | Check focus, error, loading and disabled states that actually exist. |

Do not use `overflow: hidden` on large containers to hide overflowing text. Find and fix the cause.

## 8. Common mistakes

| Mistake | Instead |
| --- | --- |
| Global `letter-spacing` or `palt` on all text | Apply to headings or display copy only |
| `white-space: nowrap` on buttons and headings | Allow wrapping; shorten only with permission |
| Typing spaces between Japanese and Latin | Use `text-autospace` or leave as is |
| Shrinking text to fit a box | Change the layout or allow wrapping |
| Text inside images | Use real text, unless the image is a logo or essential |
| Inventing numbers, reviews or logos to fill a section | Use only supplied content, or leave the section out |
