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

Report the status words and digest, NOT the absolute account path or login credentials. If the tar is absent or the target already has files, **STOP**. If neither SHA tool is available in SSH, run Stage B2 from a Mac and do not extract the archive until its SHA-256 and byte equality both succeed. A checksum mismatch is a STOP. These checks alone perform no runtime extraction and do not expose public MCP.

## Stage B2 — transfer confirmed, but SSH has no hash tool

On 2026-10-19 the Owner performed Stage A and Stage B. Mac reported `LOCAL_ARCHIVE_SHA_OK` and `scp ... 100% 779KB`. The authenticated remote shell passed `test -f runtime.tar.gz` and `test ! -e vendor/src/public`, but printed **HASH_TOOL_UNAVAILABLE**: neither sha256sum nor openssl exists on the remote SSH PATH. No extraction followed. This is NOT a checksum mismatch or evidence of corruption, just a missing verification utility.

**Preferred fallback: read back the exact server-side archive and hash/compare it on Mac.** This needs no additional server-side packages, PHP scripts or temporary public endpoints. Run only in a local Mac terminal:

```sh
(
  set -eu
  WORK="$HOME/Downloads/kmhn-mcp-stage"
  SOURCE="$WORK/runtime.tar.gz"
  RETURNED="$WORK/runtime.from-lolipop.tar.gz"
  EXPECTED='5d814cc505374bbf126d058119ece6b04e9eaf757938600eedfb2e3983f6a3e1'
  test -f "$SOURCE" || { echo 'LOCAL_SOURCE_MISSING'; exit 1; }
  test ! -e "$RETURNED" || { echo 'RETURN_FILE_ALREADY_EXISTS'; exit 1; }
  REMOTE_USER='<SSH_USERNAME_FROM_PRIVATE_LOLIPOP_PANEL>'
  REMOTE_ARCHIVE='<VERIFIED_ABSOLUTE_NON_WEB_PRIVATE_SERVER_PATH>/runtime.tar.gz'
  scp -P 2222 "$REMOTE_USER@ssh.lolipop.jp:$REMOTE_ARCHIVE" "$RETURNED"
  REMOTE_DIGEST="$(shasum -a 256 "$RETURNED" | awk '{print $1}')"
  test "$REMOTE_DIGEST" = "$EXPECTED" || { echo 'REMOTE_ARCHIVE_SHA_NG'; exit 1; }
  cmp -s "$SOURCE" "$RETURNED" || { echo 'REMOTE_ARCHIVE_BYTES_NG'; exit 1; }
  echo 'REMOTE_ARCHIVE_SHA_OK'
  echo 'REMOTE_ARCHIVE_BYTES_OK'
)
```

If the return file already exists, do not overwrite it silently; inspect or delete that local test copy before rerunning. This procedure reads the server-held archive and writes only a new local file on the Mac. **Do not run in an SSH shell.** After the digest and byte-by-byte equality succeed, Stage B archive-integrity gate is verified. Otherwise STOP before extracting.

### SSH transport warnings

The SCP upload printed an OpenSSH 10.1+ warning about missing post-quantum key exchange and a `client_global_hostkeys_prove_confirm` RSA host-key-update proof warning. These do not by themselves negate the SCP 100% completion, but require accurate SSH-host identity verification using the provider's host-key guidance. Do not disable StrictHostKeyChecking, ignore fingerprint changes or treat warnings as artifact-hash evidence. Prefer a provider-side SSH algorithm update where offered.

## Stage B2 result — PASSED (Owner readback)

Owner's Mac terminal reported **REMOTE_ARCHIVE_SHA_OK** and **REMOTE_ARCHIVE_BYTES_OK** after SCP readback of the server-held 779KB tarball. The server file matches SHA-256 `5d814cc505374bbf126d058119ece6b04e9eaf757938600eedfb2e3983f6a3e1` and has identical bytes to the verified local source. Server-side sha256sum/openssl are not needed.

The pinned GitHub Actions artifact was additionally inspected: 1,227 tar entries (1,067 regular files, 160 directories), no absolute/parent traversal paths, no symlinks/hardlinks/devices and no `runtime/config.php`. **Do not read this as a signed publisher attestation;** these are checks against the downloaded pinned artifact matched by checksum.

## Stage C — private-only extraction (no public bootstrap yet)

On the authorized Lolipop SSH shell, set FTP_ROOT to the Owner-confirmed `web` root locally, then execute the reviewed script **only after** verifying its source:

    FTP_ROOT='<OWNER_CONFIRMED_ABSOLUTE_WEB_ROOT>'
    # Execute universal/tools/unpack_private_runtime.sh via verified transfer / prechecked download.

The script checks FTP root, private realpath, public kmhn, no pre-existing public/index/vendor/src/runtime, archive presence, server tar availability and the tar listing before extracting with umask 077. Afterwards it checks the required runtime files, `vendor/autoload.php`, rules registry and Composer lock, and confirms `runtime/config.php` and both public bootstrap files remain ABSENT. It has no password, database, billing or public deployment.

Expected successful status markers:

    PRIVATE_TAR_PREFLIGHT_OK
    PRIVATE_RUNTIME_EXTRACTED
    PRIVATE_REQUIRED_FILES_OK
    PRIVATE_CONFIG_ABSENT
    PUBLIC_BOOTSTRAP_UNCHANGED
    MCP_NOT_PUBLIC

If `TAR_UNAVAILABLE`, `ARCHIVE_CANNOT_BE_LISTED`, `PRIVATE_TARGET_NOT_EMPTY` or any other error occurs, STOP without attempting workarounds under `web`. If extraction partly failed, leave the partially extracted files for careful review/rollback instead of blindly removing directories.

Web PHP read access to the candidate private folder and its file presence have been confirmed, but actual SDK dependency execution, writable session storage, other vhost isolation and live MCP protocol remain subsequent release gates.

### Stage D — after Stage C success (NOT AUTHORIZED BY PASS ALONE)

Create private `runtime/config.php` from the production template (never publish it), verify PHP dependencies/session permissions and isolation; only then publish exactly two bootstrap files under `web/kmhn`. Run actual HTTPS initialize/tools/list/tools/call. Do not merge main or release clients without Owner Gate.



- Extract only the pinned runtime tarball into the verified **private** server directory. Do not extract the ZIP itself into web.
- Create private `runtime/config.php` from the production example (`host=mcp-kmhn.landco.co.jp`). Make the sessions folder writable to the actual Web PHP UID without mode 777.
- Recheck no public vhost maps to the private directory. Confirm file ownership and runtime readiness. Only then install the two public bootstrap files from the approved ZIP into existing `web/kmhn`.
- Run external HTTPS MCP initialize, tools/list and tools/call, then separate client tests, preserving rollback.

Never treat `PRIVATE_PHP_READ=PASS` as completed end-to-end MCP deployment.
