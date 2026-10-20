# TEST_REPORT — executed scope and unresolved checks

These are this session's executions, not counts from the historical plugin report. Logs are under evidence/. Source candidates do not imply production acceptance.

| Execution | Observed result | Scope / limitation |
|---|---|---|
| Fresh-main root unittest baseline |91 tests passed | Before any implementation. |
| Fresh-main Ziheng baseline |26 tests passed | Before any implementation. |
| New `test_ziheng_v020_*.py` |18 tests passed | Context, byte preservation, segment roles, evidence requirements,32-item mapping, standalone and packaging contracts. |
| Current branch root discovery |109 tests,4 failures |105 pass. All4 are listed below; no skip/relaxation used. |
| Current branch legacy Ziheng discovery |26 tests passed | Existing rule/schema/profile/link/host-page tests. |
| `build_ziheng.py --check` |passed |165 generated outputs including exact historical allowlist, non-writing. |
| `build_ziheng_hosts.py --check` |passed |32 Claude/Gemini generated outputs including retained metadata/archives. |
| `build_ziheng_site.py --check` |passed |13 Ziheng-only surfaces generated from canonical copy/templates. |
| Japanese `build_dist.py --check` |passed |148 outputs, Japanese0.1.8 unchanged. |
| `check_ja_type_011_cases.py` |exit0 | Existing Japanese fixture consistency. |
| Current branch `build_seo.py --check` |failed at preservation generation | Shared checker does not yet admit the exact Ziheng source transition; other preceding generator checks succeeded. |
| Current branch `check_seo_preservation.py` |failed | Same held shared source transition, not historical ZIP loss. |
| Unapplied shared-integration patch, isolated staging |109 root tests passed; SEO and preservation passed | Separate copied tree with proposed shared patch, not this branch/HEAD. Patch dry-run against branch passed. Must be reconciled with #120 then rerun. |
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
