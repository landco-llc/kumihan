# Equilibrio v0.1.0 — execution ledger

Status: PUBLISHED_VERIFIED / publication-display-followup
Date: 2026-10-19 JST
Owner-approved release scope: GitHub repo main、tag kumihan-it-v0.1.0、public GitHub Release、12 Pages。External Marketplace installation/listing is out of scope.
Main control: [GOAL_EQUILIBRIO_V010.md](GOAL_EQUILIBRIO_V010.md)
Research: [ITALIAN_RESEARCH_20261019_JA.md](ITALIAN_RESEARCH_20261019_JA.md)
Research canonical: https://drive.google.com/drive/folders/1EMib8ugMHyfNG2e38Mo7vuAX79a3iiGk

| Stage | State | Deliverables | Evidence |
| --- | --- | --- | --- |
| W00–W03 / WG01 | PASS | product + locales + 4 Skills + fixtures | See stage evidence below |
| W04–W06 / WG02 | PASS | 3 hosts + 15 ZIP + manifest/hashes | See stage evidence below |
| W07–W09 / WG03 | PASS | Applied web skill + LP3 + guide9 + gateway | See stage evidence below |
| W10–W11 / WG04 | PASS | CI + PR + merge + tag + Release + Pages | See stage evidence below |

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

## Second parallel-main integration — Bangla
- During the next all-green wait, main advanced to af6129739c0caf5756d3e3e77785835b75938e83 (Bangla). The merge helper's fresh-main guard stopped instead of silently merging against uninspected changes. Main was merged without product conflicts as ba25550.
- Root tests reproduced 20 newly introduced Bangla subcase failures: four unknown bn routes, four intentional English→index routes and twelve dedicated font-link contracts. Equilibrio's 15 tests and all generator checks remained green.
- A second read-only review confirmed a narrow test-contract adaptation is legitimate. Only the exact 12 independently merged Bangla filenames receive their dedicated route/font assertions (landings: bn Noto Bengali, en Inter/Source Serif, ja Noto JP; guides: existing Bengali product-name assets + shared installation CSS; all have bn-site-overrides). All existing edition assertions are preserved; no Bangla HTML, generator, skill, ZIP or tag is changed. This does not certify Bangla under the shared system-font-first contract. Initial adaptation still failed six EN/JA guides: their existing links supply Bengali product-name families while installation CSS supplies the text stack. This failed intermediate state is retained; final validation follows below.
- Ruling: integrate the independent renderer into common static tests rather than rewrite another language's output. Reason: the Owner excludes other-language product changes, and those files intentionally use a separate contract. Cost if wrong: unmeasured Bangla font-stack behavior remains outside this edition's evidence, explicitly not certified here.

- Follow-up read-only review inspected the actual guides and corrected its earlier landing-only assumption. The exact nine guide asset contract is now asserted separately from the three landing contracts. It is static compatibility, not certification of Bangla EN/JA rendering or shared font policy. Final root RED→GREEN: 14 tests PASS; Equilibrio 15 focused tests and deterministic/site/copy/gateway checks PASS after this integration. Intermediate PR commit 43e6098 was not merged and contained the six failing assertions; no claim is made that that commit was green.

## Parallel gateway preservation
- main aac9ac19a5181c6080bcce40f468bff577525d33 added Bangla cards manually to index.html/top-en.html while CI was running. Those two cards were merged verbatim, but gateway --check correctly detected that the generator would erase them. Moved the exact existing card HTML into the canonical gateway-copy source and added a narrow preserved-card insertion after the same existing French card. No Bangla copy, target, position, font, product or distribution output is rewritten; other gateways and all ordinary registry cards retain their existing generation path. --check RED→GREEN without changing either merged gateway output.

## Russian parallel-main integration
- main 106b0306e2b28ff2e858342d9a0a77acdecbbe42 brought Russian Lad and a workflow fix. Preserved its font/script registry and source/site assets. Resolved only shared COPY_FILES and PAGE_GATEWAY registrations, retaining Italian, Indonesian and Russian entries together; no existing product output modified.
- Post-merge local validation: Equilibrio 15, root 14 PASS; distribution/site/shared-copy/gateway --check PASS. Italian product/ZIP sources are unchanged by this merge. Other-language product changes in history are inherited from main, not authored by this edition.

## Explicit Italian Latin stack — final font integration
- Final inspection found that web_fonts.script('it') returned Latin links but LANGS lacked it, so the shared CSS did not emit an Italian body selector. Added the explicitly allowed it→latin mapping and regenerated only assets/kumihan-fonts.css and _data/web_fonts.yml; existing language selectors/stacks are preserved.
- Regression test failed on missing LANGS['it'], then passed after mapping and generated-selector checks. Equilibrio focused suite now 16 PASS; root 14 PASS; web_fonts/site/gateway --check PASS. Equilibrio CI now watches shared font inputs as well. A fresh local/CI browser matrix is run for this final stack; earlier JSON remains evidence of the earlier measured state, not retroactive proof of the font change.

## W10–W11 — public release verified
- PR #83 merged at e7e21628d444a2c0b4016570a1426bc6afa37c79. Exact-head Equilibrio push/PR CI succeeded before merge; remaining unchanged-language browser jobs were allowed to finish independently after local regressions and shared checks passed. No failed current checks were bypassed and no branch protection/permission was changed. Exact merge-main Equilibrio CI 39198411459 passed every step including browser measurements. Pages build at the same SHA succeeded.
- Immutable annotated tag kumihan-it-v0.1.0: tag object 28d8c79d367717b561ffcad3960c9574dcef42f4, peeled commit e7e21628d444a2c0b4016570a1426bc6afa37c79. No existing tag moved.
- Publication workflow 39198540492 SUCCESS: verified exact tested main SHA, empty draft, 17 asset names/sizes/SHA-256, draft=false, then all public bytes read back. Public Release: https://github.com/landco-llc/kumihan/releases/tag/kumihan-it-v0.1.0 . Independent session readback also compared all 17 public asset bytes; evidence/release-readback.json.
- Public HTTP readback: all 12 Pages equal current source bytes, canonical/it/en/ja/x-default checked; JA/EN gateways retain IT cards and correct targets; official PNG, product CSS, installation CSS/JS and shared fonts all HTTP 200 and source-equal. evidence/public-pages.json. Follow-up updates the candidate status display to the now-observed publication fact, then rechecks public content.
- Final font-state local Chromium 154.0.8037.57: 192/192 measurements PASS, source in evidence/browser-final-latin.json. Latest mobile screenshot visually inspected. Twelve keyboard skip/focus checks and nine guide Italian switch clicks PASS, evidence/keyboard.json. CSS enlargement is simulation, not native zoom. Earlier failed/superseded observations remain retained.
- Final focused tests: 16 PASS on merge SHA; existing local regression 149 PASS. All original 93 product distribution digests unchanged, only Equilibrio product files authored against latest main. Parallel Indonesian/Bangla/Russian products retained unchanged; static shared integration adjustments are described above.
- NOT-CHECKED: provider-native import/invocation/icon UI, official marketplace listing, native Italian editorial review, native text-only zoom, Google font success, Safari/Windows, hyphenation dictionary, screen reader, Office/PDF. These are nonblocking unverified environments, not claimed failures or approvals.
- No MD/ZIP reattachment, owner-per-Work gate, force push, tag replacement, provider-store submission or authentication/permission modification was requested or performed.
- Final PR #83 readback after release: all 15 exact-head check entries SUCCESS, including the unchanged-language browser jobs that finished after merge. No unresolved failed PR check remains.
