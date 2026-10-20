# KUMIHAN Universal MCP — G2 controlled public bootstrap trial

Status: **G3 live HTTPS MCP PASS**; two public files installed, 4 tools / 21 modules verified, client integrations and general release pending.
Source: https://github.com/landco-llc/kumihan/pull/101, Draft/unmerged.
Target: https://mcp-kmhn.landco.co.jp/mcp

## Scope, evidence and restrictions

- 2026-10-19 Owner's SSH output: `PRIVATE_PATH_OUTSIDE_WEB_OK`, `PUBLIC_KMHN_EMPTY_OK`, `KMHN_SYMLINK_SCOPE_CLEAR`, `PRIVATE_RUNTIME_FILES_PRESENT_OK`, `SCOPED_PREBOOTSTRAP_CHECKS_PASS`, `WEB_WIDE_SYMLINK_SCAN_NOT_ATTESTED`, `OTHER_VHOST_UPLOAD_MAPPINGS_NEED_OWNER_REVIEW`, `MCP_NOT_PUBLIC`.
- Owner separately confirmed every configured domain/subdomain upload mapping was reviewed and none refers to the private MCP runtime. This is a manual attestation, not a full symlink scan of unrelated inaccessible website folders.
- Web PHP 8.5.11/LiteSpeed, 21 language modules, Composer SDK/autoload and private session read/write/delete PASS.
- Only the two files under the dedicated `web/kmhn/` subdomain are eligible for installation. No credentials, vendor, registry, source tree, or runtime config under the FTP root.
- General publication, main merge and client installation are NOT authorized by this scoped trial.

## Exact trial artifact

Operator's local deployment ZIP: `KUMIHAN_MCP_Lolipop_DeployKit_v0.1.0-preview_20261019.zip`. Verify its complete SHA-256 first:

    0f876361ba593441a90428a4b8919b4f10e84b00988e1d7f21a38f8382c703ca

Extract ONLY these ZIP entries on the Mac:

| Entry | Expected SHA-256 |
| --- | --- |
| `public/kmhn/index.php` | `603b6b77e87f96176e5762127384bfde95c56706db16aef53a3311119846a715` |
| `public/kmhn/.htaccess` | `c83a8917efadb548c16d37c8234f5ea9af9080891e5b60afac7b341516e1e80a` |

The public entrypoint includes the verified absolute private app path and contains no passwords or tokens. Never add this operator-specific file to public source control.

## G2-A: Mac validation and private-only staging

1. Verify ZIP digest locally with `shasum -a 256` and both extracted file digests. Do not use Markdown-formatted hyperlinks inside shell variables.
2. Using authenticated Lolipop SSH, first create a **new, empty** private staging directory `<private server root>/.kmhn-public-stage` with mode 0700, only if it does not already exist.
3. From the Mac (not the remote shell), SCP the two authenticated files into that private staging folder. This stage is OUTSIDE FTP root.
4. SCP the staged copies **back** into a separate local directory; verify each digest equals the expected SHA and `cmp -s` equals the originally extracted local copy. Do not stage in public `web/kmhn` directly.
5. Return to the authenticated SSH shell and run the pinned reviewed `universal/tools/install_public_trial.sh`, passing `FTP_ROOT` and `KUMIHAN_G2_TRIAL_APPROVED=YES` as operator-local environment values. This is the explicit limited-public-trial approval. Never allow the script to overwrite any public file.

### G2 installer output

    G2_PUBLIC_PRECHECK_PASS
    G2_TWO_FILE_BOOTSTRAP_INSTALLED
    MCP_HTTPS_E2E_NOT_CHECKED
    CLIENT_ADAPTERS_NOT_RELEASED

Installer always writes `.htaccess` first, then `index.php`, with noclobber protections; on a partial failure it attempts to remove only those two files that it created. A successful installer is NOT a passing MCP protocol test.

## G2-A result — private stage transfer and readback PASS

Owner Mac terminal reported on 2026-10-19:

    G2_LOCAL_FILE_SHA_OK
    G2_PRIVATE_STAGE_CREATED
    G2_SCP_READBACK_SHA_OK
    G2_SCP_READBACK_BYTES_OK
    G2_ONLY_PRIVATE_STAGED

