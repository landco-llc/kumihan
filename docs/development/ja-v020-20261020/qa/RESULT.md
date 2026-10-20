# JA v0.2.0 additional acceptance QA — Owner Gate

Management: #121 / original #119 / Draft candidate #120. QA branch `qa/ja-v020-acceptance-20261020`, stacked against `feat/ja-v020-research-20261020`. This is source-guided acceptance evidence, not a native-host certification or shipping approval.

## Scope state

| Scope | State | Evidence / practical limit |
| --- | --- | --- |
| QA-V01 synthetic positive correction | VERIFIED | Original オ／ンライン reproduced. Fixture + generating script corrected locally; exact label, 4 widths × 18/36px CSS, focus/fit and assisted meaning reviewed. [before/after](evidence/v01-comparisons.jpg), [Web result](evidence/web-result.md). Native user zoom untested. |
| QA-V02 JA version panels | VERIFIED | Literal separator fixes no-CSS/raw text in ja/en/zh. Actual styled baseline already visually separated; no deployed-site defect inferred. Real Jekyll before/after,320/1024, toggle and browser AX captured. [version result](evidence/version-result.md). |
| Actual Web artifact | VERIFIED for observed Chromium states | 5 widths320/375/768/1024/1440 × normal/CSS200/spacing/serif fallback. Exact protected fields, keyboard/local demo action, measured fonts/overflow, all20 images inspected. No registration backend, speech reader or all-browser claim. |
| Actual report PDF | VERIFIED for observed preview and extraction | Six A4 pages, repeated table headers across pages2–5,44 fictional rows/final note; all six images inspected; exact protected extraction. [audit grid](evidence/documents-result.md). |
| Saved eight-slide PPTX + LO preview | PARTIALLY_VERIFIED | Saved XML exact and all eight preview images inspected. **P1 FAILED: LibreOffice-export PDF exact extraction adds spaces**. Native Microsoft Office/editability not-checked. No global G2 exact-export PASS. |
| Static/build/package/SEO | VERIFIED locally; final CI see linked PR | 97 unit +29 SEO tests,10/10 required local commands, real Jekyll build,274 built pages /272 sitemap URLs. 15 ZIP CRC/hash/path and two rebuilds identical. [checks](evidence/final-checks.json). |
| Native AI hosts / native zoom / native Office / physical / readership | NOT-CHECKED / ACCESS_NEEDED | 0/12 actual host-skill invocations. [per-host packet](evidence/native-host-results.json), [operator protocol](HOST_SMOKE.md). No simulated PASS or incompatibility declaration. |

## Provenance and changed paths

Fresh Read main/base: `8b647cc752d7a9bc3db48356fa0ab7b221bb66d6`; original candidate HEAD `ce2fd8d23e4afb0816b5870625e02af3aa7a96b8`, TREE `0a654d87b38d036b2f7401e1de507696af8b1ba8`. Original PR HEAD did not move. Control branch fetched fresh; its SHA/TREE, concurrent #101/#116/#118 identities, environment/fonts, clean initial worktree and input digests are in [fresh-read.json](evidence/fresh-read.json).

Exact tested implementation HEAD/TREE is recorded in `revision.json` when the implementation commit is frozen. The final reporting commit cannot embed its own hash; the final Issue #121/#119 reports and Draft PR identify the actual final HEAD/TREE. Reporting-only additions are separated from tested implementation. Final CI must match that actual final PR HEAD; an older green run is not substituted.

Bounded production-source changes: `tools/version_display.py` + three JA generated fragments separate labels; synthetic fixture + `tools/render_ja_v020_research.py` retain the visual correction. `_config.yml` and `tools/seo_inventory.py` exclude `docs/development/` consistently from built Pages and source sitemap discovery so standalone QA HTML is not misclassified as public content. Existing SEO discovery still detects new public directories; regression red/green is retained. `.github/workflows/ja-acceptance-qa.yml` adds read-only unit/distribution/SEO/Jekyll CI for the stacked feature-base PR; no deploy/release step. New `tools/qa_*` scripts reproduce bounded evidence. QA reports and actual outputs are isolated below this directory. [changed paths](changed-paths.txt).

All2,627 protected baseline paths (JA skills/shared references/inventories/manifests/archives/registry and all20 non-JA editions) remain byte-identical. Frozen39 rule IDs,6 profiles,7 statuses and schema bytes unchanged. [preservation and two rebuilds](evidence/reproducibility-preservation.json). Historical research RESULT/case-results/release-manifest and negative evidence unchanged. The shared source transition record was not refreshed or weakened. Public v0.1.8 Release remains current; source candidate v0.2.0 stays unpublished. Universal MCP production and unrelated PR branches untouched.

