<?php
declare(strict_types=1);

require __DIR__ . '/../src/Registry.php';
require __DIR__ . '/../src/LanguageRouter.php';
require __DIR__ . '/../src/UniversalTools.php';

use Kumihan\Mcp\LanguageRouter;
use Kumihan\Mcp\Registry;
use Kumihan\Mcp\UniversalTools;

function check(bool $condition, string $message): void
{
    if (!$condition) {
        throw new RuntimeException('FAIL: ' . $message);
    }
}

$registry = new Registry(__DIR__ . '/../runtime/registry.json');
$router = new LanguageRouter($registry);
$tools = new UniversalTools($registry);
$languages = $tools->listLanguages();
check($languages['count'] >= 20, 'all listed modules registered');
check($router->detect('日本語の文章')['module_id'] === 'ja', 'Kana Japanese');
check($router->detect('문장')['module_id'] === 'ko', 'Hangul Korean');
check($router->detect('ภาษาไทย')['module_id'] === 'th', 'Thai');
check($router->detect('ភាសាខ្មែរ')['module_id'] === 'km', 'Khmer');
check($router->detect('বাংলা')['module_id'] === 'bn', 'Bengali');
check($router->detect('漢字')['language'] === 'und', 'Han alone is ambiguous');
check($router->detect('語言不同，文字編排也會改變。設計時應留意標點與換行。')['language'] === 'und', 'Chinese punctuation must not imply Japanese or Korean');
check(!in_array('kana', $router->detect('文字，排版。')['scripts'], true), 'Han punctuation must not register kana');
check(!in_array('hangul', $router->detect('文字，排版。')['scripts'], true), 'Han punctuation must not register Hangul');
check($router->detect('文字，排版。', 'zh-Hant')['module_id'] === 'zh-Hant', 'Explicit Traditional Chinese preserved');
check($router->detect('Hello world')['language'] === 'und', 'Latin alone is ambiguous');
check($router->detect('سلام')['language'] === 'und', 'Arabic script does not select ar/fa');
check($router->detect('नमस्ते')['language'] === 'und', 'Devanagari is not always Hindi');
check($router->detect('Привет')['language'] === 'und', 'Cyrillic is not always Russian');
check($router->detect('日本語 and English')['needs_review'], 'mixed text needs segment review');
check($router->detect('Bonjour', 'fr-CA')['locale'] === 'fr-CA', 'explicit regional French');
check($router->detect('Hello', 'auto', 'fr-FR')['module_id'] === 'fr', 'metadata language');
check($router->detect('Hallo', 'de', 'fr-CA')['module_id'] === 'de', 'user beats document metadata');
check($router->detect('Bonjour', 'fr-XX')['language'] === 'und', 'unsupported locale not assumed');
check($tools->getGuidance('fr-FR')['status'] === 'guidance_only', 'source backed guidance');
$review = $tools->reviewText('Bonjour', 'fr-FR');
check($review['source_unchanged'] === true, 'source text preserved');
check(count($review['checked']) === 0, 'no fabricated checks');
check(in_array('visual_rendering', $review['not_checked'], true), 'render not checked');
fwrite(STDOUT, 'KUMIHAN Universal PHP registry/router smoke PASS; modules=' . $languages['count'] . PHP_EOL);