The 453-byte operator-specific public `index.php` and 192-byte `.htaccess` were copied **only** into private `.kmhn-public-stage` via authenticated SCP and downloaded again to Mac. Both SHA-256 values and byte-for-byte equality against the extracted, verified ZIP members passed. No public file was installed and no HTTP MCP connection has been attempted.

## G2-B next — guarded trial install, explicit operator approval

1. On authenticated Lolipop SSH, download pinned `universal/tools/install_public_trial.sh` (inspect source) to an SSH-home temporary file using `curl` or `wget`; do not pipe raw network data into a shell, do not use `mktemp` (unavailable on host).
2. Verify nonempty download and `sh -n`. In the same SSH session with `cd` to the already verified FTP-root `web`, execute with `KUMIHAN_G2_TRIAL_APPROVED=YES FTP_ROOT="$(pwd -P)" sh "$SCRIPT"`.
3. The installer checks private/public boundaries, staged files, expected private entrypoint, rewrites, runtime files, no existing public entries, and creates `.htaccess` then `index.php` under `web/kmhn` using `set -C` no-clobber protection. Only those two files are affected; no source/vendor/runtime moves. Partial errors trigger limited cleanup.
4. **IMPORTANT: This makes `/mcp` reachable from the public Internet immediately**, even though it is called a limited trial. No authentication or per-user quota is configured. Do not run unless immediate G3 HTTPS smoke and rollback are ready.

Expected messages:

    G2_PUBLIC_PRECHECK_PASS
    G2_TWO_FILE_BOOTSTRAP_INSTALLED
    MCP_HTTPS_E2E_NOT_CHECKED
    CLIENT_ADAPTERS_NOT_RELEASED

Do not repeat installer on an error or after success. In the next step use the standalone `universal/tools/probe_remote.py --mode mcp --endpoint https://mcp-kmhn.landco.co.jp/mcp` from Mac (current script accepts explicit endpoint without a repo checkout). A successful HTTP TLS handshake alone is not MCP readiness.

Rollback available in `universal/tools/rollback_public_trial.sh` after an explicit local approval flag. It refuses to remove files whose content differs from the staged copies and leaves private runtime untouched. If public MCP smoke fails, attempt rollback promptly and report status; if rollback refuses because files changed, STOP for manual investigation rather than deleting unrelated files.

## G3: immediate real HTTPS MCP transport verification

From a Mac or GitHub runner, use the reviewed `universal/tools/probe_remote.py --mode mcp`. It performs real HTTPS initialize, tools/list and tools/call. Do not substitute a browser GET or a successful TLS connection for MCP readiness. Verify actual host name, response headers, WAF and errors, protocol versions and session behavior; test client adapters separately.

If live MCP smoke fails, do not modify DNS/SSL or disable WAF globally. Record HTTP status and response type without customer content, then roll back the public files with the explicit operator-gated `universal/tools/rollback_public_trial.sh` **only when** both installed files still exactly match their staged copies. The rollback retains the private runtime for diagnostics and touches no other websites.

Remaining product gates after G3: genuine ChatGPT/Codex, Claude Code and Gemini CLI connections, abuse controls, installer compatibility, operator evidence, explicit Owner main merge and release authorization. The full FTP-root symlink scan remains `NOT_CHECKED_PERMISSION_LIMIT` and never becomes PASS implicitly.

## G3 live evidence — verified

Owner's Mac printed `G2_TWO_FILE_BOOTSTRAP_INSTALLED`, TLSv1.3, `MCP_PASS ... tools=4 modules=21`, `MCP_TRIAL_PASS`, and `PUBLIC_BOOTSTRAP_REMAINS_INSTALLED`.

A second, independent read-only check from the connected Mac also PASSed HTTPS MCP initialize, tools/list and tools/call `kumihan_list_languages`. Tested GETs against `vendor/autoload.php`, `runtime/config.php`, `runtime/registry.json`, and `src/Registry.php` all returned HTTP 404; `.env` returned 403. These probes do **not** constitute an exhaustive security review.

This endpoint is publicly reachable without authentication or per-user quotas. Keep the trial distinct from general release, client adapters and main merge; do not publish client plugins without a further Owner gate. Previous G2 rollback succeeded in an earlier trial, but **do not roll back this successfully verified live trial unless Owner requests it**.
