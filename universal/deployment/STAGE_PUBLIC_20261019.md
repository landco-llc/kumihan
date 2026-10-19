# KUMIHAN Universal MCP — public bootstrap owner gate

**Prepared only; NOT yet executed on Lolipop.** Date: 2026-10-19.
Implementation: https://github.com/landco-llc/kumihan/pull/101 (Draft, no main merge).
Endpoint intended: https://mcp-kmhn.landco.co.jp/mcp

## Observed gates

- SSL/TLS for hostname PASS from GitHub Actions.
- SSH web root with existing kmhn subfolder PASS; parent outside web writable.
- Private PHP 8.5.11 litespeed PASS; Web PHP SDK autoload, 21 modules, json/fileinfo, private config and session write/delete **ALL PASS**.
- The private source/vendor/registry extracted from a SHA-pinned CI archive, source ZIP and SCP readback SHA + byte equality PASS.
- Public `kmhn/index.php` and `kmhn/.htaccess` remain **ABSENT**. A temporary Web PHP readiness probe was designed for EXIT cleanup, but independently verifying its absence remains part of the next preflight.
- Isolation against *all* alternate domain upload mappings remains Owner review / NOT CHECKED. Do not mark it passed from a local path test alone.

## Owner gate G1 — no-write filesystem preflight

Run the reviewed [tools/preflight_public_bootstrap.sh](../tools/preflight_public_bootstrap.sh) over authorized SSH. It checks the real private path is outside web, both public bootstrap destinations are unused, the entire kmhn folder has no other entries (including probes), private config/vendor/registry/sessions exist, and no symlinks exist anywhere inside the account FTP root. Any symlink causes manual review and STOP. The script does **not** modify any files.

In the Lolipop control panel, review every configured domain/subdomain's 公開（アップロード）フォルダ and confirm the web public area is inside the account FTP root and no alias reaches the separate non-Web private PHP directory. Only the Owner can attest those settings; they cannot be proven through GitHub runner or one SSH scan.

Expected local output if no conflicts:

    PRIVATE_PATH_OUTSIDE_WEB_OK
    PUBLIC_KMHN_EMPTY_OK
    PRIVATE_RUNTIME_FILES_PRESENT_OK
    WEB_SYMLINK_SCAN_CLEAR
    LOCAL_PREBOOTSTRAP_GATE_PASS
    OTHER_VHOST_UPLOAD_MAPPINGS_NEED_OWNER_REVIEW
    MCP_NOT_PUBLIC

These results are not permission to bypass the all-vhost review or to publish the final client adapters. Errors must stop publication, without removing/overwriting unrelated live files.

## Owner gate G2 — approved two-file public bootstrap (only AFTER G1)

Prepared local deployment ZIP in Owner's ChatGPT conversation: `KUMIHAN_MCP_Lolipop_DeployKit_v0.1.0-preview_20261019.zip`. Verified ZIP SHA256 `0f876361ba593441a90428a4b8919b4f10e84b00988e1d7f21a38f8382c703ca`.

Public ZIP paths:

- `public/kmhn/.htaccess` — SHA256 `c83a8917efadb548c16d37c8234f5ea9af9080891e5b60afac7b341516e1e80a`.
- `public/kmhn/index.php` — SHA256 `603b6b77e87f96176e5762127384bfde95c56706db16aef53a3311119846a715`.

The index.php contains only an absolute PHP include of the already-verified private application entrypoint; it does **NOT** expose vendor/registry/config into web. Note that this operator-specific file contains an account filesystem path: do NOT commit it into public GitHub, distribute it as a public plugin, or rename it to an unactioned text extension in web (which could disclose its PHP source).

Transfer the two approved files first into the non-Web private staging directory over SCP, verify identity/expected digest, and install the `.htaccess` then `index.php` with guarded no-overwrite operations into the existing `web/kmhn` only after the Owner gate is complete. The `.htaccess` needs Web-server read permission; the PHP front controller must be served as PHP, never downloaded as source.

Rollback: if a live MCP test fails, remove or revert ONLY the two files installed for this deployment, after verifying they still match the expected package content. Retain the private runtime for diagnostics without exposing it.

## Owner gate G3 — real MCP HTTPS E2E

After installing both public files, use [tools/probe_remote.py](../tools/probe_remote.py) from a real Internet-connected computer or GitHub Actions runner in `--mode mcp`, not a GET in a browser. The smoke performs JSON-RPC initialize, tools/list, and tools/call kumihan_list_languages; it cannot certify ChatGPT, Claude or Gemini compatibility. Check WAF rules, HTTP headers, 64 KiB input cap, 4xx/5xx behavior and modern transport separately. No customer data is required.

Keep Draft PR and unmerged main, do not publish/install client plugin packages until explicit Owner release and real client tests.
