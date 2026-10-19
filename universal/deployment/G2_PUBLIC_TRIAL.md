# KUMIHAN Universal MCP — G2 controlled public bootstrap trial

Status: G1 scoped PASS and Owner's domain upload-folder mapping review PASS; **G2 public files NOT YET INSTALLED**.
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

## G3: immediate real HTTPS MCP transport verification

From a Mac or GitHub runner, use the reviewed `universal/tools/probe_remote.py --mode mcp`. It performs real HTTPS initialize, tools/list and tools/call. Do not substitute a browser GET or a successful TLS connection for MCP readiness. Verify actual host name, response headers, WAF and errors, protocol versions and session behavior; test client adapters separately.

If live MCP smoke fails, do not modify DNS/SSL or disable WAF globally. Record HTTP status and response type without customer content, then roll back the public files with the explicit operator-gated `universal/tools/rollback_public_trial.sh` **only when** both installed files still exactly match their staged copies. The rollback retains the private runtime for diagnostics and touches no other websites.

Remaining product gates after G3: genuine ChatGPT/Codex, Claude Code and Gemini CLI connections, abuse controls, installer compatibility, operator evidence, explicit Owner main merge and release authorization. The full FTP-root symlink scan remains `NOT_CHECKED_PERMISSION_LIMIT` and never becomes PASS implicitly.
