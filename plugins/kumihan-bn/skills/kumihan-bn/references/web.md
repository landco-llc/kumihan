# Web / Web UI

**For bn-BD and bn-IN:** use the shared Bengali/Bangla script core with distinct editorial locale profiles. Exact approved text must remain intact across UI, CTA, routes, SSR, PDF export and alt text. Keep semantic headings, accessible focus states and action labels. Check 320px, 200% zoom, dark/light if supported, touch targets, overflow and inherited CSS.

Unicode logical order vs glyph order: `কি` stores KA then VOWEL SIGN I; `কৌ` stores KA then VOWEL SIGN AU. A renderer performs reordering. Treat `ক্ষ`, `স্ত্র`, `র‍্য`, `অ্যা`, `ক্‌ষ` as high-risk for splitting/reveal. `Intl.Segmenter` is not a complete typographic boundary proof.

Baseline CSS is only a starting proposal:
```css
:lang(bn) { word-break: normal; letter-spacing: normal; hyphens: manual; }
.long-token { overflow-wrap: anywhere; }
```

Never call CSS-only presence checks proof that a page renders correctly; observe screenshots/DOM text and viewport sizes. Underline, italic, punctuation, paragraph density and type role require context, not blanket bans.
