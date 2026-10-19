# /goal — KUMIHAN Universal (modular multilingual MCP)

Status: instruction for autonomous Codex Cloud / Codex App implementation
Repository: https://github.com/landco-llc/kumihan
Starting design branch: feat/universal-modular-mcp-rfc
Primary specification: docs/universal-mcp/ARCHITECTURE.md

## Mission

Implement ONE installable **KUMIHAN** unified plugin backed by a shared stateless MCP server and independent multilingual rule/Skill modules. Each language must be independently addable, upgradeable, testable, disableable and rollback-able. Support all eligible languages on the latest source branch, not only a hardcoded 2026-10-19 list.

Do not merely return a plan. Execute W00–W09 as a contiguous, bounded Work group; dispatch independent subtasks in parallel when safe. Do not ask a human to manually re-attach MD/ZIP to the next Work. Persist continuation instructions, manifests and evidence in this repository / PR.

## Execution environment and permissions

- Preferred: Codex Cloud or Codex App, on the GitHub repo landco-llc/kumihan.
- Start from the latest remote main and this design branch, avoid stale assumptions. Create an implementation branch/PR (new PR or extend the design PR safely). Never force-push main, rewrite release tags, alter published ZIPs, or silently merge.
- Read README, existing AGENTS policy if present, docs/development.md, root skills, all standalone plugins, existing workflows and this Architecture before changes. Inventory recent/in-flight language PRs and include merged ones. Mark others pending, not completed.
- Use Python build scripts for deterministic packaging if suitable and PHP 8.5 on server runtime. Avoid local Codex CLI via Remote Desktop Commander when Cloud/App can do the work.
- The user has specified existing Lolipop rental server, High-Speed plan, LiteSpeed PHP 8.5. Do not migrate hosting or incur new paid dependencies without approval.
- Public artifact release, credential use, deploying to the real hosting account, changing DNS, and installing into user accounts require proper Owner approval. Work independently on all non-blocked implementation and tests.

## Work group

### W00 — Fresh read / baseline

Read the actual current repository, main and open language-module PRs, release inventories, installed skill structures, manifest schemas, CI and constraints. Record exact HEAD, file mapping, existing rule formats, source-of-truth findings, optional assets/icons and package versions. Preserve the original Japanese root and existing 13+ standalone packs. Do not rely solely on this document's dated snapshot.

Deliver: BASELINE.md (commit, eligible module inventory, pending modules, observed limitations, blockers).

### W01 — contracts / registry

Implement language-module schema and versioned manifest, schema validation, deterministic discover/generate registry, content hashes, engine compatibility, status/capabilities and locale tags. Add at least one fixture module test that proves discovery requires no core-code edit.

Deliver: automated schema tests and registry generation proof.

### W02 — canonical migration / compatibility

Build incremental extractors/mappings to canonical universal/modules/{module_id} from existing source locations. Preserve each package's actual rule provenance, regional variants, sources and licensing. Where scripted text validation depends on Python or a host, mark guidance_only or unsupported until deterministic PHP checks exist. Do not pretend every module is equally complete. Ensure existing standalone packaging remains stable, ideally by generation rather than duplicated manual rule edits.

Deliver: module inventory with individual versions and feature support; reproducible sync scripts and unchanged legacy release snapshots.

### W03 — conservative language router

Implement explicit selection > element/doc metadata > evidence-based detection > undetermined. Distinguish UI language from content language, locale/region from script, and per-segment routing from whole-document review. Return confidence categories and evidence. Avoid false positives for short Latin, Han-only, Arabic-family, Cyrillic-family, Devanagari and Bengali-family cases; do not infer regional punctuation styles absent locale signals.

Deliver: deterministic routing unit tests for mixed JA/EN, Chinese scripts, French locales, Portuguese locales, Arabic RTL, Hindi, Bengali/Cyrillic ambiguity and unsupported languages.

### W04 — MCP server / PHP 8.5

Create stateless Streamable HTTP server for Lolipop using official PHP SDK if compatible. Implement stable small tool surface:
- kumihan_list_languages
- kumihan_detect_language
- kumihan_get_guidance
- kumihan_review_text
Keep layout review for the stage when actual artifact evidence is available.

