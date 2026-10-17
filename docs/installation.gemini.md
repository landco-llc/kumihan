# Install for Gemini

[日本語](installation.gemini.ja.md) · [Back to top](../README.md)

<br>

This guide explains how to use KUMIHAN with Gemini CLI and the Gemini app.

> **About this preview (v0.1.5 preview)**  
> This version is for trying KUMIHAN in your own environment. Behavior in each tool has not yet been fully verified, so some steps may not work as expected.

<br>

## 1. Choose an installation method

| Where you want to use it | Recommended method |
| --- | --- |
| Gemini CLI (all four skills) | [A. Install as an extension](#a-gemini-cli-install-as-an-extension) |
| Gemini CLI (only the skills you need) | [B. Install individual skills](#b-gemini-cli-install-individual-skills) |
| Gemini app (web, Mac, mobile) | [C. Upload skills](#c-gemini-app-upload-skills) |

<br>

## A. Gemini CLI: install as an extension

This installs all four skills at once.

```sh
gemini extensions install https://github.com/landco-llc/kumihan --ref main
```

Review the confirmation prompt before continuing. Once installed, the extension is active in all projects.

**To update**

```sh
gemini extensions update kumihan
```

Restart Gemini CLI after updating.

**Installing from a ZIP**

1. Download the [extension ZIP](../downloads%20Gemini/extensions/kumihan-Gemini-CLI-extension-0.1.5-preview.zip).
2. Create an empty `kumihan` folder and extract the ZIP into it.
3. Install from that folder:

   ```sh
   gemini extensions install "/absolute/path/kumihan"
   ```

An extension installed from a ZIP does not update automatically. When a new version is released, replace it with the new ZIP.

<br>

## B. Gemini CLI: install individual skills

This installs only the skills you need, for a single project. You don't need this if you used method A.

For example, to install `kumihan`, run this in your project:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path skills/kumihan --scope workspace
```

For other skills, change `--path` to:

- `skills/kumihan-web` — web pages
- `skills/kumihan-documents` — reports and slides
- `skills/kumihan-review` — review

`--scope workspace` limits the skill to this project. Without it, the skill is available in all your projects.

**To update**

Run the same command again. The installed skill will be replaced, so save any changes you made to it first.

<br>

## C. Gemini app: upload skills

1. Download the skill ZIPs you want to use.
   - [kumihan](../downloads%20Gemini/skills/kumihan-Gemini-Apps-skill-0.1.5-preview.zip) — starting point
   - [kumihan-web](../downloads%20Gemini/skills/kumihan-web-Gemini-Apps-skill-0.1.5-preview.zip) — web pages
   - [kumihan-documents](../downloads%20Gemini/skills/kumihan-documents-Gemini-Apps-skill-0.1.5-preview.zip) — reports and slides
   - [kumihan-review](../downloads%20Gemini/skills/kumihan-review-Gemini-Apps-skill-0.1.5-preview.zip) — review
2. In Gemini, open **Customize** (or **More** if you don't see it) → **Skills** → **Upload**.
3. Choose one ZIP at a time, review the details, and select **Create**.

**Notes**

- Available for personal Google accounts of users 18 and older. Work and school accounts are not supported at this time.
- **Keep Activity** must be turned on.
- The feature is rolling out gradually and may not be available to you yet. See [Gemini Help](https://support.google.com/gemini/answer/17094296).
- The extension ZIP (for Gemini CLI) does not work here.
- Uploaded skills do not update automatically. When a new version is released, upload it again.

<br>

## 2. Try it out

We recommend starting with a request that doesn't change any files:

> I'm planning a Japanese presentation. What should I keep in mind? Please don't change any files.

<br>

## Verify your downloads (optional)

To check that your downloads are intact, use [SHA256SUMS.txt](../downloads%20Gemini/SHA256SUMS.txt).

Keep the same folder layout as the downloads page (`extensions/` and `skills/`), then run this in the macOS Terminal:

```sh
cd "downloads Gemini"
shasum -a 256 -c SHA256SUMS.txt
```

If every line shows `OK`, the files are intact.

<br>

---

Other tools: [ChatGPT / Codex](installation.md) · [Claude](installation.claude.md)

Screens and availability may change. Please check each service's official guidance for the latest information (last checked: October 14, 2026).
