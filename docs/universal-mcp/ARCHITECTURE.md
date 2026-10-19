# KUMIHAN Universal — modular MCP architecture

Status: implementation proposal / Codex execution specification, 2026-10-19
Owner: L&Co. LLC
Repository: https://github.com/landco-llc/kumihan
Target runtime: Lolipop shared hosting, High-Speed plan, LiteSpeed PHP 8.5

## 1. Product decisions

- Publish ONE discoverable integrated plugin, display name **KUMIHAN**. Preserve all original individual product names (e.g. KUMIHAN｜字衡, KUMIHAN｜Accord, KUMIHAN｜Grafía) as module metadata and optional legacy packages.
- Provide ONE common remote MCP service; language packs are independently versioned, added, upgraded, disabled, and rolled back.
- Source of truth is the GitHub repository. Do not invent language packs absent from it. Future parallel implementation is picked up through a generated registry after it becomes available and passes validation.
- A lightweight unified Skill describes the workflow and invokes shared MCP tools; language-specific instructions and rule references are loaded by tool on demand. Local/offline installs may embed pinned module snapshots.
- Do not destroy or silently modify existing standalone language plugins, URLs, immutable tags, or distribution archives. Incremental migration, backwards compatibility, and explicit deprecation planning only.
- The project is free/open-source and requires neither billing nor an admin console for v0.
- Original text must be preserved. Static checks are not visual-rendered evidence. Unknown, unsupported, or unchecked must never be reported as PASS.

## 2. Existing source inventory (snapshot, not an allowlist)

Fresh GitHub main observed 2026-10-19: commit 34988d8068e7b1109330771ced1a19a11e2c4fad.

| Module candidate | Current source | Existing package version |
|---|---|---|
| ja | skills/kumihan and other root Japanese skills | root plugin 0.1.7-preview |
| zh-Hant | plugins/kumihan-ziheng | 0.1.0-preview |
| zh-Hans | plugins/kumihan-zilu | 0.1.0 |
| ko | plugins/kumihan-geuljjaim | 0.1.0 |
| th | plugins/kumihan-th | 0.1.1 |
| ar | plugins/kumihan-ar | 0.1.0 |
| fr | plugins/kumihan-accord | 0.1.1 |
| es | plugins/kumihan-grafia | 0.1.0 |
| pt | plugins/kumihan-compasso | 0.1.0 |
| de | plugins/kumihan-satzbild | 0.1.0 |
| pl | plugins/kumihan-szyk | 0.1.0 |
| vi | plugins/kumihan-nhip-chu | 0.1.0 |
| hi | plugins/kumihan-hi | 0.1.0 |
| id | plugins/kumihan-laras | 0.1.0 |

Notes:
1. The repository currently contains 13 standalone language plugin directories plus root Japanese skills. A present directory is an inventory fact, not proof of behavioral validation or publication.
2. Concurrent language development (including languages not in the above main snapshot) must be discovered by a fresh read at execution. Register only usable, tested modules, never blindly based on website HTML.
3. Do not assume heterogeneous Python runtime scripts are runnable by the PHP service. Use capability flags and port deterministically where necessary.

## 3. Proposed directory layout

    kumihan/
      universal/
        core/
          routing/                  # locale/language/script resolution
          contracts/                # module and tool data schemas
          guidance/                 # base design policies and safe fallbacks
        modules/
          ja/
            module.json
            skills/                 # canonical skill guidance for this language
            rules/                  # text/layout guidance data
            profiles/               # web, document, slides, display, audit
            locales/                # regional variations
            fixtures/
            sources.json
          fr/
            module.json
            ...
          [additional-language-id]/
            module.json
            ...
        registry/
          modules.lock.json         # generated, deterministic, verified
        server/
          php/
            composer.json
            public/index.php       # only publicly accessible entrypoint
            src/
            tests/
        adapters/
          openai/
          claude-code/
          gemini-cli/
        build/
          discover_modules.py
          build_registry.py
          build_packages.py
          validate_modules.py
        dist/                       # generated; no independent manual edits
      docs/universal-mcp/
        ARCHITECTURE.md
        GOAL.md

The canonical source for each language is ONE location. For legacy packages, migrate gradually using a reproducible extraction/mapping process and generate compatible distributions where practical. Avoid copying divergent copies of rules among the four skills.

