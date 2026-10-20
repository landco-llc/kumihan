# QA-V02 — FIXED within JA candidate version panels

Scope: local genuine Jekyll 3.10.0 built `kumihan.html`, Chromium 154.0.8037.57; 320 and 1024 CSS px, Japanese / English / Traditional Chinese language toggle. Local build and screenshot capture, not a deployed Pages test or native screen reader test.

## Root cause and bounded correction

`tools/version_display.py:panel` placed `</strong><span>` and successive metadata spans adjacent without text nodes. The actual site's flex gap already visually separated the styled labels: no styled production-layout concatenation was reproduced. Removing CSS and extracting raw text reproduced `Current Version v0.1.8Source v0.2.0` in both widths; Japanese/Chinese had the same missing separator boundary.

Added a literal ASCII space before following metadata spans **only when edition is `ja`**. The shared source generator and the three generated JA fragments changed. Current publication remains v0.1.8; candidate source stays v0.2.0. No dependency, other-language output, release registry or publication change.

Regression test `JapaneseVersionSeparation` first produced nine failing locale/slot subtests (`version-red.log`), then all 16 edition-version tests passed (`version-green.log`). This checks raw extraction separation independently of visual CSS. `version/non-ja-renderer-preservation.json` records 180 byte-identical old/new renderer comparisons across 20 non-JA editions × 3 locales × 3 slots.

## Genuine built-site evidence

Portable Ruby 3.3.6 from ruby/ruby-builder was used outside the repository. Both baseline and corrected JA fragments were independently built through the repository Gemfile using Jekyll 3.10.0 / Liquid 4.0.4 (`version/jekyll-before.log`, `jekyll-after.log`). Corrected built HTML passed `tools/check_seo.py --site-dir /tmp/kumihan-version-site-after`: 274 pages. Temporary Ruby, gems, Bundler configuration and servers are not deliverables; Gemfile.lock bytes were restored exactly.

`tools/qa_version_capture.py` captures actual local served build: real language-button clicks, pressed state, actual `html[lang]`, full rendered HTML, full-page screenshots, focused styled and no-CSS panel screenshots, Chromium accessibility snapshots and raw DOM text. CSS-disabled screenshots explicitly hide inactive locale wrappers for focused fallback inspection; this is stated in the script and is not a claim that CSS-off language switching works. All three locale toggle states matched requested lang and `aria-pressed=true` in both widths. Two visible version panels (hero/install) were extracted per state.

Before raw English hero: `Current Version v0.1.8Source v0.2.0`.
After raw English hero: `Current Version v0.1.8 Source v0.2.0`.

All six after raw hero states include a separating space. Styled before/after panels remain visually separate, contained and readable at the two tested widths. Manual inspection of `version/contact-styled.png` and `version/contact-no-css.png` covers every locale/width before/after panel. Full-page captures preserve the context; scope acceptance is the version panel, not an audit of unrelated editorial content. Accessibility snapshots are browser accessibility-tree observations; no native screen reader or speech-prosody claim.

## Artifacts

- `version/{before,after}-measurements.json`: exact DOM text/HTML, visible panel dimensions, locale/toggle observations.
- `version/{before,after}-{ja,en,zh-Hant-TW}-{320,1024}-{styled,no-css,page}.png`: before/after images.
- Matching `.html` and `-accessibility.yml`: complete built markup and browser accessibility tree.
- `version/manifest.json`: artifact byte sizes and SHA-256.

No remaining observed P1 QA-V02 issue in the tested JA version panels. Published/deployed site, native accessibility clients and other browser engines remain not-checked. No Pages publication was performed.
