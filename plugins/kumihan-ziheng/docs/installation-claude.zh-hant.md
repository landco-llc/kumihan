# KUMIHAN｜字衡 — Claude / 安裝指南

完整套件與四個獨立技能使用相同的字衡規則。請從對應主機的網站指南取得目前已驗證的公開 ZIP、SHA-256 與版本；不要從日本語 KUMIHAN 的 monorepo 根目錄安裝字衡。

## 目前公開版與下載校驗

[安裝指南](https://landco-llc.github.io/kumihan/docs/install-ziheng-claude.html)

Claude Code 可從 KUMIHAN marketplace 安裝獨立字衡插件，或將完整套件解壓縮後使用本機插件資料夾。Claude 應用程式若提供技能匯入功能，使用個別 Skill ZIP。

```sh
claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
```

```text
/plugin install kumihan-ziheng@kumihan-marketplace
```

```sh
claude --plugin-dir "/absolute/path/kumihan-ziheng"
```

## Skills

- `kumihan-ziheng`
- `kumihan-ziheng-web`
- `kumihan-ziheng-documents`
- `kumihan-ziheng-review`

先備份既有資料夾，校驗 ZIP 後完整替換相同主機與版本的套件，再重新載入。不要混搭不同版本的 references、rules 或 scripts。

原始碼的 active MANIFEST.json 和 SHA256SUMS.txt 描述本次原始碼配布；它可能比網站的正式公開版新。v0.1.0 與 v0.2.0 的舊 ZIP 保留，原 manifest 與 checksum 在 history/<version>/。

- [MANIFEST.json](../downloads%20Claude/MANIFEST.json)
- [SHA256SUMS.txt](../downloads%20Claude/SHA256SUMS.txt)

實際主機探索、安裝、技能呼叫與描畫仍需在使用者環境驗收。以 zh-Hant-TW／zh-Hant-HK 及固定原稿測試；直排時分別檢查標點、混排、閱讀順序與 Unicode 序列。
