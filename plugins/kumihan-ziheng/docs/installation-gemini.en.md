# KUMIHAN｜字衡 — Gemini / Installation guide

The full bundle and four independent Skills use the same ZiHeng rules. Use the host-specific website guide for the currently verified published ZIPs, SHA-256 values and version. The Japanese KUMIHAN monorepo root is a different product.

## Current published downloads and checksums

[Installation guide](https://landco-llc.github.io/kumihan/docs/install-ziheng-gemini.en.html)

Extract the Gemini CLI extension ZIP into a new local folder, then install that folder. Use individual Skill ZIPs when the Gemini app provides skill import.

```sh
gemini extensions install "/absolute/path/to/extracted-ziheng-extension"
```

## Skills

- `kumihan-ziheng`
- `kumihan-ziheng-web`
- `kumihan-ziheng-documents`
- `kumihan-ziheng-review`

Back up the existing folder, verify the ZIP and replace the complete package for the same host and version, then reload. Do not mix references, rules or scripts from different versions.

The active source MANIFEST.json and SHA256SUMS.txt describe the source distribution, which may be newer than the published version shown on the website. Historical v0.1.0 and v0.2.0 ZIPs remain available; their original metadata is under history/<version>/.

- [MANIFEST.json](../downloads%20Gemini/MANIFEST.json)
- [SHA256SUMS.txt](../downloads%20Gemini/SHA256SUMS.txt)

Native host discovery, installation, invocation and rendering require acceptance in the intended environment. Test zh-Hant-TW and zh-Hant-HK with fixed text; inspect vertical punctuation, mixed runs, reading order and unchanged Unicode sequences separately.
