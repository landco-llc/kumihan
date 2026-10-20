# KUMIHAN JA v0.2.0 — 追加受入QA Work群

Workgroup ID: KUMI-JA-V020-QA-20261020-01  
State: QA instructions / NOT shipping approval / NOT implemented by this control commit  
Owner approval scope: 2026-10-20の「OK, 進めて」は追加QAの着手を承認する。main merge・tag・Release・Pages本番・Marketplace申請の承認ではない。

## 0. 対象と原則

- Repository: landco-llc/kumihan
- Target: Draft PR #120, implementation HEAD ce2fd8d23e4afb0816b5870625e02af3aa7a96b8（作成時）。作業開始時に必ず再読する。
- Base main at review: 8b647cc752d7a9bc3db48356fa0ab7b221bb66d6
- Control branch: control/ja-v020-qa-20261020
- QA execution branch recommendation: qa/ja-v020-acceptance-20261020, based on this control branch after reading its new docs. Existing branches must never be overwritten or force-pushed.
- Existing source result: docs/development/ja-v020-20261020/RESULT.md
- Existing observations: docs/development/ja-v020-20261020/case-results.json, evidence/, release-manifest.json
- QA input: QA_OBSERVATIONS.md, QA_MATRIX.json and HOST_SMOKE.md in this directory. Existing research source: docs/development/ja-v020-20261020/WORKGROUP.md and RESEARCH_CASES.md
- Execution: Codex Cloud or Codex app. This control does not run Codex CLI on a remote/local desktop.
- Source-of-truth boundary: this QA confirms the independent source candidate, not the v0.1.8 public Release or live Universal MCP.
- Product shape: 4 Japanese skills across 3 host distribution families (15 ZIPs). JA rule IDs=39, medium profiles=6, report statuses=7; preserve.
- No changes to other languages, existing report schema, live Universal PHP/MCP, general document-generation roadmap, external credentials or unrelated PR branches.

**Do not substitute a source fixture contract, unit test, CSS.supports result, PDF text extraction, or a screenshot of a synthetic page for native-host end-to-end evidence.** Mark out-of-reach checks not-checked (not unsupported, unless incompatibility is actually demonstrated).

## 1. QA Goal

Establish whether v0.2.0 guidance measurably improves real Japanese text composition, avoids unsafe claims, and can be packaged and invoked in intended host workflows. Separate the following independent gates:

- G0 — baseline/provenance/frozen interface preservation.
- G1 — existing static/unit/CI/package integrity.
- G2 — genuine browser/PDF/slide artifact readability and protected text preservation.
- G3 — exact host installation/invocation for each supported distribution target, or precise NOT-CHECKED admission.
- G4 — claims/evidence/release source-versus-published-version integrity.
- G5 — independent review and Owner release decision.

Passing G1 does not imply G2/G3. A release cannot claim an unexecuted native-host/physical/readership capability. Actual P0 semantic/render failures must be corrected or held, not waived by a positive static test.

## 2. W00 — Fresh read and scope freeze

- [ ] Fetch PR #120 HEAD/base, open PRs #101/#116/#118, target docs and all 15 distribution records. Stop on unrelated worktree edits; retain them.
- [ ] Confirm current published Japanese version is 0.1.8 and candidate source version is 0.2.0; the installed Universal MCP is presently observed as ja module 0.1.8 (not a v0.2.0 test).
- [ ] Read references in all four skill entries. Do not treat the common shared copy as a native host installation.
- [ ] Record exact BASE SHA, HEAD SHA, worktree state, Python/Chromium/LibreOffice and host versions, available fonts and permissions in qa/evidence/fresh-read.json.
- [ ] Copy existing case-results only as historical baseline; never overwrite the previous result or rewrite negative observations.

Gate W00: all inputs pinned; unsupported environments explicitly named and non-affected Work continues.

## 3. W01 — Reproduce and correct two visual observations

### QA-V01 / PV-006

Observed in existing evidence/web-320.png, web-1024.png and pdf-page-1.png: the intentionally “good” button example breaks the uninterrupted term 「オンライン」 as 「オ」/「ンライン」. The original screenshot also uses a very short final line 「取り消す」. Existing PV-006 JA-TYPE-004 is needs-review, NOT passed. This is a flaw in the synthetic positive specimen / visual acceptance, **not proof that the KUMIHAN runtime rewrote content**.

- [ ] Reproduce baseline screenshot with the same synthetic input and 240px control.
- [ ] Compare normal wrapping, legitimate local phrase grouping/optional break and a layout-width change at 320/375/768/1024px. Do not normalize, insert spaces or edit the protected Unicode wording.
- [ ] Check textContent codepoint equality, end-of-line/line-start map, click/focus, overflow and 200% effective sizing; separately judge phrase integrity and composition.
- [ ] Correct the fixture or recipe/example only if a narrower bounded fix is demonstrated. Do not add a blanket style that breaks Latin words or hides the button.
- [ ] Save BEFORE/AFTER images and DOM/click/effective-width measurements. PV-006 assisted status stays needs-review until a reasoned semantic review supports the exact observed region.
- [ ] Regression: PV-005 remains a known negative; do not “fix” its failed baseline or relabel its expected negative as passed.

