# KUMIHAN｜विन्यास -Vinyāsa

संस्कृतपाठस्य अक्षरविन्यासे साहाय्यम्। मूलपाठं रक्षति। / Source-preserving Sanskrit typography guidance for Devanagari and explicitly identified IAST, web, documents and read-only review.

स्थापनम्। / Installation. Version 0.1.0; developer L&Co. LLC.

स्थापनात् पूर्वं निर्देशाः पठनीयाः। सम्पूर्णः सञ्चयः स्थापनीयः; केवलं SKILL.md न पर्याप्तम्। मूलपाठः, नामानि, संख्याः, चिह्नानि च रक्षणीयानि। / Read the instructions before installation. Install the complete package; SKILL.md alone is insufficient. Preserve the original text, names, numbers and marks.

Use the matching versioned host archive. For ChatGPT/Codex select the plugin through the host plugin installer, or place an extracted standalone Skill directory in the host-supported skills location. The plugin exposes four Skills through .codex-plugin/plugin.json.

For Claude Code use its local plugin installer with this extracted plugin directory (contains .claude-plugin/plugin.json); standalone Skills go into your selected .claude/skills directory. For Gemini CLI run `gemini extensions install /absolute/path/to/kumihan-vinyasa` for the extracted extension, or install a standalone Skill through the host-supported skills location. Confirm the host version supports the relevant mechanism before installation.

Extract each standalone archive retaining its complete top-level Skill folder; do not copy SKILL.md alone. No network credentials or MCP setup is required. If a host rejects metadata, report its actual version and error rather than editing source text. Host installation and invocation are not_checked until tested on your client.

Checksum files: `SHA256SUMS-gpt-codex`, `SHA256SUMS-claude`, and `SHA256SUMS-gemini`; choose the file for your host.