Verify JSON-RPC request/response, official MCP lifecycle revisions required by supported clients, correct tool schemas, no long-running server process/DB, no arbitrary file read/write, secure public endpoint boundaries, request limits and no raw-text logging. Document PHP 8.5 extension/Composer requirements. If SDK does not satisfy real client or hosting constraints, record objective evidence and use the smallest standards-compliant alternate PHP implementation, not an unverified success claim.

Deliver: server tests, example requests/responses, composer lockfile and staging deployment instructions.

### W05 — distribution adapters / runtime Skill

Create a single unified OpenAI plugin with display name KUMIHAN and the required logo metadata, small Skill launcher and remote MCP tool configuration. Create tested client-appropriate packages for Claude Code and Gemini CLI. Do not assume that same ZIP works across all three. Unified Skill reads rules via remote MCP so language module updates are available without reinstalling as long as tool contracts remain compatible. Document that changes to installed bundled SKILL.md still require updating installed package.

Deliver: three tested distribution adapters, build script, package version and asset manifests.

### W06 — test and compatibility matrix

Test changing only FR module without changing JA/KO modules; add a synthetic new language through module.json and fixtures without changing core; test per-module rollback. Test all existing registered languages with source-preserving read-only review; evaluate ambiguity, mixed scripts, locale correctness, stable output, no hallucinated rendered screenshots, and offline/unknown behavior. Run regression suites for legacy packages and reproducible build twice.

Deliver: test matrix and pass/fail evidence; do not suppress genuine FAILs.

### W07 — hosting PoC and client integration

Prepare a Lolipop-compatible deployment bundle and instructions that keep PHP sources outside public directory where possible. Test locally/CI first, and test on the actual authorized Lolipop PHP 8.5 environment only when access is available. Diagnose WAF, redirects, CORS/Origin, TLS, transport protocol, lifecycle and request limits. Connect real clients individually: ChatGPT/Codex, Claude Code, Gemini CLI where accessible. If credentials or host access are missing, mark REAL_HOST_NOT_TESTED and continue other Work.

Deliver: compatibility matrix with explicit OBSERVED / NOT_CHECKED / BLOCKED labels, deployment plan, health check and rollback plan.

### W08 — documentation / release packaging

Document architecture and public client installation paths, one KUMIHAN plugin plus its per-language language-pack status list. Maintain existing language URLs and names; do not silently replace published assets. Generate module inventory table and migration guides. Keep updated descriptions accurate: not all APIs/hosts necessarily share a single install procedure.

Deliver: documentation PR and reproducible release candidate artifacts, not an invented public release.

### W09 — independent light review / Owner Gate

Review routing safety, provenance, source integrity, new-language discoverability, compatibility, distribution, PHP host constraints and release quality. Fix actionable findings, rerun tests, produce release-readiness summary. Stop only for verified blockers or requested Owner decisions such as live server credentials, public publishing, or merging.

Deliver: PR(s), work reports, test evidence, deployment checklist and explicit GO / NO-GO.

## Acceptance checks

- Every eligible module can be added/updated/pinned/rolled back independent of core and other modules.
- New module is discoverable by list_languages after manifest/fixture addition with no core edit.
- User-selected languages and document-tagged spans beat automatic detection; ambiguity yields undetermined instead of silent wrong guidance.
- No silent cross-language copy rewriting or applying regional conventions by guessing.
- All installed bundled Skill updates are distinguished from live MCP rule updates.
- PHP 8.5 server runs as short-lived requests with no special daemon. Real-host success is claimed only after direct evidence.
- Unified plugin identity remains KUMIHAN; author remains L&Co. LLC; original independent language branding continues.
- All tests and generated files are source-backed; no obsolete main/stale tag overwrite.
- Test each platform separately before claims of support or public release.

## Start instruction for Codex

/goal

Repository: landco-llc/kumihan
Design branch: feat/universal-modular-mcp-rfc
Read docs/universal-mcp/ARCHITECTURE.md and docs/universal-mcp/GOAL.md.
Execute W00 through W09 as one autonomous Work group. Prefer Codex Cloud/App. Keep a Draft PR and store all evidence in the repository. Never require human MD/ZIP reattachment between Work stages. Implement safe work even when host credentials are missing. Do not claim live deployment or public distribution without evidence and approval.
