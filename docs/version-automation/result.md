# KUMI-VERSION-AUTO-WG00-WG04-20261019-01 — Owner Gate result

`PR_URL`: https://github.com/landco-llc/kumihan/pull/115 (OPEN / DRAFT).

`BRANCH`: `feature/version-automation-wg00-wg04-20261019`.

`BASE_SHA`: `fe36ef38ba8cb03bb45d24b93649339782237113`; BASE TREE `107afb0699b213e3740c49174c7e90d8ea08fdae`. Main was fetched fresh and this remained the remote main SHA at closeout.

Implementation: `8fb68175da04054c43c2f3b11a0a4847e3ea8311`; reviewed TREE `5c800742058e9fd0e5b8dbde05b5f9349c4a42ed`.

Review-fix implementation: `7705ad83d5cd1d647d007ef2b7ff1c4ffe76da7b`; TREE `e93548960279c8ace6be68b4f655ea8d8ba7a4af`.

`HEAD_SHA` / `TREE_SHA`: the final evidence commit includes this document, so its exact immutable HEAD/TREE are read back **after committing** and recorded in the PR description and final return. The implementation revisions above identify all production behavior tested here.

## WORKGROUP_STATUS

| Workgroup | Works | Result |
| --- | --- | --- |
| WG00 | W00–W01 | DONE: latest main, open PRs, generator paths and per-edition source/Release/ZIP facts read and fixed |
| WG01 | W02–W03 | IMPLEMENTED WITH OWNER CONDITIONS: shared facts, strict admission and read-only release/manual patch proposal; no unattended main/site publication |
| WG02 | W04–W05 | DONE: shared generation for all six requested display surfaces and bilingual README status |
| WG03 | W06–W07 | VERIFIED WITH LIMITS: offline/synthetic/API/ZIP/Jekyll/Chromium checks and one independent bounded review; both P2 findings fixed |
| WG04 | W08 | DRAFT PR / OWNER GATE: feature-only commits and push; exact final HEAD CI recorded in the PR, no merge or public deployment |

No native `/goal` controller was exposed in this session. The equivalent WG00–WG04 sequence ran autonomously in the selected managed cloud environment. One new independent read-only reviewer was used for W07 only.

## VERSION_SOURCE

The canonical facts are [`assets/edition-versions.json`](../../assets/edition-versions.json). Exact ZIP-role contracts contain templates only, not a second live version source: [`assets/edition-release-contracts.json`](../../assets/edition-release-contracts.json).

19 stable editions / 277 actual Release ZIPs passed pinned source-version, manifest, SHA256SUMS (where attached), API size/digest, actual SHA/size and ZIP CRC checks. Japanese v0.1.8 is **published**, dated `2026-10-19T12:51:29Z`; its API Release has 15 ZIPs and no attached manifest/checksum files, so its three host manifests/checksums are read from the pinned tag source. Non-Japanese published editions carry 15 ZIPs plus manifest/checksums, except Bengali: seven ZIPs plus manifest/checksums. No repository-wide `/latest` was used.

ZiHeng and ZiLu source v0.1.0 each have 15 locally verified source ZIPs, but no independent formal Release. Their formal download controls are labelled unavailable and source repository links remain. No unpublished Release URL is invented.

ZiHeng's first formal promotion additionally requires an Owner-adopted flat filename/role mapping: its current source plugin and entry Skill share `kumihan-ziheng-0.1.0.zip` in different directories. GitHub cannot attach two same-named assets. The contract is explicitly unconfigured; existing ZIPs were not renamed. This is an unresolved first-publication prerequisite, not a claim that all 21 release contracts are ready.

The read-only initial/final API projection of all 25 Releases (including draft/prerelease states and asset ids/names/sizes/digests) is identical: [`release-readback.json`](release-readback.json).

## DISPLAY_COVERAGE

| Surface | Measured count | Evidence |
| --- | --- | --- |
| Gateway cards | 22 pages × 21 cards | Generated and real built HTML checked |
| Edition landing hero + install status/date/Release | 63 pages | Both slots on every real built page, with JA language-switch variants |
| Install sidebar + versioned downloads | 186 pages | Real built HTML; every ZIP href belongs to that edition's verified asset set |
| README | 21 rows + JA/EN status/prose | Same facts, repeat generation unchanged; future first-publication prose tested |
| Chromium representative displays | 13 pages × 320/390/1280 = 39 | No page/version overflow; visible version links at least 44 CSS px high |

