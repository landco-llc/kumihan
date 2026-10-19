# KUMIHAN Universal MCP — Lolipop / kmhn deployment runbook

Status: **DNS+TLS VERIFIED, PUBLIC FOLDER CONFIRMED, MCP NOT DEPLOYED** (2026-10-19).
Owner: L&Co. LLC. Implementation PR: https://github.com/landco-llc/kumihan/pull/101

## Locked parameters

| Item | Confirmed state |
|---|---|
| Hosting | Lolipop shared rental server, High-Speed |
| Target runtime | LiteSpeed PHP 8.5 (effective runtime not independently checked) |
| Hostname | mcp-kmhn.landco.co.jp |
| MCP URL | https://mcp-kmhn.landco.co.jp/mcp |
| Subdomain 公開（アップロード）フォルダ | **kmhn** (Owner confirmed 2026-10-19) |
| DNS/TLS | GitHub Actions TLS 1.3, hostname/certificate PASS; certificate expires 2027-01-17 |
| PHP MCP | 21-module CI-tested preview; NOT DEPLOYED |

TLS evidence: https://github.com/landco-llc/kumihan/actions/runs/39246702661
Official hosting docs: https://lolipop.jp/manual/user/doku-subsett// and https://support.lolipop.jp/hc/ja/articles/360048391094 .

**Do not recreate the subdomain, reissue SSL, or change the configured kmhn document root.**

## Security boundary — critical

Lolipop FTP root may itself be served from the default Lolipop-hosted domain, even when the kmhn subdomain is mapped to a subfolder. A directory next to kmhn **inside FTP root is NOT automatically private**.

The original universal/server/public/index.php expects src/, vendor/ and runtime/ in its server parent directory. Uploading that file directly into FTP-root/kmhn and keeping src/vendor/runtime in FTP-root is UNSAFE. Use a small public bootstrap that includes the original entrypoint from a verified non-Web absolute path.

Recommended ROLES (the actual SSH account paths are NOT yet verified):

    <SSH account home>/
      <FTP root>/                    # possibly served by the default account domain
        kmhn/                       # confirmed subdomain public folder
          index.php                 # generated two-file bootstrap
          .htaccess                 # /mcp rewrite
      kmhn-mcp-private/             # sample ONLY; outside FTP root and EVERY other HTTP root
        server/
          public/index.php         # original PHP MCP server front controller
          src/
          vendor/
          runtime/
            config.php             # private; NEVER commit
            registry.json
            sessions/
          composer.json
          composer.lock

The private path must be accessible to PHP on this specific shared hosting account. If that cannot be achieved, STOP and redesign. Never use an unverified FTP-root sibling containing secrets as a workaround.

## 1. Verify hosting account paths (no secrets in chat)

1. In Lolipop Subdomain Settings, confirm the existing host maps to **kmhn**. This is already Owner-confirmed; do not recreate it.
2. Under PHP Settings, confirm this exact hostname runs LiteSpeed PHP 8.5.
3. Under SSH, enable it if necessary. Host ssh.lolipop.jp; port 2222; account and password must stay private.
4. From SSH, inspect pwd and real paths for the FTP root and the account's home directory. The Lolipop account info also has a フルパス field. Be sure FTP root is identified, not just the kmhn folder.
5. Confirm that the proposed private server root can be created and read by Web PHP OUTSIDE FTP root and any other website document roots, and that sessions can be written without permissions 777.
6. Inspect kmhn before any upload and back up existing files. Leave WAF enabled unless an observed request issue requires targeted investigation.

## 2. Build safe two-file public loader OFFLINE

Only after actual SSH filesystem paths have been verified, run from a KUMIHAN source checkout (example argument names, NOT literal paths):

    python3 universal/tools/build_lolipop_bootstrap.py \
      --ftp-root '/VERIFIED/ABSOLUTE/FTP_ROOT' \
      --private-server-root '/VERIFIED/ABSOLUTE/PRIVATE_ROOT/server' \
      --output-dir '/ABSOLUTE/LOCAL/OFFLINE_BUILD_DIR'

The tool generates ONLY:
- OFFLINE_BUILD_DIR/kmhn/index.php
- OFFLINE_BUILD_DIR/kmhn/.htaccess
- OFFLINE_BUILD_DIR/placement.json (offline deployment map, NOT for upload)

Its security checks reject private paths within FTP root, invalid absolute paths, and direct build output into hosting folders. It makes no SSH/SFTP connection. The generated bootstrap has NO passwords and returns HTTP 503 without stacktraces if the private entrypoint is absent.

When private runtime is already prepared, upload ONLY generated kmhn/index.php and kmhn/.htaccess into the **existing FTP-root/kmhn directory**. Do not upload the whole repository, vendor/ or archive into kmhn.

## 3. Private server artifact

The GitHub Actions workflow Universal MCP PHP 8.5 produces a private staging bundle containing:
- server/public/index.php (the actual MCP runtime front controller)
- server/src, vendor, Composer lock
- generated runtime/registry.json and private config EXAMPLE

Download artifact only from the reviewed commit. Check the SHA-256 checksum. Extract its internal files into the verified NON-WEB private server root. Create private runtime/config.php by copying runtime/config.production.example.php; ensure host is mcp-kmhn.landco.co.jp and allowed_origins is an explicit list (empty for server-to-server). Keep all credentials outside repo.

The generated public loader includes the original server/public/index.php by its absolute verified private path. The original script uses dirname(__DIR__) relative to its actual file location, so its private vendor/src/runtime paths remain correct.

PHP extensions, file readability, writable session folder, Composer dependencies, SDK protocol compatibility and default account-domain exposure are go/no-go checks. On failure, roll back only the two new public files and restore any prior versions.

## 4. Public verification commands

TLS was already verified by GitHub Actions. Optional recheck:

    python3 universal/tools/probe_remote.py --mode tls

ONLY after PHP is deployed:

    python3 universal/tools/probe_remote.py --mode mcp

This sends harmless MCP initialize, tools/list and language-list requests. Opening /mcp with a browser GET is NOT a functional MCP test. Check status/headers/WAF, both protocol generations, PHP 8.5, and actual client integration.

**Security check:** attempt safe unauthenticated GETs against likely config/vendor paths under both the subdomain and the default Lolipop domain; require 403/404. Never deliberately publish private data as a test.

Run separate compatibility checks for ChatGPT/Codex, Claude Code and Gemini CLI. Regenerate their installable packages only after the live MCP endpoint passes. Public plugin publishing still needs Owner approval.

## 5. Gate checklist

- [x] Owner reports subdomain and SSL set
- [x] External DNS/TLS certificate verification PASS
- [x] Public upload folder confirmed: kmhn
- [ ] Exact SSH/FTP root and PHP-readable non-Web private root verified
- [ ] Effective PHP 8.5 on this domain verified
- [ ] Composer lock and dependency audit finalized
- [ ] Private artifact installed without exposing vendor/src/runtime
- [ ] Public two-file bootstrap installed in existing kmhn
- [ ] Live HTTPS MCP initialize/tools/list/tools/call PASS
- [ ] ChatGPT/Codex, Claude Code and Gemini CLI verified separately
- [ ] Owner authorizes main merge, client package distribution and publication

Per-user call quotas remain deferred until identity/rate policy is approved. Do not confuse an AI platform's shared IP with an individual user.

Machine-readable deployment state: universal/deployment/target.json.
