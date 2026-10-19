<?php
declare(strict_types=1);

// Production TEMPLATE ONLY. DNS and TLS verified, but MCP is NOT DEPLOYED.
// Copy to runtime/config.php ONLY inside the verified NON-WEB private server root.
// The publicly configured subdomain folder is kmhn. Never place this file there or in FTP root.
// Never commit runtime/config.php, credentials, or secrets.
// Local CI must continue using config.example.php (127.0.0.1).
return [
    'host' => 'mcp-kmhn.landco.co.jp',
    'allowed_origins' => [],
];
