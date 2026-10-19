#!/bin/sh
# One-shot shared-host PHP-to-private-path preflight.
# Run ONLY after logging into Lolipop via SSH, passing FTP_ROOT privately.
# No account IDs, passwords or absolute FTP_ROOT in public logs.
# Creates a private candidate directory and tiny temporary canary/probe.
# Removes both files even on error, leaves the candidate directory only.
set -eu

if [ "$(uname -s)" != "Linux" ]; then
  echo "NOT_ON_LINUX_SERVER"
  exit 1
fi
if [ -z "$FTP_ROOT" ]; then
  echo "FTP_ROOT_NOT_SUPPLIED"
  exit 1
fi
if ! cd "$FTP_ROOT"; then
  echo "FTP_ROOT_UNAVAILABLE"
  exit 1
fi
FTP_ROOT="$(pwd -P)"
if [ "$(basename "$FTP_ROOT")" != "web" ] || [ ! -d "$FTP_ROOT/kmhn" ]; then
  echo "WRONG_DOCUMENT_ROOT"
  exit 1
fi
if [ ! -w "$(dirname "$FTP_ROOT")" ]; then
  echo "PARENT_NOT_WRITABLE"
  exit 1
fi

umask 077
PRIVATE="$(dirname "$FTP_ROOT")/kmhn-mcp-private/server"
mkdir -p "$PRIVATE"
if [ ! -d "$PRIVATE" ] || [ ! -w "$PRIVATE" ]; then
  echo "PRIVATE_DIR_UNAVAILABLE"
  exit 1
fi

NONCE="$(date +%s)_$$"
MARKER=".kmhn-read-$NONCE"
PROBE="kmhn_private_probe_$NONCE.php"
MARKER_PATH="$PRIVATE/$MARKER"
PROBE_PATH="$FTP_ROOT/kmhn/$PROBE"
if [ -e "$MARKER_PATH" ] || [ -e "$PROBE_PATH" ]; then
  echo "PROBE_COLLISION"
  exit 1
fi

cleanup() {
  rm -f "$MARKER_PATH" "$PROBE_PATH"
}
trap cleanup 0
trap 'exit 1' 1 2 3 15

printf '%s' 'KUMIHAN_PRIVATE_READ_CANARY' > "$MARKER_PATH"
cat > "$PROBE_PATH" <<PHP
<?php
@ini_set('display_errors', '0');
header('Content-Type: text/plain; charset=utf-8');
header('Cache-Control: no-store');
\$file = dirname(__DIR__, 2) . '/kmhn-mcp-private/server/$MARKER';
\$ok = is_readable(\$file) && @file_get_contents(\$file) === 'KUMIHAN_PRIVATE_READ_CANARY';
echo 'PHP_VERSION=' . PHP_VERSION . "\\n";
echo 'PHP_SAPI=' . PHP_SAPI . "\\n";
echo 'PRIVATE_PHP_READ=' . (\$ok ? 'PASS' : 'FAIL') . "\\n";
PHP
# Public PHP must be readable by the web server, no credentials in this test.
chmod 604 "$PROBE_PATH"
URL="https://mcp-kmhn.landco.co.jp/$PROBE"
if command -v curl >/dev/null 2>&1; then
  if ! OUT="$(curl --fail --silent --show-error --connect-timeout 8 --max-time 15 "$URL")"; then
    echo "PUBLIC_PHP_HTTP_NOT_VERIFIED"
    exit 1
  fi
elif command -v wget >/dev/null 2>&1; then
  if ! OUT="$(wget -q -O - -T 15 -t 1 "$URL")"; then
    echo "PUBLIC_PHP_HTTP_NOT_VERIFIED"
    exit 1
  fi
else
  echo "NO_HTTPS_CLIENT_AVAILABLE"
  exit 1
fi
printf '%s\n' "$OUT"
case "$OUT" in
  *"PRIVATE_PHP_READ=PASS"*)
    echo "PRIVATE_WEB_PHP_PRECHECK_PASS"
    ;;
  *)
    echo "PRIVATE_WEB_PHP_PRECHECK_NOT_VERIFIED"
    exit 1
    ;;
esac
