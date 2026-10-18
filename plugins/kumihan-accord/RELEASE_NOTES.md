# KUMIHAN｜Accord v0.1.1 — Icon packaging fix

Español: se incluye el logotipo oficial de KUMIHAN en cada skill y plugin. ChatGPT/Codex utiliza `logo` y `composerIcon`; los skills llevan `agents/openai.yaml`. Claude incluye `displayName` e `icon`; Gemini lleva el recurso gráfico, aunque Gemini CLI no documenta un campo estándar para mostrar iconos.

English: the approved KUMIHAN logo now ships inside all 15 ZIPs. ChatGPT/Codex plugin and skills use documented icon metadata. Claude plugin includes its directory icon metadata. Gemini CLI package includes the logo, but its published extension manifest does not define an icon UI field.

- 4 independently installable skills across ChatGPT, Claude and Gemini.
- 3 host plugin/extension ZIPs, all with packaged image assets.
- Original v0.1.0 remains immutable and available. v0.1.1 fixes missing icons without modifying typography rules.
- Host UI render/display requires actual installed-client verification and must not be claimed from ZIP tests.