### QA-V02 / source-version panel

Observed in evidence/site-version-panel.png: English no-styles specimen visually displays “v0.1.8Source v0.2.0”; the Jekyll fragment has adjacent closing strong / opening span without a separating text node.

- [ ] Reproduce both fragment-without-CSS and actual built Pages CSS at desktop/mobile, including language toggle where present, and accessibility text extraction.
- [ ] If raw or actual output concatenates versions, repair the source generator/template in the smallest scope, then regenerate. Verify Japanese/English/Traditional Chinese, including no-CSS fallback and screen-reader-friendly separation.
- [ ] Do not silently present unpublished source v0.2.0 as current published version. Keep publication v0.1.8.
- [ ] Save full HTML, source diff, before/after screenshots and visible text comparison.

Gate W01: each finding explicitly FIXED (evidence) / REPRODUCED_UNRESOLVED / NOT-REPRODUCED (environment and explanation). An actual content/visual defect in the positive deliverable cannot be passed merely because a regression test ran.

## 4. W02 — Real Web artifact QA (not synthetic fixture alone)

- [ ] Load the actual v0.2.0 kumihan + kumihan-web skill guidance and capture which files were used.
- [ ] Create a standalone Japanese information/marketing+UI prototype with original protected Unicode text from PV-001, long registration-cancellation button from PV-005/006, Japanese + embedded English, visible mandatory date/place/price, a readable long paragraph, mixed-locale glyph comparison.
- [ ] Positive and deliberately negative example files must be separate. The positive artifact must not have hidden mandatory information, punctuation stranded at line start, single-word splits in compounds where an accepted better local layout exists, or text under decorative shapes.
- [ ] Render in Chromium at 320, 375, 768, 1024, 1440 CSS px and record actual loaded fonts/fallback. Record at least one 200% enlarged view; distinguish native browser text zoom from CSS-only simulation.
- [ ] Test real focus/click/keyboard route for a named UI control, screen-reader/DOM structure only if tools are available and actual output is captured. Never claim a backend function from clicking a static demo.
- [ ] Evaluate normal CSS, user text-spacing overrides (relevant Japanese+Latin features), no-webfont fallback, dark/background contrast if artifact contains it. Keep output text and extracted source sequences for comparing exact code points.
- [ ] Record visual inspection result per viewport and region with screenshot links (no invented machine vision quality score).

Gate W02: no unresolved actual P0 clipping or protected-value change in the positive Web artifact; visual acceptance and browser interaction on attempted states documented separately.

## 5. W03 — Document/PDF and presentation artifact QA

- [ ] Load candidate kumihan-documents. Create a realistic Japanese paginated report, at least 4 pages, including heading hierarchy, body/note, a table crossing pages, supplementary legend, protected values and Japanese/Latin mixed content.
- [ ] Create a genuine PPTX candidate, at least 8 slides with title, text+diagram, dense comparison, chart/values, caution callout, long caption, note, and summary. Include a slide with a complex shape/text relationship similar to past failure where text was behind shapes (not a contrived negative in the accepted deliverable).
- [ ] Render all PDF pages and ALL slides to images; manually inspect each, not a single sample. Report clipping, overlap/occlusion, line-head punctuation, semantic breaks, alignment, title versus body role, mandatory data visibility, missing glyphs and reading order.
- [ ] Check exact protected Unicode input against extractable content where supported; this is a static extraction result, not itself visual acceptance.
- [ ] Audit page splitting / table headers / footnote continuity. For slide decks, PPTX structural inspection + rendered images + text extraction; PDF export does not prove native MS Office behavior.
- [ ] Save actual PPTX, PDF, input source, render pages and a per-page/per-slide audit grid under qa/evidence/ (or bounded artifact link with digest).

Gate W03: positive report and slide deliverables inspected end to end; native Office still not-checked without native Office.

## 6. W04 — Actual native host acceptance, not simulation

See HOST_SMOKE.md. A Codex Cloud reading SKILL.md is not a ChatGPT, Claude or Gemini native host install. For each target host where approved test access exists:
- [ ] Install the exact candidate full plugin/extension ZIP or prescribed 4-skill form, record host app/version, user-provided test workspace, filename and SHA-256; no official public submission.
- [ ] Invoke each of four Japanese skills with deterministic test prompts and record raw outputs/commands/captures; assert route and read-only review semantics.
- [ ] Confirm the original special-name / decomposed Unicode / numeric source is unchanged. Distinguish exact text and visual/PPTX output.
- [ ] If host cannot be accessed from Cloud, prepare the human-run evidence request in HOST_SMOKE.md and mark NOT-CHECKED / ACCESS_NEEDED. Do not substitute the currently connected KUMIHAN Universal ja 0.1.8 for candidate 0.2.0.
- [ ] No credential sharing or public marketplace submission.

Gate W04: per-host actual evidence, or a precise named blocker; public claims exclude unverified pathways.

## 7. W05 — Risk-based 30-case closure