## 4. Versioned language module contract

Every module MUST contain module.json and a schema-validated fixture suite. Example (illustrative, not an assertion of a deployed version):

    {
      "schema_version": "1.0",
      "module_id": "fr",
      "display_name": "KUMIHAN｜Accord",
      "module_version": "0.1.1",
      "language": "fr",
      "supported_locales": ["fr-FR", "fr-CA", "fr-BE", "fr-CH"],
      "default_locale": null,
      "engine_compatibility": ">=0.1.0 <1.0.0",
      "status": "preview",
      "capabilities": ["guidance", "static_text_review"],
      "entry_skill": "skills/kumihan-accord/SKILL.md",
      "rule_catalog": "rules/catalog.json",
      "fixtures_dir": "fixtures",
      "source_repository_path": "plugins/kumihan-accord"
    }

Contract requirements:
- IDs and locale tags are stable BCP 47-style identifiers; separate the language family from script and region. Normalize aliases without conflating zh-Hant and zh-Hans.
- Version engine, module, and schema separately using semantic versioning or a documented preview convention. Pin tested module versions in a generated registry lockfile with hashes and source commit.
- Registry loader MUST reject unsupported module/schema versions, malformed paths, missing fixtures, non-UTF-8 content, unapproved module IDs, and duplicate IDs.
- A language module is declarative guidance and data, never executable untrusted code loaded per request.
- A region-specific rule is applied ONLY after an explicit region selection or validated regional metadata; never silently treat French France rules as French Canada rules.
- Separate per-medium profiles (web / report / presentation / display-copy / review) from language routing.
- Disabled/preview modules must be accurately surfaced, not implicitly claimed generally available.

## 5. Language selection and mixed-language processing

Resolution order:
1. Explicit user-specified target language/locale or explicit per-span instruction.
2. Explicit source-document/per-element metadata (HTML lang, tagged span, document language, explicitly configured locale).
3. Conservative Unicode script analysis and language-specific lexical evidence.
4. Optional host-model suggestion only as an advisory signal; the PHP server must not require a paid model or external detection API.
5. If evidence is insufficient, return und (undetermined), with needs_review=true. Do not default to Japanese/English or invent confidence.

Rules:
- UI response language is separate from the document's typography language.
- Support independent segments for multilingual paragraphs, mixed CJK/Latin labels, RTL/LTR spans; preserve source offsets and original text.
- Script alone does not uniquely identify Arabic vs Persian, Hindi vs other Devanagari languages, or Russian vs other Cyrillic languages. Han characters alone may be insufficient to select Japanese vs Chinese, or Simplified vs Traditional variants. Short Latin headings often remain ambiguous.
- Return confidence levels high/medium/low/undetermined with evidence and provenance, not arbitrary confidence percentages.
- Preserve protected spans such as code, URLs, names, prices and quoted source. No implicit translation and no silent editorial rewriting.
- When fallback is needed, use only safe shared rules and label unresolved locale-dependent checks.
- Run each language module on eligible segments; shared design rules operate over the complete artifact. Never apply one language's punctuation fixes to other-language spans.

Illustrative request:

    {
      "text": "日本語の見出し / Bonjour !",
      "language": "auto",
      "target_locale": null,
      "medium": "web",
      "mode": "review",
      "metadata": {"html_lang": null}
    }

Response MUST include module provenance, segment-level routing, needs_review/unchecked distinctions and source_unchanged=true.

## 6. Common MCP tools (stable contract)

Expose few general tools, NOT one tool for each language:
- kumihan_list_languages: available modules, supported locales, capabilities, versions, preview/disabled states.
- kumihan_detect_language: segments, script, candidate language, confidence category, evidence, provenance, ambiguities.
- kumihan_get_guidance: resolved module guidance for medium/mode/locale and version, with source/provenance.
- kumihan_review_text: deterministic checks when rules are executable in the PHP runtime; returns findings with IDs, severity, evidence, module version and checked/not-checked states.
- Optional subsequent kumihan_review_layout, only with actual supplied layout/render evidence. Never claim browser rendering was observed based on textual guidance.

