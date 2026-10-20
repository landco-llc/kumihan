#!/bin/sh
# KUMIHAN Universal MCP — bounded private configuration + temporary Web PHP smoke.
# Run ONLY from an authenticated Lolipop SSH shell, after the six private
# extraction PASS markers. Never run on Mac or inside a public web directory.
# Changes: copy no-secret production example to private config.php (only if
# absent), create+remove one short-lived public PHP probe, and create+remove
# one temporary private session marker through the Web PHP process.
# Does NOT install a public MCP bootstrap, start the MCP server, or publish.
set -eu

fail() { echo "$1"; exit 1; }
test "$(uname -s)" = "Linux" || fail "NOT_LINUX_REMOTE"
test -n "$FTP_ROOT" || fail "FTP_ROOT_NOT_SET"
cd "$FTP_ROOT" || fail "FTP_ROOT_MISSING"
FTP_ROOT="$(pwd -P)"
test "$(basename "$FTP_ROOT")" = "web" || fail "WRONG_WEB_ROOT"
test -d "$FTP_ROOT/kmhn" || fail "PUBLIC_FOLDER_MISSING"
test ! -e "$FTP_ROOT/kmhn/index.php" || fail "PUBLIC_BOOTSTRAP_ALREADY_PRESENT"
test ! -e "$FTP_ROOT/kmhn/.htaccess" || fail "PUBLIC_HTACCESS_ALREADY_PRESENT"

