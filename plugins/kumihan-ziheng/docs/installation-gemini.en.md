# KUMIHAN｜字衡 — Gemini / Install ZiHeng

**v0.1.0-preview** — One Gemini CLI extension and four standalone skill ZIPs for supported Gemini app accounts.

> This package offers typography guidance, not an automatic renderer. Native host installation and invocation have not yet passed live host acceptance. Test both Taiwan and Hong Kong samples first.

## Installation steps

**1.** Download the dedicated Gemini CLI extension ZIP and extract it into a new empty folder.

```sh
unzip kumihan-ziheng-Gemini-CLI-extension-0.1.0-preview.zip -d /absolute/path/kumihan-ziheng
```

**2.** Install that local directory using Gemini CLI, restart, then verify the skills appear.

```sh
gemini extensions install "/absolute/path/kumihan-ziheng"
```

**3.** The GitHub monorepo root contains the Japanese KUMIHAN extension; installing the root URL is not a ZiHeng install.

```sh
gemini extensions list
```

**4.** Gemini app: if your account supports Skills upload, import individual skill ZIPs and run host-specific acceptance tests.

## Downloads and checksums

- [Download full package (kumihan-ziheng-Gemini-CLI-extension-0.1.0-preview.zip)](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/extensions/kumihan-ziheng-Gemini-CLI-extension-0.1.0-preview.zip)
- Full package SHA-256: `9d0820df5206da8d44057fdc68639c14177cf556f0be67aeb0b831b4192d30c0`

### Four individual skills

- [kumihan-ziheng](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-Gemini-Apps-skill-0.1.0-preview.zip)
- [kumihan-ziheng-web](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-web-Gemini-Apps-skill-0.1.0-preview.zip)
- [kumihan-ziheng-documents](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-documents-Gemini-Apps-skill-0.1.0-preview.zip)
- [kumihan-ziheng-review](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-review-Gemini-Apps-skill-0.1.0-preview.zip)

Taiwan and Hong Kong use explicit zh-Hant-TW and zh-Hant-HK profiles. Preserve the original characters.

`shasum -a 256 -c SHA256SUMS.txt`

- [View source](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng)

- [SHA256SUMS.txt](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng/downloads%20Gemini/SHA256SUMS.txt)
