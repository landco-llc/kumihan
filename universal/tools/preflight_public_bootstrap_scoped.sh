#!/bin/sh
# KUMIHAN Universal MCP — scoped, read-only pre-publication check.
# Deliberately does not recurse into unrelated FTP/web website subtrees.
# This is NOT a global public-vhost/symlink clearance: Owner must review
# all active domain/subdomain upload-root mappings independently.
set -eu
fail() { echo "$1"; exit 1; }
test "$(uname -s)" = "Linux" || fail "NOT_REMOTE_LINUX"
test -n "$FTP_ROOT" || fail "FTP_ROOT_NOT_SET"
cd "$FTP_ROOT" || fail "FTP_ROOT_MISSING"
WEB="$(pwd -P)"
test "$(basename "$WEB")" = "web" || fail "WRONG_FTP_ROOT"
test -d "$WEB/kmhn" || fail "PUBLIC_KMHN_MISSING"
test ! -L "$WEB/kmhn" || fail "PUBLIC_KMHN_SYMLINK_BLOCKED"

PARENT="$(cd "$WEB/.." && pwd -P)" || fail "PARENT_MISSING"
test ! -L "$PARENT/kmhn-mcp-private" || fail "PRIVATE_PARENT_SYMLINK_BLOCKED"
test ! -L "$PARENT/kmhn-mcp-private/server" || fail "PRIVATE_SERVER_SYMLINK_BLOCKED"
PRIVATE="$PARENT/kmhn-mcp-private/server"
test -d "$PRIVATE" || fail "PRIVATE_SERVER_MISSING"
test "$(cd "$PRIVATE" && pwd -P)" = "$PRIVATE" || fail "PRIVATE_REALPATH_MISMATCH"
case "$PRIVATE" in
  "$WEB"|"$WEB"/*) fail "PRIVATE_INSIDE_FTP_ROOT" ;;
esac
echo "PRIVATE_PATH_OUTSIDE_WEB_OK"

test ! -e "$WEB/kmhn/index.php" || fail "PUBLIC_INDEX_CONFLICT"
test ! -L "$WEB/kmhn/index.php" || fail "PUBLIC_INDEX_SYMLINK_BLOCKED"
test ! -e "$WEB/kmhn/.htaccess" || fail "PUBLIC_HTACCESS_CONFLICT"
test ! -L "$WEB/kmhn/.htaccess" || fail "PUBLIC_HTACCESS_SYMLINK_BLOCKED"

if OTHER="$(find "$WEB/kmhn" -mindepth 1 -maxdepth 1 -print 2>&1)"; then
  test -z "$OTHER" || fail "PUBLIC_KMHN_HAS_EXISTING_FILES"
else
  fail "PUBLIC_KMHN_SCAN_INCOMPLETE"
fi
echo "PUBLIC_KMHN_EMPTY_OK"

if LINKS="$(find "$WEB/kmhn" -type l -print 2>&1)"; then
  test -z "$LINKS" || fail "KMHN_SYMLINKS_NEED_REVIEW"
else
  fail "KMHN_SYMLINK_SCOPE_INCOMPLETE"
fi
echo "KMHN_SYMLINK_SCOPE_CLEAR"

for file in public/index.php src/Registry.php vendor/autoload.php runtime/config.php runtime/registry.json composer.lock; do
  test -s "$PRIVATE/$file" && test -r "$PRIVATE/$file" || fail "PRIVATE_RUNTIME_FILE_MISSING"
done
test -d "$PRIVATE/runtime/sessions" || fail "PRIVATE_SESSIONS_DIR_MISSING"
echo "PRIVATE_RUNTIME_FILES_PRESENT_OK"

echo "SCOPED_PREBOOTSTRAP_CHECKS_PASS"
echo "WEB_WIDE_SYMLINK_SCAN_NOT_ATTESTED"
echo "OTHER_VHOST_UPLOAD_MAPPINGS_NEED_OWNER_REVIEW"
echo "MCP_NOT_PUBLIC"