PARENT="$(cd "$FTP_ROOT/.." && pwd -P)" || fail "ACCOUNT_PARENT_MISSING"
test ! -L "$PARENT/kmhn-mcp-private" || fail "PRIVATE_SYMLINK_BLOCKED"
test ! -L "$PARENT/kmhn-mcp-private/server" || fail "PRIVATE_SYMLINK_BLOCKED"
PRIVATE="$PARENT/kmhn-mcp-private/server"
cd "$PRIVATE" || fail "PRIVATE_DIR_UNAVAILABLE"
test "$(pwd -P)" = "$PRIVATE" || fail "PRIVATE_REALPATH_MISMATCH"
case "$PRIVATE" in
 "$FTP_ROOT"|"$FTP_ROOT"/*) fail "UNSAFE_PRIVATE_IN_WEB" ;;
esac

for f in public/index.php src/Registry.php src/UniversalTools.php src/LanguageRouter.php vendor/autoload.php runtime/registry.json runtime/config.production.example.php composer.json composer.lock; do
  test -s "$f" || fail "PRIVATE_REQUIRED_FILE_MISSING"
done
test -d runtime/sessions || fail "SESSION_DIR_MISSING"
test ! -L runtime/config.production.example.php || fail "CONFIG_TEMPLATE_SYMLINK_BLOCKED"
test ! -e runtime/config.php || fail "PRIVATE_CONFIG_ALREADY_EXISTS"
test ! -L runtime/config.php || fail "PRIVATE_CONFIG_SYMLINK_BLOCKED"

# No credential or token is in the production template.
umask 077
cp runtime/config.production.example.php runtime/config.php || fail "PRIVATE_CONFIG_COPY_FAILED"
chmod 600 runtime/config.php || fail "PRIVATE_CONFIG_PERMISSION_FAILED"
if ! grep -Fq "'host' => 'mcp-kmhn.landco.co.jp'" runtime/config.php; then
  fail "PRIVATE_CONFIG_HOST_INVALID"
fi
if ! grep -Fq "'allowed_origins' => []" runtime/config.php; then
  fail "PRIVATE_CONFIG_ORIGINS_INVALID"
fi
echo "PRIVATE_CONFIG_CREATED"

NONCE="$(date +%s)_$$"
PROBE_PATH="$FTP_ROOT/kmhn/kmhn_runtime_check_$NONCE.php"
test ! -e "$PROBE_PATH" || fail "PUBLIC_PROBE_COLLISION"
test ! -L "$PROBE_PATH" || fail "PUBLIC_PROBE_SYMLINK_BLOCKED"
cleanup() { rm -f "$PROBE_PATH"; }
trap cleanup 0
trap 'exit 1' 1 2 3 15

cat > "$PROBE_PATH" <<'PHP'
<?php
declare(strict_types=1);
@ini_set('display_errors', '0');
@ini_set('log_errors', '0');
header('Content-Type: text/plain; charset=utf-8');
header('Cache-Control: no-store');

$root = dirname(__DIR__, 2) . '/kmhn-mcp-private/server';
$checks = [
    'WEB_PHP85' => PHP_VERSION_ID >= 80500 && PHP_VERSION_ID < 80600,
    'WEB_SAPI_LITESPEED' => PHP_SAPI === 'litespeed',
    'EXTENSIONS' => extension_loaded('json') && extension_loaded('fileinfo'),
    'PRIVATE_CONFIG' => false,
    'SDK_AUTOLOAD' => false,
    'REGISTRY' => false,
    'SESSION_WRITE' => false,
];
$moduleCount = 0;

try {
    $configFile = $root . '/runtime/config.php';
    if (is_readable($configFile)) {
        $cfg = require $configFile;
        $checks['PRIVATE_CONFIG'] =
            is_array($cfg)
            && ($cfg['host'] ?? '') === 'mcp-kmhn.landco.co.jp'
            && ($cfg['allowed_origins'] ?? null) === [];
    }
} catch (Throwable $e) {
    // Do not disclose private paths, error details or application contents.
}

try {
    $autoload = $root . '/vendor/autoload.php';
    if (is_readable($autoload)) {
        require_once $autoload;
        $checks['SDK_AUTOLOAD'] =
            class_exists(\Mcp\Server::class)
            && class_exists(\Kumihan\Mcp\Registry::class);
    }
    if ($checks['SDK_AUTOLOAD']) {
        $registry = new \Kumihan\Mcp\Registry($root . '/runtime/registry.json');
        $moduleCount = count($registry->languages());
        $checks['REGISTRY'] = $moduleCount === 21;
    }
} catch (Throwable $e) {
    // Do not disclose server implementation details.
}

try {
    $sessions = $root . '/runtime/sessions';
    if (is_dir($sessions) && is_writable($sessions)) {
        $marker = $sessions . '/.kmhn-smoke-' . bin2hex(random_bytes(12));
        $file = @fopen($marker, 'x');
        if ($file !== false) {
            $written = fwrite($file, 'ok');
            fclose($file);
            $removed = @unlink($marker);
            $checks['SESSION_WRITE'] = $written === 2 && $removed;
        }
    }
} catch (Throwable $e) {
    // No sensitive output.
}
echo 'PHP_VERSION=' . PHP_VERSION . PHP_EOL;
echo 'PHP_SAPI=' . PHP_SAPI . PHP_EOL;
echo 'REGISTRY_MODULES=' . $moduleCount . PHP_EOL;
foreach ($checks as $name => $ok) {
    echo $name . '=' . ($ok ? 'PASS' : 'FAIL') . PHP_EOL;
}
PHP
chmod 604 "$PROBE_PATH" || fail "PUBLIC_PROBE_PERMISSION_FAILED"
URL="https://mcp-kmhn.landco.co.jp/$(basename "$PROBE_PATH")"
if command -v curl >/dev/null 2>&1; then
    if ! BODY="$(curl --fail --silent --show-error --connect-timeout 8 --max-time 20 "$URL")"; then
        fail "WEB_RUNTIME_HTTP_NOT_VERIFIED"
    fi
elif command -v wget >/dev/null 2>&1; then
    if ! BODY="$(wget -q -O - -T 20 -t 1 "$URL")"; then
        fail "WEB_RUNTIME_HTTP_NOT_VERIFIED"
    fi
else
    fail "NO_WEB_HTTP_CLIENT"
fi
printf '%s\n' "$BODY" | grep -E '^(PHP_VERSION|PHP_SAPI|REGISTRY_MODULES|WEB_PHP85|WEB_SAPI_LITESPEED|EXTENSIONS|PRIVATE_CONFIG|SDK_AUTOLOAD|REGISTRY|SESSION_WRITE)=' || fail "WEB_RUNTIME_UNEXPECTED_RESPONSE"
for name in WEB_PHP85 WEB_SAPI_LITESPEED EXTENSIONS PRIVATE_CONFIG SDK_AUTOLOAD REGISTRY SESSION_WRITE; do
    printf '%s\n' "$BODY" | grep -Fxq "$name=PASS" || fail "WEB_RUNTIME_NOT_READY"
done
echo "PRIVATE_RUNTIME_WEB_READY"
test ! -e "$FTP_ROOT/kmhn/index.php" || fail "PUBLIC_BOOTSTRAP_CHANGED"
test ! -e "$FTP_ROOT/kmhn/.htaccess" || fail "PUBLIC_HTACCESS_CHANGED"
echo "MCP_NOT_PUBLIC"
