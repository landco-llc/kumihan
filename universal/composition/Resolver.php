<?php
declare(strict_types=1);

namespace Kumihan\Composition;

/**
 * Isolated exact-locale prototype for PHP 8.5. Internal only, no MCP registration.
 * The caller must first use the approved development contract validator.
 * This is NOT a JSON Schema validator, detector, renderer or evidence verifier.
 */
final class Resolver
{
    public static function exactLocale(string $languageTag, array $registry): array
    {
        if (($registry['schema_version'] ?? null) !== '1.0' || !is_array($registry['modules'] ?? null)) {
            throw new \InvalidArgumentException('Legacy registry 1.0 required');
        }
        $matches = [];
        foreach ($registry['modules'] as $id => $module) {
            foreach ($module['locales'] as $locale) {
                if (strcasecmp($languageTag, $locale) === 0) {
                    $matches[$id] = $module;
                    break;
                }
            }
        }
        // No prefix fallback, script equality or implicit English; collisions fail closed.
        if (count($matches) !== 1) {
            return ['resolver_version' => 'exact-locale-1', 'language_tag' => $languageTag,
                'module_id' => null, 'module_version' => null, 'module_sha256' => null,
                'module_status' => null, 'capability_state' => 'unsupported'];
        }
        $id = array_key_first($matches);
        $module = $matches[$id];
        return ['resolver_version' => 'exact-locale-1', 'language_tag' => $languageTag,
            'module_id' => $id, 'module_version' => $module['version'],
            'module_sha256' => $module['module_sha256'], 'module_status' => $module['status'],
            'capability_state' => 'declared'];
    }
}
