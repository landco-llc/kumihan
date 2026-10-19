<?php
declare(strict_types=1);

namespace Kumihan\Mcp;

/**
 * Conservative typography router. Unicode scripts are not equivalent to languages.
 * Returned span offsets are UTF-8 BYTE offsets and never imply rendered positions.
 */
final class LanguageRouter
{
    private const PATTERNS = [
        'kana' => '/[\p{Hiragana}\p{Katakana}]+/u',
        'hangul' => '/\p{Hangul}+/u',
        'thai' => '/\p{Thai}+/u',
        'khmer' => '/\p{Khmer}+/u',
        'bengali' => '/\p{Bengali}+/u',
        'devanagari' => '/\p{Devanagari}+/u',
        'arabic' => '/\p{Arabic}+/u',
        'cyrillic' => '/\p{Cyrillic}+/u',
        'han' => '/\p{Han}+/u',
        'latin' => '/\p{Latin}+/u',
        'hebrew' => '/\p{Hebrew}+/u',
    ];

    private const UNIQUE_SCRIPT_MODULES = [
        'kana' => 'ja',
        'hangul' => 'ko',
        'thai' => 'th',
        'khmer' => 'km',
        'bengali' => 'bn',
    ];

    public function __construct(private Registry $registry)
    {
    }

    public function detect(string $text, string $language = 'auto', string $documentLang = ''): array
    {
        if (!mb_check_encoding($text, 'UTF-8')) {
            return $this->unknown('invalid-utf8', []);
        }
        if (strlen($text) > 30000) {
            return $this->unknown('input-too-large', []);
        }

        $spans = $this->spans($text);
        if ($language !== '' && strcasecmp($language, 'auto') !== 0) {
            return $this->explicit($language, 'user-explicit', $spans);
        }
        if (trim($documentLang) !== '') {
            return $this->explicit($documentLang, 'document-metadata', $spans);
        }

        $significant = [];
        foreach ($spans as $span) {
            $significant[$span['script']] = true;
        }
        // A mixture of individually recognizable writing systems needs per-span review.
        $differentScripts = array_keys($significant);
        $eligible = array_values(array_filter($differentScripts, fn(string $s): bool => isset(self::UNIQUE_SCRIPT_MODULES[$s])));
        if (count($eligible) === 1) {
            $id = self::UNIQUE_SCRIPT_MODULES[$eligible[0]];
            $selected = $this->registry->resolve($id);
            if ($selected !== null) {
                return [
                    'language' => $id,
                    'locale' => $id,
                    'module_id' => $id,
                    'confidence' => count($differentScripts) === 1 ? 'high' : 'medium',
                    'reason' => 'distinctive-script-signal',
                    'needs_review' => count($differentScripts) !== 1,
                    'scripts' => $differentScripts,
                    'spans' => $spans,
                    'source_unchanged' => true,
                ];
            }
        }
        return $this->unknown(
            $eligible ? 'mixed-distinct-scripts' : ($differentScripts ? 'script-not-unique-to-language' : 'no-language-evidence'),
            $spans
        );
    }

    private function explicit(string $language, string $provenance, array $spans): array
    {
        $selected = $this->registry->resolve($language);
        if ($selected === null) {
            return $this->unknown('explicit-locale-not-registered', $spans, $language);
        }
        return [
            'language' => $selected['module_id'],
            'locale' => $selected['locale'],
            'module_id' => $selected['module_id'],
            'confidence' => 'explicit',
            'reason' => $provenance,
            'needs_review' => false,
            'scripts' => array_values(array_unique(array_column($spans, 'script'))),
            'spans' => $spans,
            'source_unchanged' => true,
        ];
    }

    private function unknown(string $reason, array $spans, string $requested = ''): array
    {
        return [
            'language' => 'und',
            'locale' => null,
            'module_id' => null,
            'confidence' => 'undetermined',
            'reason' => $reason,
            'requested' => $requested,
            'needs_review' => true,
            'scripts' => array_values(array_unique(array_column($spans, 'script'))),
            'spans' => $spans,
            'source_unchanged' => true,
        ];
    }

    private function spans(string $text): array
    {
        $spans = [];
        $matches = [];
        // Each run is only a script clue. Spaces/punctuation remain untouched.
        preg_match_all('/[\p{Hiragana}\p{Katakana}]+|\p{Hangul}+|\p{Thai}+|\p{Khmer}+|\p{Bengali}+|\p{Devanagari}+|\p{Arabic}+|\p{Cyrillic}+|\p{Han}+|\p{Latin}+|\p{Hebrew}+/u', $text, $matches, PREG_OFFSET_CAPTURE);
        foreach ($matches[0] ?? [] as $match) {
            [$run, $byteOffset] = $match;
            $script = 'unknown';
            foreach (self::PATTERNS as $name => $pattern) {
                if (preg_match($pattern, $run) === 1) {
                    $script = $name;
                    break;
                }
            }
            $spans[] = [
                'script' => $script,
                'byte_start' => $byteOffset,
                'byte_length' => strlen($run),
                'candidate_language' => self::UNIQUE_SCRIPT_MODULES[$script] ?? 'und',
            ];
            if (count($spans) >= 256) {
                break;
            }
        }
        return $spans;
    }
}
