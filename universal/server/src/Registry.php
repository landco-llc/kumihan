<?php
declare(strict_types=1);

namespace Kumihan\Mcp;

use RuntimeException;

/** Immutable, generated language registry. No runtime remote fetch or arbitrary path loads. */
final class Registry
{
    private array $modules;

    public function __construct(string $registryFile)
    {
        if (!is_file($registryFile)) {
            throw new RuntimeException('KUMIHAN registry not built');
        }
        $raw = file_get_contents($registryFile);
        $data = json_decode($raw === false ? '' : $raw, true, 512, JSON_THROW_ON_ERROR);
        if (($data['schema_version'] ?? null) !== '1.0' || !is_array($data['modules'] ?? null)) {
            throw new RuntimeException('Unsupported module registry schema');
        }
        $this->modules = $data['modules'];
    }

    public function languages(): array
    {
        $items = [];
        foreach ($this->modules as $id => $module) {
            $items[] = [
                'id' => $id,
                'name' => $module['name'],
                'version' => $module['version'],
                'status' => $module['status'],
                'capabilities' => $module['capabilities'],
                'locales' => $module['locales'],
                'rule_count' => count($module['rules']),
                'module_sha256' => $module['module_sha256'],
            ];
        }
        return $items;
    }

    public function resolve(string $language): ?array
    {
        $language = trim(str_replace('_', '-', $language));
        if ($language === '' || strcasecmp($language, 'auto') === 0) {
            return null;
        }
        // Match a BCP47 tag against declared IDs/locales, without guessing missing regions.
        foreach ($this->modules as $id => $module) {
            foreach ($module['locales'] as $locale) {
                if (strcasecmp($locale, $language) === 0) {
                    return ['module_id' => $id, 'locale' => $locale, 'module' => $module];
                }
            }
        }
        return null;
    }

    public function module(string $id): ?array
    {
        return $this->modules[$id] ?? null;
    }
}
