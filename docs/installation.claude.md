# Claude installation and updates

[日本語](installation.claude.ja.md) · [GPT/Codex installation](installation.md) · [Claude downloads](../downloads%20Claude/)

Preview **0.1.0-preview.1**, published by **L&Co.LLC**. Claude Code plugins and Claude chat skills use different routes. Installation, upload, discovery, invocation and updates remain untested. All 96 skill files and existing GPT-Codex downloads are unchanged.

## Claude Code: Git marketplace

Follow the [official install guide](https://code.claude.com/docs/en/discover-plugins). Register the catalog in a supported client:

```sh
claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
```

In a Claude Code conversation, open details and review the installation scope:

```text
/plugin install kumihan@kumihan-marketplace
```

After installation, check `/kumihan:kumihan`, `/kumihan:kumihan-web`, `/kumihan:kumihan-documents` and `/kumihan:kumihan-review` and their local resources. None of these operations was executed here.

Explicit refresh examples:

```sh
claude plugin marketplace update kumihan-marketplace
claude plugin update kumihan@kumihan-marketplace
```

The [official version guidance](https://code.claude.com/docs/en/plugins/host-marketplace) requires a version change for updated versioned packages. Future content changes must bump `.claude-plugin/plugin.json`; the catalog does not repeat the version. Third-party marketplace auto-update defaults to off. This distribution does not configure it. Confirm application/reload using your actual host.

## Claude Code: manual ZIP

Verify and extract the [Code plugin ZIP](../downloads%20Claude/plugins/kumihan-Claude-Code-plugin-0.1.0-preview.1.zip), yielding `kumihan/`. Example local loading:

```sh
claude --plugin-dir "/absolute/path/kumihan"
```

This loads an extracted folder; it is distinct from marketplace installation and chat Skill upload. Preserve the manifest, all skills, licenses and notices. Do not overwrite an existing folder or mix private files into the package.

## Claude chat: individual skill ZIPs

The [official Skills guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude) includes Free and other plans and requires code execution. Check your account and organization permissions; no account setting was changed here.

Use the add control in `Customize > Skills`, choose `Upload a skill`, and upload [individual skill ZIPs](../downloads%20Claude/skills/) one at a time. Do not upload the Code plugin ZIP there. Each individual ZIP contains one matching skill-name folder, `SKILL.md` and all 24 files. Preserve filenames/case, then confirm enablement and use. Git pushes and Code plugin updates do not synchronize manually uploaded chat skills.

## Integrity and limits

Download [SHA256SUMS.txt](../downloads%20Claude/SHA256SUMS.txt) and [MANIFEST.json](../downloads%20Claude/MANIFEST.json) from the same revision; keep the ZIPs in `plugins/` and `skills/`. From the download folder's parent, on macOS:

```sh
cd "downloads Claude"
shasum -a 256 -c SHA256SUMS.txt
```

Require OK for every entry. Integrity is not host acceptance or a security certification. These workflows provide guidance; they are not automatic detectors. Rendering and native Office compatibility are unverified. Claude's authoritative validator and actual host have not been run; static field/path checks do not establish successful loading.
