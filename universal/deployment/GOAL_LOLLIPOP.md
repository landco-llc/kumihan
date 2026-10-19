# /goal — KUMIHAN MCP / Lolipop private runtime deployment

Owner: L&Co. LLC
Repository: landco-llc/kumihan
Implementation branch: feat/universal-mcp-php-runtime
Target endpoint: https://mcp-kmhn.landco.co.jp/mcp
Status: DNS/TLS PASS; FTP root and kmhn SSH verified; LiteSpeed PHP 8.5.11 + Web-PHP private-canary read PASS; private MCP runtime source/vendor/registry EXTRACTED with 6 PASS markers; private config, SDK Web-PHP session-write, public bootstrap and real MCP transport NOT YET VERIFIED.

## Authority and privacy

The Owner supplied the absolute FTP-root/full-path account value in the orchestration chat. Do not request it again where already provided. It contains an account-specific identifier and must NEVER be committed to this public repository, a public issue or a log. Obtain the exact value from the authorized local deployment context. Public document-root role is web/kmhn. The private candidate resides outside web; its SSH write permissions, PHP canary read, and successful extraction of the runtime are now verified. This is not proof that the directory is unreachable from every other virtual host or that Web PHP can load the SDK and write session files. Do not change existing subdomain, SSL or neighboring sites.

## Work group W00–W04

### W00 Fresh read and baseline
Fresh-read main, Draft PR #101, latest CI artifacts/checksum, deployment/target.json, Lolipop runbook and any server filesystem state visible through authorized credentials. Preserve published Skills and live sites. Record head SHA and separate observed facts from plans.

### W01 Read-only host diagnostics
Use an authorized SSH session with the privately supplied FTP root to validate its realpath and kmhn child. Run universal/tools/check_lolipop_layout.py --ftp-root "$FTP_ROOT" or equivalent read-only POSIX checks. Check whether the parent of web is writable to the SSH user, without creating directories. Confirm effective LiteSpeed PHP 8.5 on mcp-kmhn.landco.co.jp in the Lolipop control panel; CLI PHP is not proof. Check Web PHP ability to read a private path outside web (and possible open_basedir restrictions), and that candidate is outside ALL virtual-host document roots. Never paste or log passwords, user/account IDs, secrets or absolute SSH paths. If no safe private path exists, record PRIVATE_RUNTIME_UNAVAILABLE and stop deployment; never move vendor/runtime/config into the exposed FTP root.

### W02 Preflight, artifact and rollback
Using the approved SHA, retrieve the GitHub Actions kumihan-universal-mcp-php85-staging artifact and validate SHA256, Composer lock/version/advisories, 21+ registry modules and expected files. Generate a two-file public bootstrap through universal/tools/build_lolipop_bootstrap.py using verified private path inputs; do NOT use guessed example paths. Map which files belong to public kmhn and which belong to private server. Prepare sanitized evidence, rollback procedures and permissions. This Work can proceed without host credentials but must remain STAGED until W01 succeeds.

### W03 Owner-gated host installation
Owner already transferred and Mac-readback-verified the private tarball, and successfully extracted its source/vendor/registry with zero changes to kmhn. Next perform the one-shot Web-PHP private config, SDK autoload, 21-module Registry and session-write check via universal/tools/check_private_runtime_web.sh. Requires proven non-Web PHP-readable path and authorized credential-safe SSH/SFTP deployment. Back up kmhn and target directory, unpack src/vendor/registry/Composer files to private host path, create runtime/config.php only there, confirm session write permissions and runtime PHP 8.5, then upload ONLY kmhn/index.php and kmhn/.htaccess. If unsafe paths, incorrect permissions or unexpected existing public files: STOP and do not overwrite. Roll back changed files on a failed hosting smoke.

### W04 HTTPS MCP acceptance and platform adapters
From independent public network test /mcp initialize, tools/list, tools/call, protocol revisions/session lifecycle, header/WAF behavior, and no public access to source/vendor/runtime through all domains. Test actual ChatGPT/Codex, Claude Code and Gemini CLI clients separately. Update gate flags only for direct observed evidence. Prepare a release candidate/PR, but do NOT merge or publish the integrated plugin before Owner publication approval.

## Start text for Codex Cloud/App

/goal

Repository: landco-llc/kumihan
Branch: feat/universal-mcp-php-runtime
Read universal/deployment/GOAL_LOLLIPOP.md, universal/LOLLIPOP_SETUP.md, universal/deployment/target.json, and all applicable agent policies.
Execute W00–W04 as one bounded autonomous Work group. Continue all independently safe work if server access is missing. The absolute web root was provided in the private orchestration conversation; keep it private. No remote production deployment or public publication without verified host prerequisites and Owner authorization.
