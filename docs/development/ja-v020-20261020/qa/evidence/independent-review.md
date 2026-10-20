# W07 independent read-only QA review

Reviewer: independent child agent, separate from Web/version/document authors. Scope is the current QA worktree against pinned PR #120 candidate `ce2fd8d23e4afb0816b5870625e02af3aa7a96b8`, not a public/native release acceptance.

## Result by scope

- QA-V01: bounded synthetic positive correction is supported. Before image reproduces オ／ンライン at 240px; after region retains the exact source and lexical ranges. The fixture and its source generator carry the same correction. Ordinary and CSS-enlarged examples differ visibly; native text zoom remains not-checked.
- QA-V02: genuine built Jekyll panels and raw DOM/no-CSS observations support the JA-only separator fix. Styled panels already had a CSS gap; no styled production concatenation was inferred. Published v0.1.8 and source v0.2.0 remain distinct. Native screen-reader output was not claimed.
- New Web artifact: inspected 320 and 1440 contact sheets (normal/CSS200/spacing/fallback), plus measurements and DOM/AX evidence. No clipping or occluded mandatory text was observed in this independent sample. The author's five-width/end-to-end audit is separately documented; this reviewer does not pretend that a sample equals independent full-state inspection.
- Documents: independently inspected report pages 3 and 6 and slides 3, 5 and 6. Table continuation header and content are visible; corrected comparison columns align; caution text sits in front of its background; long cancellation caption is visible. Full 6-page/8-slide author inspection is separately recorded. Native Microsoft Office, projection and reader performance remain not-checked.
- Preservation: reviewer independently rehashed all 2,627 paths in preservation-baseline.json; none changed. Prior case-results.json and historical evidence diff is empty. Rebuild logs/manifest retain 15 archive identities and two matching deterministic rebuilds.
- SEO boundary correction: docs/development/ is excluded in Jekyll and source SEO inventory. New QA HTML is excluded while the existing test still requires an unrelated new public guides/ page to be audited. No public sitemap rewrite was introduced.
- CI workflow: stacked-base PR trigger, contents:read, checks and local Jekyll build only. No deploy/merge/tag/release/submission step.

## Findings and limits

No additional source P0/P1 defect was found in the inspected diff or sampled positive images. This is a scoped review, not a claim that every environment or all 30 planned scenarios passed.

**P1, converter export fidelity — remains open:** LibreOffice PDF export's extracted numeric/Japanese boundaries introduce spaces, so the protected-string exact-substring checks are false. Saved PPTX XML and Chromium report extraction retain the originals. Keep the converter extraction check failed and limit acceptance of that export; do not turn source preservation or a readable preview into copy/paste fidelity. Evidence: documents/measurements.json converter_fidelity and presentation-extracted.txt.

**ACCESS_NEEDED:** twelve native host-skill invocations, native Office and user-native text zoom are not checked. No approved native test workspace/operator evidence is present. Physical projection/signage and reader studies are also unexecuted. These are missing evidence, not demonstrated incompatibility.

W05 must preserve exact original cases and their negatives. New artifact spacing observations do not by themselves execute original PV-016/017 inputs. They are supplemental named scopes. PV-021 syntax-only condition cannot become a real-font pass because a separate PV-022 sample was rendered. Before/after corrections do not rewrite historical failed artifacts.

## Review integrity

Only this independent-review.md is authored by the reviewer. Source/artifact targets were read without modifying them. Authors completed reporting files concurrently during the first broad snapshot; those changes are not attributed to the reviewer. The stable substantive target hashes below were checked again at review close. No stable target changed during that final review window.

## W05 final case classification review

