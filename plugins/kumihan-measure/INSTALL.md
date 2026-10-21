# Offline installation / オフライン導入

Download the versioned Measure v0.1.0 ZIP for your host from this repository's `downloads GPT-Codex/`, `downloads Claude/`, or `downloads Gemini/` directory. Verify it against `kumihan-measure-v0.1.0-SHA256SUMS.txt` in the same directory before extracting. Each host directory provides one complete plugin/extension and four independent Skills (core, web, documents, review). Choose a complete plugin or the individual Skills you need.

These ZIPs preserve the exact reviewed v0.1.0 package bytes. Their bundled README/INSTALL text still calls them a Private candidate and refers to a Private checkout; the public repository download locations above supersede that retrieval instruction. No Private repository access is needed. This main-branch delivery is separate from a GitHub Release. Native-host invocation and rendering remain not checked.

GPT/Codex: extract a standalone Skill folder into the host's configured skills directory, or install the GPT-Codex plugin folder using the host's local plugin flow. Claude Code: add the extracted plugin folder as a local plugin (`claude --plugin-dir /absolute/path/kumihan-measure`); standalone Skills go in `.claude/skills/`. Gemini CLI: `gemini extensions link /absolute/path/kumihan-measure`; standalone Skills go in the host-configured skills directory if supported. Check your installed CLI's help before running version-specific commands.

各ホストのローカル導入先へ展開します。Claude/Geminiを含む全ZIPに公式PNGを同梱しています。ネイティブホスト実機の受入は未確認です。

For updates, inspect `codex --version`, `claude --version`, or `gemini --version`, compare package inventory version and hashes, then replace the approved local package using that host's documented update flow. Preserve user edits first. No nonexistent Release/update endpoint is required. Run `python runtime/check_source.py SOURCE --locale en-US --medium review` in any extracted Skill folder. The checker reads but never rewrites the source.
