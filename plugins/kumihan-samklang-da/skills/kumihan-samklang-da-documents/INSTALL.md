# KUMIHAN｜Samklang

## Dansk

Pak ud uden at ændre mappestrukturen. En selvstændig Skill installeres som en hel mappe med SKILL.md og alle undermapper i værtens Skill-mappe. Plugin/udvidelse installeres med værtens normale lokale installationsmekanisme; vælg den udgave, der passer til værten. OpenAI/Codex bruger .codex-plugin/plugin.json, Claude Code .claude-plugin/plugin.json og Gemini CLI gemini-extension.json samt GEMINI.md. Brug kun én udgave af samme Skill i samme søgesti.

Læs værtens aktuelle installationsvejledning. Brug --locale da-DK til offlinehjælperen. Installation i en native vært er ikke bekræftet af den statiske kontrol. Ingen konto, netværk eller eksterne skrifter kræves af offlinehjælperen.

## English

Extract without changing the directory structure. Install each standalone Skill folder, including SKILL.md and every resource subfolder, into the host's documented Skill location. Install the matching plugin/extension through the host's normal local installation mechanism. OpenAI/Codex uses .codex-plugin/plugin.json, Claude Code uses .claude-plugin/plugin.json, and Gemini CLI uses gemini-extension.json plus GEMINI.md. Avoid duplicate installations of the same Skill in one search path.

Consult the host's current installation documentation. Use --locale da-DK for the offline helper. Static checks do not establish native-host installation acceptance. The helper requires no account, network or external fonts.

## Lokale kommandoer / Local commands

Claude Code: `claude --plugin-dir /absolute/path/kumihan-samklang-da`; selvstændige Skills / standalone Skills: `.claude/skills/`. Gemini CLI: `gemini extensions link /absolute/path/kumihan-samklang-da`; selvstændige Skills i værtens dokumenterede mappe, hvis understøttet / standalone Skills in the documented host directory, where supported. GPT/Codex: brug værtens konfigurerede Skills-mappe eller lokale plugininstallation / use the configured Skills directory or local plugin flow. Kontroller CLI-hjælp for din version / Check installed CLI help for version-specific support.
