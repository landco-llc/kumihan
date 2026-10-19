# KUMIHAN Universal MCP — Lolipop / kmhn deployment runbook

Status: **WEB PHP SDK, 21 LANGUAGES AND SESSION I/O VERIFIED; PUBLIC MCP BOOTSTRAP NOT INSTALLED** (2026-10-19).
Owner: L&Co. LLC. Implementation PR: https://github.com/landco-llc/kumihan/pull/101

## Locked parameters

| Item | Confirmed state |
|---|---|
| Hosting | Lolipop shared rental server, High-Speed |
| Target runtime | **LiteSpeed PHP 8.5.11** (actual Web PHP probe PASS, Owner terminal evidence) |
| Hostname | mcp-kmhn.landco.co.jp |
| MCP URL | https://mcp-kmhn.landco.co.jp/mcp |
| Subdomain 公開（アップロード）フォルダ | **kmhn** (Owner confirmed 2026-10-19) |
| FTP root full path | **Owner supplied; basename web confirmed**. Intentionally omitted from public source to avoid disclosing hosting account identifiers |
| Effective public path | FTP root + /kmhn (equivalently account-relative web/kmhn) |
| DNS/TLS | GitHub Actions TLS 1.3, hostname/certificate PASS; certificate expires 2027-01-17 |
| PHP MCP | 21-module source, Composer vendor and registry extracted; **private config created, SDK and sessions Web PHP PASS**; public MCP bootstrap not installed |

TLS evidence: https://github.com/landco-llc/kumihan/actions/runs/39246702661
Official hosting docs: https://lolipop.jp/manual/user/doku-subsett// and https://support.lolipop.jp/hc/ja/articles/360048391094 .

**Do not recreate the subdomain, reissue SSL, or change the configured kmhn document root.**

## Security boundary — critical

Lolipop FTP root may itself be served from the default Lolipop-hosted domain, even when the kmhn subdomain is mapped to a subfolder. A directory next to kmhn **inside FTP root is NOT automatically private**.

The original universal/server/public/index.php expects src/, vendor/ and runtime/ in its server parent directory. Uploading that file directly into FTP-root/kmhn and keeping src/vendor/runtime in FTP-root is UNSAFE. Use a small public bootstrap that includes the original entrypoint from a verified non-Web absolute path.

Recommended ROLES (the Owner supplied the absolute path for the FTP/web root; SSH realpath and private runtime access remain unverified):

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

## SSH verification: distinguish local Mac from remote Lolipop

The full path given in the Owner's account panel is a **server filesystem path**. It does NOT exist on the local Mac. A prompt containing a personal Mac hostname, rather than the authenticated Lolipop SSH host, indicates a local shell. Results of cd, test -d kmhn, or test -w .. from that local shell are INVALID for Lolipop. A failed cd must stop the test; never continue in the previous working directory.

First log in over SSH, using the SSH server, account and password displayed in the Owner's private Lolipop control panel. Do NOT commit or paste account credentials:

    ssh -p 2222 '<YOUR_SSH_ACCOUNT>@<SSH_HOST_SHOWN_IN_PANEL>'

The official general server is ssh.lolipop.jp; use the exact host displayed in the account panel if different. Password input is invisible. Check the server fingerprint against current provider information before accepting it.

ONLY AFTER successful SSH login, run this fail-closed, read-only block (replace the variable with the Owner-provided full web-root path locally, not in GitHub):

    FTP_ROOT='<OWNER_PROVIDED_ABSOLUTE_WEB_ROOT>'
    if [ "$(uname -s)" != "Linux" ]; then
      echo "NOT_ON_REMOTE_LOLLIPOP_SERVER"; exit 1
    fi
    if ! cd "$FTP_ROOT"; then
      echo "REMOTE_WEB_NOT_FOUND"; exit 1
    fi
    if test -d kmhn; then echo "KMHN_OK"; else echo "KMHN_NG"; fi
    if test -w ..; then echo "PRIVATE_PARENT_WRITABLE"; else echo "PRIVATE_PARENT_NOT_WRITABLE"; fi

This block creates, modifies and removes no files. The earlier failed test from a Mac shell is NOT a server failure. A writable parent still does not prove PHP can access it; PHP read access and virtual host isolation require separate verification.


## 1. Verify hosting account paths (no secrets in chat)

