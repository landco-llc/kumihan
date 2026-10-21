# KUMIHAN｜Samklang

Veiledning i norsk typografi for bokmål og nynorsk, med bevaring av originaltekst og tydelig skille mellom lesetekst, grensesnitt og uttrykksfull tekst. | Norwegian typography guidance for Bokmål and Nynorsk, preserving original text and distinguishing reading text, interfaces and expressive copy.

Versjon / Version: 0.1.0. Utvikler / Developer: L&Co. LLC. Apache-2.0.

Installer enten hele vertspakken eller én selvstendig Skill. Pakk ut arkivet først. Codex: bruk `.codex-plugin/plugin.json`; Claude Code: bruk `.claude-plugin/plugin.json` og den lokale plugin-mappen; Gemini CLI: `gemini extensions install /sti/til/kumihan-samklang-no`. Kontroller kommandoene i din klientversjon.

Install either a full host package or one standalone Skill. Extract the archive first. Codex uses `.codex-plugin/plugin.json`; Claude Code uses `.claude-plugin/plugin.json` in the local plugin directory; Gemini CLI: `gemini extensions install /path/to/kumihan-samklang-no`. Verify commands against your client version.

Standalone Skills: install the extracted Skill directory in your host’s configured Skill location; retain its bundled files. Select the core, web, documents or review Skill by task. Never require a sibling Skill.

Les [arbeidsflyten](references/workflow.md) / Read the [workflow](references/workflow.md). Kjør / Run: `python runtime/check_source.py SOURCE --locale nn-NO`. Native klienter, rendering, Office/PDF og språkfaglig fullkontroll er ikke prøvd. Native clients, rendering, Office/PDF and full expert proofreading are not checked.

Checksum files: `SHA256SUMS-gpt-codex`, `SHA256SUMS-claude`, and `SHA256SUMS-gemini`; choose the file for your host.
