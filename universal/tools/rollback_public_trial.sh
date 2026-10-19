#!/bin/sh
# Roll back ONLY the 2 files installed by KUMIHAN G2 public trial.
# Requires exact byte-for-byte equality with the private staged copies.
# Does NOT delete private SDK, config, registry, or any unrelated public file.
set -eu
fail() { echo "$1"; exit 1; }
test "$(uname -s)" = "Linux" || fail "NOT_REMOTE_LINUX"
test "$KUMIHAN_TRIAL_ROLLBACK_APPROVED" = "YES" || fail "ROLLBACK_EXPLICIT_APPROVAL_REQUIRED"
test -n "$FTP_ROOT" || fail "FTP_ROOT_UNSET"
cd "$FTP_ROOT" || fail "FTP_ROOT_NOT_FOUND"
WEB="$(pwd -P)"
test "$(basename "$WEB")" = "web" || fail "WRONG_WEB_ROOT"
test -d "$WEB/kmhn" && test ! -L "$WEB/kmhn" || fail "PUBLIC_ROOT_INVALID"
PRIVATE="$(cd "$WEB/.." && pwd -P)/kmhn-mcp-private/server"
test -d "$PRIVATE/.kmhn-public-stage" || fail "PRIVATE_STAGE_MISSING"
test ! -L "$PRIVATE/.kmhn-public-stage" || fail "PRIVATE_STAGE_SYMLINK_BLOCKED"

for name in index.php .htaccess; do
  file="$WEB/kmhn/$name"
  staged="$PRIVATE/.kmhn-public-stage/$name"
  test -f "$file" && test ! -L "$file" || fail "PUBLIC_FILE_CHANGED_OR_ABSENT"
  test -f "$staged" && test ! -L "$staged" || fail "STAGED_FILE_CHANGED_OR_ABSENT"
  # Avoid dependencies unavailable on Lolipop (sha256sum, openssl, cmp).
  test "$(cat "$file")" = "$(cat "$staged")" || fail "PUBLIC_FILE_CONTENT_MISMATCH_STOP"
done

rm -f "$WEB/kmhn/index.php" || fail "INDEX_REMOVE_FAILED"
rm -f "$WEB/kmhn/.htaccess" || fail "HTACCESS_REMOVE_FAILED"
echo "G2_PUBLIC_TRIAL_ROLLED_BACK"
echo "PRIVATE_RUNTIME_RETAINED"
echo "MCP_NOT_PUBLIC"
