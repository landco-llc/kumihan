# Installation and evidence limits

تنزيلات مستقلة مع تحقق من البصمات | Independent downloads with checksum verification.

Use downloads/MANIFEST.json and SHA256SUMS.txt to match the exact v0.1.0 archive and bytes. All ZIPs contain one safe top-level directory; extract before using host-specific local installation instructions. Never upload private source unless you have chosen the provider and its data handling.

## ChatGPT / Codex

Plugin: kumihan-ar-GPT-Codex-plugin-v0.1.0.zip includes agent plugin.json and .codex-plugin/plugin.json compatibility metadata. Standalone: kumihan-ar, kumihan-ar-web, kumihan-ar-documents and kumihan-ar-review -v0.1.0.zip. For Codex local skills, extract the chosen skill directory into an approved skills directory (for example project .agents/skills/), then reload and invoke the matching skill. ChatGPT plugin availability depends on the product's available import surface; a ZIP alone does not establish ChatGPT acceptance. Manual / native import not-checked.

Official references: https://developers.openai.com/plugins/build/plugins and https://developers.openai.com/codex/skills/ . No directory listing or approval is claimed.

## Claude Code / Claude

Plugin: kumihan-ar-Claude-Code-plugin-v0.1.0.zip contains .claude-plugin/plugin.json and skills/. Extract then run Claude Code with `claude --plugin-dir /absolute/path/kumihan-ar`. Standalone files use -Claude-skill-v0.1.0.zip; extract a chosen skill root into an approved .claude/skills/ directory. Claude chat skill upload availability is account/product dependent. Native installation and invocation not-checked.

Official references: https://code.claude.com/docs/en/plugins and https://code.claude.com/docs/en/skills . No marketplace listing is claimed.

## Gemini CLI / Gemini

Extension: kumihan-ar-Gemini-CLI-extension-v0.1.0.zip contains gemini-extension.json, GEMINI.md and skills/. Extract then install the local extension with `gemini extensions install /absolute/path/kumihan-ar`; review the host's trust prompt and restart as required. Standalone files use -Gemini-Apps-skill-v0.1.0.zip and contain portable SKILL.md roots. These are manual / unverified for Gemini Apps: do not assume the chat app accepts a CLI extension or this skill ZIP format. Native installation and invocation not-checked.

Official references: https://geminicli.com/docs/extensions/reference/ and https://geminicli.com/docs/cli/creating-skills/ . No Gemini gallery or Apps-native import approval is claimed.

## Self-contained use

Read SKILL.md from the extracted skill root and its bundled references. Run `python runtime/check_source.py input.html` or add `--candidate candidate.txt` to compare original UTF-8 bytes without editing either file. Static diagnostic success is separate from native import, actual rendering, source copy, export and native wording review.
