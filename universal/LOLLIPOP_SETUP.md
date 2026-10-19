# KUMIHAN MCP — Lolipop High-Speed / LiteSpeed PHP 8.5 setup

Status: OWNER HOST SETUP ON HOLD due to Lolipop security maintenance on 2026-10-19. No hosting-side changes performed. This document is a prepared runbook, not evidence of a working MCP endpoint.

Designated production hostname: **mcp-kmhn.landco.co.jp** (user decision 2026-10-19).
Planned endpoint: **https://mcp-kmhn.landco.co.jp/mcp** (NOT LIVE / SSL AND DNS NOT VERIFIED).
Versioned machine-readable target: [deployment/target.json](deployment/target.json).

## Current external blocker (2026-10-19)

Lolipop's official emergency notice (https://lolipop.jp/info/news/8232/) reports that all user control-panel functions have been temporarily unavailable since 2026-10-19 12:43 JST. New subscriptions and WebDAV are also affected, while existing website and mail services continue. The provider has not confirmed a restoration time. Do not repeatedly attempt domain/SSL/config changes until the maintenance notice indicates recovery. Do not attempt workarounds via alternative admin APIs.

Once recovered, follow the numbered checklist below, then update the deployment target flags ONLY after direct evidence. GitHub CI and local PHP tests may continue independently.

## 0. Hosting assumptions

Existing **Lolipop rental server, High-Speed plan**, LiteSpeed PHP **8.5** as stated by Owner. Shared hosting: NO root access and NO new permanent Node.js process. MCP HTTP can run per PHP request. Composer dependencies can be built in CI/dev and uploaded as a complete vendor directory if CLI composer/PHP differs from the web runtime.

## 1. Owner settings in Lolipop control panel

1. **Subdomain**: under サブドメイン設定 → 新規作成 register **mcp-kmhn.landco.co.jp** (subdomain label `mcp-kmhn` under `landco.co.jp`). Confirm `landco.co.jp` is registered as an independent domain in the same Lolipop account and verify DNS authority; if not, arrange domain/DNS association first. Set the 公開（アップロード）フォルダ to a dedicated location such as `mcp-service/public` *only after* checking actual account folder mapping. Expose ONLY the PHP front controller, not the full repository.
   - https://lolipop.jp/manual/user/doku-subsett//
2. **SSL**: under 証明書お申し込み・設定 select the new subdomain and activate 独自SSL（無料）. Confirm HTTPS certificate and URL. Eligibility may depend on the authoritative DNS and whether the main domain is also hosted there.
   - https://lolipop.jp/manual/user/ssl-free-order/
   - https://support.lolipop.jp/hc/ja/articles/360049142333
3. **PHP version**: in PHP設定 verify the NEW subdomain uses LiteSpeed PHP 8.5. A website domain's PHP setting is not proof of this new subdomain's effective runtime.
4. **SSH**: in SSH click SSHを有効にする. Official SSH host ssh.lolipop.jp, port 2222, account shown in control panel; no root. SSH credentials must NEVER be pasted into chat or checked into GitHub.
   - https://lolipop.jp/manual/user/ssh/
5. **WAF**: leave enabled first. If request POSTs with Content-Type application/json / MCP-Protocol-Version or long response headers are blocked, capture status/time without raw user text and isolate the rule. Avoid persistent global disable.
6. **DNS**: confirm the subdomain resolves to the Lolipop server and free SSL can be issued. Allow for propagation.

## 2. Secure server folders

Illustrative account filesystem hierarchy (actual Lolipop home path depends on account):

    <account-root>/
      mcp-service/
        public/            # ONLY folder mapped as the subdomain public folder
          index.php
          .htaccess
        src/               # NOT publicly served
          Registry.php
          LanguageRouter.php
          UniversalTools.php
        vendor/            # NOT publicly served
        runtime/           # NOT publicly served
          config.php       # copy from config.production.example.php; do not commit
          registry.json    # generated from current repo
          sessions/        # writable by web PHP, not publicly served
        composer.json

The artifact built by CI contains vendor/ and registry.json but NOT your real config.php or SSH credentials. After maintenance and host preparation, copy `runtime/config.production.example.php` to private `runtime/config.php` (do NOT copy the localhost-only `config.example.php` to production). Expected production configuration:

    <?php
    return [
      'host' => 'mcp-kmhn.landco.co.jp',
      'allowed_origins' => [],
    ];

If browser cross-origin use becomes necessary, list approved HTTPS origins explicitly instead of allowing '*'. Public host must match the incoming Host header; test with real TLS/reverse proxy.

