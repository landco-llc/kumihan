# START_HERE — Universal MCP 日本語モジュールをv0.2.0へ更新

Status: AUTHORIZED / NOT_DEPLOYED. This is an execution handoff, not a claim of live update.

- Execution: Codex Cloud / Codex App in `landco-llc/kumihan`.
- MCP management: [Issue #127](https://github.com/landco-llc/kumihan/issues/127).
- Prerequisite GitHub public release: [Issue #126](https://github.com/landco-llc/kumihan/issues/126), immutable `v0.2.0` tag and 15 verified ZIPs.
- Control branch: `control/universal-ja-v020-20261020`, based on PR #101 source HEAD `5d32ea64618e33a171705363c223fe43060c31e1`.
- Workgroup: `universal/deployment/ja-v020-20261020/WORKGROUP.md`.
- Baseline and 20-language digests: `universal/deployment/ja-v020-20261020/MODULE_CONTRACT.json`.
- Live connected endpoint: `https://mcp-kmhn.landco.co.jp/mcp` (existing host, not to be re-created).

## Execute W00–W07

Fresh Read repository, Draft #101/#116/#118, existing live MCP and source Release. Read WORKGROUP and MODULE_CONTRACT before implementation. Use a fresh feature branch off PR #101, preserving all parallel work and all other language source/digests. Only Japanese v0.2.0 module data and backwards-compatible source-backed guidance references are approved. Existing `getGuidance` only returns capped entry SKILL + rule list: implement bounded allowlisted Japanese v0.2.0 research/reference delivery so the update is **substantive**, not just a version label. Never return 78 KB claim ledger verbatim on every request or introduce a new data-writing MCP tool.

Run registry/PHP8.5/SDK/4-tool tests. Create a Draft PR stacked on #101 with minimal diff, exact source-tag provenance, 21-module count, 20 unchanged source hashes and rollback/deployment plan.

Owner authorized the JA production reflection if—and only if—actual hosting/private path, credentials, current live file identities, safe backups/rollback, staged PHP/registry and read-only test evidence permit it. Obtain private credentials only through already-authorized secure operator channels; never paste credentials into GitHub or chats. If Cloud cannot access the actual host, finish source/CI and output a precise private operator deployment packet; mark live `ACCESS_NEEDED` rather than claiming it occurred.

When deployed, call the **live connected** Universal MCP list_languages/get_guidance/review_text/detect_language and verify: JA `module_version=0.2.0`, v0.2.0 typography references actually exposed, 21 modules, all other 20 module hashes unchanged, original Unicode unchanged, still guidance-only/not-checked for unrendered checks. Separately retain known Chinese punctuation router problem; no unrelated fix.

Report final source PR, source SHA/TREE, test/CI, registry snapshot, live before/after module digests, result or exact blocker, rollback evidence, residual native claims to Issue #127/#119. Marketplace submission remains outside scope. Do not re-publish the Japanese GitHub Release or reset another language's version.
