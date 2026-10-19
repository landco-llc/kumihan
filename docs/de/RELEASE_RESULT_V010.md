# KUMIHAN｜Satzbild public release result

Status: **PUBLISHED_VERIFIED**. Verified 2026-10-19 UTC. Owner authorization: Issue #75 and GOAL_SATZBILD_V010.md. W00–W11 complete.

## Immutable source and publication

| Evidence | Result |
| --- | --- |
| Implementation / tag SHA | `fd380a61823017f921bcdf09724fcd6c1c232ff6` |
| Public site source SHA | `fef8dca1d9829b8c63c24e2ed900d97303bc6299` |
| Implementation PR | https://github.com/landco-llc/kumihan/pull/77 — merged, all 13 checks green |
| Published-copy PR | https://github.com/landco-llc/kumihan/pull/78 — merged, both checks green |
| Tag | `kumihan-de-v0.1.0`, never moved |
| Public Release | https://github.com/landco-llc/kumihan/releases/tag/kumihan-de-v0.1.0 — draft=false, 17 assets |
| Main implementation CI | https://github.com/landco-llc/kumihan/actions/runs/39190834291 — success |
| Published-copy main CI | https://github.com/landco-llc/kumihan/actions/runs/39191180565 — success |
| Publisher / download readback | https://github.com/landco-llc/kumihan/actions/runs/39190944159 — success |
| Final site Jekyll / Pages deployment | https://github.com/landco-llc/kumihan/actions/runs/39191179674 — success |

## Acceptance receipt

| Scope | Result / evidence |
| --- | --- |
| Four skills | passed: independent local references, schemas, rules, profiles, locale settings and official PNG |
| Three host families, five packages each | static adapter identity/path/metadata checks passed; native invocation and host UI not-checked |
| Official icon | SHA-256 matched canonical master; bundled in every skill/archive; native display not-checked |
| DE/EN metadata | descriptions, exact display name KUMIHAN｜Satzbild, L&Co. LLC, 0.1.0 verified |
| Installation paths | plugin helper paths and standalone roots verified; guides distinguish local skills, plugins/extensions and account-dependent chat features |
| Fifteen ZIPs / manifest | deterministic regeneration, no-write check, safe members, CRC, inventories, size and SHA-256 passed |
| Research 44 / 48 | 44 guidance candidates registered, one bounded CSS candidate rule; 48 proposed cases retain their separate not-checked ledger; not represented as all passed |
| Content / locale | original bytes retained; explicit de-DE/de-AT/de-CH; currency/timezone/du/Sie/house style independent; normalization and unauthorized edits rejected by comparison |
| Existing regression | 128 existing tests passed; existing Japanese/other-language package bytes unchanged |
| Focused suite | 22 tests passed; includes 20 representative preserved strings across three locales and unauthorized mutation comparisons |
| Site | canonical 8-section layout and shared install frame; base_copy JA/EN and all generation checks passed |
| Browser | final published copy 192/192 passed: 12 pages × 4 widths × 2 computed text sizes × 2 spacing conditions; 6 additional keyboard/long-label checks passed |
| Public URLs | 12 pages exact body bytes, DE gateway and 5 shared CSS/JS/logo resources verified; see PUBLIC_VERIFICATION.json |

## Public pages

- https://landco-llc.github.io/kumihan/kumihan-de.html — HTTP 200, source bytes matched
- https://landco-llc.github.io/kumihan/kumihan-de.en.html — HTTP 200, source bytes matched
- https://landco-llc.github.io/kumihan/kumihan-de.ja.html — HTTP 200, source bytes matched
- https://landco-llc.github.io/kumihan/docs/install-satzbild-chatgpt.html — HTTP 200, source bytes matched
- https://landco-llc.github.io/kumihan/docs/install-satzbild-chatgpt.en.html — HTTP 200, source bytes matched
- https://landco-llc.github.io/kumihan/docs/install-satzbild-chatgpt.ja.html — HTTP 200, source bytes matched
- https://landco-llc.github.io/kumihan/docs/install-satzbild-claude.html — HTTP 200, source bytes matched
- https://landco-llc.github.io/kumihan/docs/install-satzbild-claude.en.html — HTTP 200, source bytes matched
- https://landco-llc.github.io/kumihan/docs/install-satzbild-claude.ja.html — HTTP 200, source bytes matched
- https://landco-llc.github.io/kumihan/docs/install-satzbild-gemini.html — HTTP 200, source bytes matched
- https://landco-llc.github.io/kumihan/docs/install-satzbild-gemini.en.html — HTTP 200, source bytes matched
- https://landco-llc.github.io/kumihan/docs/install-satzbild-gemini.ja.html — HTTP 200, source bytes matched

## Distribution verification

All 17 public assets were independently downloaded, then compared byte-for-byte with committed files. The publication workflow also verified GitHub size/digest metadata and downloaded all assets after draft=false. `SHA256SUMS.txt` covers the 15 ZIPs plus MANIFEST.json; it excludes its own digest. Complete stable URLs, sizes and SHA-256 values are in [PUBLIC_VERIFICATION.json](PUBLIC_VERIFICATION.json). Reproduce using `python tools/verify_satzbild_public.py` from the repository checkout matching the live site.

MANIFEST.json SHA-256: `aaad69624c88050f5380a1f78418177cd6d0aab4b4eeab68bc3f33789a6b1ec1`.

## Scope limits

Native ChatGPT/Codex, Claude and Gemini import/invocation/icon display, provider marketplace listing, native German proofreading, Office/PDF, screen readers, Safari/Windows fonts, native text zoom and online web-font download remain not-checked. Adapter fields were statically checked against repository host structures; no claim of complete native-host schema execution. Browser evidence uses Chromium with external fonts blocked and computed element sizes doubled; this is CSS simulation, distinct from native zoom. CLDR49 research references and observed Node24/ICU78.3/CLDR48 output remain separate. Private Drive originals and paid DIN5008 text were not read.

## Existing-file changes

Only intended common integration changed: base_copy adds DE, gateway source/output adds DE cards/pagination, web_fonts adds de to the existing Latin selector plus generated output, and layout-parity tests cover DE. Existing product directories, distributions and release tags were not changed. Full execution/design receipts: [EXECUTION_LEDGER.md](EXECUTION_LEDGER.md), [DESIGN_APPLICATION_RECEIPT.md](DESIGN_APPLICATION_RECEIPT.md), [QA_browser.json](QA_browser.json), [QA_interaction.json](QA_interaction.json), [INTL_RUNTIME_OBSERVATIONS.json](INTL_RUNTIME_OBSERVATIONS.json).
