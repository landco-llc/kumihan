# MCP_HANDOFF — source contract only

Source: dedicated branch `feat/zh-hant-v020-research-20261020`, source version0.2.0. Base8b647cc752d7a9bc3db48356fa0ab7b221bb66d6. Final commit/tree are pinned in the PR/task return. Current archive module candidates are pinned by SHA256 in release-manifest.json; they are **not** the live registry/module digest.

Read `plugins/kumihan-ziheng/runtime/context.py`, checks.py, evidence.py, v2 schemas, fixture cases, sources and progressive references. `candidate_rule_ids` is the profile/medium universe; `applicable_rule_ids` satisfies declared conditions but has not been executed; `deferred_rules` carries missing conditions or unused-feature reasons; `selection_only=true`. No candidate count is a pass/fail denominator.

TW excludes004 and HK excludes003 from applicability. Unknown zh-Hant and MO retain neutral scope without TW/HK fallback. HK does not imply written Cantonese. Unselected quote style, vertical writing and ruby remain deferred with reasons. `evidence/synthetic-mcp-contract.json` records four synthetic contexts; no live get_guidance call or production acceptance is claimed.

The separate MCP owner must review registry regeneration inputs (entrypoints, references, rule/source records, standalone inventories and new local helpers), regenerate module/registry digests, preserve candidate/applicable semantics, and run language router, guidance, read-only review and live protocol acceptance in its authorized lane. Source integration and formal release naming remain blocked/pending as described in NEXT_GATE.md.

No writes were made to universal/, running PHP, PR #101/#116/#118, deployed registry or server settings. The running MCP version remains unverified and unchanged by this work. Replacing it requires its own explicit integration/deployment gate; this source branch is not deployment authorization.