1. In Lolipop Subdomain Settings, confirm the existing host maps to **kmhn**. This is already Owner-confirmed; do not recreate it.
2. Under PHP Settings, confirm this exact hostname runs LiteSpeed PHP 8.5.
3. Under SSH, enable it if necessary. Host ssh.lolipop.jp; port 2222; account and password must stay private.
4. The Owner has already supplied the Lolipop アカウント情報 > フルパス, which ends in /web. Use that value locally with SSH; do not request or record it again in the public repository. Run read-only validation of the actual FTP root and kmhn directory before proposing a private sibling. See verification command below.
5. Confirm that the proposed private server root can be created and read by Web PHP OUTSIDE FTP root and any other website document roots, and that sessions can be written without permissions 777.
6. Inspect kmhn before any upload and back up existing files. Leave WAF enabled unless an observed request issue requires targeted investigation.

### Read-only SSH check: FTP root and private parent

SSH access is supported on Lolipop High-Speed, but the username/password are obtained only from the private control panel. Do NOT paste secrets into ChatGPT or GitHub. Before writing files or generating a bootstrap, on an authorized SSH session:

    # Set FTP_ROOT in the terminal to the exact full path from Lolipop Account Information.
    cd "$FTP_ROOT"
    pwd -P
    test -d "$FTP_ROOT/kmhn" && echo "KMHN_PUBLIC_DIR_EXISTS" || echo "KMHN_DIR_NOT_FOUND"
    test -w "$(dirname "$FTP_ROOT")" && echo "PARENT_WRITABLE_BY_SSH" || echo "PARENT_NOT_WRITABLE"

Optional: on an authorized machine with a KUMIHAN repository checkout, run the non-mutating inspector:

    python3 universal/tools/check_lolipop_layout.py --ftp-root "$FTP_ROOT"

The script does **not** print the full FTP path, create directories, or perform network operations. It reports whether the candidate ../kmhn-mcp-private/server would be outside FTP root and whether the account parent is writable by the SSH user.

**These tests do not prove that web PHP can include files outside web or that other hostnames cannot serve that path.** Those remain separate release gates. If SSH only permits writes under web, do NOT fall back to FTP root; stop and assess alternate deployment/security design.


### One-shot Web PHP / private-read test (next W01 step)

The Owner has already confirmed the following from an authenticated Lolipop SSH terminal:

    KMHN_OK
    PRIVATE_PARENT_WRITABLE

The Owner then ran the one-shot Web PHP preflight and reported:

    PHP_VERSION=8.5.11
    PHP_SAPI=litespeed
    PRIVATE_PHP_READ=PASS
    TARGET_WEB_PHP85=PASS
    PRIVATE_WEB_PHP_PRECHECK_PASS

This proves SSH access, successful cd into the web FTP root, the kmhn directory, and account-parent write permission. The preflight has created a private candidate directory and verified read access from Web PHP. The script was designed to remove the temporary probe and marker at exit, but actual absence of the temporary files has not yet been independently checked.

The critical SSH-vs-Web-PHP preflight was executed successfully using the bounded helper:

- tools/check_private_php_web.sh

It is reviewed source, not an auto-executing GitHub Action. A future rerun is only warranted if host settings change. The helper:
1. Confirms it is on Linux and in the expected web/kmhn directory.
2. Creates only ../kmhn-mcp-private/server (outside FTP root), with umask 077.
3. Creates a uniquely named harmless private marker and a temporary public PHP probe, obtains the probe response over HTTPS, confirms actual Web PHP is 8.5 and able to read the marker.
4. Removes the marker and public PHP probe via EXIT cleanup, including on ordinary errors. Only the private candidate directory remains.
5. Prints non-sensitive status lines: PHP_VERSION, PHP_SAPI, TARGET_WEB_PHP85, PRIVATE_PHP_READ, PRIVATE_WEB_PHP_PRECHECK_PASS.

If HTTP/WAF/DNS fails from the SSH server, the result remains NOT_VERIFIED (not an automatic server failure). The helper never puts passwords, the account full path or customer documents in HTTP responses; however the actual PHP probe source temporarily exposes a trivial directory role. No production application file is overwritten and MCP is not deployed.

This test does NOT prove the candidate lies outside every other domain document root or that Composer/vendor can be read under that PHP configuration. Check that separately before any real runtime upload. Do not grant 777 permissions as a workaround.


### Running the one-shot check without mktemp

The Lolipop shared SSH environment may not include `mktemp`. The operator's first attempt stopped before downloading the checker with `-bash: mktemp: コマンドが見つかりません`. This is a **local tool availability** issue, not proof of failure of the private runtime. Do not install extra command-line tools to solve it.

Run the checker after an authenticated SSH login, using a temporary **HOME** file (outside the public FTP root) created with umask 077. Supply the already-known FTP full path privately; this public document intentionally uses a placeholder. The script URL is a raw HTTPS URL and must **not** be pasted in Markdown `[label](url)` format:

