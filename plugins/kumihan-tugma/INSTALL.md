# KUMIHAN｜Tugma

Ihambing muna ang SHA256SUMS-* ng naaangkop na ZIP. I-extract ang buong package. / Verify the matching archive checksum and extract the complete package.

For GPT/Codex, use the installed host's local plugin flow, or put a standalone Skill folder into `~/.agents/skills/`. For Claude Code, use `claude --plugin-dir /absolute/path/kumihan-tugma` for the plugin or put a standalone Skill in `.claude/skills/`. For Gemini CLI, use `gemini extensions link /absolute/path/kumihan-tugma` for the extension; standalone Skills use the installed CLI's documented skills flow. Check your CLI version and help before installation. No MCP service is needed.

Apat na Skill ang kasama, bawat isa ay may sariling dependencies at opisyal na icon. / Four Skills are included, each independently installable with all dependencies and the official icon. No native-host smoke test is claimed. For updates preserve user changes and compare version/hash inventory before replacing the local package.

Checksum files: `SHA256SUMS-gpt-codex`, `SHA256SUMS-claude`, and `SHA256SUMS-gemini`; choose the file for your host.
