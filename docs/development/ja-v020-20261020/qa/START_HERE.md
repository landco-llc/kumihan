# START HERE — JA v0.2.0 additional QA

Issue: https://github.com/landco-llc/kumihan/issues/121
Original implementation: https://github.com/landco-llc/kumihan/pull/120
Previous result: https://github.com/landco-llc/kumihan/issues/119

## Environment

- Codex Cloud or Codex App in repository landco-llc/kumihan
- QA instructions: branch control/ja-v020-qa-20261020, directory docs/development/ja-v020-20261020/qa/
- Original candidate branch: feat/ja-v020-research-20261020
- Candidate SHA at QA plan creation: ce2fd8d23e4afb0816b5870625e02af3aa7a96b8
- New QA work branch suggestion: qa/ja-v020-acceptance-20261020
- Main branch is off limits to this QA. No local Codex CLI via Remote Desktop.

## First reads

1. Fresh Read PR #120 status/HEAD/main and concurrent #101/#116/#118; preserve unrelated changes.
2. Read qa/WORKGROUP.md, qa/QA_OBSERVATIONS.md, qa/QA_MATRIX.json, qa/HOST_SMOKE.md.
3. Read RESULT.md / case-results.json / release-manifest.json and the actual four Japanese Skills.
4. If the PR HEAD changed, compare to pinned candidate and re-evaluate the two visual findings.

## Execute

Continue W00 through W08 autonomously with focused child/reviewer work. Prioritize QA-V01 PV-006 「オ／ンライン」 and QA-V02 raw version-label separator. Then produce REAL artifact tests and, where available, native host smoke; do not substitute source-only reads for native installation. Some hosts may need an authorized human. Continue independent QA if native access is blocked.

Keep previous negative fixtures and their failed statuses intact. Preserve protected text, 39 rule IDs, 6 profiles, the 7 report statuses, all other language packages and the shared Universal MCP production. Run full current-head unit/build/SEO/CI after any fixes; recheck all 15 ZIP SHA-256 and reproducible build. Create a Draft stacked PR against feat/ja-v020-research-20261020, record RESULT.md and next gate in Issue #121 and #119.

Stop before main merge, tags, public GitHub Releases, Pages publication, public plugin-directory submissions, production MCP changes and any tool action that requires new Owner approval.

## Required answer back

State: VERIFIED / PARTIALLY_VERIFIED / BLOCKED, by scope, not an aggregate quality label.
Provide: actual final HEAD and TREE; Draft QA PR; before/after images (all pages/slides); issue result; native host evidence or exact ACCESS_NEEDED; 30-case status differences; latest CI runs; 15 ZIP checksums; remaining P0/P1 issues; final Owner Gate condition.

The existence of these files is NOT a QA PASS.
