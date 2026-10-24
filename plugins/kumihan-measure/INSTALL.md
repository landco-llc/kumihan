# Offline installation / オフライン導入

Download the versioned v0.1.1 ZIP for your host from [downloads/](downloads/) in the [consumer repository](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-measure/downloads). These packages live at `plugins/kumihan-measure/downloads/`; use `SHA256SUMS-gpt-codex`, `SHA256SUMS-claude` or `SHA256SUMS-gemini` to verify your download. Each host offers a whole plugin/extension and four standalone Skills. Install either the whole package or the Skills you need.

ホストに合った版数付きZIPを製品専用の `downloads/` から取得し、対応するホスト別SHA256SUMSで照合してください。

GPT/Codex: extract a standalone Skill folder into the host's configured skills directory, or install the GPT-Codex plugin folder using the host's local plugin flow. Claude Code: add the extracted plugin folder as a local plugin (`claude --plugin-dir /absolute/path/kumihan-measure`); standalone Skills go in `.claude/skills/`. Gemini CLI: `gemini extensions link /absolute/path/kumihan-measure`; standalone Skills go in the host-configured skills directory if supported. Check your installed CLI's help before running version-specific commands.

各ホストのローカル導入先へ展開します。Claude/Geminiを含む全ZIPに公式PNGを同梱しています。ネイティブホスト実機の受入は未確認です。

For updates, inspect `codex --version`, `claude --version`, or `gemini --version`, compare package inventory version and hashes, then replace the approved local package using that host's documented update flow. Preserve user edits first. No nonexistent Release/update endpoint is required. Run `python runtime/check_source.py SOURCE --locale en-US --medium review` in any extracted Skill folder. The checker reads but never rewrites the source.
