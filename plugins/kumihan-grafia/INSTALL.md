# Instalación / Installation

Download the host-specific ZIP and MANIFEST.json / SHA256SUMS.txt from downloads or the exact Grafía release. Verify SHA256 before installation. In a directory holding all 17 release files, run `sha256sum -c SHA256SUMS.txt` (macOS: `shasum -a 256 -c SHA256SUMS.txt`). For one ZIP compare its digest and byte length with MANIFEST.json.

- ChatGPT/Codex: full plugin extracts to kumihan-grafia/ with plugin.json and .codex-plugin/plugin.json. Use the client's actual plugin import interface only if available. For Codex directory Skills, extract each chosen standalone folder into a supported project `.agents/skills/` location. ChatGPT ZIP Skill upload requires an actual account Skills entry point; attaching ZIPs to chat is not installation.
- Claude Code: full plugin extracts to kumihan-grafia/. Run `claude plugin validate /absolute/path/kumihan-grafia` when available; launch with `claude --plugin-dir /absolute/path/kumihan-grafia`. In Claude chat upload individual Skills only through a provided Skills interface. A local plugin is not a marketplace listing.
- Gemini CLI: extension ZIP has gemini-extension.json at the archive root. Extract into an empty dedicated folder, then `gemini extensions install /absolute/path/to/folder`, reading installer consent. Do not install this monorepo root as Grafía. Individual Skills use the installed CLI's directory Skills flow. Gemini Apps account support is not verified.

Invoke: “Usa kumihan-grafia-review; conserva el original, las cifras y los nombres.” Verify actual discovery and invocation in your host; descriptor validation is a different observation. No remote API or runtime dependency is required by Grafía.

Official docs: https://developers.openai.com/codex/skills/ · https://developers.openai.com/codex/plugins/ · https://code.claude.com/docs/en/plugins-reference · https://geminicli.com/docs/extensions/ · https://geminicli.com/docs/cli/skills/
