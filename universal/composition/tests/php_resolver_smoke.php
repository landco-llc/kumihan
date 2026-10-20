<?php
declare(strict_types=1);
$prototype = dirname(__DIR__) . '/Resolver.php';
if (!is_file($prototype)) { fwrite(STDERR, "FAIL: isolated PHP resolver missing\n"); exit(1); }
require $prototype;
$registry = json_decode(file_get_contents($argv[1]), true, 512, JSON_THROW_ON_ERROR);
$cases = json_decode(file_get_contents(__DIR__ . '/php_resolver_cases.json'), true, 512, JSON_THROW_ON_ERROR);
$count = 0;
foreach ($cases as $case) {
    $before = serialize($registry);
    $result = \Kumihan\Composition\Resolver::exactLocale($case['tag'], $registry);
    if ($result['module_id'] !== $case['expected'] || $result['capability_state'] === 'verified' || serialize($registry) !== $before) {
        throw new RuntimeException('Exact-locale/source-preserving resolver case failed');
    }
    $count++;
}
$registry['modules']['duplicate'] = $registry['modules']['ja'];
if (\Kumihan\Composition\Resolver::exactLocale('ja', $registry)['module_id'] !== null) {
    throw new RuntimeException('Ambiguous declarations must remain unresolved');
}
echo 'PASS: ' . ($count+1) . " resolver cases; no PHP Schema conformance claim\n";
