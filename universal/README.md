# KUMIHAN Universal MCP — phase 1 runtime

Status: **implementation candidate, not deployed**. GitHub source of truth: landco-llc/kumihan.
Production hostname **mcp-kmhn.landco.co.jp** selected on 2026-10-19; planned endpoint **https://mcp-kmhn.landco.co.jp/mcp**. GitHub Actions independently verified public DNS and TLS 1.3 for the hostname ([evidence](https://github.com/landco-llc/kumihan/actions/runs/39246702661)). The real document root, PHP 8.5 hosting runtime, SSH/SFTP and live MCP endpoint are still NOT VERIFIED. The prior maintenance blocker no longer prevents Owner configuration. See [target manifest](deployment/target.json).
Specification: [modular architecture proposal](https://github.com/landco-llc/kumihan/pull/87) (separate draft PR until merged).

## Purpose and supported behaviors

One common MCP server uses independent, versioned language modules generated from the existing standalone KUMIHAN skills. Each module preserves its original name, version, rule catalog, provenance and source Skill. Adding a new language requires only a new declarative entry in universal/languages.json and a source skill package, not a core/server code edit.

The current map tracks the 20 standalone languages in the source repository at the observed main snapshot plus Japanese (21 modules). Regenerate after integrating new main changes; new packages absent from the map must be inventoried and added, not silently claimed supported.

Four read-only MCP tools:

1. kumihan_list_languages: list version, ID, supported locales, source hash and preview status.
2. kumihan_detect_language: explicit locale > document metadata > conservative Unicode script signal > undetermined; byte-offset script spans included.
3. kumihan_get_guidance: source-backed Skill and rule candidates, medium and review mode, module version/hash.
4. kumihan_review_text: route and provide review candidates; do not modify input or report checks as PASS without implementation.

Important: phase 1 provides guidance, not a completed typography validator. Rendering and real client behavior remain NOT_CHECKED. Regional punctuation is never silently inferred. Generic Latin, Han, Arabic-family, Devanagari and Cyrillic scripts do not uniquely identify a language.

## Build and tests

From the repo root:

    python3 -m unittest discover -s universal/tests -v
    python3 universal/tools/build_registry.py
    python3 universal/tools/build_registry.py --check

From universal/server on a PHP 8.5 development machine (Composer is needed for SDK HTTP integration):

    composer install --no-dev
    php -l src/Registry.php
    php -l src/LanguageRouter.php
    php -l src/UniversalTools.php
    php -l public/index.php
    php tests/smoke.php

The generated universal/server/runtime/registry.json is the complete deployment data snapshot. It is NOT committed and can be regenerated from each new source commit. IDs and aliases are BCP47-style and modules are pinned by per-module SHA-256. A module version update changes that module's digest only.

### Local SDK HTTP smoke

Copy runtime/config.example.php to runtime/config.php (test only), then:

    php -S 127.0.0.1:8989 -t public

Send a handshake-era initialize POST to http://127.0.0.1:8989/index.php; use the returned Mcp-Session-Id for subsequent requests. CI automates this check with the official MCP PHP SDK. For modern protocol clients the SDK also supports the 2026-07-28 stateless protocol era. The HTTP front controller supports both. On real hosting use /mcp through .htaccess rewrite.

## Lolipop deployment

See [LOLLIPOP_SETUP.md](LOLLIPOP_SETUP.md). Existing rental server: Lolipop High-Speed plan, LiteSpeed PHP 8.5.

- Keep server/vendor, server/src, server/runtime (config, registry, sessions) OUTSIDE subdomain public upload folder. Only server/public is web-exposed.
- Production config host MUST be explicitly set to the dedicated DNS name. Origin wildcard is rejected.
- SDK uses a shared, file-based session directory for handshake-era clients so PHP workers do not lose MCP sessions; modern-era calls are stateless.
- HTTPS/TLS, remote MCP compatibility, WAF and shared-host behavior must be proven on the actual service before release.
- Do not publish a live endpoint or claim ChatGPT/Claude/Gemini compatibility solely from CI.
- No database, daemon, paid model API or customer billing is assumed.
- No raw request text is logged by our app. Body limit is 64 KiB; later fair-use metering must be privacy-preserving, not ad-hoc IP paywalls.

## Deployment blocker

Production hostname is selected but NOT provisioned; hosting deployment authorization and direct server access are not supplied. No credentials are stored. Do not install private config from the public repo. Do not merge or publish the integrated plugin until end-to-end evidence is available.
