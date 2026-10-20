<?php
declare(strict_types=1);

use Http\Discovery\Psr17Factory;
use Kumihan\Mcp\Registry;
use Kumihan\Mcp\UniversalTools;
use Laminas\HttpHandlerRunner\Emitter\SapiEmitter;
use Mcp\Server;
use Mcp\Server\Session\FileSessionLock;
use Mcp\Server\Session\FileSessionStore;
use Mcp\Server\Transport\Http\Middleware\CorsMiddleware;
use Mcp\Server\Transport\Http\Middleware\DnsRebindingProtectionMiddleware;
use Mcp\Server\Transport\StreamableHttpTransport;

// Public document root contains ONLY this front controller and .htaccess.
// Registry, Composer dependencies, session files, and config stay outside it.
$root = dirname(__DIR__);
$configPath = $root . '/runtime/config.php';
$vendorPath = $root . '/vendor/autoload.php';
if (!is_file($configPath) || !is_file($vendorPath)) {
    http_response_code(503);
    header('Content-Type: application/json; charset=utf-8');
    echo '{"error":"KUMIHAN_MCP_NOT_CONFIGURED"}';
    exit;
}

require $vendorPath;
try {
    $config = require $configPath;
    $host = (string) ($config['host'] ?? '');
    $allowedOrigins = $config['allowed_origins'] ?? [];
    // Never trust arbitrary Host headers, wildcards or publicly exposed PHP config.
    if (!preg_match('/^[a-z0-9.-]+$/i', $host)
        || $host === ''
        || !is_array($allowedOrigins)
        || in_array('*', $allowedOrigins, true)
    ) {
        throw new RuntimeException('Invalid MCP host configuration');
    }
    $sessions = $root . '/runtime/sessions';
    if (!is_dir($sessions) || !is_writable($sessions)) {
        throw new RuntimeException('Session directory is unavailable');
    }

    $registry = new Registry($root . '/runtime/registry.json');
    $tools = new UniversalTools($registry);

    $server = Server::builder()
        ->setServerInfo('KUMIHAN Universal', '0.1.0-preview')
        // Handshake-era clients on shared PHP workers need a shared file store;
        // the modern 2026-07-28 era remains stateless.
        ->setSession(new FileSessionStore($sessions))
        ->setSessionLock(new FileSessionLock($sessions))
        ->addTool([$tools, 'listLanguages'], name: 'kumihan_list_languages',
            description: 'List available KUMIHAN language modules, versions and declared capabilities.')
        ->addTool([$tools, 'detectLanguage'], name: 'kumihan_detect_language',
            description: 'Detect candidate typography languages conservatively; explicit locale and document metadata take priority.')
        ->addTool([$tools, 'getGuidance'], name: 'kumihan_get_guidance',
            description: 'Fetch source-backed language guidance; never claim rendered verification.')
        ->addTool([$tools, 'reviewText'], name: 'kumihan_review_text',
            description: 'Provide read-only typography guidance with explicit not-checked status, without editing original text.')
        ->build();

    $request = (new Psr17Factory())->createServerRequestFromGlobals();
    $transport = new StreamableHttpTransport(
        $request,
        middleware: [
            new CorsMiddleware(allowedOrigins: $allowedOrigins),
            new DnsRebindingProtectionMiddleware(
                allowedHosts: [$host],
                allowedOrigins: $allowedOrigins
            ),
        ],
        maxBodyBytes: 64 * 1024,
    );
    (new SapiEmitter())->emit($server->run($transport));
} catch (Throwable $error) {
    // Never print exception traces, paths or user-supplied content to public clients.
    http_response_code(503);
    header('Content-Type: application/json; charset=utf-8');
    echo '{"error":"KUMIHAN_MCP_UNAVAILABLE"}';
}
