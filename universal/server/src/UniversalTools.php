<?php
declare(strict_types=1);

namespace Kumihan\Mcp;

use InvalidArgumentException;

/** Read-only MCP tools. These never edit supplied source or imply visual inspection. */
final class UniversalTools
{
    private LanguageRouter $router;

    public function __construct(private Registry $registry)
    {
        $this->router = new LanguageRouter($registry);
    }

    /** Return installed language modules, independently pinned versions and capabilities. */
    public function listLanguages(): array
    {
        $languages = $this->registry->languages();
        return [
            'product' => 'KUMIHAN Universal',
            'count' => count($languages),
            'languages' => $languages,
            'note' => 'Preview registry; presence does not prove host-specific or rendered validation.',
        ];
    }

    /**
     * Conservatively detect language with explicit user/metadata precedence.
     * Unicode scripts cannot resolve all languages; ambiguous Latin, Han and Arabic-family text is undetermined.
     */
    public function detectLanguage(string $text, string $language = 'auto', string $documentLang = ''): array
    {
        return $this->router->detect($text, $language, $documentLang);
    }

    /**
     * Load source-backed typography/design guidance from a single language module.
     * Guidance is not equivalent to deterministic verification or rendered proof.
     */
    public function getGuidance(string $language, string $medium = 'web', string $mode = 'review', int $limit = 12): array
    {
        if (!in_array($medium, ['web', 'document', 'presentation', 'display-copy', 'print'], true)) {
            throw new InvalidArgumentException('Unsupported medium');
        }
        if (!in_array($mode, ['study', 'build', 'review', 'refine', 'audit'], true)) {
            throw new InvalidArgumentException('Unsupported mode');
        }
        $selected = $this->registry->resolve($language);
        if ($selected === null) {
            return ['status' => 'unsupported_or_ambiguous', 'language' => $language, 'needs_review' => true];
        }
        $module = $selected['module'];
        $max = min(max($limit, 1), 25);
        $rules = [];
        foreach (array_slice($module['rules'], 0, $max) as $rule) {
            $rules[] = [
                'id' => $rule['id'],
                'title' => $rule['title'],
                'verification' => $rule['verification'],
                'source_file' => $rule['source_file'],
                'application' => 'candidate_requires_context',
            ];
        }
        return [
            'status' => 'guidance_only',
            'language' => $selected['module_id'],
            'locale' => $selected['locale'],
            'medium' => $medium,
            'mode' => $mode,
            'module_name' => $module['name'],
            'module_version' => $module['version'],
            'module_sha256' => $module['module_sha256'],
            'entry_skill_path' => $module['entry_skill_path'],
            'entry_guidance' => substr($module['entry_skill_text'], 0, 4500),
            'rules' => $rules,
            'rules_total' => count($module['rules']),
            'notes' => 'Rule catalog items are advisory candidates, not automatically executed checks. Locale-specific rules require selected region/house style.',
        ];
    }

    /**
     * Review text conservatively. Returns source-preserving guidance and explicit unchecked findings.
     * This first release DOES NOT claim a visual, browser, document-render or automatic typography audit.
     */
    public function reviewText(string $text, string $language = 'auto', string $documentLang = '', string $medium = 'web'): array
    {
        if (!in_array($medium, ['web', 'document', 'presentation', 'display-copy', 'print'], true)) {
            throw new InvalidArgumentException('Unsupported medium');
        }
        $route = $this->router->detect($text, $language, $documentLang);
        $guidance = $route['module_id'] === null ? null : $this->getGuidance((string) $route['locale'], $medium, 'review', 5);
        return [
            'status' => $route['needs_review'] ? 'needs-review' : 'guidance-only',
            'source_unchanged' => true,
            'language_resolution' => $route,
            'module_version' => $guidance['module_version'] ?? null,
            'module_sha256' => $guidance['module_sha256'] ?? null,
            'rule_candidates' => $guidance['rules'] ?? [],
            'findings' => [],
            'checked' => [],
            'not_checked' => [
                'visual_rendering', 'fonts_and_glyph_coverage', 'line_wrap_on_target_device',
                'locale_specific_typography', 'semantic_copy_quality',
                'automatic_rule_detection_not_yet_implemented',
            ],
            'notice' => 'No edits were made. This tool currently routes and provides rule guidance; it does not assert a passed layout or text validation.',
        ];
    }
}
