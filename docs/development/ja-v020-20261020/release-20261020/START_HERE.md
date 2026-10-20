# START_HERE — 日本語v0.2.0 GitHub限定公開

Status: OWNER_AUTHORIZED / RELEASE_NOT_YET_CREATED. This is an execution entry, not the Release itself.

- Execution: Codex Cloud or Codex App, repository `landco-llc/kumihan`.
- GitHub tracking: [Issue #126](https://github.com/landco-llc/kumihan/issues/126).
- Control branch: `control/ja-v020-github-release-20261020`.
- Main instruction: `docs/development/ja-v020-20261020/release-20261020/WORKGROUP.md`.
- Release text: `docs/development/ja-v020-20261020/release-20261020/RELEASE_NOTES.md`.
- Fixed reviewed candidate: PR #125 HEAD `1f205124cee538235f4cee384ca67f414c5e0e26` (after logical #120 and #123). Tag planned: `v0.2.0`.
- Source version `0.2.0`; current observed published version `0.1.8`.
- GitHub main ruleset: linear history; only squash/rebase PR; required `static-and-distribution`.

## Autonomously execute

Read WORKGROUP and existing `docs/versioning.md`, `docs/version-automation/README.md`, release-manifest, main/PR CI. Fresh Read all live refs before any merge. Complete W00–W05 as an integrated task group. Since original #120/#123/#125 are nested, preserve their heads and audit history; if a single clean protected-main integration PR is technically safer, construct it from those deltas IN ORDER and prove exact final reviewed tree/ZIP hashes. Do not force-push or bypass rules.

On successful protected-main integration, fix the immutable source commit, create `v0.2.0` draft release, upload/verify **exactly 15 versioned ZIPs** and publish GitHub Release. Confirm from actual GitHub Releases API and asset bytes, then apply existing verified edition version patch-only workflow and inspect GitHub Pages actual output. Old `v0.1.8` assets untouched; other 20 editions unchanged.

Owner authorized these bounded GitHub actions. Do not request per-Work confirmation when conditions are satisfied. Do not publish to Marketplace, reconfigure permissions or deploy Universal MCP here. No native host acceptance claims. Historical LibreOffice alpha issue must appear in Release notes, not be hidden.

If GitHub App/gh Release upload permission, required CI, asset integrity, source SHA or other hard gate is unavailable, stop that affected operation, preserve all completed independent work and report a single exact blocker; never report the Release as Published before verified.

## Reporting

Provide final main HEAD/TREE, Release tag/URL/status, 15 asset names/sizes/SHA256, integrated PR and required CI run, verified version metadata patch, public site download/readback results, non-JA SHA preservation, known limitations and handoff to MCP Issue #127. Write release RESULT.md and comment on #126/#119/#121; link any remaining owner action. Avoid empty status updates as substitute for evidence.
