# KUMIHAN｜字衡 — Gemini / Install ZiHeng

**v0.1.0** — One Gemini CLI extension and four standalone skill ZIPs for supported Gemini app accounts.

> This package offers typography guidance, not an automatic renderer. Native host installation and invocation have not yet passed live host acceptance. Test both Taiwan and Hong Kong samples first.

## Installation steps

**1.** Download the dedicated Gemini CLI extension ZIP and extract it into a new empty folder.

```sh
unzip kumihan-ziheng-Gemini-CLI-extension-0.1.0.zip -d /absolute/path/kumihan-ziheng
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

- [Download full package (kumihan-ziheng-Gemini-CLI-extension-0.1.0.zip)](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/extensions/kumihan-ziheng-Gemini-CLI-extension-0.1.0.zip)
- Full package SHA-256: `6f199799a7905d55636c28cf5598bd143cadc90b7aa2460aa4b7befb9df24e75`

### Four individual skills

- [kumihan-ziheng](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-Gemini-Apps-skill-0.1.0.zip)
- [kumihan-ziheng-web](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-web-Gemini-Apps-skill-0.1.0.zip)
- [kumihan-ziheng-documents](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-documents-Gemini-Apps-skill-0.1.0.zip)
- [kumihan-ziheng-review](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-review-Gemini-Apps-skill-0.1.0.zip)

Taiwan and Hong Kong use explicit zh-Hant-TW and zh-Hant-HK profiles. Preserve the original characters.

`shasum -a 256 -c SHA256SUMS.txt`

- [View source](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng)

- [SHA256SUMS.txt](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng/downloads%20Gemini/SHA256SUMS.txt)


Version candidate: v0.2.0. Back up the existing folder, verify the active host MANIFEST/SHA256, replace the complete folder and reload. Historical v0.1.0 URLs remain available. Native host acceptance and formal Release are not implied.

Current v0.2.0 full bundle SHA-256: `f535fdd34b66ef3b87d594e80b2fd60396e8ae3d3a8cc014dac71c4f7f36ce71`. The older checksum above applies only to its explicitly named v0.1.0 archive.
