# KUMIHAN MCP — Lolipop High-Speed / LiteSpeed PHP 8.5 setup

Status: Owner operations checklist; no host actions have been performed by the assistant.

## 0. Hosting assumptions

Existing **Lolipop rental server, High-Speed plan**, LiteSpeed PHP **8.5** as stated by Owner. Shared hosting: NO root access and NO new permanent Node.js process. MCP HTTP can run per PHP request. Composer dependencies can be built in CI/dev and uploaded as a complete vendor directory if CLI composer/PHP differs from the web runtime.

## 1. Owner settings in Lolipop control panel

1. **Subdomain**: choose a dedicated host, e.g. mcp.YOUR-OWN-DOMAIN.example (replace placeholder; no real hostname is chosen yet). Under サブドメイン設定 → 新規作成, set 公開（アップロード）フォルダ to a dedicated path such as mcp-service/public. Do not point the entire repository to web root.
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
          config.php       # copy from config.example.php and edit 'host'
          registry.json    # generated from current repo
          sessions/        # writable by web PHP, not publicly served
        composer.json

The artifact built by CI contains vendor/ and registry.json but NOT your real config.php or SSH credentials. Create runtime/config.php privately with actual dedicated subdomain and no wildcard:

    <?php
    return [
      'host' => 'mcp.YOUR-OWN-DOMAIN.example',
      'allowed_origins' => [],
    ];

If browser cross-origin use becomes necessary, list approved HTTPS origins explicitly instead of allowing '*'. Public host must match the incoming Host header; test with real TLS/reverse proxy.

Create the sessions directory as writable by PHP; avoid world-writable 777. PHP framework integration uses a FileSessionStore and FileSessionLock for pre-2026-07-28 handshake clients; recent stateless calls do not need those sessions.

## 3. Deploy and verify

1. In CI build the current registry from GitHub language packages. Check that listed module IDs and versions match the merged source, and that preview/unsupported states are accurate.
2. Build the official MCP PHP SDK v0.9.x vendor using Composer in a reproducible CI/dev environment. Before production pin composer.lock and run Composer advisory audit; upstream SDK is pre-1.0.
3. Upload server/public, server/src, server/vendor, server/runtime/registry.json and private config to the non-public/public directory structure shown above. When upgrading, make a versioned staging copy and switch after smoke tests; retain last-known-good artifact.
4. Verify https://mcp.YOUR-OWN-DOMAIN.example/mcp accepts MCP Streamable HTTP initialization and tools/list from an actual client. A browser opening the endpoint with GET is NOT a valid MCP tool-function test.
5. Verify the exact target clients separately: ChatGPT/Codex, Claude Code and Gemini CLI. Compatibility with CLI does NOT prove compatibility with every consumer chat UI.
6. Verify the response and error headers, Origin / DNS-rebinding controls, WAF, 4xx/5xx, request size 64 KiB cap, request concurrency, session persistence across PHP workers, and hosting timeouts. Never log full user content.
7. Record the tested domain, PHP extensions, current revision, SDK version, CI artifact hash, rollback artifact and Owner approval before publishing/installing plugin packages.

## 4. Decisions / TODO

- Production domain / subdomain: OWNER TO CHOOSE.
- DNS and HTTPS / SSL setup: OWNER.
- SSH credentials: OWNER, keep in account manager; do not send to GPT.
- Live deployment and public release: pending Owner authorization + real host smoke.
- Billing/paywalls: NOT in first release. Initial call budgets may be applied to prevent abuse, but per-user usage metering needs authentication/identity design and a privacy policy; do not rate-limit all ChatGPT users as one IP.
- Hosting cost: existing plan. No extra VPS / data store needed for this first implementation.

## 5. Definition of production ready

PHP 8.5 + SDK Composer dependencies resolved; HTTPS, WAF and stateless/handshake protocol lifecycle verified on the actual domain; session storage safe; source integrity documented; at least one real client can list modules and retrieve guidance; deployment rollback documented. Until then status remains STAGING / NOT DEPLOYED.
