# Install for Claude

[日本語](installation.claude.ja.md) · [Back to top](../README.md)

<br>

This guide explains how to use KUMIHAN with Claude Code and Claude chat.

> **About this preview (0.1.0-preview.2)**  
> This version is for trying KUMIHAN in your own environment. Behavior in each tool has not yet been fully verified, so some steps may not work as expected.

<br>

## 1. Choose an installation method

| Where you want to use it | Recommended method |
| --- | --- |
| Claude Code | [A. Install from GitHub](#a-claude-code-install-from-github) (easy to update) |
| Claude Code (from a ZIP) | [B. Install from a ZIP](#b-claude-code-install-from-a-zip) |
| Claude chat (claude.ai and apps) | [C. Upload skills](#c-claude-chat-upload-skills) |

Claude Code and Claude chat use different installation methods.

<br>

## A. Claude Code: install from GitHub

1. In your terminal, add the KUMIHAN marketplace.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. In a Claude Code conversation, enter:

   ```text
   /plugin install kumihan@kumihan-marketplace
   ```

3. Review the details, choose a scope (just you, this project, and so on), and install.

Once installed, these commands become available:

- `/kumihan:kumihan`
- `/kumihan:kumihan-web`
- `/kumihan:kumihan-documents`
- `/kumihan:kumihan-review`

For updates, see the [update guide](updates.md#claude-code).

<br>

## B. Claude Code: install from a ZIP

1. Download the [Claude Code plugin ZIP](../downloads%20Claude/plugins/kumihan-Claude-Code-plugin-0.1.0-preview.2.zip).
2. Extract it to get a `kumihan` folder.
3. Start Claude Code with that folder:

   ```sh
   claude --plugin-dir "/absolute/path/kumihan"
   ```

**Notes**

- Use the folder as is. Don't remove files or add other files to it.
- This method does not update automatically. When a new version is released, replace the folder with the new ZIP.

<br>

## C. Claude chat: upload skills

Use this method for claude.ai and the Claude apps.

1. Download the skill ZIPs you want to use.
   - [kumihan](../downloads%20Claude/skills/kumihan-Claude-skill-0.1.0-preview.2.zip) — starting point
   - [kumihan-web](../downloads%20Claude/skills/kumihan-web-Claude-skill-0.1.0-preview.2.zip) — web pages
   - [kumihan-documents](../downloads%20Claude/skills/kumihan-documents-Claude-skill-0.1.0-preview.2.zip) — reports and slides
   - [kumihan-review](../downloads%20Claude/skills/kumihan-review-Claude-skill-0.1.0-preview.2.zip) — review
2. In Claude, open **Customize → Skills**, then choose **Upload a skill** from the add button.
3. Upload the ZIPs one at a time and enable each skill.

**Notes**

- The Claude Code plugin ZIP does not work here. Use the individual skill ZIPs.
- Upload the ZIPs without renaming them.
- Skills require code execution to be turned on in your settings. See [Claude's guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- On organization accounts, availability may depend on your admin's settings.
- Uploaded skills do not update automatically. When a new version is released, upload it again.

<br>

## 2. Try it out

We recommend starting with a request that doesn't change any files:

> I'm planning a Japanese web page. What should I keep in mind? Please don't change any files.

<br>

## Verify your downloads (optional)

To check that your downloads are intact, use [SHA256SUMS.txt](../downloads%20Claude/SHA256SUMS.txt).

Keep the same folder layout as the downloads page (`plugins/` and `skills/`), then run this in the macOS Terminal:

```sh
cd "downloads Claude"
shasum -a 256 -c SHA256SUMS.txt
```

If every line shows `OK`, the files are intact.

<br>

---

Other tools: [ChatGPT / Codex](installation.md) · [Gemini](installation.gemini.md)

Screens and availability may change. Please check each service's official guidance for the latest information (last checked: October 14, 2026).
