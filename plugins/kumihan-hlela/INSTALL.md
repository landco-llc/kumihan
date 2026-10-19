# KUMIHAN｜Hlela — Installation / Ukufaka

Download GitHub Release kumihan-zu-v0.1.0 and verify SHA256SUMS.txt.

Claude Code: unpack kumihan-hlela-claude-code-plugin-v0.1.0.zip and run claude plugin validate /absolute/path/kumihan-hlela before claude --plugin-dir /absolute/path/kumihan-hlela. Claude skills may be placed in .claude/skills/<skill-name>.

Gemini CLI: unpack kumihan-hlela-gemini-cli-extension-v0.1.0.zip and run gemini extensions install /absolute/path/kumihan-hlela. Gemini standalone skills may be placed in .gemini/skills/<skill-name>.

Codex: place standalone skills in .agents/skills/<skill-name>. ChatGPT and Gemini Apps availability varies by client/account; uploading a ZIP is not equivalent to provider marketplace registration.

Review prompt: Use kumihan-hlela-review on this isiZulu text without editing it; list exact issues and evidence status.

Offline source check: python runtime/checks.py source.txt --locale zu-ZA --candidate rendered.txt
