# KUMIHAN｜字衡 — Claude / Install ZiHeng

**v0.1.0-preview** — One Claude Code plugin and four independent skill ZIPs for supported Claude chat accounts.

> This package offers typography guidance, not an automatic renderer. Native host installation and invocation have not yet passed live host acceptance. Test both Taiwan and Hong Kong samples first.

## Installation steps

**1.** Claude Code: register the KUMIHAN marketplace from GitHub without replacing the Japanese plugin.

```sh
claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
```

**2.** Install the ZiHeng plugin by its distinct name from within Claude Code.

```text
/plugin install kumihan-ziheng@kumihan-marketplace
```

**3.** Alternatively extract the plugin ZIP and load its local folder directly.

```sh
claude --plugin-dir "/absolute/path/kumihan-ziheng"
```

**4.** Claude chat: if Skill import is supported on your account, import one standalone skill ZIP at a time; the Claude Code plugin ZIP is not the chat skill upload format.

## Downloads and checksums

- [Download full package (kumihan-ziheng-Claude-Code-plugin-0.1.0-preview.zip)](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/plugins/kumihan-ziheng-Claude-Code-plugin-0.1.0-preview.zip)
- Full package SHA-256: `a4d7e1d49c1a84545cc8fe8d207f3ea706032a18b80518c162ec27f3a1566c3b`

### Four individual skills

- [kumihan-ziheng](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-Claude-skill-0.1.0-preview.zip)
- [kumihan-ziheng-web](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-web-Claude-skill-0.1.0-preview.zip)
- [kumihan-ziheng-documents](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-documents-Claude-skill-0.1.0-preview.zip)
- [kumihan-ziheng-review](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-review-Claude-skill-0.1.0-preview.zip)

Taiwan and Hong Kong use explicit zh-Hant-TW and zh-Hant-HK profiles. Preserve the original characters.

`shasum -a 256 -c SHA256SUMS.txt`

- [View source](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng)

- [SHA256SUMS.txt](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng/downloads%20Claude/SHA256SUMS.txt)