The MCP server is text-only for v0. Tool schemas and descriptions remain small and stable as modules are added, allowing remote rule updates without re-installing a unified plugin. No direct file editing or deployment tool is exposed publicly.

## 7. Release and update semantics

1. Update a single language under universal/modules/[id] and its independent tests; issue a patch/minor module version without requiring other modules to change.
2. Add language by adding valid module data + fixtures + manifest; generation discovers it without core code changes.
3. CI validates schema, hashes, optional source/license constraints, regression tests, build determinism, and all cross-language routing cases.
4. On approved main merge/tag: build immutable versioned artifacts; generate modules.lock.json; atomically publish a verified registry snapshot to Lolipop. Keep prior manifests for rollback.
5. Fetch runtime guidance from the MCP server so updated language rules can become usable by an already-connected unified plugin when MCP tool contracts remain unchanged.
6. Caveat: updating files bundled inside an installed Skill/plugin package still requires its normal update/reinstall mechanism. Server-side updates do NOT silently replace installed SKILL.md files. Publish a regenerated package if instructions or packaged assets change.
7. Older individual language packages remain available during transition, and independent releases retain their version numbers and names.
8. If the remote service is offline, report offline/unavailable accurately. If an optional bundled snapshot exists, label it pinned/offline and expose its version.

## 8. Lolipop PHP deployment constraints

Hosting: existing Lolipop High-Speed shared hosting, LiteSpeed edition PHP 8.5. New VPS, long-running Node process, DB, Redis, queue, scheduled daemon and paid APIs are NOT assumed.

- Prioritize official modelcontextprotocol/php-sdk, composer-pinned and tested with PHP 8.5, using an appropriate stateless Streamable HTTP request lifecycle.
- New MCP protocol revision 2026-07-28 changes initialization and transport. Also consider older 2025-11-25 clients. Use the SDK's supported revision matrix and test real clients; do not implement ambiguous single-version assumptions.
- Verify SDK dependency compatibility, PHP extensions (including intl/mbstring if needed), POST JSON-RPC, required response headers, reverse proxy/WAF behavior, timeout/body-size limits, origin checking and TLS using an actual Lolipop PoC.
- Keep composer/vendor, module source and private configuration outside document root if permitted; otherwise explicitly deny access and test. Expose only the intended MCP entrypoint.
- Minimum controls: HTTPS, valid origin handling, request length limits, basic rate controls, no arbitrary paths, no arbitrary process calls, no user-code execution, no persistent raw-content logs. Public access and abuse protection must be assessed before release.
- No claim of live deployment, supported transport, or client compatibility until a test record exists.

## 9. Definition of done / acceptance evidence

A. Every existing *eligible* main-branch language is inventoried and either registered with capabilities or documented as blocked with reason; no silent omission.
B. Module addition test demonstrates a new fixture module appears through kumihan_list_languages without core changes.
C. Editing one language's test rule does not change other module checksums/artifacts; module-level rollback is verified.
D. Locale selection precedences tested, including zh-Hant/zh-Hans, fr-FR/fr-CA, pt-PT/pt-BR, ambiguous short text, mixed Japanese/English, Arabic RTL + Latin, Hindi/Devanagari ambiguity, Cyrillic ambiguity, and unknown languages.
E. Source integrity and read-only reviews verified; generated output reports static-only vs actual-render observations.
F. PHP 8.5 / Lolipop PoC and genuine MCP initialization/tool call pass before calling a hosted release supported.
G. ChatGPT/Codex, Claude Code and Gemini CLI integrations are tested separately. General Claude/Gemini chat support must not be inferred from CLI tests.
H. Automated packaging outputs OpenAI plugin + Claude Code + Gemini CLI adapters, with versioned ZIP assets where appropriate; name KUMIHAN for universal plugin, not a union of display names.
I. No publishing, merging or production DNS/credential work is asserted complete unless actual evidence and required Owner approvals exist.

## 10. Execution stages

Use the accompanying GOAL.md for a cohesive W00-W09 group executed via /goal. No repeated human MD/ZIP handoff between internal Work stages. Support independent validation, lightweight reviews (open source, no heavy governance), and stop only at genuine permission/credential/hosting/public-release gates.

Relevant specs:
- https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- https://github.com/modelcontextprotocol/php-sdk
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/concepts/plugins
