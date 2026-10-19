# KUMIHAN｜字衡 — Gemini / 字衡安裝

**v0.1.0** — 提供 Gemini CLI 專用擴充功能及 Gemini 應用程式的四個獨立技能 ZIP。

> 此套件只提供組版指引；原生主機的安裝／技能呼叫未於本次測試驗收。請先用臺灣與香港小樣本核對。

## 安裝步驟

**1.** 下載專用的 Gemini CLI 擴充功能 ZIP 並解壓縮至新的空白資料夾。

```sh
unzip kumihan-ziheng-Gemini-CLI-extension-0.1.0.zip -d /absolute/path/kumihan-ziheng
```

**2.** 將此資料夾指定給 Gemini CLI 安裝指令，重新啟動工作階段後檢查技能。

```sh
gemini extensions install "/absolute/path/kumihan-ziheng"
```

**3.** GitHub monorepo 根目錄屬於「日文 KUMIHAN」擴充功能；不得直接使用根網址安裝並宣稱裝好了字衡。

```sh
gemini extensions list
```

**4.** Gemini 應用程式：若帳戶支援技能匯入，請使用下方的單一技能 ZIP，並於該主機重新驗收。

## 下載與校驗

- [下載完整套件 (kumihan-ziheng-Gemini-CLI-extension-0.1.0.zip)](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/extensions/kumihan-ziheng-Gemini-CLI-extension-0.1.0.zip)
- SHA-256（完整套件）: `6f199799a7905d55636c28cf5598bd143cadc90b7aa2460aa4b7befb9df24e75`

### 四個獨立技能

- [kumihan-ziheng](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-Gemini-Apps-skill-0.1.0.zip)
- [kumihan-ziheng-web](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-web-Gemini-Apps-skill-0.1.0.zip)
- [kumihan-ziheng-documents](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-documents-Gemini-Apps-skill-0.1.0.zip)
- [kumihan-ziheng-review](https://raw.githubusercontent.com/landco-llc/kumihan/main/plugins/kumihan-ziheng/downloads%20Gemini/skills/kumihan-ziheng-review-Gemini-Apps-skill-0.1.0.zip)

臺灣與香港的規則分別對應 zh-Hant-TW、zh-Hant-HK。請明確指定地區並保留原稿。

`shasum -a 256 -c SHA256SUMS.txt`

- [查看原始碼](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng)

- [SHA256SUMS.txt](https://github.com/landco-llc/kumihan/tree/main/plugins/kumihan-ziheng/downloads%20Gemini/SHA256SUMS.txt)
