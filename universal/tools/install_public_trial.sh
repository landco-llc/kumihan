#!/bin/sh
# KUMIHAN Universal MCP — guarded public two-file limited trial installer.
# Must be run on authorized Lolipop SSH after:
#  - Owner verified all domain upload-folder mappings,
#  - final scoped no-write G1 PASS,
#  - SHA256+byte-matched public files staged outside web.
# Never deploys vendor/src/runtime and never touches other sites.
set -eu

fail() { echo "$1"; exit 1; }
test "$(uname -s)" = "Linux" || fail "NOT_REMOTE_LINUX"
test "$KUMIHAN_G2_TRIAL_APPROVED" = "YES" || fail "G2_EXPLICIT_APPROVAL_REQUIRED"
test -n "$FTP_ROOT" || fail "FTP_ROOT_UNSET"
cd "$FTP_ROOT" || fail "FTP_ROOT_NOT_FOUND"
WEB="$(pwd -P)"
test "$(basename "$WEB")" = "web" || fail "WRONG_FTP_ROOT"
test -d "$WEB/kmhn" || fail "PUBLIC_KMHN_MISSING"
test ! -L "$WEB/kmhn" || fail "PUBLIC_KMHN_SYMLINK_BLOCKED"

PARENT="$(cd "$WEB/.." && pwd -P)" || fail "ACCOUNT_PARENT_MISSING"
test ! -L "$PARENT/kmhn-mcp-private" || fail "PRIVATE_ROOT_SYMLINK_BLOCKED"
test ! -L "$PARENT/kmhn-mcp-private/server" || fail "PRIVATE_SERVER_SYMLINK_BLOCKED"
PRIVATE="$PARENT/kmhn-mcp-private/server"
test -d "$PRIVATE" || fail "PRIVATE_RUNTIME_MISSING"
test "$(cd "$PRIVATE" && pwd -P)" = "$PRIVATE" || fail "PRIVATE_REALPATH_MISMATCH"
case "$PRIVATE" in
  "$WEB"|"$WEB"/*) fail "PRIVATE_INSIDE_WEB_ROOT" ;;
esac

STAGE="$PRIVATE/.kmhn-public-stage"
test -d "$STAGE" || fail "PUBLIC_STAGE_NOT_FOUND"
test ! -L "$STAGE" || fail "PUBLIC_STAGE_SYMLINK_BLOCKED"
for file in index.php .htaccess; do
  test -f "$STAGE/$file" && test -s "$STAGE/$file" || fail "STAGED_PUBLIC_FILE_MISSING"
  test ! -L "$STAGE/$file" || fail "STAGED_PUBLIC_FILE_SYMLINK"
done

for file in public/index.php vendor/autoload.php runtime/config.php runtime/registry.json; do
  test -f "$PRIVATE/$file" && test -r "$PRIVATE/$file" || fail "PRIVATE_RUNTIME_NOT_READY"
done
test -d "$PRIVATE/runtime/sessions" || fail "PRIVATE_SESSIONS_NOT_READY"

# Mac must validate the public ZIP SHA256 + members and SCP-readback bytes.
# Validate only structural invariants on the restricted SSH shell.
grep -Fq "$PRIVATE/public/index.php" "$STAGE/index.php" || fail "STAGED_BOOTSTRAP_TARGET_MISMATCH"
grep -Fq 'RewriteRule ^mcp/?$ index.php [L,QSA]' "$STAGE/.htaccess" || fail "STAGED_REWRITE_MISMATCH"
grep -Fq 'Options -Indexes' "$STAGE/.htaccess" || fail "STAGED_HTACCESS_MISMATCH"

test ! -e "$WEB/kmhn/index.php" || fail "PUBLIC_INDEX_ALREADY_EXISTS"
test ! -L "$WEB/kmhn/index.php" || fail "PUBLIC_INDEX_SYMLINK_BLOCKED"
test ! -e "$WEB/kmhn/.htaccess" || fail "PUBLIC_HTACCESS_ALREADY_EXISTS"
test ! -L "$WEB/kmhn/.htaccess" || fail "PUBLIC_HTACCESS_SYMLINK_BLOCKED"

if ENTRIES="$(find "$WEB/kmhn" -mindepth 1 -maxdepth 1 -print 2>&1)"; then
  test -z "$ENTRIES" || fail "PUBLIC_KMHN_NOT_EMPTY"
else
  fail "PUBLIC_KMHN_SCAN_INCOMPLETE"
fi
if LINKS="$(find "$WEB/kmhn" -type l -print 2>&1)"; then
  test -z "$LINKS" || fail "PUBLIC_KMHN_SYMLINKS_NEED_REVIEW"
else
  fail "PUBLIC_KMHN_SYMLINK_SCAN_INCOMPLETE"
fi
echo "G2_PUBLIC_PRECHECK_PASS"

# Noclobber creation. .htaccess first; rollback partial files made here on
# failure. Existing unrelated public content is never replaced.
installed_htaccess=0
installed_index=0
complete=0
cleanup_partial() {
  if [ "$complete" != 1 ]; then
    if [ "$installed_index" = 1 ]; then rm -f "$WEB/kmhn/index.php"; fi
    if [ "$installed_htaccess" = 1 ]; then rm -f "$WEB/kmhn/.htaccess"; fi
    echo "G2_PARTIAL_INSTALL_REVERTED"
  fi
}
trap cleanup_partial 0
umask 022
set -C
cat "$STAGE/.htaccess" > "$WEB/kmhn/.htaccess" || fail "PUBLIC_HTACCESS_WRITE_FAILED"
installed_htaccess=1
chmod 644 "$WEB/kmhn/.htaccess" || fail "PUBLIC_HTACCESS_MODE_FAILED"
cat "$STAGE/index.php" > "$WEB/kmhn/index.php" || fail "PUBLIC_INDEX_WRITE_FAILED"
installed_index=1
chmod 644 "$WEB/kmhn/index.php" || fail "PUBLIC_INDEX_MODE_FAILED"

test -s "$WEB/kmhn/index.php" || fail "PUBLIC_INDEX_EMPTY"
test -s "$WEB/kmhn/.htaccess" || fail "PUBLIC_HTACCESS_EMPTY"
complete=1

echo "G2_TWO_FILE_BOOTSTRAP_INSTALLED"
echo "MCP_HTTPS_E2E_NOT_CHECKED"
echo "CLIENT_ADAPTERS_NOT_RELEASED"
