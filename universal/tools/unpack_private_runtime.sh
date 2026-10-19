#!/bin/sh
# KUMIHAN Universal: private-only extraction of a VERIFIED runtime archive.
# Prerequisite: Owner's Mac readback: REMOTE_ARCHIVE_SHA_OK + REMOTE_ARCHIVE_BYTES_OK.
# This script does NOT calculate a checksum: Lolipop SSH lacks sha256sum/openssl.
# No public bootstrap, production config, privilege or other website changes.
set -eu

fail() { echo "$1"; exit 1; }

test "$(uname -s)" = "Linux" || fail "NOT_LINUX_REMOTE"
test -n "${FTP_ROOT:-}" || fail "FTP_ROOT_UNSET"
cd "$FTP_ROOT" || fail "FTP_ROOT_NOT_FOUND"
FTP_ROOT="$(pwd -P)"
test "$(basename "$FTP_ROOT")" = "web" || fail "WRONG_FTP_ROOT"
test -d "$FTP_ROOT/kmhn" || fail "PUBLIC_KMHN_MISSING"

PARENT="$(cd "$FTP_ROOT/.." && pwd -P)" || fail "ACCOUNT_PARENT_NOT_FOUND"
test ! -L "$PARENT/kmhn-mcp-private" || fail "PRIVATE_PARENT_SYMLINK_BLOCKED"
test ! -L "$PARENT/kmhn-mcp-private/server" || fail "PRIVATE_SERVER_SYMLINK_BLOCKED"
PRIVATE="$PARENT/kmhn-mcp-private/server"
test -d "$PRIVATE" || fail "PRIVATE_SERVER_MISSING"
cd "$PRIVATE" || fail "PRIVATE_SERVER_NOT_ACCESSIBLE"
test "$(pwd -P)" = "$PRIVATE" || fail "PRIVATE_REALPATH_MISMATCH"

case "$PRIVATE" in
  "$FTP_ROOT"|"$FTP_ROOT"/*) fail "UNSAFE_PRIVATE_IN_PUBLIC_ROOT" ;;
esac

test -f runtime.tar.gz || fail "PRIVATE_ARCHIVE_MISSING"
test ! -L runtime.tar.gz || fail "PRIVATE_ARCHIVE_SYMLINK_BLOCKED"
for entry in public src vendor runtime composer.json composer.lock; do
  test ! -e "$entry" || fail "PRIVATE_TARGET_NOT_EMPTY"
done
test ! -e "$FTP_ROOT/kmhn/index.php" || fail "PUBLIC_INDEX_ALREADY_PRESENT"
test ! -e "$FTP_ROOT/kmhn/.htaccess" || fail "PUBLIC_HTACCESS_ALREADY_PRESENT"

command -v tar >/dev/null 2>&1 || fail "TAR_UNAVAILABLE"
tar -tzf runtime.tar.gz >/dev/null || fail "ARCHIVE_CANNOT_BE_LISTED"
echo "PRIVATE_TAR_PREFLIGHT_OK"

# The exact artifact is SHA256-pinned, has already been inspected for traversal,
# symlinks, hardlinks, dev nodes and config.php, and matches the Mac readback.
# Extract only into current non-Web directory, with a restrictive umask.
umask 077
if ! tar -xzf runtime.tar.gz; then
  echo "PRIVATE_EXTRACTION_PARTIAL_STOP"
  exit 1
fi

test -f public/index.php || fail "PRIVATE_EXTRACT_INCOMPLETE"
test -f src/Registry.php || fail "PRIVATE_EXTRACT_INCOMPLETE"
test -f src/UniversalTools.php || fail "PRIVATE_EXTRACT_INCOMPLETE"
test -f src/LanguageRouter.php || fail "PRIVATE_EXTRACT_INCOMPLETE"
test -f vendor/autoload.php || fail "PRIVATE_EXTRACT_INCOMPLETE"
test -s runtime/registry.json || fail "PRIVATE_REGISTRY_MISSING"
test -f composer.json || fail "PRIVATE_COMPOSER_MISSING"
test -f composer.lock || fail "PRIVATE_COMPOSER_LOCK_MISSING"
test ! -e runtime/config.php || fail "PRIVATE_CONFIG_UNEXPECTED"
test ! -e "$FTP_ROOT/kmhn/index.php" || fail "PUBLIC_CHANGED_UNEXPECTED"
test ! -e "$FTP_ROOT/kmhn/.htaccess" || fail "PUBLIC_CHANGED_UNEXPECTED"

echo "PRIVATE_RUNTIME_EXTRACTED"
echo "PRIVATE_REQUIRED_FILES_OK"
echo "PRIVATE_CONFIG_ABSENT"
echo "PUBLIC_BOOTSTRAP_UNCHANGED"
echo "MCP_NOT_PUBLIC"
