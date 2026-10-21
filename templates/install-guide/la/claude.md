> **English-language installation guide**
> This installation guide is provided in English while a reviewed local-language translation is unavailable. The LA edition and its four skills are language-specific; native-host import and actual rendering have not been fully verified.

This guide explains how to use {{brand}} with Claude Code and Claude chat.

> **About v{{version}}**
> This version is for trying {{brand}} in your own environment. Behavior in each tool has not yet been fully verified, so some steps may not work as expected.

## 1. Choose an installation method

| Where you want to use it | Recommended method |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Install from GitHub](#a) (easy to update) |
{{/if}}
| Claude Code (from a ZIP) | [{{L_zip}}. Install from a ZIP](#{{l_zip}}) |
| Claude chat (claude.ai and apps) | [{{L_chat}}. Upload skills](#{{l_chat}}) |

Claude Code and Claude chat use different installation methods.

{{#if marketplace}}
## A. Claude Code: install from GitHub

1. In your terminal, add the KUMIHAN marketplace.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. In a Claude Code conversation, enter:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Review the details, choose a scope (just you, this project, and so on), and install.

Once installed, these commands become available:

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: install from a ZIP

1. Download the [Claude Code plugin ZIP]({{plugin_url}}).
{{#if plugin_folder}}
2. Extract it to get a `{{plugin_folder}}` folder.
{{else}}
2. Create an empty `{{plugin}}` folder and extract the ZIP into it.
{{/if}}
3. Start Claude Code with that folder:

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Notes**

- Use the folder as is. Don't remove files or add other files to it.
- This method does not update automatically. When a new version is released, replace the folder with the new ZIP.

## {{L_chat}}. Claude chat: upload skills

Use this method for claude.ai and the Claude apps.

1. Download the skill ZIPs you want to use.
{{skills_list_indented}}
2. In Claude, open **Customize → Skills**, then choose **Upload a skill** from the add button.
3. Upload the ZIPs one at a time and enable each skill.

**Notes**

- The Claude Code plugin ZIP does not work here. Use the individual skill ZIPs.
- Upload the ZIPs without renaming them.
- Skills require code execution to be turned on in your settings. See [Claude's guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- On organization accounts, availability may depend on your admin's settings.
- Uploaded skills do not update automatically. When a new version is released, upload it again.

## 2. Try it out

We recommend starting with a request that doesn't change any files:

> I'm planning a web page in {{lang}}. What should I keep in mind? Please don't change any files.

## Verify your downloads (optional)

To check that your downloads are intact, use [SHA256SUMS.txt]({{sums}}).

Put SHA256SUMS.txt in the same folder as the ZIP files you downloaded, then run this in a terminal. If `shasum` is unavailable, use an equivalent SHA-256 command such as PowerShell `Get-FileHash` on Windows:

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

If the lines for your downloaded files show `OK`, the files are intact.

---

Other tools: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Screens and availability may change. Please check each service's official guidance for the latest information (last checked: October 14, 2026).
