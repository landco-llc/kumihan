<!-- Generated from authored installation Markdown; do not edit. -->
# Install for ChatGPT and Codex

[日本語](installation.ja.md) · [Back to top](../README.md)

<br>

This guide explains how to use KUMIHAN with ChatGPT and Codex.

> **About v0.2.0**
> This version is for trying KUMIHAN in your own environment. Behavior in each tool has not yet been fully verified, so some steps may not work as expected.

<br>

## 1. Choose an installation method

| Where you want to use it | Recommended method |
| --- | --- |
| ChatGPT (if skill upload is available) | [A. Add skills one by one](#a-add-skills-to-chatgpt) |
| ChatGPT (as your own private plugin) | [B. Register as a plugin](#b-register-a-plugin-in-chatgpt) |
| Codex (on your computer) | [C. Copy skill folders](#c-copy-skill-folders-for-codex) |

A **skill** is a single feature. The **plugin** bundles all four skills into one package.

<br>

## 2. Download the files

All files are on the [downloads page](https://github.com/landco-llc/kumihan/releases/tag/v0.2.0).

**Plugin (all four skills)**

- [kumihan-GPT-Codex-plugin-0.1.8.zip](https://github.com/landco-llc/kumihan/releases/download/v0.2.0/kumihan-GPT-Codex-plugin-0.2.0.zip)

**Individual skills**

- [kumihan](https://github.com/landco-llc/kumihan/releases/download/v0.2.0/kumihan-GPT-Codex-skill-0.2.0.zip) — starting point
- [kumihan-web](https://github.com/landco-llc/kumihan/releases/download/v0.2.0/kumihan-web-GPT-Codex-skill-0.2.0.zip) — web pages
- [kumihan-documents](https://github.com/landco-llc/kumihan/releases/download/v0.2.0/kumihan-documents-GPT-Codex-skill-0.2.0.zip) — reports and slides
- [kumihan-review](https://github.com/landco-llc/kumihan/releases/download/v0.2.0/kumihan-review-GPT-Codex-skill-0.2.0.zip) — review

On GitHub, open a file and use the download button at the top right.

<br>

## A. Add skills to ChatGPT

Use this method if your ChatGPT shows **Skills** with an upload option.

1. Upload one skill ZIP.
2. Review the details and add it.
3. Repeat for each skill you want to use.

**Notes**

- The plugin ZIP does not work here. Use the individual skill ZIPs.
- Attaching a file to a chat does not install it as a skill.
- If you don't see the option, it may not be available for your plan or app yet. See [OpenAI's guide](https://learn.chatgpt.com/docs/build-skills).

<br>

## B. Register a plugin in ChatGPT

This method registers all four skills as your own private plugin.

1. Start a new conversation in ChatGPT and select `@plugin-creator`.
2. Attach the plugin ZIP.
3. Ask:

   > Please register this package as my private plugin. Do not submit it to the public directory.

4. Once registered, **KUMIHAN v0.1.6** appears under Plugins, in "Personal" or "Created by me".
5. Install it if needed, then enable it in a new conversation.

**Notes**

- The plugin may be saved to your team workspace. If you want it to be personal only, check the destination before registering.
- This feature may not be available depending on your plan or workspace settings. See [Build plugins](https://learn.chatgpt.com/docs/build-plugins) and [Plugins](https://learn.chatgpt.com/docs/plugins).
- A plugin registered this way is only available to your account. It is not listed in the public directory.

<br>

## C. Copy skill folders for Codex

Extracting a skill ZIP gives you a folder such as `kumihan`. Copy that folder to where Codex looks for skills.

| Scope | Destination |
| --- | --- |
| One project only | `.agents/skills/` inside the project |
| All projects | `~/.agents/skills/` in your home folder |

For example, to add `kumihan` to a project:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R kumihan /path/to/your-project/.agents/skills/
```

**Notes**

- Copy the whole folder with everything in it. The skill will not work correctly with only some files.
- If a folder with the same name already exists, check its contents before overwriting.

To install directly from GitHub or through the Codex marketplace, see the [update guide](updates.md).

<br>

## 3. Try it out

Open a new conversation and call a skill.

| Tool | How to call |
| --- | --- |
| ChatGPT | Choose it from `@` |
| Codex | Choose it from `$` or `/skills` |

We recommend starting with a request that doesn't change any files:

> I'm planning a Japanese report. What should I keep in mind? Please don't change any files.

<br>

## Verify your downloads (optional)

To check that your downloads are intact, use [SHA256SUMS.txt](https://raw.githubusercontent.com/landco-llc/kumihan/f5f8dc16f745b57013bc71e77940400765db6248/downloads%20GPT-Codex/SHA256SUMS.txt).

Keep the same folder layout as the downloads page (`plugins/` and `skills/`), then run this in a terminal. If `shasum` is unavailable, use an equivalent SHA-256 command such as PowerShell `Get-FileHash` on Windows:

```sh
cd "downloads GPT-Codex"
shasum -a 256 -c SHA256SUMS.txt
```

If every line shows `OK`, the files are intact.

<br>

---

Other tools: [Claude](installation.claude.md) · [Gemini](installation.gemini.md)

Screens and availability may change. Please check each service's official guidance for the latest information (last checked: October 14, 2026).
