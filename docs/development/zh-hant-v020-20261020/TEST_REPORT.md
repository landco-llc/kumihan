# TEST_REPORT — integrated candidate evidence

Public metadata mapping: the original reviewed source `6be142c57300de933caaae94a59436aa1f319a0b` is published as `ad9c31f2a33ea038fea7288d3febc809db00b883` with the identical TREE `a819dc438089509c4ad5a4f399540059aab84b36`. GitHub GH007 rejected the initial push; only unpublished author/committer metadata was corrected using the authenticated owner’s existing public noreply identity. No executable bytes, review report, remote history, settings or publication authority changed. See [mapping](evidence/public-commit-map.json).

Fixed implementation source: `6be142c57300de933caaae94a59436aa1f319a0b`, TREE `a819dc438089509c4ad5a4f399540059aab84b36`. All required actual-branch commands exited0; no test was removed, skipped or relaxed. The original112/4 failures were reproduced before correction in evidence/shared-root-before.log. Source0.2.0 and old0.1.0 contracts now pass together.

| Execution | Result | Evidence / scope |
|---|---|---|
| Root unittest discovery |118 tests PASS, no skips | evidence/integration-validation-root-tests.log |
| Legacy tests/ziheng discovery |26 tests PASS | evidence/integration-validation-ziheng-tests.log |
| New shared boundary methods |6 PASS after source/display RED | evidence/shared-regression-red.log; evidence/shared-regression-green.log |
| Isolated version naming |7 PASS | evidence/shared-naming-after.log |
| build_ziheng / build_ziheng_hosts / build_ziheng_site --check | All exit0 | evidence/integration-validation-build_ziheng*.log |
| build_dist --check; check_ja_type_011_cases | Both exit0 | evidence/integration-validation-build_dist.log; evidence/integration-validation-check_ja_type_011_cases.log |
| build_seo --check | PASS,274 pages / sitemap272 URLs | evidence/integration-validation-build_seo.log |
| check_seo_preservation; git diff --check | Both exit0 | evidence/integration-validation-check_seo_preservation.log; evidence/integration-validation-diff-check.log |
| Current15 + old15 ZIPs | Size/SHA256/CRC/safe member paths PASS; distinct sets; byte unchanged | evidence/integration-validation-distributions.json |
| Existing distribution bytes / old URLs |252 fixed files unchanged;15 old URLs matched SHA256 | evidence/integration-validation-distributions.json; evidence/integration-validation-old-url-readback.json |
| Integrated pages | Chromium1024/320; keyboard Tab/Enter CTA to #install | evidence/integration-validation-browser.log; screenshots |
| First hosted CI |8 workflows success /1 new cross-locale failure | evidence/hosted-ci-first.json; corrected-head CI pending |

The first hosted candidate `3d7a892613cdec0f04259bacc00becbe5c61c70f` completed9 workflows:8 success and1 new ZiLu failure. All four originally failing workflows succeeded. ZiLu's unchanged Other-language regression exposed12 Ziheng output hashes in the Thai historical regression consumer. This failure and merge checkout `78220612f5928cb26e479eed2c26a8b930c1e9bd` are preserved in [first CI](evidence/hosted-ci-first.json) and [diagnosis](evidence/shared-ci-diagnosis.md).

A bounded shared regression correction now pins the original immutable Thai baseline and exactly12 registered Ziheng old→new full-output digests, with exact source hashes and frozen transition guards. The original fixture, resolver, Thai/ZiLu product sources, workflows and all distribution bytes are unchanged. No skip or expected-output normalization is used. Separate correction validation passed Thai22 / root119 / Ziheng26 and all11 commands,18 unchanged contexts,6 unchanged Japanese outputs,12 complete current Ziheng outputs and18 rejection probes. Evidence: [correction validation](evidence/integration-correction-validation-summary.json). The one initial source review remains scoped to its fixed tree; this later bounded correction has separate test evidence and no second review claim. Corrected-head hosted CI is pending push/readback.

The six regression methods check source-only edition changes; other edition/distribution/snapshot facts unchanged; exact registered retained manifests; unknown history still reaches the original version assertion; unknown transition paths/old hash/snapshot hash/after hash/frozen baseline/candidate tampering; one-byte mutation and deletion of an old ZIP; and displayed old/new source versions with unpublished Release facts.

The four former failures were corrected by connecting exact transition validation, changing only zh-hant source_version, admitting only validated historical manifests, and asserting current0.2.0 separately from retained0.1.0. The original unapplied patch and isolated112 PASS remain historical proposal evidence. They do not substitute for actual118 PASS. New isolated naming execution also exposed missing retention-module import resolution; explicit tools path setup corrected it before full-root rerun.

PR #120 coexistence is separately documented in JA120_SHARED_HANDOFF.md and evidence/ja120-*; its synthetic tree never establishes actual PR #122 CI or future main acceptance. The completed single bounded shared-integration review (evidence/shared-integration-review.md) found no actionable defects and is separate from the earlier four-finding review and its recorded corrections. It is a nonformal same-task technical review, not independent audit certification. Raw historical failure logs retain three trailing-space lines; this formatting limitation is distinct from the clean working-tree whitespace check.

32 fixture definitions remain14 partial /18 unexecuted /0 fully accepted. New keyboard navigation observations concern the local LP only; system clipboard, external navigation, real UA200%, regional glyph/IVS support, native Office/PDF, AT, native host invocation and TW/HK proofreading remain unverified as scoped. No production action is implied.

