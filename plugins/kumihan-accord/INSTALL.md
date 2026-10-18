# KUMIHAN｜Accord — Instalación / Installation

## Español

El nombre público es KUMIHAN｜Accord. Descarga el ZIP v0.1.1 de tu host en https://github.com/landco-llc/kumihan/releases/tag/kumihan-fr-v0.1.1 y comprueba SHA256SUMS.txt o MANIFEST.json. Cada uno de los cuatro skills es autónomo. Selecciona el idioma, el estilo editorial y el modo de trabajo. No modifiques el texto original sin autorización.

## English

The public name is KUMIHAN｜Accord. Download the host-specific v0.1.1 ZIP from https://github.com/landco-llc/kumihan/releases/tag/kumihan-fr-v0.1.1; verify SHA-256 before installing. Each of the four skills is self-contained. Set locale, house style and work mode explicitly; preserve supplied content.

## Claude Code plugin

Unzip kumihan-accord-claude-code-plugin-v0.1.1.zip, keeping the kumihan-accord directory:

    claude --plugin-dir /absolute/path/kumihan-accord

When supported, validate with:

    claude plugin validate /absolute/path/kumihan-accord

The repository Claude marketplace manifest also contains this product:

    /plugin marketplace add landco-llc/kumihan
    /plugin install kumihan-accord@kumihan-marketplace

Claude Skills upload: use the individual *-claude-skill-v0.1.1.zip through an available Skills installation UI. This does not guarantee marketplace catalog listing.

## Gemini CLI extension

Unzip kumihan-accord-gemini-cli-extension-v0.1.1.zip into an empty directory so gemini-extension.json is inside the kumihan-accord directory:

    gemini extensions install /absolute/path/kumihan-accord
    gemini extensions list

Standalone Gemini skill ZIPs are supplied for CLI Skills support. Gemini chat/app upload has not been verified. Do not install the monorepo root as this extension; it is the Japanese product.

## ChatGPT / Codex

Use kumihan-accord-chatgpt-codex-plugin-v0.1.1.zip with a supported plugin importer or the individual *-chatgpt-skill-v0.1.1.zip through a Skills interface where available. A chat file attachment is not installation. Official Plugin Directory approval is a separate process.

## Example / Ejemplo

Use study for research, build for new content, audit for read-only findings or refine for authorized edits. Specify fr-FR with fr-fr-editorial, or fr-CA with fr-ca-oqlf; institutional house styles override only by explicit selection.

Optional read-only check:

    python runtime/checks.py input.txt --locale fr-FR --house-style fr-fr-editorial

Optional preview for *generated plain text only*:

    python runtime/checks.py generated.txt --source-origin generated --propose --house-style fr-fr-editorial

The checker never rewrites a source file or certifies browsers, Office/PDF rendering or native host activation.


## Icon fix v0.1.1

Español: instala la nueva versión para recibir el logotipo oficial de KUMIHAN; una instalación anterior no se actualiza por sí sola.
English: v0.1.1 embeds the official icon. Reinstall/update using your host; already-installed v0.1.0 is not automatically patched.