## W00–W08 execution

| Work | Actual execution / result | Remaining limit |
| --- | --- | --- |
| W00 | Fresh inputs, PR/main/concurrent identities and15 archive identities pinned; actual four candidate entries/relevant references read | Cloud source reads are not native installation |
| W01 | Both visual observations reproduced and bounded corrections verified; original negative fixtures preserved | Native host and user zoom not-checked |
| W02 | Actual fictional Japanese information/UI prototype,20 rendered states,fonts/DOM/AX/focus/Enter/local status/contrast | Browser AX is not screen-reader speech; regional glyph reference not supplied |
| W03 | Actual6-page PDF and8-slide editable PPTX; all14 raster images audited; slide3 pseudo-column issue locally corrected with before/after | P1 LO PDF extraction mismatch; native Office/projection unverified |
| W04 | Three package identities and12 host-skill rows prepared; deterministic operator prompts available | ACCESS_NEEDED: private authorized host install/discovery/invocation and captures |
| W05 | [all30 original-status differences](case-differences.md), [machine-readable records](case-results.json); no historical overwrite |15 partially-run /15 not-run original scenarios; no whole-case pass |
| W06 | All required local tests/builds/checks,15 hashes/CRC/member inventories/two deterministic rebuilds; non-JA/frozen preservation | PR final-HEAD CI recorded externally and in result issue |
| W07 | Separate read-only reviewer sampled real output and audited claims/source/preservation; taxonomy corrections adopted | [independent review](evidence/independent-review.md); no release waiver |
| W08 | Draft stacked PR + this RESULT + evidence and final reports to #121/#119 | Owner Gate remains closed |

## Artifacts and evidence

- Web: [positive](evidence/web-positive.html), [separate negative](evidence/web-negative.html), [measurements](evidence/web-observations.json), [AX tree](evidence/web-accessibility-tree.json), [all-state audit/links](evidence/web-result.md). Before/after V01 four viewport pairs and CSS200 are retained beside these files.
- Report: [source](evidence/documents/report.html), [PDF](evidence/documents/report.pdf), all report-01…06.png in [page audit grid](evidence/documents-result.md).
- Slides: [PPTX](evidence/documents/presentation.pptx), [LO export PDF](evidence/documents/presentation.pdf), all presentation-01…08.png, source inputs/notes/extraction and before/after slide3 in the [slide audit grid](evidence/documents-result.md).
- Version: real built HTML, before/after full-page/panel/no-CSS images and browser accessibility observations for all locale/width combinations; [manifest](evidence/version/manifest.json), [result](evidence/version-result.md).
- Focused: [vertical scroll/palt/context diagnostics](evidence/focused/inspection.md), with exact font file hash, GPOS support, used-font identity and measured width difference. These do not retroactively execute a distinct syntax-only original condition.

## Original30-case delta

Baseline11 partially-run /19 not-run remains immutable. Additional bounded original-scenario observations advance PV-004,019,022,030 to partially-run: now15 partially-run /15 not-run, **zero full-case certifications**. Supplemental prototype scopes for PV-003/010/012/016/017/018/020/027/028 are explicitly distinguished from the original conditions/inputs. In particular the new correct-date Web does not execute PV-012's contradictory-date negative, nor PV-010's decorative-crop condition. Original PV-005/011/027 failed negatives remain failed. PV-006 JA-TYPE-004 now has an assisted pass only for the exact corrected regions; native zoom/host remains not-checked. PV-021 original syntax-only effect stays not-checked; actual resolved-font comparison is PV-022. Projection/sign/reader cases remain not-checked without fabricated participants or equipment.

## Final archives (unpublished source candidates)