The reviewer identified that original PV-003 (family-only/no-glyph-evidence condition), PV-010 (decorative cropping plus complete re-presentation) and PV-012 (conflicting 11月4日 plus correct 11月3日) were not actually exercised by the all-positive new Web prototype. The author corrected their original statuses to not-run while retaining new prototype findings as supplemental scopes. Final original-scenario rollup is **15 partially-run / 15 not-run**, versus historical **11 / 19**; no complete-case certification. PV-016/017 spacing and the different positive report table remain supplemental, historical negatives retained. PV-021 remains not-checked for its original syntax-only condition; PV-022 records the separate resolved-font observation. The failed LibreOffice extraction and native Office not-checked observations remain explicit.

## Verification handoff

Final local record reports 97 unit tests, 29 SEO tests, and all ten final commands exit 0. The earlier source SEO failure and red/green reproduction are retained separately. The actual final-head GitHub Actions result and final HEAD/TREE must still be linked by the parent after commit/push; this review does not substitute for those pending CI results. Draft PR plus Issue #121/#119 report and Owner Gate remain closeout requirements, not publication approval.

| Target | SHA-256 before = after |
| --- | --- |
| `tools/version_display.py` | `e17257f5b44221208aa4b2e50d9fafe1d903e3d168d041ec369dcfd36287be31` |
| `tools/render_ja_v020_research.py` | `9f927197211874eb8ba2b1c45ca8b6945150bda06711bff2ba2ddc220a234d63` |
| `tools/seo_inventory.py` | `7f8ea40e55ee96217c7a7d9f89aec983a30794a09934e7ecf27e44481d1c03af` |
| `tests/fixtures/ja_v020/web-contrasts.html` | `0be9dcde80500a80365166ffa6f1a7bf9444f468b19480deb7d9c5e612ca3fd7` |
| `_config.yml` | `e5f70e0501b1173a36ecdf643975b4aa8af571670495d3ddf8d3c1dac87aa81f` |
| `.github/workflows/ja-acceptance-qa.yml` | `7f09d5276d266e9edd00b26a3b002684194b33ff00727ff914a4b97724ac0fcd` |
| `docs/development/ja-v020-20261020/qa/evidence/web-positive.html` | `798bf7b07ab6706e05d265dde751ba08528a7c0cc4f896f6b174b406c902618f` |
| `docs/development/ja-v020-20261020/qa/evidence/web-negative.html` | `9478af8f76eb31a6080065c746c1934b20b8ae0bf0ac4d7ee85034119f73570c` |
| `docs/development/ja-v020-20261020/qa/evidence/web-observations.json` | `593cee657825162e876edadc35c0cc9336ace33aa6797719a0d8a07229319172` |
| `docs/development/ja-v020-20261020/qa/evidence/v01-before.html` | `84481cc355c0c46f20302bfc8815c1182ca13e098f34d7bf06ccdc1f6da18c09` |
| `docs/development/ja-v020-20261020/qa/evidence/v01-after.html` | `0be9dcde80500a80365166ffa6f1a7bf9444f468b19480deb7d9c5e612ca3fd7` |
| `docs/development/ja-v020-20261020/qa/evidence/documents/presentation.pptx` | `792a8f79d94a5a16b5738e27297ba9dd00fe518f8169c3c6a147253954414f33` |
| `docs/development/ja-v020-20261020/qa/evidence/documents/presentation.pdf` | `1138f714b2e17d08af80a4f95ed7c65849c12537ea16ffd9694c18f4c17efd36` |
| `docs/development/ja-v020-20261020/qa/evidence/documents/report.pdf` | `fe65ee60544c7b2f466d449500cdd240c4e4b2650a7cfc91445c2e03f1cce6e4` |
| `docs/development/ja-v020-20261020/qa/evidence/documents/report.html` | `8f703847e346b28022ddf754110dab673f4b7e86736d9984204c50eb28b20fd9` |
| `docs/development/ja-v020-20261020/qa/evidence/documents/source.json` | `ec7a8b47bd3e201c55cbedcc92ffa33f2a2763bc9228da0f020903875a2acc02` |
| `docs/development/ja-v020-20261020/qa/evidence/version/after-measurements.json` | `d241777db6ac4dfcf0f3fc128e9fb2290665d20d442c8ec560287c1e6388b74c` |

