# Install / 설치 / 導入

KUMIHAN｜글짜임 0.1.0 is independent of Japanese KUMIHAN and 字衡. Choose the package for your host. Verify its SHA-256 against downloads/SHA256SUMS.txt. The distribution now contains **15 ZIPs**: one bundle and four standalone Skills for each host.

| Host | Bundle | Standalone Skills |
|---|---|---|
| ChatGPT / Codex | `downloads/plugins/kumihan-geuljjaim-plugin-0.1.0.zip` | `downloads/skills/<skill>-0.1.0.zip` |
| Claude / Claude Code | `downloads/claude/kumihan-geuljjaim-claude-bundle-0.1.0.zip` | `downloads/claude/<skill>-claude-skill-0.1.0.zip` |
| Gemini CLI | `downloads/gemini/kumihan-geuljjaim-gemini-bundle-0.1.0.zip` | `downloads/gemini/<skill>-gemini-skill-0.1.0.zip` |

Skill names: `kumihan-geuljjaim`, `kumihan-geuljjaim-web`, `kumihan-geuljjaim-documents`, `kumihan-geuljjaim-review`. Copy the complete folder, not SKILL.md alone.

## Claude

Extract the Claude bundle; its root `kumihan-geuljjaim/` contains `.claude-plugin/plugin.json` and four `skills/` folders. From the extraction directory, run:

```sh
claude plugin validate ./kumihan-geuljjaim
claude --plugin-dir ./kumihan-geuljjaim
```

Alternatively, extract a Claude standalone ZIP and copy its Skill folder to the project `.claude/skills/`. If your Claude account provides custom Skills upload, select the standalone ZIP in that setting and enable it. Plugin ZIPs are for Claude Code, not ordinary chat attachments.

## Gemini CLI

Extract the Gemini bundle; its root contains `gemini-extension.json`, `GEMINI.md`, and four `skills/` folders. From the extraction directory, run:

```sh
gemini extensions install ./kumihan-geuljjaim
gemini extensions list
gemini skills list --all
```

Review the host's trust/consent prompt. Alternatively, extract a Gemini standalone ZIP and copy its Skill folder to the project `.gemini/skills/`. Restart the CLI or use `/skills reload`. These packages target Gemini CLI; uploading to the Gemini consumer app is not claimed.

## ChatGPT / Codex

Use compatible local plugin import when provided, or extract standalone Skills into the project's `.agents/skills/`. Ordinary chat attachment is not installation. Native ChatGPT/Codex invocation remains unverified.

## Smoke / updates

Back up existing same-name folders/configuration. Replace only this Korean product and reload the host. Ask for a read-only ko-KR review preserving names, prices, origin and numbers. Confirm that the source files are unchanged and unperformed checks are not reported as passed.

No API key, MCP server, startup hook or runtime network is required by these packages. Python 3.9+ stdlib is optional for static helpers. Archive/manifest validation does not prove authenticated model invocation, native Korean editing or Office/PDF compatibility. Marketplace listing and Release uploads are separate owner operations.

Official format references: [Claude plugin manifest](https://code.claude.com/docs/en/plugins-reference), [Claude Skills](https://code.claude.com/docs/en/skills), [Gemini extensions](https://geminicli.com/docs/extensions/reference/), [Gemini Skills](https://geminicli.com/docs/cli/skills/).
