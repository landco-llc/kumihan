# START_PIPELINE — KUMIHAN JA v0.2.0 GitHub Release → Universal MCP

Status: **Owner authorized two sequential bounded actions / no actual release or deployment yet**.

This is one Codex Cloud/App launch entry for the user's 2026-10-20 approval. Both downstream workgroups remain separate sources of truth and separate PR/release/deployment evidence scopes. The second phase depends on a verified GitHub `v0.2.0` public Release.

## Repository and pinned instructions

Repository: `landco-llc/kumihan`. Execution: Codex Cloud or Codex App. Start in a fresh bounded workspace, never overwrite other branches or remote host secrets.

**Stage A — GitHub publication** (Issue [#126](https://github.com/landco-llc/kumihan/issues/126)):
- Control branch `control/ja-v020-github-release-20261020`
- `docs/development/ja-v020-20261020/release-20261020/START_HERE.md`
- `docs/development/ja-v020-20261020/release-20261020/WORKGROUP.md`
- `docs/development/ja-v020-20261020/release-20261020/RELEASE_NOTES.md`
- JA source stack #120 → #123 → #125; reviewed source head `1f205124cee538235f4cee384ca67f414c5e0e26`.

**Critical current-main gate:** PR #122 Traditional Chinese v0.2.0 source **already merged** into main at `de6ec7d6c393a832ffff8f842be47a5335d3ecd0` (must Fresh Read). Provisional Draft PR [#128](https://github.com/landco-llc/kumihan/pull/128) is **unmergeable stale**; DO NOT merge/force update it. Read `docs/development/zh-hant-v020-20261020/JA120_SHARED_HANDOFF.md` and WORKGROUP §W00B. Compose JA source+QA on top of the NEW main preserving six documented shared paths and ZH-HANT unpublished0.2.0 source facts. No test skips or permission bypass. Verify new PR main CI, then create GitHub `v0.2.0` new Release with exactly 15 hash-verified JA ZIPs, not the Marketplace. Update reviewed verified-edition patch and read back actual Pages. Existing v0.1.8 immutable.

**Stage B — MCP Japanese module update** (Issue [#127](https://github.com/landco-llc/kumihan/issues/127)):
- Control branch `control/universal-ja-v020-20261020`
- `universal/deployment/ja-v020-20261020/START_HERE.md`
- `universal/deployment/ja-v020-20261020/WORKGROUP.md`
- `universal/deployment/ja-v020-20261020/MODULE_CONTRACT.json`
- Source branch separately anchored to Draft PR #101. DO NOT merge unrelated #101/#116/#118 runtime/publication work or PR #122 to deploy JA data.

**Dependency gate:** Stage B imports the JA module only from the verified immutable new Release tag SHA, not from old candidate or movable main. Current directly connected Universal MCP has 21 modules and JA `0.1.8`. A version label alone is inadequate: existing `getGuidance` lacks v0.2.0 reference contents. Implement and test minimal bounded read-only `reference_guidance` on existing MCP tool, preserve exact 20 other module hashes and existing 4 MCP signatures. If authorized secure private hosting access and rollback checks are available, deploy new PHP guidance reader then atomic registry swap; directly query live MCP for JA `0.2.0` and actual new reference text. If not, produce secure operator run packet and report `ACCESS_NEEDED` without claiming live reflection.

## Workgroup orchestration

Run Stage A W00–W05 first. If Stage A source integration is blocked by the concurrent ZH-HANT changes, Stage B may continue **design and read-only testing only**; it must NOT publish/deploy an untagged Japanese module. Once Stage A Release is confirmed public with verified 15 assets, run Stage B W00–W07 autonomously within available permissions. Do not ask per-Work approvals; the user has authorized the scoped publication and Japanese live reflection, but not bypassing hard safety/technical prerequisites.

At completion, return two independent statuses:
1. `GITHUB_RELEASE_PUBLISHED` or specific `BLOCKED`: Release tag/URL, immutable SHA, 15 hashes, merged integration PR, Pages verified status.
2. `MCP_JA_LIVE_0.2.0` or `STAGED_ACCESS_NEEDED` / `BLOCKED`: live direct plugin output, 20 unchanged hashes, source-backed v0.2.0 references, authenticated deployment/rollback evidence.

Preserve historical LO alpha P1 disclosure, unverified native hosts, all other editions, 39 JA canonical rules/78 prior Universal normalized candidates, security/privacy and old Release asset immutability. No Marketplace, native-host certification or unrelated router/Composer changes.