Each path below was read independently; safe unique member paths, CRC, byte size and SHA-256 matched the historical manifest, then matched both new builds. [Full member inventories](evidence/archive-verification.json).

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `downloads Claude/plugins/kumihan-Claude-Code-plugin-0.2.0.zip` | 509143 | `78eb29f367d9c0014709825a6f45f496e75930db77fc4b2198590092a2edeba1` |
| `downloads Claude/skills/kumihan-Claude-skill-0.2.0.zip` | 124375 | `44d87e11078c48de44eea2d18aacdef74ba67620bab6b23adbe4592b031c76ca` |
| `downloads Claude/skills/kumihan-documents-Claude-skill-0.2.0.zip` | 124694 | `d09b422f8f149fffd51c1e79f3ef3050ec7d5604f99fdaf9e9dcbe0d78a68242` |
| `downloads Claude/skills/kumihan-review-Claude-skill-0.2.0.zip` | 124674 | `d292651bb180d688b5328857607ca34f6f05f31b005f76634b9cb95f301a5d69` |
| `downloads Claude/skills/kumihan-web-Claude-skill-0.2.0.zip` | 124727 | `858c6eea185817a4ac228087ea88efd06d8d9428a6fe2ad0f19e0954b792e3c6` |
| `downloads GPT-Codex/plugins/kumihan-GPT-Codex-plugin-0.2.0.zip` | 1309156 | `1f8b2aaa943cd619dd9b3ffa918fc144f3c76d08c097472a2e9c372bcc1564f2` |
| `downloads GPT-Codex/skills/kumihan-GPT-Codex-skill-0.2.0.zip` | 124375 | `44d87e11078c48de44eea2d18aacdef74ba67620bab6b23adbe4592b031c76ca` |
| `downloads GPT-Codex/skills/kumihan-documents-GPT-Codex-skill-0.2.0.zip` | 124694 | `d09b422f8f149fffd51c1e79f3ef3050ec7d5604f99fdaf9e9dcbe0d78a68242` |
| `downloads GPT-Codex/skills/kumihan-review-GPT-Codex-skill-0.2.0.zip` | 124674 | `d292651bb180d688b5328857607ca34f6f05f31b005f76634b9cb95f301a5d69` |
| `downloads GPT-Codex/skills/kumihan-web-GPT-Codex-skill-0.2.0.zip` | 124727 | `858c6eea185817a4ac228087ea88efd06d8d9428a6fe2ad0f19e0954b792e3c6` |
| `downloads Gemini/extensions/kumihan-Gemini-CLI-extension-0.2.0.zip` | 506683 | `db68ec074cc45fecb48b1748f2048ab4f9a3ea73fcdbc362aafd353cd037cd3a` |
| `downloads Gemini/skills/kumihan-Gemini-Apps-skill-0.2.0.zip` | 123799 | `067236ccd6b23ce97e50651a4bf4ee29cac8fa22de4b1240cf4df37845a58de8` |
| `downloads Gemini/skills/kumihan-documents-Gemini-Apps-skill-0.2.0.zip` | 123398 | `a0997a0f216fcecfefc0520f557240ae03c09d2f298c883e65d984e24969fc0d` |
| `downloads Gemini/skills/kumihan-review-Gemini-Apps-skill-0.2.0.zip` | 123594 | `f36b62bdbdc76330dc6e8a72602fee1b7937c82eed99a07b3decfd3492526231` |
| `downloads Gemini/skills/kumihan-web-Gemini-Apps-skill-0.2.0.zip` | 123863 | `3a07dd00511cfaf1b6c9ca15ea6fc83007a4db52862404c209167583bfe943cc` |

## Failures, access needed and Owner Gate

- **P0:** no unresolved observed positive clipping, mandatory-field occlusion, protected PPTX/source mutation, schema/package failure in the tested scopes. Historical deliberate failures remain visible.
- **P1:** LibreOfficeDev26.8 PDF copy/extraction fidelity failed: spaces inserted in protected strings. Saved PPTX XML and report PDF remain exact. Hold any claim of exact text fidelity for this converter output until corrected or separately scoped by Owner; do not normalize to pass. No source-package corruption established.
- **P1 acceptance gaps:** actual private ChatGPT/Codex, Claude/Claude Code and Gemini/Gemini CLI installation/discovery/four invocations each; native Microsoft Office; real user enlargement mechanism. An authorized operator must use the exact ZIP hashes and HOST_SMOKE prompts and return raw captures/version/workspace information. No credentials should be pasted. These pathways remain NOT-CHECKED, not unsupported or accepted.
- **P2 limits:** independently referenced regional glyph correctness, other engines, actual screen-reader speech, physical print/sign/projection and reader-performance experiments. These are not claimed by this evidence.

Independent review found no additional source P0/P1 after the bounded fixes. Local build-seo initially failed because new QA HTML was discovered as public; failure log is retained under pre-final-check-05.log. Source inventory and Jekyll exclusion were aligned; failing regression and corrected run retained; all latest local commands pass. Any future change invalidates affected checks and requires current-head CI.

Owner must review the exact final PR/CI and artifacts, resolve or explicitly narrow the failed converter-fidelity scope, decide native-host evidence/release scope and separately authorize publication. **NO main merge, v0.2.0 Git tag, public Release, Pages production deployment or Marketplace submission.** This QA stops at Owner Gate; no production MCP handoff/update has been sent.
