# KUMIHAN｜字衡 — Claude / Install ZiHeng

**v0.1.0** — One Claude Code plugin and four independent skill ZIPs for supported Claude chat accounts.

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

- [Download full package (kumihan-ziheng-Claude-Code-plugin-0.1.0.zip)](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/plugins/kumihan-ziheng-Claude-Code-plugin-0.1.0.zip)
- Full package SHA-256: `b37ee0c95c7575b773667f0256eadd3ecf983d7f1e9db26761614ee71c76fe0e`

### Four individual skills

- [kumihan-ziheng](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-Claude-skill-0.1.0.zip)
- [kumihan-ziheng-web](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-web-Claude-skill-0.1.0.zip)
- [kumihan-ziheng-documents](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-documents-Claude-skill-0.1.0.zip)
- [kumihan-ziheng-review](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-review-Claude-skill-0.1.0.zip)

Taiwan and Hong Kong use explicit zh-Hant-TW and zh-Hant-HK profiles. Preserve the original characters.

`shasum -a 256 -c SHA256SUMS.txt`

- [View source](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng)

- [SHA256SUMS.txt](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng/downloads%20Claude/SHA256SUMS.txt)


Version candidate: v0.2.0. Back up the existing folder, verify the active host MANIFEST/SHA256, replace the complete folder and reload. Historical v0.1.0 URLs remain available. Native host acceptance and formal Release are not implied.

Current v0.2.0 full bundle SHA-256: `5da65c3d2085ec55e48309c01ee8a6a148ffecff13f490ec9747b24a0c51b06e`. The older checksum above applies only to its explicitly named v0.1.0 archive.