- [ ] Preserve historical 11 partially-run /19 not-run and add a separate new QA results file, with evidence of genuine new executions only.
- [ ] Prioritize PV-006 meaning and line breaks; PV-003/004 locale glyph and font; PV-010/012 mandatory-info accessibility; PV-016/017 spacing; PV-019 vertical scroll axis; PV-020 native zoom; PV-021/022 resolved palt; PV-027/028 paginated PDF/native distinction; PV-030 colloquial condition and context.
- [ ] For PV-023/024 real projection, PV-025/026 physical sign and reader-performance studies, do not invent equipment/participants. Explicitly declare whether v0.2.0 claims them; if no, retain limitation and out-of-scope release text.
- [ ] Record statuses only for exact rule/scope/method/environment; document expected vs observed separately. No blanket declaration that all 30 cases passed.
- [ ] Use QA_MATRIX.json for nonnegotiable core checks; failed real positive artifact prevents release recommendation until corrected.

Gate W05: no unresolved P0 actual failures in supported claimed delivery scope; every unexecuted scenario retains visible limitation and requested owner/human equipment decision.

## 8. W06 — Production safety and packaging consistency

- [ ] Re-run the full current test and deterministic build pipeline on FINAL implementation HEAD: python -m unittest discover -s tests -v; python tools/check_ja_type_011_cases.py; python tools/build_dist.py --check; python tools/build_seo.py --check; python tools/check_seo_preservation.py; git diff --check.
- [ ] Rebuild 15 ZIPs twice, compare byte-for-byte; validate path, CRC, archive member inventory, bytes and SHA-256 against a generated new manifest. Check 4 entry inventory files and the correct host/plugin layouts.
- [ ] Check all 20 non-JA editions and source manifests/archives remain byte-identical; JA 39 rule IDs, six profiles, seven report statuses and existing schema remain unmodified. Record any differences and seek decision rather than silently absorb them.
- [ ] Verify current public version still v0.1.8 in factual registry; source candidate v0.2.0 is clearly labelled. Independently inspect built-site user-visible version panel, no raw string concatenation, install links.
- [ ] Require latest PR-head GitHub Actions and full SEO/Pages build PASS, with run URLs. Existing old CI is not evidence for a newly edited HEAD.
- [ ] Keep Universal PHP/MCP, #101/#116/#118 out of this PR. Send only a version/registry handoff after Owner release decision.

Gate W06: exact final HEAD/TREE, immutable old Releases, no release/merge.

## 9. W07 — Independent review and minimal fixes

- [ ] Assign a separate read-only QA reviewer to compare requirement vs evidence on the latest branch.
- [ ] Triage each finding as source code, recipe/guidance, sample artifact, host environment or inconclusive. Include image refs and reproducible minimal input.
- [ ] Fix bounded issues on the QA branch only, not direct main; rerun impacted QA and global regressions. Never turn a missing native-host test into unsupported or passed.
- [ ] Prepare Draft stacked PR against feature branch feat/ja-v020-research-20261020, referencing original #120 and Issue #119. No auto-merge, no tag/Release.
- [ ] Capture review results and explicit remaining limitations; do not inherit earlier CI success if code changes.

## 10. W08 — Closeout / Owner Gate

Write docs/development/ja-v020-20261020/qa/RESULT.md containing:

1. Latest HEAD/TREE, original/final commits, changed path list and why.
2. W00–W07 execution table: attempted, passed, failed, blocked, not checked.
3. Before/after screenshots and all output artifacts, with page/slide audit grid and real browser sizes.
4. Existing 30-case baseline versus newly observed results (do not overwrite original), with PV-006 semantic outcome.
5. Per-host actual invocation and package identity or human-action-needed.
6. Final 15 ZIP sizes/hashes, CI run links, published/source split and non-JA preservation.
7. Blockers ranked P0/P1/P2, explicit risk/acceptance scope, next recommendation.
8. Statement: NO main merge, v0.2.0 Git tag, public Release, Pages production deployment or Marketplace submission.

One final issue report to the assigned QA Issue and Issue #119 with Draft PR link. Stop at Owner Gate; the Owner later chooses release scope or further work.

## 11. Failure-mode policy / fail closed only where needed

- Actual protected field altered, mandatory text truly occluded, invalid source ZIP, broken schema, unauthorized unrelated changes: BLOCKED within affected work and no release recommendation.
- A synthetic negative fixture fails visually as designed: EXPECTED NEGATIVE; not a product defect and never called a passed artifact.
- Semantic break in synthetic positive: action item until corrected/qualified, not inferred product-code corruption.
- Inaccessible native environment: NOT-CHECKED/ACCESS_NEEDED; continue independent work. Do not invent runtime observations.
- Exception/waiver: only if prior applicable policy authorizes it; QA reviewer alone cannot waive release Owner Gate.
- If a dependency is inaccessible, continue W02/W03/W05/W06 and report exact blocker. Avoid repeated approval requests between Work steps.

This instruction is an execution plan. Its presence in Git does not mean new tests ran or defects were repaired.
