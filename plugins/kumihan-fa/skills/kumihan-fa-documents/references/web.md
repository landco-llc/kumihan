# Persian web and UI recipe

Set the actual language and base paragraph direction explicitly: e.g. <html lang="fa-IR" dir="rtl"> for an Iranian-Persian primary page. Language, text alignment and Bidi direction have different roles. Keep DOM and focus order meaningful; prefer CSS logical properties such as padding-inline and text-align:start, not blanket row-reverse.

Protect Persian joining and ZWNJ: no per-letter span split, arbitrary letter spacing, forced word-break:break-all, overflow-wrap:anywhere for ordinary prose or clipping to disguise a defect. Use structural isolation for LTR URLs, emails, versions and phone/technical codes. Do not automatically rewrite punctuation, numbers, date/calendar and currencies.

Consider Vazirmatn (regular/non Farsi-digits) as one test candidate for Persian UI and Estedad as an alternative—not a required aesthetic. Verify font availability and licenses. Test پ چ ژ گ ک ی, ۴ ۵ ۶ ۷, ezafe and diacritical marks, joining at several weights, browser shaping and fallback, line height and narrow screens.

Perform observed responsive and interaction tests at 320 / 390 / 768 / 1280 CSS pixels, 200% text enlargement and keyboard use. Inspect actual mixed-direction glyph display, focus, overflow, links, field selection and copy-paste. Static parsing is not a visual or host test.

For each page, choose the composition for its content: editorial, cards, table, article, story, gallery or UI. Do not make all Persian-language designs use calligraphic decoration, the same artificial gradients or repeated icon cards.
