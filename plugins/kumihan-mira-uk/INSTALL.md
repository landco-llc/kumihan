# KUMIHAN｜Міра

Встановлення · Installation

Install exactly one host edition at a time. Verify the versioned ZIP hash before extracting. Keep the extracted plugin directory intact. Each standalone Skill includes its own rules, helper, sources, license and official PNG.

- Codex: install the local plugin directory containing `.codex-plugin/plugin.json` using the host plugin installer; standalone Skill folders belong in the host Skill directory.
- Claude Code: load the extracted plugin with `claude --plugin-dir /absolute/path/kumihan-mira-uk`. For standalone Skills copy the extracted Skill folder into `~/.claude/skills/`.
- Gemini CLI: run `gemini extensions install /absolute/path/kumihan-mira-uk` for the extracted extension with `gemini-extension.json` and `GEMINI.md`. Use the CLI Skill installer for standalone Skills, subject to your installed version.

Задайте локаль `uk` або `uk-UA`. Код `uk` означає українську мову, а не англійську Великої Британії.
Set explicit `uk` or `uk-UA`; `uk` means Ukrainian, not UK English. Host installation and invocation have not been exercised here. No credential, MCP connection or network service is required for the offline helper. Python 3 is needed only for optional static checks.

Run a detached Skill helper: `python runtime/check_source.py source.txt --locale uk-UA`. It reports source bytes and advice without rewriting. Uninstall by removing only this plugin/Skill via the host interface; original documents are untouched.

Checksum files: `SHA256SUMS-gpt-codex`, `SHA256SUMS-claude`, and `SHA256SUMS-gemini`; choose the file for your host.
