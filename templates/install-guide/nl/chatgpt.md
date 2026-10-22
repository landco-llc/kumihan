> **English-language installation guide**
> This installation guide is provided in English while a reviewed local-language translation is unavailable. The NL edition and its four skills are language-specific; native-host import and actual rendering have not been fully verified.

This guide explains how to use {{brand}} with ChatGPT and Codex.

> **About v{{version}}**
> This version is for trying {{brand}} in your own environment. Behavior in each tool has not yet been fully verified, so some steps may not work as expected.

## 1. Choose an installation method

| Where you want to use it | Recommended method |
| --- | --- |
| ChatGPT (if skill upload is available) | [A. Add skills one by one](#a) |
| ChatGPT (as your own private plugin) | [B. Register as a plugin](#b) |
| Codex (on your computer) | [C. Copy skill folders](#c) |

A **skill** is a single feature. The **plugin** bundles all four skills into one package.

## 2. Download the files

All files are on the [release page]({{release}}). Select a link to download the ZIP file.

**Plugin (all four skills)**

- {{plugin_link}}

**Individual skills**

{{skills_list}}

## A. Add skills to ChatGPT

Use this method if your ChatGPT shows **Skills** with an upload option.

1. Upload one skill ZIP.
2. Review the details and add it.
3. Repeat for each skill you want to use.

**Notes**

- The plugin ZIP does not work here. Use the individual skill ZIPs.
- Attaching a file to a chat does not install it as a skill.
- If you don't see the option, it may not be available for your plan or app yet. See [OpenAI's guide](https://learn.chatgpt.com/docs/build-skills).

## B. Register a plugin in ChatGPT

This method registers all four skills as your own private plugin.

1. Start a new conversation in ChatGPT and select `@plugin-creator`.
2. Attach the plugin ZIP.
3. Ask:

   > Please register this package as my private plugin. Do not submit it to the public directory.

4. Once registered, **{{display}}** appears under Plugins, in "Personal" or "Created by me".
5. Install it if needed, then enable it in a new conversation.

**Notes**

- The plugin may be saved to your team workspace. If you want it to be personal only, check the destination before registering.
- This feature may not be available depending on your plan or workspace settings. See [Build plugins](https://learn.chatgpt.com/docs/build-plugins) and [Plugins](https://learn.chatgpt.com/docs/plugins).
- A plugin registered this way is only available to your account. It is not listed in the public directory.

## C. Copy skill folders for Codex

Extracting a skill ZIP gives you a folder such as `{{first}}`. Copy that folder to where Codex looks for skills.

| Scope | Destination |
| --- | --- |
| One project only | `.agents/skills/` inside the project |
| All projects | `~/.agents/skills/` in your home folder |

For example, to add `{{first}}` to a project:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Notes**

- Copy the whole folder with everything in it. The skill will not work correctly with only some files.
- If a folder with the same name already exists, check its contents before overwriting.

## 3. Try it out

Open a new conversation and call a skill.

| Tool | How to call |
| --- | --- |
| ChatGPT | Choose it from `@` |
| Codex | Choose it from `$` or `/skills` |

We recommend starting with a request that doesn't change any files:

> I'm planning a report in {{lang}}. What should I keep in mind? Please don't change any files.

## Verify your downloads (optional)

To check that your downloads are intact, use [SHA256SUMS.txt]({{sums}}).

Put SHA256SUMS.txt in the same folder as the ZIP files you downloaded, then run this in a terminal. If `shasum` is unavailable, use an equivalent SHA-256 command such as PowerShell `Get-FileHash` on Windows:

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

If the lines for your downloaded files show `OK`, the files are intact.

---

Other tools: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Screens and availability may change. Please check each service's official guidance for the latest information (last checked: October 14, 2026).
