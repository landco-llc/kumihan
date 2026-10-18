# KUMIHAN｜字律

安装与更新 / Installation and updates · v0.1.0

从本产品 `downloads/` 下载正确的 Host ZIP；在 downloads 目录运行 `sha256sum -c SHA256SUMS.txt`，或使用 `shasum -a 256 -c SHA256SUMS.txt`。只下载单一 ZIP 时，对照 MANIFEST.json 的对应 SHA256，不要忽略真正的校验失败。 / Download the matching host ZIP and verify its checksum. For a single file, compare its SHA256 with the corresponding manifest entry.

## ChatGPT / Codex

完整插件 `plugins/kumihan-zilu-plugin-v0.1.0.zip` 含 portable plugin.json 与兼容 .codex-plugin。使用当前客户端提供的 Plugin import/本地插件安装入口，选择解压后的 kumihan-zilu 目录；仅支持 Skills 的客户端使用 skills/ 中的四个独立 ZIP。导入入口与账户权限因Host版本而异。没有插件导入功能时，从源码读取 SKILL.md 是人工指导，不能称作插件安装。 / Import the complete plugin using the current client's supported plugin installation UI, where available, or install individual skills through its supported Skills interface. Reading files in chat is not plugin installation.

## Claude

Claude Code：解压 `claude/kumihan-zilu-claude-plugin-v0.1.0.zip`，测试 `claude --plugin-dir /absolute/path/kumihan-zilu`。如 CLI 提供验证器，运行 `claude plugin validate /absolute/path/kumihan-zilu`。这是一会话本地加载，不是官方商店上架。 / Extract and load with --plugin-dir; use plugin validate if provided by your CLI. Local loading does not imply marketplace listing.

Claude chat：仅在账户提供 Skills 上传时上传 `claude/*-claude-skill-v0.1.0.zip`，每次选择一个；无需其他语言插件。 / Use the individual skill ZIP in the Skills upload interface when available. Attaching it to a conversation is not installation.

官方说明 / Official documentation: https://code.claude.com/docs/en/plugins-reference and https://support.claude.com/en/articles/12512180-using-skills-in-claude

## Gemini

Gemini CLI：把 `gemini/kumihan-zilu-gemini-extension-v0.1.0.zip` 解压到空目录，使 gemini-extension.json 在该目录根部，运行 `gemini extensions install /absolute/path/to/folder`；安装器要求的权限应单独阅读。不要安装本仓库根URL来获取字律（根部是其他产品）。 / Extract into an empty directory and install that local directory. Review the CLI's permission prompt. The monorepo root URL selects another product.

单个 Skill：解压 `gemini/*-gemini-skill-v0.1.0.zip`，根据当前 Gemini CLI Skills 安装说明安装该 Skill 目录。Gemini App 的 Skills 导入能力未验证；仅在实际账户有入口时尝试，不承诺通用 App 上传功能。 / Install the extracted skill directory using your CLI's supported Skills workflow. Gemini App import is NOT VERIFIED; these packages do not establish an app capability.

官方说明 / Official documentation: https://geminicli.com/docs/extensions/ and https://geminicli.com/docs/cli/skills/

## 启动与更新 / Invoke and update

入口：`kumihan-zilu`；网页：`kumihan-zilu-web`；文档：`kumihan-zilu-documents`；只读审查：`kumihan-zilu-review`。 / Entry, web, documents and read-only review.

示例：使用 kumihan-zilu-web，在保留原文与数字的前提下检查这个页面。 / Use kumihan-zilu-review to review this Simplified Chinese document without changing source text or numbers.

更新前保存已有定制，校验新版本 ZIP，再用当前Host支持的更新/卸载重装流程；不要覆盖其他语言插件。 / Back up customizations, verify new packages, then use the host's update or reinstall workflow without overwriting other products.

原生Host调用、显示名称与图标、商店上架尚未验证。Claude/Gemini manifest name 限ASCII，产品正文/description保持 KUMIHAN｜字律；未声称CLI提供独立Unicode显示名字段。 / Native invocation, UI branding and marketplace listing remain unverified. Claude/Gemini use an ASCII technical name; the product name is preserved in descriptions and content.
