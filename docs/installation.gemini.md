# KUMIHAN for Gemini (preview)

[日本語](installation.gemini.ja.md) · [Downloads and SHA256](../downloads%20Gemini/README.md)

Developer: L&Co.LLC. `0.1.0-preview.1` describes a distribution preview. Installation, acceptance, invocation and updates in Gemini CLI / Apps have not been tested. This is not a stable release, Google directory listing or compatibility guarantee. The four skills provide Japanese layout guidance. Official references checked on 2026-10-14.

## Gemini CLI extension: all four skills

With CLI and Git available, optionally use the [official extension workflow](https://geminicli.com/docs/extensions/reference/):

```sh
gemini extensions install https://github.com/landco-llc/kumihan --ref main
```

The root `gemini-extension.json` and `skills/<name>/SKILL.md` are the entry points. Extensions are enabled globally by default; inspect destination and consent prompts. This extension adds no MCP server, hook or secret setting. Check for duplicate skills installed through other routes.

A Git push does not refresh your installed copy. Explicitly update and restart CLI:

```sh
gemini extensions update kumihan
```

Future distribution changes also require an extension version bump. For manual transport, extract the [extension ZIP](../downloads%20Gemini/extensions/kumihan-Gemini-CLI-extension-0.1.0-preview.1.zip) into an empty folder named `kumihan`. Confirm its manifest is directly inside that folder, then:

```sh
gemini extensions install "/absolute/path/kumihan"
```

This local route does not follow Git. Replace files from a newer ZIP manually and consult your CLI's local-source update workflow. Direct ZIP installation is not documented here.

## Gemini CLI: select individual skills

Skip this route when using the extension. The [Agent Skills documentation](https://geminicli.com/docs/cli/skills/) supports installing a Git subdirectory. In your intended project:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path skills/kumihan --scope workspace
```

Substitute `skills/kumihan-web`, `skills/kumihan-documents` or `skills/kumihan-review` as needed. Workspace scope is project-specific; the default user scope applies personally across projects. Refresh through the same installation command. The [official implementation](https://github.com/google-gemini/gemini-cli/blob/main/packages/cli/src/utils/skillUtils.ts) replaces an existing directory of the same name; save any local edits first. `/skills reload` rescans discovery; it does not download Git changes. No `gemini skills update` command is prescribed.

The official CLI implementation recognizes ZIP packages with a `.skill` extension. These Apps `.zip` files have not been validated as CLI `.skill` packages. Use Git or an extracted skill directory for CLI; renaming an extension does not establish compatibility.

## Gemini Apps: personal upload

[Official Apps help](https://support.google.com/gemini/answer/17094296?hl=en) describes gradual availability for personal Google accounts aged 18+ with Keep Activity enabled, currently excluding work/school accounts. Check your eligibility yourself. Web, Mac and mobile UI availability varies.

On the web, use Customize (or More) → Skills → Upload. Select one Apps ZIP from the [skills folder](../downloads%20Gemini/skills/), inspect it, then Create. Choose any of the four skills. Each ZIP has `SKILL.md` and 23 reference files directly at its root. The extension ZIP is for CLI.

Apps does not track Git updates. Upload a newer ZIP manually and review replacement or duplicate entries. All bundled skill files are text and each unpacked archive is below 100MB. Actual Apps acceptance and application remain unverified.

[ChatGPT / Codex](installation.md) · [Claude](installation.claude.md) · [Updates](updates.md)