```sh
(
  set -eu
  FTP_ROOT='<OWNER_SUPPLIED_ABSOLUTE_WEB_ROOT>'
  cd "$FTP_ROOT" || exit 1
  SCRIPT="$HOME/.kmhn-check-$.sh"
  if [ -e "$SCRIPT" ]; then echo 'TEMP_FILE_ALREADY_EXISTS'; exit 1; fi
  umask 077
  trap 'rm -f "$SCRIPT"' EXIT
  URL='https://raw.githubusercontent.com/landco-llc/kumihan/bbed55a9e5021e56f57fb0ba9c173dfdf3f6c3bf/universal/tools/check_private_php_web.sh'
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL --connect-timeout 10 --max-time 30 -o "$SCRIPT" "$URL"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "$SCRIPT" "$URL"
  else
    echo 'NO_CURL_OR_WGET'; exit 1
  fi
  if [ ! -s "$SCRIPT" ]; then echo 'EMPTY_OR_MISSING_SCRIPT'; exit 1; fi
  sh -n "$SCRIPT"
  FTP_ROOT="$(pwd -P)" sh "$SCRIPT"
)
```

The temporary downloaded checker is removed by EXIT cleanup. The checker may create a private candidate folder and a short-lived PHP canary/probe in kmhn; those test files are removed at exit. If the server has neither curl nor wget or blocks outbound access to GitHub, stop and provide the tool-error output; do not pipe unverified network content directly into sh. PHP-read, PHP 8.5 and public path isolation remain separate go/no-go conditions.

### Next: inspect private directory, public probe cleanup and vhost exposure

Before staging any application files, use an authenticated SSH shell to confirm the candidate private directory exists, has expected ownership and contains no leftover temporary marker. Confirm no remaining probe files in kmhn. Do not print hosting account IDs into public issues.

The PHP canary was under a directory outside the known FTP root, so the default-host static public path should not directly reach it. However this still needs verification against other configured virtual hosts and symlinks on the same account. **Do not claim global nonexposure based only on the read PASS.**

Then validate the Composer lock and security advisories for the actual pinned PHP SDK (CI audit step), inspect the staging artifact file inventory and SHA-256, prepare rollback, and deploy the private runtime before installing the public bootstrap. The initial HTTP endpoint remains unserved until these gates pass.

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

## W03 update: 2026-10-19 private archive transfer

The Owner's Mac verified the local ZIP + nested runtime tarball, completed SCP upload (`100%`, 779KB), **then SCP-read the server archive back** and obtained `REMOTE_ARCHIVE_SHA_OK` and `REMOTE_ARCHIVE_BYTES_OK`. The private archive therefore matches the pinned SHA-256 and local original byte-for-byte. SSH checks confirmed the tar file exists and `vendor`, `src`, `public` are not yet extracted. The remote verification script stopped at `HASH_TOOL_UNAVAILABLE` because neither `sha256sum` nor `openssl` was available in the Lolipop SSH environment. This is **NOT** a verified checksum mismatch.

**Readback gate now PASS.** The Mac successfully ran `shasum -a 256` plus `cmp` against the local verified archive. Next is **private-only extraction** from the SSH session using `universal/tools/unpack_private_runtime.sh` after checking that `tar` exists and the private deployment target remains empty; see [STAGE_PRIVATE_20261019.md](deployment/STAGE_PRIVATE_20261019.md). The helper does not install the public bootstrap or create the runtime configuration. Never extract inside the FTP `web` root.

SSH warnings: the Mac OpenSSH client reported missing post-quantum key exchange and an RSA host-key-update signature warning. Maintain strict host-key verification; validate the server identity against the provider information rather than bypassing SSH trust controls. The cryptographic archive readback is a separate content-integrity check.

## 3. Private server artifact

The GitHub Actions workflow Universal MCP PHP 8.5 produces a private staging bundle containing:
- server/public/index.php (the actual MCP runtime front controller)
- server/src, vendor, Composer lock
- generated runtime/registry.json and private config EXAMPLE

Download artifact only from the reviewed commit. Check the SHA-256 checksum. Extract its internal files into the verified NON-WEB private server root. Create private runtime/config.php by copying runtime/config.production.example.php; ensure host is mcp-kmhn.landco.co.jp and allowed_origins is an explicit list (empty for server-to-server). Keep all credentials outside repo.

The generated public loader includes the original server/public/index.php by its absolute verified private path. The original script uses dirname(__DIR__) relative to its actual file location, so its private vendor/src/runtime paths remain correct.

PHP extensions, file readability, writable session folder, Composer dependencies, SDK protocol compatibility and default account-domain exposure are go/no-go checks. On failure, roll back only the two new public files and restore any prior versions.

