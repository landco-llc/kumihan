# KUMIHAN｜Лад v0.1.0 — Установка / Installation

Download and verify `SHA256SUMS.txt` from https://github.com/landco-llc/kumihan/releases/tag/kumihan-ru-v0.1.0 .

- **Claude Code:** extract `kumihan-lad-claude-code-plugin-v0.1.0.zip` and use `claude --plugin-dir /absolute/path/kumihan-lad`; use supported marketplace if available. Four standalone Claude Skills also available.
- **Gemini CLI:** extract `kumihan-lad-gemini-cli-extension-v0.1.0.zip`; run `gemini extensions install /absolute/path/kumihan-lad`; verify with `gemini extensions list`. Four Gemini Skills also available.
- **Codex / ChatGPT:** extract a `*-chatgpt-skill-v0.1.0.zip` to project `.agents/skills/` or import the plugin using supported UI. Chat attachments do not register plugins.

Run `python runtime/checks.py original.txt --locale ru-RU`. Static and native host checks are separate; no marketplace listing is implied by GitHub release.
