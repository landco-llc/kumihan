# Equilibrio v0.1.0 — execution ledger

Status: IN_PROGRESS / WG03_COMPLETE
Date: 2026-10-19 JST
Owner-approved release scope: GitHub repo main、tag kumihan-it-v0.1.0、public GitHub Release、12 Pages。External Marketplace installation/listing is out of scope.
Main control: [GOAL_EQUILIBRIO_V010.md](GOAL_EQUILIBRIO_V010.md)
Research: [ITALIAN_RESEARCH_20261019_JA.md](ITALIAN_RESEARCH_20261019_JA.md)
Research canonical: https://drive.google.com/drive/folders/1EMib8ugMHyfNG2e38Mo7vuAX79a3iiGk

| Stage | State | Deliverables | Evidence |
| --- | --- | --- | --- |
| W00–W03 / WG01 | PASS | product + locales + 4 Skills + fixtures | none |
| W04–W06 / WG02 | PASS | 3 hosts + 15 ZIP + manifest/hashes | none |
| W07–W09 / WG03 | PASS | Applied web skill + LP3 + guide9 + gateway | none |
| W10–W11 / WG04 | IN_PROGRESS | CI + PR + merge + tag + Release + Pages | none |

- 40 rules and 48 evaluation cases are research candidates; the status of all cases begins as NOT_CHECKED.
- Only completed and evidence-backed work can be marked PASS or PUBLISHED_VERIFIED.
- Update this file cumulatively at each stage; do not request manual reattachment of spec/ZIP for handoff.

## W00–W06 — 2026-10-19 JST
- Fresh read: main a588f07; master, WG01–WG04 and complete Italian research snapshot read. No AGENTS.md found. Existing PR #76 already closed; open #72 Russian edition is outside this scope. No existing Italian product/tag/release found in main/release list. Work branch feat/equilibrio-v0.1.0 tracks latest main; no existing edits overwritten.
- Read canonical layouts and generators; compared French/Spanish/German/Polish edition patterns. Reused the bounded deterministic German packaging infrastructure, authored Italian guidance and research extraction independently; no German linguistic rules used.
- Product: plugins/kumihan-equilibrio; four independent entrypoints and generated standalone skills; it-IT/it-CH locales, six medium profiles, separate house style/source policy/content role/voice/audience/evidence. Unknown locale stays unknown; baseline it-IT is an explicit selection, not inference.
- 40 research rules registered with scope/context/severity/expected/source_refs/status. 48 candidate fixtures registered with initial not-checked states; no full fixture PASS is claimed. All 40 are guidance; R21 additionally reports bounded CSS patterns as needs-review. Grammar and semantic decisions need context; dictionaries/native hosts remain not-checked.
- Red→green: initial 10 tests failed for absent implementation, then passed. Missing-reference regression failed before closure rejection was added. Final 12 focused tests PASS, including 21 preservation strings × 2 locales, six mutation counterexamples, CLI read-only, deterministic 15 ZIP matrix, inventories, CRC, safe paths, symlink rejection, missing references and --check nonwriting. Commands: python -m unittest discover -s tests/equilibrio -v; python tools/build_equilibrio.py --check.
- Distribution: 15 ZIP + MANIFEST.json + SHA256SUMS.txt, fixed 2026-10-19 timestamp/permissions, official PNG digest 1d1ae2cb4f7f69f7b5f54b050ff8c6fb2c315b75ded8003f8b605855d633f96e, member summaries and reference closure. Source and descriptions Italian | English; author L&Co. LLC. Native import/icon/store: NOT-CHECKED.
- Interface preflight: WG01 source resources → WG02 closed archives → WG03 actual filenames → WG04 immutable release assets; filenames aligned with existing host suffixes. Ruling: preserve all proposed research fixture states separately from focused subproperty tests, because byte-preservation tests alone do not validate grammar/rendering. Cost if wrong: unmeasured language judgments remain explicitly unavailable.

## W07–W10 — implementation and local validation
- Completed Skill read/application receipt precedes site generation. Canonical product_site.canonical_css and install_frame reused: 3 LP + 9 guides, real release filenames, Italian/English/Japanese alternates and canonical URLs. IT card added from gateway-copy source; 12 gateway outputs regenerated, existing card dimensions and content retained.
- Browser evidence: docs/it/evidence/{browser-initial,browser-final,intl}.json and two screenshots. 192 final measurements PASS in Chromium 154.0.8037.57; fallback only, CSS 200% simulation, native zoom NOT-CHECKED. Initial transient one-failure observation retained; diagnostic and repeat were green, stabilized final matrix green. Focus/Tab/Enter and accent/quote specimens inspected.
- Node v24.19.0 / ICU 78.3 / CLDR 48.0: typed it-IT/it-CH output observed, independent from institutional rules. No ambiguous strings parsed. Python 3.12.14.
- Existing regression: root suite 14 PASS; Satzbild 22; Szyk 7; Grafía 13; Accord 26; Ziheng 26; Zilu 10; Geuljjaim 9; Thai 22. Existing Japanese build_dist --check, German distribution/site, shared copy and gateway --check PASS. All 93 existing product distribution files retain byte digests; no existing language product changed.
- Lightweight fresh subagent review (requesting-code-review) found Important wrong Italian switch label “Deutsch”; fixed with RED→GREEN test and regenerated all guides. Minor generator docstring corrected. Additional footer-link regression RED→GREEN. No remaining Important/Critical findings. No paid security scan or extra owner gate introduced.
- Equilibrio focused suite now 15 tests (12 product/distribution + 3 site); final full rerun PASS (15 tests, 7.988s), all four generators/checks PASS before commit. Added focused CI and immutable-tag draft→digest-check→public→download-readback publish workflow. Main integration and release still pending; no publication success claimed.

## Parallel-main integration — 2026-10-19 JST
- All 15 PR #83 checks succeeded on a1ac61a54edad999496be59dfbca52afec126c14. Merge attempt detected a fresh conflicting main update: 34988d8068e7b1109330771ced1a19a11e2c4fad (Indonesian Laras). No force push or overwrite attempted.
- Merged main into the implementation branch, retaining both it/equilibrio and id/laras registry entries. New Indonesian pages exposed four KeyError:id errors in the existing global gateway test. Added only id=index.html to the shared test mapping, matching those untouched pages; this is a test registry integration fix, not a Laras product change. Shared copy, Equilibrio site and gateway --check remained green.
- Current official host documentation read from anthropics/claude-code plugins/README.md (plugin root .claude-plugin/plugin.json + skills/) and google-gemini/gemini-cli docs/extensions/reference.md (root manifest name/version/context and local-folder installation). Static archive structure matches those documented paths; native install is still not-checked. Existing Codex adapter format retained from reviewed current repository editions.