## W03 progression — private extraction PASS, next Web PHP readiness

Authenticated SSH transcript reported all six private extraction markers: `PRIVATE_TAR_PREFLIGHT_OK`, `PRIVATE_RUNTIME_EXTRACTED`, `PRIVATE_REQUIRED_FILES_OK`, `PRIVATE_CONFIG_ABSENT`, `PUBLIC_BOOTSTRAP_UNCHANGED`, `MCP_NOT_PUBLIC`. No source/vendor/registry data is in the public FTP root.

Next run a single bounded readiness check from the SSH shell: [tools/check_private_runtime_web.sh](tools/check_private_runtime_web.sh), as described in [deployment/STAGE_PRIVATE_20261019.md](deployment/STAGE_PRIVATE_20261019.md). It copies the no-secret production config into the NON-WEB private runtime **only if absent**, validates its expected host and origins, and makes a short-lived test request to Web PHP under `kmhn`. The HTTPS probe checks vendor SDK autoload, Registry constructor/21 modules, json+fileinfo PHP extensions and real PHP create/write/delete permission inside private `runtime/sessions`. Its public test PHP file is automatically removed; no permanent public MCP entrypoint is installed.

Treat any failure as STOP: a private config file may be left in place intentionally, so do not blindly rerun. Pass does not certify that no other virtual host maps the private directory, nor actual MCP initialize/tools/list/call; those remain separate release gates.

## W03 Web PHP readiness PASS — next read-only exposure check

Owner's authenticated SSH execution returned `PRIVATE_CONFIG_CREATED`, Web PHP `PHP_VERSION=8.5.11`, `PHP_SAPI=litespeed`, `REGISTRY_MODULES=21`, plus `WEB_PHP85=PASS`, `WEB_SAPI_LITESPEED=PASS`, `EXTENSIONS=PASS`, `PRIVATE_CONFIG=PASS`, `SDK_AUTOLOAD=PASS`, `REGISTRY=PASS`, `SESSION_WRITE=PASS`, `PRIVATE_RUNTIME_WEB_READY`, `MCP_NOT_PUBLIC`.

These results establish actual Web PHP SDK/autoload, 21-language registry construction and create/write/delete of private session test file. The private config now exists and is web-PHP-readable. This is **not** a working public MCP endpoint; no public bootstrap has been installed.

Next, run the **non-writing** `universal/tools/preflight_public_bootstrap.sh` on the authenticated SSH account before any public-file upload. It checks correct FTP-root/private realpaths, present private source/vendor/config/registry/session tree, that `kmhn` has no existing files to overwrite, and performs a conservative symlink scan of the known public FTP tree. Any discovered symlink requires human review; no symlink is automatically considered safe. It does not prove or assert the upload-folder mappings of other virtual hosts.

**Additionally review the Lolipop domain/subdomain control panel for all active virtual hosts.** Confirm each published upload folder is inside the intended FTP web root and none aliases/symlinks into the non-Web MCP private directory. Treat this as Owner-reviewed, not automatically tested. Without that confirmation do not claim all-vhost isolation. The public bootstrap must still wait for explicit operator action and immediate external MCP smoke tests.

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
- [x] Full FTP root path supplied by Owner (kept out of public GitHub)
- [x] SSH login successful; Owner's actual web root and existing kmhn directory verified by remote shell
- [x] SSH access to web parent is writable (Owner observed PRIVATE_PARENT_WRITABLE)
- [x] Web PHP read-access to candidate outside FTP root verified via one-shot marker (PASS)
- [ ] Non-Web private folder's absence from every other HTTP virtual host independently verified
- [x] Actual Web PHP SAPI=litespeed and PHP_VERSION=8.5.11 verified
- [ ] Composer lock and dependency audit finalized
- [x] Private tarball transferred and verified by Mac SSH readback (SHA256 and cmp PASS)
- [x] Private MCP source/vendor/registry extracted; required files PASS; public directory unchanged
- [x] Web PHP SDK autoload, registry 21 modules, PHP extensions, private config and session WRITE verified
- [ ] Private location isolation from all other document roots independently verified
- [ ] Public two-file bootstrap installed in existing kmhn
- [ ] Live HTTPS MCP initialize/tools/list/tools/call PASS
- [ ] ChatGPT/Codex, Claude Code and Gemini CLI verified separately
- [ ] Owner authorizes main merge, client package distribution and publication

Per-user call quotas remain deferred until identity/rate policy is approved. Do not confuse an AI platform's shared IP with an individual user.

Machine-readable deployment state: universal/deployment/target.json. Account-specific absolute filesystem paths must remain only in operator-local variables or private deployment secrets, not the public GitHub repository.
