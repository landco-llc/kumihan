<?php
declare(strict_types=1);

// Copy to config.php OUTSIDE the public document root.
// Use the dedicated MCP subdomain; NEVER use '*' for host or origins.
return [
    'host' => '127.0.0.1', // Replace with your real public subdomain for production.
    'allowed_origins' => [], // Leave empty for server-to-server MCP. Explicit URLs only if browser use is needed.
];
