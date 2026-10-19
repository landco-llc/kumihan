<?php
declare(strict_types=1);

// Production TEMPLATE ONLY. This hostname is planned; DNS, SSL and service are NOT yet provisioned.
// Copy to runtime/config.php OUTSIDE the document root only after host setup and authorization.
// Never commit runtime/config.php, credentials, or secrets.
// Local CI must continue using config.example.php (127.0.0.1).
return [
    'host' => 'mcp-kmhn.landco.co.jp',
    'allowed_origins' => [],
];
