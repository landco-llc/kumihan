#!/bin/sh
# KUMIHAN — diagnose an incomplete Lolipop full-web symlink scan.
# Read-only: never creates, changes, removes, or publishes anything.
# Does not print file names, account IDs, paths, or contents.
set -e

fail() { echo "$1"; exit 1; }
test "$(uname -s)" = "Linux" || fail "NOT_REMOTE_LINUX"
test -n "$FTP_ROOT" || fail "FTP_ROOT_NOT_SET"
cd "$FTP_ROOT" || fail "FTP_ROOT_MISSING"
WEB="$(pwd -P)"
test "$(basename "$WEB")" = "web" || fail "WRONG_FTP_ROOT"
test -d "$WEB/kmhn" || fail "PUBLIC_KMHN_MISSING"
test ! -L "$WEB/kmhn" || fail "PUBLIC_KMHN_SYMLINK_PRESENT"

# Check the exact subdomain folder independently of unrelated websites.
# Captured output is intentionally never printed.
if KMHN_RESULT="$(LC_ALL=C find "$WEB/kmhn" -type l -print 2>&1)"; then
  if [ -z "$KMHN_RESULT" ]; then
    echo "KMHN_SYMLINK_SCOPE_CLEAR"
  else
    echo "KMHN_SYMLINKS_NEED_REVIEW"
  fi
else
  echo "KMHN_SYMLINK_SCOPE_INCOMPLETE"
fi

# Previous preflight returned nonzero for this scope, with stderr hidden.
# Preserve both streams solely for local classification, never display paths.
if WEB_RESULT="$(LC_ALL=C find "$WEB" -type l -print 2>&1)"; then
  if [ -z "$WEB_RESULT" ]; then
    echo "WEB_WIDE_SYMLINK_SCAN_CLEAR"
  else
    echo "WEB_WIDE_SYMLINKS_NEED_REVIEW"
  fi
else
  case "$WEB_RESULT" in
    *"Permission denied"*|*"Operation not permitted"*)
      echo "WEB_WIDE_SCAN_PERMISSION_LIMIT"
      ;;
    *"No such file or directory"*|*"File not found"*)
      echo "WEB_WIDE_SCAN_CHANGED_OR_MISSING_ENTRY"
      ;;
    *"unknown predicate"*|*"invalid predicate"*|*"unrecognized"*)
      echo "WEB_WIDE_SCAN_FIND_INCOMPATIBLE"
      ;;
    *)
      echo "WEB_WIDE_SCAN_OTHER_ERROR"
      ;;
  esac
  echo "WEB_WIDE_SYMLINK_SCAN_INCOMPLETE"
fi

echo "OTHER_VHOST_UPLOAD_MAPPINGS_NEED_OWNER_REVIEW"
echo "NO_FILES_CHANGED"