[`rendered/report.json`](rendered/report.json) and six PNGs record actual Chromium output. Japanese language switching keeps one current-version block visible; its version link is present in Chromium's accessibility tree. This does **not** establish a native screen-reader session. New non-Japanese/Chinese metadata is explicitly English; native translation review remains unverified. Existing approved copy/translation JSON is preserved.

## AUTO_UPDATE

`release: published` and manual dispatch → trusted main checkout → full paginated Release API → exact per-product tag/ZIP-role admission and real bytes → atomic facts replacement only after all editions succeed → shared builders/README → tests/`--check` → bounded patch artifact with fixed base SHA.

Drafts/prereleases/unrelated tags cannot promote; older formal releases cannot downgrade; duplicate events are idempotent. Missing/withdrawn current formal Releases and network/manifest/SHA/size/role failures abort without replacing the snapshot. API verification was actually run against this Work's releases; a real new Release event was **not** sent.

The workflow has `contents: read`, no remote write, automatic merge, tag/Release creation or deploy step. Owner applies a nonempty patch through a reviewed feature PR. It cannot become an active event handler until merged; automatic delivery and later Pages publishing remain unverified and human-controlled. No permissions, Secrets or Pages settings were changed.

## QA

- **368 tests / 24 suites PASS** after the same distribution preparation used by language CI. Root suite: 87 tests; new admission/display/preservation tests: 15. [`tests.json`](tests.json) lists suite results.
- Four archive suites initially failed because their generated downloads were absent (Laras, Lumnung, Mizani, Hlela); the same failures reproduced on the fixed main baseline. Running their existing builders created local test artifacts; all four then passed. Those generated ZIPs are not committed.
- `python tools/build_seo.py --check`: all builders PASS; sitemap 272 URLs and SEO source contracts 274 pages PASS. `base_copy.py --check`: PASS.
- `python tools/build_dist.py --check`: Japanese v0.1.8, 148 generated files unchanged.
- Jekyll 3.10.0 / Liquid 4.0.4 in Ruby 3.3 Docker: real build PASS; `check_seo.py --site-dir ...`: 274 built pages PASS. Tooling and site output stayed local; no deployment.
- `sync_edition_versions.py --check`: all 21 editions verified, facts unchanged after stricter review fixes.
- Synthetic regressions: first publication with an adopted contract, draft/prerelease, older stable/unrelated tags, partial assets, manifest/source/API/checksum/byte mismatch, network error, duplicate event, same-count wrong-role ZIP, missing/withdrawn current Release, unconfigured first-Release naming, source/published separation, generated coverage, concrete commands and preservation corruption.
- One independent review: no P0/P1; two P2 findings fixed. [`review.md`](review.md) records scope and reproductions. Fixes were locally verified; no second independent review is claimed.
- `git diff --check`: PASS. No existing product ZIP, source skill, license, font, privacy or SEO metadata policy changed.

## Current HEAD GitHub CI

PR Actions execution was observed: 23 workflows / 24 check-runs, including the new `verify-renderers` job. The release/manual proposal job is intentionally skipped on PR events. Exact check conclusions for the final immutable evidence HEAD are read back after committing this document and recorded in the PR description; the snapshot here points to that external readback to avoid claiming a commit's own future CI result.

Repository Actions-permissions inspection returned HTTP 403 (`Resource not accessible by integration`), but actual PR job execution was observed. No settings, permissions or manual release/deploy workaround was used. Actual Release-event delivery is still unverified until the workflow is adopted and a genuine approved future event occurs.

## PROTECTION / UNVERIFIED / OWNER_GATE

- Original SEO preservation snapshot unchanged. Its 2,608 protected paths retain original hashes except the explicitly requested README update; the exact feature overlay separately records README, 254 body and six Jekyll-input before/after hashes. Privacy and all other protected paths cannot use that exception. Unlisted mutation negative controls pass.
- SEO PR #93 was already merged in the fixed baseline (`41b89e6bcfe06a719c0319dadb5df603a9cb3369`). MCP PR #101 remained open at `b032c6ab179ed3acf8f1aeacbee753c8546b9c25`; neither PR branch was modified.
- No main push/merge, actual tag/Release creation/edit/deletion, production deployment, marketplace publication, server/Secrets/settings change, paid service or simultaneous language bump.
- Unverified: actual Release-event delivery, future Owner patch application/Pages publishing, ZiHeng flat Release naming, native hosts, all environments/native screen readers, Office/PDF, marketplaces and native metadata translations.

**OWNER_GATE: レビュー完了、未merge、未公開。** Draft PR and local evidence are complete. Current-HEAD CI is recorded on the PR; the named first-publication/publishing prerequisites remain explicit Owner gates.
