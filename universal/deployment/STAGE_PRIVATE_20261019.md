# KUMIHAN Universal MCP — W03 private staging packet

Status: **READY FOR OPERATOR PRIVATE STAGING / PUBLIC MCP NOT DEPLOYED** (2026-10-19).
Repository: `landco-llc/kumihan`, implementation Draft PR #101. Do not merge or publish the client plugins until real-host MCP checks and Owner Gate.

## Verified host gates

- SSH account authenticated; owner-confirmed `web/kmhn` exists and the parent of `web` is writable.
- The candidate private server directory `../kmhn-mcp-private/server` exists; Web PHP 8.5.11 (LiteSpeed) can read a temporary canary from it.
- Public `kmhn/index.php` and `kmhn/.htaccess` do not exist; earlier temporary PHP probe and private marker glob checks returned no matches.
- TLS 1.3 for `mcp-kmhn.landco.co.jp` verified from GitHub Actions. **MCP service not deployed**.
- All OTHER document-root/vhost access to the private candidate and PHP session-write permission have not yet been tested. Never upload the runtime into any path underneath the account's `/web` FTP root.

## Immutable source packet

Source: GitHub Actions run https://github.com/landco-llc/kumihan/actions/runs/39255977471
Source commit: `74b5d74549619c73e9543bbce0bf665a1fa5cec1` (audit + PHP MCP smoke PASS).
Operator conversation attachment: `KUMIHAN_MCP_Lolipop_DeployKit_v0.1.0-preview_20261019.zip` (not a public GitHub release).
ZIP SHA256: `0f876361ba593441a90428a4b8919b4f10e84b00988e1d7f21a38f8382c703ca`.
Nested private tarball SHA256: `5d814cc505374bbf126d058119ece6b04e9eaf757938600eedfb2e3983f6a3e1`.
Archive independently inspected: tar paths relative, no traversal, symlinks, hardlinks or `runtime/config.php`; contains `public/`, `src/`, `vendor/`, `runtime/`, `composer.json` and `composer.lock`.

## Stage A — operator Mac (transfer private tarball ONLY)

Download the approved ZIP from the ChatGPT conversation to your Mac's Downloads folder. Run in a **Mac terminal, NOT the SSH shell**, and adjust `ZIP` only if the download location differs:

```sh
set -eu
ZIP="$HOME/Downloads/KUMIHAN_MCP_Lolipop_DeployKit_v0.1.0-preview_20261019.zip"
WORK="$HOME/Downloads/kmhn-mcp-private-stage"
mkdir -p "$WORK"
test -f "$ZIP" || { echo 'ZIP_NOT_FOUND'; exit 1; }
ACTUAL="$(shasum -a 256 "$ZIP" | awk '{print $1}')"
EXPECTED='0f876361ba593441a90428a4b8919b4f10e84b00988e1d7f21a38f8382c703ca'
test "$ACTUAL" = "$EXPECTED" || { echo 'ZIP_SHA_MISMATCH'; exit 1; }
unzip -p "$ZIP" private/kumihan-mcp-php85-runtime.tar.gz > "$WORK/runtime.tar.gz"
ACTUAL="$(shasum -a 256 "$WORK/runtime.tar.gz" | awk '{print $1}')"
EXPECTED='5d814cc505374bbf126d058119ece6b04e9eaf757938600eedfb2e3983f6a3e1'
test "$ACTUAL" = "$EXPECTED" || { echo 'PRIVATE_ARCHIVE_SHA_MISMATCH'; exit 1; }
echo 'LOCAL_ARCHIVE_SHA_OK'
REMOTE_USER='<SSH_USERNAME_FROM_PRIVATE_LOLIPOP_PANEL>'
REMOTE_PRIVATE='<VERIFIED_ABSOLUTE_NON_WEB_PRIVATE_SERVER_PATH>'
scp -P 2222 "$WORK/runtime.tar.gz" "$REMOTE_USER@ssh.lolipop.jp:$REMOTE_PRIVATE/runtime.tar.gz"
```

Set the remote SSH username and the verified absolute private server directory in the operator's **local** terminal only, never in public GitHub or the PR discussion. Do not upload archives to `web` or `web/kmhn`, and do not include passwords in any command.

## Stage B — authenticated Lolipop SSH (verify archive and inspect target; no extraction yet)

```sh
FTP_ROOT='<OWNER_CONFIRMED_ABSOLUTE_WEB_ROOT>'
cd "$FTP_ROOT" || exit 1
PRIVATE="$(dirname "$(pwd -P)")/kmhn-mcp-private/server"
cd "$PRIVATE" || exit 1
test -f runtime.tar.gz && echo 'PRIVATE_ARCHIVE_PRESENT' || echo 'PRIVATE_ARCHIVE_MISSING'
test ! -e vendor && test ! -e src && test ! -e public && echo 'PRIVATE_TARGET_CLEAN' || echo 'PRIVATE_TARGET_HAS_FILES'
command -v tar >/dev/null 2>&1 && echo 'TAR_AVAILABLE' || echo 'TAR_UNAVAILABLE'
if command -v sha256sum >/dev/null 2>&1; then
  sha256sum runtime.tar.gz
elif command -v openssl >/dev/null 2>&1; then
  openssl dgst -sha256 runtime.tar.gz
else
  echo 'SERVER_SHA_TOOL_NOT_AVAILABLE'
fi
```

Report the status words and digest, NOT the absolute account path or login credentials. If the tar is absent, root has existing runtime files, hashing is unavailable, or SHA does not match, **STOP**. These checks alone perform no runtime extraction and do not expose public MCP.

## Stage C — after Stage B passes

- Extract only the pinned runtime tarball into the verified **private** server directory. Do not extract the ZIP itself into web.
- Create private `runtime/config.php` from the production example (`host=mcp-kmhn.landco.co.jp`). Make the sessions folder writable to the actual Web PHP UID without mode 777.
- Recheck no public vhost maps to the private directory. Confirm file ownership and runtime readiness. Only then install the two public bootstrap files from the approved ZIP into existing `web/kmhn`.
- Run external HTTPS MCP initialize, tools/list and tools/call, then separate client tests, preserving rollback.

Never treat `PRIVATE_PHP_READ=PASS` as completed end-to-end MCP deployment.
