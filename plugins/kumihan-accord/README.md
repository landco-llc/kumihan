# KUMIHAN｜Accord

Version 0.1.2 · Open source · Apache-2.0 · L&Co. LLC

## Español

Guía de tipografía francesa para web, documentos y presentaciones; conserva el texto original y permite revisiones de solo lectura. Cuatro skills independientes para entrada, web, documentos y revisión. Separa región, estilo editorial y formato. Selecciona explícitamente fr-fr-editorial, fr-ca-oqlf o eu-interinstitutional; fr-BE y fr-CH requieren una norma editorial concreta. Nunca reescribe el texto original sin autorización.

## English

French typography guidance for web, documents and presentations; preserves original text and supports read-only reviews. Four independent skills cover entry, web, documents and review. House style is explicit, not guessed from locale. Static candidate checks are not rendered evidence or French language correction. Source text is preserved by default.

## Skills

- [kumihan-accord](skills/kumihan-accord/SKILL.md)
- [kumihan-accord-web](skills/kumihan-accord-web/SKILL.md)
- [kumihan-accord-documents](skills/kumihan-accord-documents/SKILL.md)
- [kumihan-accord-review](skills/kumihan-accord-review/SKILL.md)

## Distribution / Distribución

Release: [GitHub Release v0.1.2](https://github.com/landco-llc/kumihan/releases/tag/kumihan-fr-v0.1.2) · 15 ZIP files · SHA256SUMS.txt · MANIFEST.json

The public display name is KUMIHAN｜Accord; versions occur only in ZIP filenames and technical manifests. Machine identifier kumihan-accord is ASCII for Claude and Gemini compatibility. The package is free. Each skill includes its full independent rules and references.

[Installation / Instalación](INSTALL.md) · [Rules](rules/catalog.json) · [Sources](sources.json) · [Review limitations](LIGHT_REVIEW.md).

GitHub releases do not imply ChatGPT, Claude or Gemini official directory approval. Native host and rendering tests need real execution.


## 0.1.1 icon correction / Corrección de iconos

Official KUMIHAN artwork is bundled in the plugin and every standalone skill. ChatGPT/Codex manifests now reference `logo` and `composerIcon`; skill UI metadata lives in `agents/openai.yaml`. Claude includes an icon path, subject to its host UI support. Gemini CLI includes the image but does not document an icon-display field. Update to v0.1.1; v0.1.0 files remain unchanged.


## Regional evidence and processing scope / Alcance regional

Version 0.1.2 separates accepted forms from explicit normalization.
The bounded helper evaluates selected French editorial, OQLF or EU punctuation;
it preserves time colons and original source bytes during audit. OQLF permits
zero or U+202F before `! ? ;`; ordinary U+0020 is evaluated separately.
Proposals are previews for authorized generated one-line plain text. They do not
edit supplied text or partially rewrite HTML, Markdown, URLs or code.

ULB, Swiss federal, Vaud and Luxembourg SIP profiles, regional vocabulary,
address forms and organization-specific design examples are **reference data**.
Their presence does not add a formatter or an executable punctuation profile.
Swiss federal four-digit grouping remains on hold; SIP is the January 2012
edition with organization and medium conditions. A country or locale never
selects an institution's editorial rules or fonts automatically.

No exact-decimal currency/date formatter, mixed-language DOM editor, browser or
Office/PDF renderer is bundled. Static results do not prove native installation,
French editorial approval, font shaping, accessibility or legal compliance.
See [capability boundaries](references/regional-capabilities.md) and the
[review protocol](references/review.md). Earlier 0.1.1 release artifacts remain unchanged.

La versión 0.1.2 distingue las formas admitidas de la
normalización solicitada. Los perfiles ULB, Suiza federal, Vaud y SIP de
Luxemburgo, el vocabulario y los ejemplos de diseño son referencias para revisión.
No implican formato numérico exacto, edición parcial de DOM ni validación visual.
Los archivos de la versión anterior 0.1.1 permanecen sin cambios.
