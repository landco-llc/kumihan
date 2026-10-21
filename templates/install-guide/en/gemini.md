This guide explains how to use {{brand}} with Gemini CLI and the Gemini app.

> **About v{{version}}**
> This version is for trying {{brand}} in your own environment. Behavior in each tool has not yet been fully verified, so some steps may not work as expected.

## 1. Choose an installation method

| Where you want to use it | Recommended method |
| --- | --- |
| Gemini CLI (all four skills) | [A. Install as an extension](#a) |
| Gemini CLI (only the skills you need) | [B. Install individual skills](#b) |
| Gemini app (web, Mac, mobile) | [C. Upload skills](#c) |

## A. Gemini CLI: install as an extension

This installs all four skills at once.

1. Download the [extension ZIP]({{plugin_url}}).
{{#if plugin_folder}}
2. Extract it to get a `{{plugin_folder}}` folder.
{{else}}
2. Create an empty `{{plugin}}` folder and extract the ZIP into it.
{{/if}}
3. Install from that folder:

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Review the confirmation prompt before continuing. Once installed, the extension is active in all projects.

An extension installed from a ZIP does not update automatically. When a new version is released, replace it with the new ZIP.

## B. Gemini CLI: install individual skills

This installs only the skills you need, for a single project. You don't need this if you used method A.

For example, to install `{{first}}`, run this in your project:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

For other skills, change `--path` to:

{{gemini_paths}}

`--scope workspace` limits the skill to this project. Without it, the skill is available in all your projects.

**To update**

Run the same command again. The installed skill will be replaced, so save any changes you made to it first.

## C. Gemini app: upload skills

1. Download the skill ZIPs you want to use.
{{skills_list_indented}}
2. In Gemini, open **Customize** (or **More** if you don't see it) → **Skills** → **Upload**.
3. Choose one ZIP at a time, review the details, and select **Create**.

**Notes**

- Available for personal Google accounts of users 18 and older. Work and school accounts are not supported at this time.
- **Keep Activity** must be turned on.
- The feature is rolling out gradually and may not be available to you yet. See [Gemini Help](https://support.google.com/gemini/answer/17094296).
- The extension ZIP (for Gemini CLI) does not work here.
- Uploaded skills do not update automatically. When a new version is released, upload it again.

## 2. Try it out

We recommend starting with a request that doesn't change any files:

> I'm planning a presentation in {{lang}}. What should I keep in mind? Please don't change any files.

## Verify your downloads (optional)

To check that your downloads are intact, use [SHA256SUMS.txt]({{sums}}).

Put SHA256SUMS.txt in the same folder as the ZIP files you downloaded, then run this in a terminal. If `shasum` is unavailable, use an equivalent SHA-256 command such as PowerShell `Get-FileHash` on Windows:

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

If the lines for your downloaded files show `OK`, the files are intact.

---

Other tools: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Screens and availability may change. Please check each service's official guidance for the latest information (last checked: October 14, 2026).
