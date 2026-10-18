# Web / Typography and content design

- Use HTML lang="pt-PT" or lang="pt-BR" on a document when its locale is known, and language spans for mixed-language content. Do not infer locale without a project decision.
- Preserve characters: á à â ã é ê í ó ô õ ú ç, uppercase Á Ã Ç, ordinal signs º and ª.
- Choose quotation conventions and numeric separators from an explicit house style. Both pt-PT and pt-BR may use different institutional/brand styles.
- Avoid automatic hyphenation for brand names, buttons and headlines. Body hyphenation must be tested with available dictionary and actual browser rendering.
- Avoid universal word-break: break-all, min-content overflow, too-tight leading, clipped diacritics, and unsupported CSS shortcuts.
- At 320 CSS px and 200% text resize preserve content and functionality. Test actual browser output; do not claim tests from a screenshot alone.
- Before using grids, gradients or cards, justify them by hierarchy, audience and content. Resist repetitive generic AI layouts.
- Report browser engine, viewport, version and untested states. Protect original DOM text and readable source.
