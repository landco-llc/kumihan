# Install the KUMIHAN preview

[日本語（主案内）](installation.ja.md) · [Project](../README.md)

**0.1.0-preview.1** is a preview for users trying installation in their own environments. It is not an audited stable v0.1 release or a public Plugin Directory listing. “Private” describes the installation's visibility; these GitHub files are public.

`downloads GPT-Codex/` contains distributions for ChatGPT and Codex. ZIP names containing `GPT-Codex-plugin` identify the four-skill plugin; `GPT-Codex-skill` identifies a standalone skill. Names describe format targets, not validated host operation.

## Choose a package

| Intended use | Download or source |
| --- | --- |
| Standalone ChatGPT Skills upload, where your UI supports it | Individual skill ZIPs below |
| Private plugin registration in your own account | [Plugin ZIP](../downloads%20GPT-Codex/plugins/kumihan-GPT-Codex-plugin-0.1.0-preview.1.zip) |
| Local Codex or Claude Code | Complete folders under [skills](../skills/) |

Individual ZIPs: [kumihan](../downloads%20GPT-Codex/skills/kumihan-GPT-Codex-skill-0.1.0-preview.1.zip), [kumihan-web](../downloads%20GPT-Codex/skills/kumihan-web-GPT-Codex-skill-0.1.0-preview.1.zip), [kumihan-documents](../downloads%20GPT-Codex/skills/kumihan-documents-GPT-Codex-skill-0.1.0-preview.1.zip), [kumihan-review](../downloads%20GPT-Codex/skills/kumihan-review-GPT-Codex-skill-0.1.0-preview.1.zip). Each contains one complete skill folder. The plugin contains all four, manifests, the original logo and licenses. Open the file on GitHub and use its Raw/download control to save the actual ZIP.

Download [SHA256SUMS.txt](../downloads%20GPT-Codex/SHA256SUMS.txt) and [MANIFEST.json](../downloads%20GPT-Codex/MANIFEST.json) from the same revision. Keep the download layout, with the plugin ZIP in `plugins/` and standalone ZIPs in `skills/`. If saving files individually, place them in those subfolders. Verify on macOS:

```sh
cd "downloads GPT-Codex"
shasum -a 256 -c SHA256SUMS.txt
```

Require OK for every line. Hash agreement is an integrity check, not host compatibility or a security certification.

## Standalone ChatGPT Skills

Consult [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills). It describes standalone skills on desktop and other supported local surfaces; a universal upload control for every plan is not established.

If your Skills screen offers an upload control, upload each individual skill ZIP, review it and choose personal use. Do not substitute the plugin ZIP, repository ZIP or SKILL.md alone. Ordinary chat attachment does not establish installation. If the control is absent, check the current official guidance instead of assuming this route is available.

## Private ChatGPT plugin

Read [Build plugins](https://learn.chatgpt.com/docs/build-plugins) and [Plugins](https://learn.chatgpt.com/docs/plugins). Workspace permissions, Plugin Creator availability, plan and app support apply.

In a supported environment, select `@plugin-creator` in a new conversation, attach the plugin ZIP and request: “Register this package as my private plugin. Do not submit it to the public directory.” Confirm the destination before saving: the package-save procedure uses an active workspace when present, otherwise the personal account. If you require personal-only registration and cannot establish that destination, stop. In a supported local Codex environment, provide the archive's absolute local path to the creator.

This route follows Plugin Creator's package-save procedure. Current public official pages do not establish a universal ZIP-import UI, and this archive has not passed a new end-to-end registration/install/use test. If registration is unavailable, do not treat installation as complete.

After successful registration, inspect your own Personal/Created by me entry, install if required, then enable **KUMIHAN Private Install Preview** in a new chat. There is no universal installation link to the author's private plugin. Public directory submission is a separate process; this preview has not passed that process. Portal eligibility and account-specific restrictions are not verified here.

## Local Codex and Claude Code

Extracting an individual skill ZIP yields a complete named `SKILL.md` folder, the format Codex loads locally. The plugin ZIP contains root `plugin.json`, a `.codex-plugin/plugin.json` compatibility manifest and four `skills/` folders; the compatibility manifest declares `skills: "./skills"`. This matches the format for trying Codex local marketplace installation, but actual host acceptance and operation remain unverified. Direct folder placement is separate from uploading a ZIP. [Codex local skill documentation](https://learn.chatgpt.com/docs/build-skills) describes project `.agents/skills/` and personal `~/.agents/skills/` locations. [Claude Code documentation](https://code.claude.com/docs/en/skills) describes `.claude/skills/` and `~/.claude/skills/`.

Copy a whole chosen folder without overwriting an existing installation. From this repository root, after confirming the destination has no same-named folder:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R skills/kumihan /path/to/your-project/.agents/skills/
```

Use `.claude/skills/` for Claude Code. Personal locations are an optional choice for users who want skills across projects; no personal installation was performed here. Preserve rules, profiles, references, schemas, sources, inventory.json and LICENSE.

[Official plugin testing guidance](https://developers.openai.com/plugins/deploy/connect-chatgpt) also describes local marketplace installation. Plugins and direct skill folders are different routes. See [Git installation and updates](updates.md) for standalone Git skill and Codex marketplace commands. These commands and host behavior have not been executed or validated here.

## Confirm installation and understand limits

Start a new conversation and confirm discovery, invocation, local resource resolution and output separately. Use `@` in ChatGPT, `$` or `/skills` in Codex, and `/kumihan` in Claude Code as applicable. Start with a read-only request such as “In study mode, explain guidance for a Japanese report; do not change files.”

All 96 files in four skill folders preserve the bytes of the [pinned source](https://github.com/landco-llc/kumihan/tree/180fdb2439c1e6a8563f24b4b29c666394bfaf67/skills). The 38 rules and six profiles are guidance, not automatic detectors. Static checks do not prove ChatGPT Chat/Work, Codex or Claude Code discovery, invocation or behavior, actual rendering, or native Office compatibility. Those results remain unverified. Consumers need no Python/development dependencies; available production/rendering tools and permissions depend on the host.

Official pages checked on 2026-10-14. Follow current documentation and your actual UI when availability changes.

For Claude, see [Claude installation and updates](installation.claude.md).
