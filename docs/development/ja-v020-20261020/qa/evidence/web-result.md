# W01 QA-V01 and W02 Web acceptance evidence

Scope: source-guided Chromium artifacts, not a native AI-host invocation. State **VERIFIED** for the named DOM equality, local interaction and measured reflow checks; **PARTIALLY_VERIFIED** for visual/semantic review; native host/zoom/glyph-reference acceptance **NOT-CHECKED**. Renderer version and platform-font runs are in `web-observations.json`.

## Candidate guidance and brief

Read actual candidate `skills/kumihan/SKILL.md`, `skills/kumihan-web/SKILL.md` and the web entry's web-recipes, typography-context, typography-recipes-by-task, review-protocol, use-case-selection, use-case-adapters, design-review-modes, visual-relationship-guidance and japanese-writing-and-type references. These were read from the candidate source, not installed through the host. `web-brief.md` was recorded before authoring the standalone fictional-event prototype. It separates the marketing, editorial, mandatory-information and UI regions. No live account, registration backend or external asset is involved.

## QA-V01: FIXED within the synthetic positive specimen

Reproducer: `python tools/qa_web_acceptance.py`. `v01-before.html` is the exact historical synthetic input and 240px control; `v01-after.html` is the bounded corrected synthetic specimen. `web-observations.json` has 32 runs: before / width270+balance only / local groups at240 / local groups at270, each at 320/375/768/1024 and CSS 100%/200%. Before/after images are `v01-{stage}-{width}-css{100,200}.png`; `v01-comparisons.jpg` shows the 320px alternatives together.

Baseline at 18px reproduces:

```
2026年度・特別会員向けオ
ンライン講座の受講登録を
取り消す
```

The smallest successful local treatment tested at both sizes uses a 270px control with max-width:100%, balance and inline nonbreaking short lexical ranges (特別会員向け, オンライン, 講座, 受講登録, 取り消す). It adds no visible/zero-width source characters, forced breaks or phrase blocks and makes no page-wide wrapping rule. The matching generator is updated alongside the fixture so regeneration cannot erase the correction. It is an example-specific treatment, not a new general KUMIHAN requirement.

After at 18px, all four viewports show:

```
2026年度・特別会員向け
オンライン講座の
受講登録を取り消す
```

After at CSS-simulated 36px:

```
2026年度・
特別会員向け
オンライン講座
の受講登録
を取り消す
```

All 32 alternatives retained exact textContent and focus and had no button overflow. Width270+balance alone still splits 講座 at 36px; local ranges remove that lexical split. Assisted inspection of the before/after comparisons finds the ordinary-size result materially clearer: modifier/subject/action correspond to the three lines, オンライン is intact, and the last line holds the whole action. Enlarged lines preserve lexical terms; particles at a line start are an accepted reflow tradeoff in this observed region, not forbidden punctuation. No optimal-typography or reader-performance assertion follows. JA-TYPE-004 can be passed by assisted review **only for these exact after regions and sizes**; native user text zoom and other fonts/hosts remain not-checked. Historical `case-results.json`, negative PV-005 and all earlier evidence are untouched.

## W02: standalone real Web artifact

`web-positive.html` is an actual authored standalone information/UI prototype; `web-negative.html` is a separate deliberate failure. The prototype contains exact repeats of:

- `髙﨑さま／料金１,２００円／が` (including compatibility character and decomposed combining mark),
- `文字の庭／2026年11月3日／文字の広場（架空会場）`,
- the original long cancellation label.

`web-observations.json` records codepoints and UTF-8 input digests, exact DOM comparisons, Range-derived visual lines, bounds and CDP used-font runs. Every one of 20 positive states passed exact field checks, button fit, page-width fit, focus and local Enter/click demo status. The active control updates only the local status and explicitly says no real registration changed. All mandatory text is visible in the full-page screenshots; it is also in the ordinary semantic DOM. `web-accessibility-tree.json` is Chromium's actual accessibility tree; no speech/screen-reader application was run.

Full-page images: `web-{320,375,768,1024,1440}-{normal,css200,spacing,fallback}.png`. All 20 were inspected end to end via the five `web-contact-{width}.jpg` sheets (four states per sheet), including headings, exact mandatory fields, button, status, mixed English/Japanese paragraphs, glyph comparison and footer. The smallest regions are available at native screenshot resolution. No clipping, decorative occlusion, missing-glyph box or forbidden line-start punctuation was observed. Range line-map checks of h1, mandatory source, protected text, article paragraphs and status found no leading `、。）」』】ゃゅょっー` in these states. The 320px enlarged state is necessarily tall but remains reachable and functional without horizontal scroll. This is assisted visual inspection, not a machine score.

| Width | normal | CSS200 | spacing | fallback |
| --- | --- | --- | --- | --- |
| 320 | inspected; fit | inspected; fit | inspected; fit | inspected; fit |
| 375 | inspected; fit | inspected; fit | inspected; fit | inspected; fit |
| 768 | inspected; fit | inspected; fit | inspected; fit | inspected; fit |
| 1024 | inspected; fit | inspected; fit | inspected; fit | inspected; fit |
| 1440 | inspected; fit | inspected; fit | inspected; fit | inspected; fit |

Spacing state applies line-height1.5, paragraph margin-bottom2em, letter-spacing.12em and embedded English word-spacing.16em. Fallback state requests an absent webfont then installed Noto Serif CJK JP; this artifact uses no remote webfont. CDP records the actual resolved fonts per named region: normal Japanese NotoSansCJKjp-Regular; Traditional Chinese NotoSansCJKtc-Regular. This is observed font resolution, **not regional glyph certification**: no independent authorized glyph reference was supplied. The serif fallback is visibly different and remains readable in observed states.

Computed palette contrast ratios: body #172d29/white 14.54:1, white/button #235d4c 7.66:1, link #164f85/#f1f5f2 7.66:1, focus #a24b00/white 5.93:1. No dark-mode variant was authored or claimed.

## Case-specific observations for W05

| Case | New observed scope | Status/method |
| --- | --- | --- |
| PV-001 | exact Unicode in #protected across20 states | CONTENT-001 passed/static; displayed rendering separately inspected |
| PV-003/004 | ja/zh-Hant-TW CDP font runs and visible comparison | WEB-007 passed/rendered for resolved font identity only; authorized regional glyph correctness not-checked |
| PV-005 | deliberately clipped historical negative | historical failed status retained; not repaired or promoted |
| PV-006 | corrected specimen at4 widths, 18/36px CSS | WEB-005 passed/rendered; JA-TYPE-004 passed/assisted for exact after region; native200% not-checked |
| PV-010/012 | exact original event source + date/place/price in full-page artifact | CONTENT-001 passed/static; WEB-005 passed/rendered for visible required information; no speech application claim |
| PV-016/017 | user-spacing overrides at5 widths | WEB-003 passed/rendered for actual overridden prototype regions; hypothetical false-pass negative remains a separate contract |
| PV-020 | CSS200 enlargement at5 widths | content/function observed; actual native enlargement mechanism not-checked, never relabelled as native passed |

The separate `web-negative-320.png` shows its intended label clipping and hidden venue. It remains a failed artifact even though the regression recognizes the failure.

## Limits

No candidate native ChatGPT/Codex/Claude/Gemini installation or invocation, actual screen-reader speech, user-native browser text zoom, other browser engines, physical display/projection, reader performance or regional-glyph correctness certification. No main merge/tag/Release/Pages update/Marketplace submission. Parent performs the global regressions and final independent review.
