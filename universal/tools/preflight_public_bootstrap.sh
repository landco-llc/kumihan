#!/bin/sh
# KUMIHAN Universal MCP — nonmutating public bootstrap preflight.
# Does NOT write, move, deploy, delete, start MCP, or call a remote service.
set -eu
fail() { echo "$1"; exit 1; }

test "$(uname -s)" = "Linux" || fail "NOT_REMOTE_LINUX"
test -n "$FTP_ROOT" || fail "FTP_ROOT_NOT_SET"
cd "$FTP_ROOT" || fail "FTP_ROOT_MISSING"
WEB="$(pwd -P)"
test "$(basename "$WEB")" = "web" || fail "WRONG_FTP_ROOT"
test -d "$WEB/kmhn" || fail "PUBLIC_KMHN_MISSING"
test ! -L "$WEB/kmhn" || fail "PUBLIC_KMHN_SYMLINK_BLOCKED"

PARENT="$(cd "$WEB/.." && pwd -P)" || fail "ACCOUNT_PARENT_MISSING"
test ! -L "$PARENT/kmhn-mcp-private" || fail "PRIVATE_ROOT_SYMLINK_BLOCKED"
test ! -L "$PARENT/kmhn-mcp-private/server" || fail "PRIVATE_SERVER_SYMLINK_BLOCKED"
PRIVATE="$PARENT/kmhn-mcp-private/server"
test -d "$PRIVATE" || fail "PRIVATE_SERVER_MISSING"
test "$(cd "$PRIVATE" && pwd -P)" = "$PRIVATE" || fail "PRIVATE_SERVER_REALPATH_MISMATCH"
case "$PRIVATE" in
  "$WEB"|"$WEB"/*) fail "PRIVATE_INSIDE_WEB_ROOT" ;;
esac
echo "PRIVATE_PATH_OUTSIDE_WEB_OK"

test ! -e "$WEB/kmhn/index.php" || fail "PUBLIC_INDEX_CONFLICT"
test ! -e "$WEB/kmhn/.htaccess" || fail "PUBLIC_HTACCESS_CONFLICT"
test ! -L "$WEB/kmhn/index.php" || fail "PUBLIC_INDEX_SYMLINK"
test ! -L "$WEB/kmhn/.htaccess" || fail "PUBLIC_HTACCESS_SYMLINK"
# Do not change or overwrite any unrelated existing file.
OTHER_FILES="$(find "$WEB/kmhn" -mindepth 1 -maxdepth 1 -print 2>/dev/null)" || fail "PUBLIC_DIRECTORY_SCAN_FAILED"
test -z "$OTHER_FILES" || fail "PUBLIC_DIR_HAS_OTHER_FILES_REVIEW"
echo "PUBLIC_KMHN_EMPTY_OK"

for file in "$PRIVATE/public/index.php" "$PRIVATE/src/Registry.php" \
            "$PRIVATE/vendor/autoload.php" "$PRIVATE/runtime/config.php" \
            "$PRIVATE/runtime/registry.json" "$PRIVATE/composer.lock"; do
  test -f "$file" && test -r "$file" || fail "PRIVATE_RUNTIME_FILE_MISSING"
done
test -d "$PRIVATE/runtime/sessions" || fail "PRIVATE_SESSIONS_DIR_MISSING"
echo "PRIVATE_RUNTIME_FILES_PRESENT_OK"

# Conservative: ANY symlink under FTP root must be reviewed. This is not a
# proof that alternate virtual hosts cannot serve the private directory.
SYMLINKS="$(find "$WEB" -type l -print 2>/dev/null)" || fail "PUBLIC_SYMLINK_SCAN_INCOMPLETE"
test -z "$SYMLINKS" || fail "WEB_SYMLINKS_REQUIRE_MANUAL_REVIEW"
echo "WEB_SYMLINK_SCAN_CLEAR"

echo "LOCAL_PREBOOTSTRAP_GATE_PASS"
echo "OTHER_VHOST_UPLOAD_MAPPINGS_NEED_OWNER_REVIEW"
echo "MCP_NOT_PUBLIC"
