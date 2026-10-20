# KUMIHAN｜字衡 — Claude / 字衡安裝

**v0.1.0** — 提供 Claude Code 插件，以及 Claude 應用程式可個別匯入的四個技能 ZIP。

> 此套件只提供組版指引；原生主機的安裝／技能呼叫未於本次測試驗收。請先用臺灣與香港小樣本核對。

## 安裝步驟

**1.** Claude Code：從 GitHub 註冊 KUMIHAN marketplace（這不會修改現有日文插件）。

```sh
claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
```

**2.** 在 Claude Code 對話中安裝字衡插件，與日文版的名稱不同。

```text
/plugin install kumihan-ziheng@kumihan-marketplace
```

**3.** 也可以下載 ZIP、解壓縮後以本機插件資料夾啟動。

```sh
claude --plugin-dir "/absolute/path/kumihan-ziheng"
```

**4.** Claude 應用程式：若帳戶有技能匯入功能，請逐一匯入下方的單一技能 ZIP。完整插件 ZIP 不適用於此步驟。

## 下載與校驗

- [下載完整套件 (kumihan-ziheng-Claude-Code-plugin-0.1.0.zip)](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/plugins/kumihan-ziheng-Claude-Code-plugin-0.1.0.zip)
- SHA-256（完整套件）: `b37ee0c95c7575b773667f0256eadd3ecf983d7f1e9db26761614ee71c76fe0e`

### 四個獨立技能

- [kumihan-ziheng](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-Claude-skill-0.1.0.zip)
- [kumihan-ziheng-web](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-web-Claude-skill-0.1.0.zip)
- [kumihan-ziheng-documents](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-documents-Claude-skill-0.1.0.zip)
- [kumihan-ziheng-review](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Claude/skills/kumihan-ziheng-review-Claude-skill-0.1.0.zip)

臺灣與香港的規則分別對應 zh-Hant-TW、zh-Hant-HK。請明確指定地區並保留原稿。

`shasum -a 256 -c SHA256SUMS.txt`

- [查看原始碼](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng)

- [SHA256SUMS.txt](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng/downloads%20Claude/SHA256SUMS.txt)


Version candidate: v0.2.0. Back up the existing folder, verify the active host MANIFEST/SHA256, replace the complete folder and reload. Historical v0.1.0 URLs remain available. Native host acceptance and formal Release are not implied.

Current v0.2.0 full bundle SHA-256: `7fcbe1c52d58b100fa92a1769f150c941849d0179a36e09ec2b72d1de84622b0`. The older checksum above applies only to its explicitly named v0.1.0 archive.
