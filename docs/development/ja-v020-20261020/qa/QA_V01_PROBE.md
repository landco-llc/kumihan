# KUMIHAN JA v0.2.0 QA-V01 — Chromium independent break comparison

Date: 2026-10-20 (JST)
Status: **independent synthetic reproduction and exploratory comparison**, not a v0.2.0 product runtime test and not shipping acceptance.

## Environment and source

- Chromium `144.0.7559.96`, headless, local environment.
- Page `probe.html` constructed from the exact long label and CSS behavior visible in PR #120 fixture `tests/fixtures/ja_v020/web-contrasts.html`. This test page includes alternate CSS/markup treatments not merged into the product.
- Protected input: `2026年度・特別会員向けオンライン講座の受講登録を取り消す`.
- Screenshots at 320, 375 and 1024 CSS px. The additional 320px CSS-simulated font-size 36px test is **not browser-native text zoom**.
- `results.json`, `scale-results.json` contain per-character `Range`-based grouped visual lines and exact `textContent` equality for each variant.

## Original issue reproduced

Baseline width240 / size18: at all three viewports the visual line mapping is:

    2026年度・特別会員向けオ
    ンライン講座の受講登録を
    取り消す

All variants preserved the original element `textContent` exactly. The baseline had no horizontal overflow but visibly broke the lexical term `オンライン` across lines.

## Exploratory alternatives

| Variant | Width / size | 320px visible lines | Horizontal overflow |
| --- | --- | --- | --- |
| baseline240 | 240px / 18px | 2026年度・特別会員向けオ · ンライン講座の受講登録を · 取り消す | No |
| responsive270 | 270px / 18px | 2026年度・特別会員向けオン · ライン講座の受講登録を取り · 消す | No |
| autophrase240 | 240px / 18px | 2026年度・ · 特別会員向けオンライン講 · 座の受講登録を取り消す | No |
| balance270 | 270px / 18px | 2026年度・特別会員 · 向けオンライン講座の · 受講登録を取り消す | No |
| phrase270action | 270px / 18px | 2026年度・特別会員向け · オンライン講座の · 受講登録を取り消す | No |

Conditional phrase retention produces an improved visual result at 18px; it should NOT be shipped as a blanket rule. In the **36px CSS simulation** at a 320px viewport, `phrase270action` has `scrollWidth=332 > clientWidth=266` and `phrase240` has `260 > 236`. These are actual overflow findings, not theoretical concerns. `phrase270` did not overflow in this particular simulation, but still had an awkward split of 特別会員. The best treatment requires a context- and effective-size-based fallback.

## Execution

`python probe.py`

`python scale_probe.py`

Requires Python Playwright and a local Chromium executable at `/usr/bin/chromium`. The scripts do not access any network or external accounts and do not mutate the KUMIHAN repository.

## Unverified

- Actual installed v0.2.0 native skill/host behavior or production pages.
- Native 200% user text zoom, actual fallback glyphs and all browsers.
- Speech prosody/reader performance; semantic line quality here is human visual judgment.

## Handoff

Issue #121: https://github.com/landco-llc/kumihan/issues/121

QA WORKGROUP branch: control/ja-v020-qa-20261020.

Keep PV-006 `JA-TYPE-004: needs-review` until a bounded solution is verified with screenshots, source preservation, zoom and host behavior. Treat synthetic PV-005 clipped negative separately; do not mark it as a positive pass.
