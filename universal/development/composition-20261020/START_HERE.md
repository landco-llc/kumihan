# START HERE — KUMIHAN Universal Multilingual Composition Core

Status: **CONTROL_PACKET_READY / NOT_LAUNCHED**. Documentation-only preparation by ChatGPT. Code has not been implemented or product-tested by this packet.

- Repo: landco-llc/kumihan
- Workspace: Codex Cloud or Codex App, **cloud-first**. No requirement to run a local Codex CLI or remote desktop agent.
- Select branch: feat/universal-composition-core-20261020
- Stacked Draft PR base: feat/universal-mcp-php-runtime (PR #101), NOT main and NOT #118's side branch
- Entrypoint: universal/development/composition-20261020/GOAL.md
- Canonical design source: reference/SPEC_SOURCE.md + reference/composition.schema.json.gz + reference/PORTS_AND_LIFECYCLE.md
- Design-only acceptance cases: reference/ACCEPTANCE_AND_ROADMAP.md
- Primary external standards only: reference/PUBLIC_SOURCES.md
- Original research archive remains in the project's private Google Drive research folder; all code-required contract material is included here without private source references.

## Copyable Codex Cloud / App startup instruction

/goal

Repo: landco-llc/kumihan
Working branch: feat/universal-composition-core-20261020
Read universal/development/composition-20261020/START_HERE.md and GOAL.md fully, then execute W00–W08 in the documented groups autonomously.
Use the checked-in exact approved schema reference after gzip decompression and SHA-256 verification.
Fresh Read current HEAD, AGENTS, PR #101 and parallel PR #118/#116/#120/#122/#123; avoid shared-file collisions.
Implement source-preserving contract, conservative cross-language resolution and read-only review within isolated source + tests; keep legacy MCP interface untouched.
Run tests, produce RESULT.md, TEST_REPORT.md, NEXT_GATE.md and EVIDENCE_MANIFEST.json; update the same Draft PR.
No production deployment, published code, marketplace submission, main merge, tag, release, credentials or other repos.
Stop only at a factual blocker or final Owner Gate. Report bounded verified evidence without treating every P-case as passed.

## Quick input integrity

The approved uncompressed Schema checksum is:
14d9226833c8ff1af8a92f8da56de4c852f003e87803f78c3ec8bf45c8c75cda

A local worktree verification (no source modification) can run:

~~~sh
gzip -dc universal/development/composition-20261020/reference/composition.schema.json.gz | sha256sum
~~~

The result must equal the checksum above. The reference is design version 0.1.0-design.1 and not an already supported production API.

## Permission boundary

The Owner approved implementation of the bounded W00–W08 candidate and tests in a Draft PR. Approval does **not** include the public MCP server, language-skill packages, deployment config, release process, or production data. Publishing any new public API is a separate gate.

## Tracking

GOAL.md has the full work and criteria. At completion use the current branch to write:

- RESULT.md
- TEST_REPORT.md
- NEXT_GATE.md
- EVIDENCE_MANIFEST.json

Any pre-existing base failure remains documented separately from new regressions. The last successful Work ID must be explicit if stopped early.
