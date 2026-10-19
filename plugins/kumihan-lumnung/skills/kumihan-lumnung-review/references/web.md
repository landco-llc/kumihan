# Khmer Web / UI

For lang="km" / "km-KH" use a capable Khmer font, e.g. "Noto Sans Khmer" with actual fallback checks.
CSS starting point (NOT a verified universal prescription):
```css
:lang(km) { font-family: "Noto Sans Khmer", sans-serif; line-height: 1.7; letter-spacing: normal; word-spacing: normal; word-break: normal; line-break: auto; overflow-wrap: normal; text-align: start; }
.machine-token { overflow-wrap: anywhere; }
```
Avoid character-by-character markup and automatic ZWSP injection. Preserve COENG, Khmer punctuation, source spacing, brand names and date/currency semantics. Test 320/375/768/1280 CSS px plus 200% text enlargement, complex conjunct shaping, vertical clipping, copy/search and keyboard input. Unknown outcomes are not-checked.
Do not copy generic AI card/hero patterns without relating them to the content.
