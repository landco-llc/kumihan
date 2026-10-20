# KUMIHAN JA v0.2.0 — GitHub limited Release Workgroup

**Authority:** Owner explicitly approved Japanese v0.2.0 GitHub limited publication on 2026-10-20 JST. This authorizes GitHub PR integration, new tag/Release with 15 ZIPs, verified release metadata and the related GitHub Pages version/status readback. It does **not** authorize Marketplace submissions, other-edition publication, host-compatibility claims, unrelated fixes, or Universal MCP changes (separate [#127](https://github.com/landco-llc/kumihan/issues/127)).

- Workgroup ID: `KUMI-JA-V020-GITHUB-RELEASE-20261020-01`
- Tracking: [#126](https://github.com/landco-llc/kumihan/issues/126). Historical implementation [#119](https://github.com/landco-llc/kumihan/issues/119), QA [#121](https://github.com/landco-llc/kumihan/issues/121).
- Repository: `landco-llc/kumihan`, default `main`, protected by active `protect-main` ruleset.
- Control branch: `control/ja-v020-github-release-20261020`, from W09 PR #125 fixed HEAD `1f205124cee538235f4cee384ca67f414c5e0e26`, tree `8d0447010255626be2351e61e61a5d22c73bcaab`. Control docs alone do not modify products.
- Observed main: `8b647cc752d7a9bc3db48356fa0ab7b221bb66d6` — must Fresh Read at start.
- Logical feature stack: Draft [#120](https://github.com/landco-llc/kumihan/pull/120) head `ce2fd8d23e4afb0816b5870625e02af3aa7a96b8` → Draft [#123](https://github.com/landco-llc/kumihan/pull/123) head `384f073ba122abde42f5836b15650c055928e724` → Draft [#125](https://github.com/landco-llc/kumihan/pull/125) final head above.
- Review/QA: 105 unit tests, 29 SEO tests, 15 candidate ZIP hashes, 20 foreign editions preserved, W09 latest-head CI #39374173510 SUCCESS; **these are fixed prior-head observations and must be repeated as needed against final main/release HEAD**.
- Release target tag `v0.2.0`; canonical plugin version `0.2.0`, user-facing `v0.2.0`, display name `KUMIHAN` unchanged.

## Release contract and known limitations

This is a **source-backed Japanese typography guidance update**, not a newly certified automatic layout engine. It adds role/intent/readingTask/prose-display-hybrid distinctions, required-information and evidence scope, conditional Web/document/presentation recipes, Japanese writing/type research and associated synthetic/real QA records. Preserve the 39 canonical JA rule IDs, six profiles, seven existing statuses and frozen report schema. All 20 other languages retain independent versions. The 15 Japanese host/skill ZIPs are source-only packages with deterministic CRC/size/SHA256 records, **not an assertion of native install success**.

Release notes MUST state:
- Original research verification: 30 synthetic scenarios; 15 partially exercised within limited conditions, 15 not run; no full 30-case certification.
- Historical **P1 FAILED**: LibreOfficeDev 26.8 alpha with the original Noto Sans CJK JP environment can insert spaces/alter visible spacing on PPTX→PDF export/extraction; alternate fontconfig success is not a fix for that original environment. Do not claim exact PDF fidelity for all converters.
- 0/12 native host+skill invocations verified across ChatGPT/Codex, Claude, Gemini. Native Microsoft Office, native user text enlargement, physical projection/signage, reader studies and actual accessibility speech are NOT_CHECKED.
- User source names, numeric values, CJK variants and unusual Unicode must not be silently normalized. Automated semantic beauty scoring, visual rendering auto-pass and end-to-end native generation are not shipped.

Old published [v0.1.8](https://github.com/landco-llc/kumihan/releases/tag/v0.1.8) and historical preview releases/tags/assets must remain immutable. Do not force tags, delete release assets or replace an old Release. Do not label `v0.2.0` Published until GitHub Releases API readback verifies public publication.

## W00 — Fresh Read / strict preflight

- [ ] Confirm current main and exact three nested PR head/base and ancestry/trees; record SHA/TREE, state, branch owners and no unrelated changes. Detect if v0.2.0 Release/tag already exists: if it exists, compare source/assets and avoid duplicate publication.
- [ ] Verify repository ruleset `protect-main`: active PR required, linear history, allowed methods `squash`/`rebase`, required `static-and-distribution`, review conversations resolved, no bypass. Do not force branch pushes or attempt a merge commit.
- [ ] Inspect all 15 source ZIPs from final candidate under `downloads Claude`, `downloads GPT-Codex`, `downloads Gemini`; compare exact paths, members, sizes, SHA-256, CRC and manifest. Flat GitHub Release asset basenames must be unique. Do not include unrelated ZIPs.
- [ ] Read repo `docs/versioning.md`, `docs/version-automation/README.md`, `tools/build_dist.py`, `tools/sync_edition_versions.py`, `assets/edition-release-contracts.json` and `tools/build_version_site.py` before mutation.
- [ ] Verify current main has no new unrelated merges or conflicting feature work. In particular [#122](https://github.com/landco-llc/kumihan/pull/122) (Traditional Chinese), [#101](https://github.com/landco-llc/kumihan/pull/101) (Universal runtime), [#116](https://github.com/landco-llc/kumihan/pull/116), [#118](https://github.com/landco-llc/kumihan/pull/118) are NOT included. If current main differs, recompute the release diff and stop only if scope cannot be preserved.
- [ ] Capture provenance and baseline in `docs/development/ja-v020-20261020/release-20261020/evidence/FRESH_READ.json` on a release control/execution branch, not on main.

## W01 — Assemble a clean linear-history release PR

GitHub main forbids merge commits. Three Draft PRs are logically nested, and their existing heads must remain immutable. Do NOT merge them blindly into each other or force-rewrite #123/#125 ancestry. Recommended narrow strategy:

1. Freeze #120→#123→#125 in that order. Verify #125's final product tree contains all accepted changes and no unapproved unrelated files.
2. Create a **dedicated release integration branch** from current main and replay the reviewed deltas in logical sequence (#120 original change, #123 QA, #125 W09) with normal commits. Preserve the exact final source/15 ZIP checksums; there must be no extra language, Universal runtime or other-pull-request data. Equivalent safe implementation: create a new direct-main integration PR from a branch with the frozen #125 tree, after proving main is its unchanged ancestor and full diff equals the reviewed stack. Use a single PR rather than mutating existing nested Draft branch refs.
3. Verify final integration tree matches the reviewed #125 tree for all source/distribution files. Release-control/evidence documents may be new only with explained, bounded diff. Compare changed path list and 2,627 protected paths against the audited baselines; ensure remaining 20 languages are byte-identical.
4. Create PR to main (initial Draft allowed), run **required** `static-and-distribution` and full 105+29/SEO/Pages checks on its latest head. Resolve all review threads and conflicts. Keep a valid final/head test identity.
5. With existing Owner scope and GitHub required checks satisfied, mark that integration PR Ready only when needed to permit merge; perform **squash or rebase** according to the active ruleset, never merge-commit, never bypass rulesets. Record resulting main SHA/TREE and verify post-merge contents. The three original PRs remain auditable. Link them as source stack; only after final publication may they be closed as superseded, without deleting branches.

**If the source tree is not equivalent, rule-required check is missing, or main includes unreviewed unrelated files: HOLD affected merge, do not alter main by direct ref.** Make a clean PR/review patch instead of bypassing protection. Do not count a Draft PR CI from a different base as the required main-target check.

## W02 — Release assets and verified source commit

- [ ] Fetch merged main/tag state. Freeze immutable `RELEASE_SOURCE_SHA`, `RELEASE_SOURCE_TREE`, JA manifests (root `plugin.json` plus host manifests) and archive content from the exact commit.
- [ ] Run `python tools/build_dist.py --check`, 15 ZIP SHA/CRC/member/size check, tests and Jekyll/SEO check; compare the old `v0.1.8` Release unchanged and other modules still frozen.
- [ ] Create **new** annotated Git tag `v0.2.0` pointing to verified main commit; never force a tag. A Draft GitHub Release is permitted while verifying assets. Release name `KUMIHAN v0.2.0`, not a versioned plugin display name.
- [ ] Upload exactly the 15 Japanese candidate ZIP files from the exact tagged tree, with their existing unique versioned filenames. Preserve all earlier asset basenames as historical releases.
- [ ] Read back GitHub Releases API: tag target commit, Draft status, 15 asset names, sizes, GitHub asset SHA-256 digests if available, compared with `SHA256SUMS`. For asset APIs without SHA, download each asset and compute independently; response metadata alone cannot establish binary identity.
- [ ] If any asset mismatch or uploaded name collision: do not publish Draft; repair in Draft and re-check. No silent new archive naming or inline replacement of existing release history.
- [ ] Publish the Draft Release only when all required assets/notes/checks agree; read back `draft=false`, correct tag, 15 downloadable ZIPs. No Marketplace submission.

No connector/API capability for attaching Release assets may be assumed. Use authorized Codex Cloud/App execution with actual `gh` credentials and permissions. If unavailable, return `ACCESS_NEEDED: GitHub Release create/upload permission` with the exact payload and remaining steps; do not claim publication or fabricate a URL.

## W03 — Verified version synchronization and Pages readback

- [ ] Public status is derived from a real stable Release, never from source/manifest version. Before publishing Release, the site may correctly show `source v0.2.0 / published v0.1.8`.
- [ ] After Release: follow `tools/sync_edition_versions.py`, actual GitHub Release API + ZIP checksums and patch-only `version-automation`. Retain semiautomatic / `PATCH_ONLY_CONSTRAINED`; the workflow may generate patch evidence, not silently push.
- [ ] Apply the reviewed source-generated status patch through a scoped PR with required checks. It must promote **JA published_version to v0.2.0 only** with exact immutable tag and 15 assets. Other 20 editions and the historical 0.1.8 release data must not be reassigned.
- [ ] After merge, read actual GitHub Pages built site `https://landco-llc.github.io/kumihan/kumihan.html` (and ja/en variants, install pages) at the published SHA; labels/download links and source/published distinction must be correct, no broken ZIP, invalid HTML, unexpected language/version change. Do not equate successful source-only generation with deployed Pages.
- [ ] If Pages build is delayed or fails, report `RELEASE_PUBLISHED / PAGES_PENDING`; do not claim Pages completed. Do not delete published release assets to solve a Pages rendering delay.

## W04 — Limited release notes and rollback policy

Use [RELEASE_NOTES.md](RELEASE_NOTES.md), verify its claims against the tagged commit and QA evidence, and include source SHA/TREE, version number, public URLs, host ZIP names. Known P1 must be explicit. English+Japanese factual copy is sufficient. No native installation or marketplace certification claims.

Rollback: before publication, leave the Release Draft until repaired; after publication, use a new Owner-reviewed forward fix/revert PR with full version/status readback. Never overwrite `v0.1.8` assets nor force-move `v0.2.0` tag. Treat public historical provenance as immutable.

## W05 — MCP handoff / complete

After GitHub Release readback, send to [MCP update #127](https://github.com/landco-llc/kumihan/issues/127): tagged SHA/TREE, `plugin.json` version, 39 JA canonical rules, SKILL/read-only reference hashes, 15 ZIP checksums and verified source provenance. This is **handoff** not a claim that live KUMIHAN Universal MCP is v0.2.0. Leave #101/#116/#118 and live PHP unchanged from Release lane.

Return one RESULT record to Issue #126, #119 and #121 with:
- actual release SHA/TREE/tag; Release URL/draft/public status and exactly 15 assets sizes/checksums;
- integration PR and main ruleset/CI evidence;
- version patch PR, GitHub Pages actual status, other 20 editions preservation;
- known LO P1 and native 0/12 limits;
- handoff URL to issue #127;
- any blocker's exact unavailable capability, not an invented publication completion.

No further Owner approval loop is required for these **explicitly authorized bounded GitHub actions** if every prescribed gate passes. Any new unrelated production/Marketplace/security scope or inability to satisfy hard release checks requires stopping that operation and reporting.


## W00B — Mandatory new-main integration update (2026-10-20, after this workgroup was created)

A concurrent main integration occurred during preparation: **PR #122 KUMIHAN｜字衡 source v0.2.0 has merged**. New main is `de6ec7d6c393a832ffff8f842be47a5335d3ecd0`; previous main `8b647cc752d7a9bc3db48356fa0ab7b221bb66d6` is no longer current. A provisional JA source integration [Draft PR #128](https://github.com/landco-llc/kumihan/pull/128) was created from frozen PR #125 before that merge; it now reports **mergeable=false**, base new main and 617 changed files. **DO NOT Ready/merge/force-rebase PR #128 as-is.** Use it only as an auditable, stale initial attempt, and build a fresh integration branch from new main.

Read the newly merged [JA/#120 shared-path coexistence handoff](https://github.com/landco-llc/kumihan/blob/de6ec7d6c393a832ffff8f842be47a5335d3ecd0/docs/development/zh-hant-v020-20261020/JA120_SHARED_HANDOFF.md) before integrating. Its disposable three-way composition validated 123 root +26 ZiHeng tests in a **synthetic** tree (not hosted integration acceptance) and identifies six shared files:

1. `README.md`: keep JA source0.2.0/published0.1.8 (before release), plus ZH-HANT source0.2.0/unpublished (retained legacy v0.1.0 source downloads).
2. `assets/edition-versions.json`: merge two per-edition records; never set ZH-HANT published_version to 0.2.0.
3. `tools/build_version_site.py`: preserve BOTH JA old→new source transition admission and ZH-HANT source transition admission.
4. `tools/check_seo_preservation.py`: retain BOTH exact transition paths and normal overlay checks; no weakening or skip.
5. `docs/version-automation/preservation.json`: regenerate combined overlay, preserving all existing preimage hashes and 330 accepted ZH-HANT rows; the README after-hash changes with JA combined status.
6. `tests/test_version_naming.py`: maintain both dynamic JA source version expectations and ZH-HANT retained-manifest/test policies.

The first disposable assembly had a known 15 old-JA-ZIP deletion loss due to rename detection; replay the original JA ZIP *deletions* explicitly with `--no-renames` or a robust exact path manifest and verify no old active ZIP remains at v0.1.8 on current source tree (old published v0.1.8 Release assets remain preserved off-tree).

A prior synthetic test failed `test_other_edition_facts_are_unchanged` because its baseline pinned JA before the new JA source transition. DO NOT skip, disable or whitewash that check. Establish a new, narrowly accepted JA-after-#122 transition record under this Release Work's evidence, with strict before/after hashes; preserve the immutable ZH-HANT historical baseline and all other source ZIP hashes.

**New integration sequence (required):**
- branch fresh from main `de6ec...` (and Fresh Read again before applying). Replay #120 Japanese source diff, then #123 QA delta, then #125 W09 delta, resolving only the authorized six shared paths and necessary generated records.
- Verify ZH-HANT source code, site, legacy ZIP and release status preserve the merged #122 exact values.
- Rerun root, ZH-HANT (26), Thai cross-locale and all originally triggered GitHub Actions, `static-and-distribution`, dist, SEO, both preservation paths and real Jekyll build on **new main-based integration SHA**. The old PR #125 and synthetic tree checks do not pass this gate.
- Create a **new clean main-target Release PR** with explicit old/new main SHA and PR #128 supersession; do not try to merge PR #128 until reconciled. If another main merge arrives, repeat Fresh Read/compare.
- If the six-file composition or cross-locale baseline cannot be made exact without mutating unrelated modules, HOLD integration and return a single blocker rather than forcing release.

GitHub v0.2.0 tag/Release/upload, verification, version sync and MCP handoff remain authorized **after** this new integration gate passes. The GitHub source-only Release must not be labelled published while #128 is unmergeable.