Create the sessions directory as writable by PHP; avoid world-writable 777. PHP framework integration uses a FileSessionStore and FileSessionLock for pre-2026-07-28 handshake clients; recent stateless calls do not need those sessions.

## 3. Deploy and verify

1. In CI build the current registry from GitHub language packages. Check that listed module IDs and versions match the merged source, and that preview/unsupported states are accurate.
2. Build the official MCP PHP SDK v0.9.x vendor using Composer in a reproducible CI/dev environment. Before production pin composer.lock and run Composer advisory audit; upstream SDK is pre-1.0.
3. Upload server/public, server/src, server/vendor, server/runtime/registry.json and private config to the non-public/public directory structure shown above. When upgrading, make a versioned staging copy and switch after smoke tests; retain last-known-good artifact.
4. Verify https://mcp-kmhn.landco.co.jp/mcp accepts MCP Streamable HTTP initialization and tools/list from an actual client. A browser opening the endpoint with GET is NOT a valid MCP tool-function test.
5. Verify the exact target clients separately: ChatGPT/Codex, Claude Code and Gemini CLI. Compatibility with CLI does NOT prove compatibility with every consumer chat UI.
6. Verify the response and error headers, Origin / DNS-rebinding controls, WAF, 4xx/5xx, request size 64 KiB cap, request concurrency, session persistence across PHP workers, and hosting timeouts. Never log full user content.
7. Record the tested domain, PHP extensions, current revision, SDK version, CI artifact hash, rollback artifact and Owner approval before publishing/installing plugin packages.

## 4. Decisions / TODO

- Production domain / subdomain: **mcp-kmhn.landco.co.jp** selected. Registration and live DNS/SSL not yet performed; blocked by 2026-10-19 provider maintenance.
- DNS and HTTPS / SSL setup: OWNER, after provider maintenance ends. Confirm TLS for exact hostname and path `/mcp`.
- SSH credentials: OWNER, keep in account manager; do not send to GPT.
- Live deployment and public release: pending Owner authorization + real host smoke.
- Billing/paywalls: NOT in first release. Initial call budgets may be applied to prevent abuse, but per-user usage metering needs authentication/identity design and a privacy policy; do not rate-limit all ChatGPT users as one IP.
- Hosting cost: existing plan. No extra VPS / data store needed for this first implementation.

## 5. Definition of production ready

PHP 8.5 + SDK Composer dependencies resolved; HTTPS, WAF and stateless/handshake protocol lifecycle verified on the actual domain; session storage safe; source integrity documented; at least one real client can list modules and retrieve guidance; deployment rollback documented. Until then status remains STAGING / NOT DEPLOYED.

## 6. Rollout gates and release sequence (pending provider maintenance)

- **G0 — external provider:** Official restoration confirmed; control-panel functions available again. The maintenance block is informational; do not infer exact restoration time.
- **G1 — domain:** Owner creates the `mcp-kmhn` subdomain under `landco.co.jp`; DNS verified at the actual account.
- **G2 — TLS and runtime:** Free SSL active for the exact hostname, LiteSpeed PHP 8.5 active on this domain, SSH setup confirmed. The public folder exposes no configuration/registry/vendor files.
- **G3 — staging upload:** Install the CI-built staging artifact from a reviewed commit. `runtime/config.php` remains private with `host=mcp-kmhn.landco.co.jp`.
- **G4 — live transport:** Genuine MCP initialize, tools/list, tools/call, session and 2026-07-28 compatibility tested over the public HTTPS URL; WAF and errors reviewed.
- **G5 — client adapters:** Generate versioned plugin packages using `python3 universal/tools/build_adapters.py --endpoint https://mcp-kmhn.landco.co.jp/mcp` **only after G4** and test actual OpenAI, Claude Code and Gemini CLI connections separately.
- **G6 — publication:** Owner approval, pinned dependencies/audit and release checklist before declaring production or publishing to directories.

Recommended completed-check wording: `G1: VERIFIED YYYY-MM-DD JST (evidence link)`. Until an item is directly checked, mark it `NOT_CHECKED`; never mark as passed because a later item was planned.

### Rate limits (deferred)

Call-count quotas are a product decision, not a prerequisite for DNS creation. For v0 protect traffic with input size caps and abuse controls. Per-user quotas require a reliable auth/account identity; do NOT simply count all traffic from ChatGPT or other shared-host IPs as one user. Keep initial public service rate policy separate from module rules.