<details>
<summary>WG00–07 historical test report, including four failures and prior four-review correction history</summary>

# TEST_REPORT — executed scope and unresolved checks

These are this session's executions, not counts from the historical plugin report. Logs are under evidence/. Source candidates do not imply production acceptance.

| Execution | Observed result | Scope / limitation |
|---|---|---|
| Fresh-main root unittest baseline |91 tests passed | Before any implementation. |
| Fresh-main Ziheng baseline |26 tests passed | Before any implementation. |
| New `test_ziheng_v020_*.py` |21 tests passed | Context, byte preservation, segment roles, evidence requirements,32-item mapping, standalone and packaging contracts. |
| Current branch root discovery |112 tests,4 failures |108 pass. All4 are listed below; no skip/relaxation used. |
| Current branch legacy Ziheng discovery |26 tests passed | Existing rule/schema/profile/link/host-page tests. |
| `build_ziheng.py --check` |passed |165 generated outputs including exact historical allowlist, non-writing. |
| `build_ziheng_hosts.py --check` |passed |32 Claude/Gemini generated outputs including retained metadata/archives. |
| `build_ziheng_site.py --check` |passed |13 Ziheng-only surfaces generated from canonical copy/templates. |
| Japanese `build_dist.py --check` |passed |148 outputs, Japanese0.1.8 unchanged. |
| `check_ja_type_011_cases.py` |exit0 | Existing Japanese fixture consistency. |
| Current branch `build_seo.py --check` |failed at preservation generation | Shared checker does not yet admit the exact Ziheng source transition; other preceding generator checks succeeded. |
| Current branch `check_seo_preservation.py` |failed | Same held shared source transition, not historical ZIP loss. |
| Unapplied shared-integration patch, isolated staging |112 root tests passed; SEO and preservation passed | Separate copied tree with proposed shared patch, not this branch/HEAD. Patch dry-run against branch passed. Must be reconciled with #120 then rerun. |
| Browser fixture |3 observed conditions |Chromium1024/320/320+spacing; local button click, DOM equality and line rectangles. No native UA200% test. |
| Instruction pressure scenarios |3 GREEN after workflow correction |Same scenarios as pre-update baseline. No native-host, regional proofreading or rendering certification. |
| Whitespace / private-boundary scan |passed in recorded scope |Changed text and all candidate ZIP members scanned for private Drive links/research-fulltext markers and private-key marker. This is a bounded scan, not secret certification. |

Current branch failing tests (introduced integration requirements, baseline was clean):

- `test_edition_versions.PreservationGate.test_unlisted_mutations_still_fail`: shared exact-transition hook is held because #120 writes the same checker/overlay.
- `test_edition_versions.SnapshotAndCoverage.test_catalogue_source_and_release_integrity` for zh-hant: shared snapshot source0.1.0 versus canonical candidate0.2.0.
- `test_version_naming.VersionNamingPolicyTests.test_current_distribution_manifest_versions_match_their_products` for archived0.1.0 manifest: legacy global test assumes every recursive manifest is active; proposed shared test distinguishes exact retained history.
- `test_version_naming.VersionNamingPolicyTests.test_ziheng_active_distribution_and_site_names`: held global test still fixes0.1.0; proposed update names current0.2.0 and retains historical URL tests.

RED evidence: initial context/evidence/fixture assertions failed before implementation; version-transition test reproduced deletion of15 old ZIP paths; later legacy-link regression failed with the proposed0.2.0 snapshot before the exact retention fallback fix. The first historical-link test before active-manifest regeneration already passed and is not claimed as RED. Skill baseline showed missing contracts, not three unsafe observed behaviors.

Build verification covers15 current ZIPs and15 historical Ziheng ZIPs independently. Current manifests contain only0.2.0; history files and retained-distributions.json preserve old bytes. SHA256/size/CRC/member-path checks, all4 independent script imports, local Markdown reference checks, official bundle icons and same-environment deterministic/non-writing tests ran. Native installation/discovery/invocation on the3 AI hosts was not run.

32 fixtures are defined;14 partially exercised and18 not exercised, whole-case passed0. Native Office/PDF editing, actual regional font/glyph/IVS, ruby/AT/search/copy, external navigation/system clipboard, real UA200%, native TW/HK proofreading, print and physical-distance acceptance remain not-checked/unsupported as scoped. No production MCP calls, registry update, Marketplace submission or publication occurred.

One whole-branch lightweight read-only review is recorded separately in evidence/final-review.md. Review findings and final CI must be read for the pinned candidate HEAD; older green jobs do not establish its acceptance.

## Single review and correction pass

The independent read-only review pinned3322d4840421cce4b53df64cd88d2f2e791ab3f8 found4 P2 issues. One correction pass installed pinned root-suite dependencies in Ziheng CI, bound old hashes to an independently frozen fresh-main baseline, restricted history exceptions to digest-validated Ziheng manifests, and rejected static-byte glyph acceptance. New failing tests reproduced the absent transition enforcement and glyph-method obligation;21 new checks now pass. Root112 retains only the same4 documented shared-path hold failures. Isolated integration root112, SEO and preservation pass. No second review or independent approval of the later revision is claimed.

Structured unknown font face/version/fallback fields were added to the limited browser record; they do not create a glyph PASS. All15 existing main download URLs were also fetched and their bytes matched the old SHA256 values (`evidence/old-url-readback.json`).

</details>
