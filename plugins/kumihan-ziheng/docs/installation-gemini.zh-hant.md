# KUMIHAN｜字衡 — Gemini / 安裝指南

完整套件與四個獨立技能使用相同的字衡規則。請從對應主機的網站指南取得目前已驗證的公開 ZIP、SHA-256 與版本；不要從日本語 KUMIHAN 的 monorepo 根目錄安裝字衡。

## 目前公開版與下載校驗

[安裝指南](https://landco-llc.github.io/kumihan/docs/install-ziheng-gemini.html)

將 Gemini CLI 專用延伸 ZIP 解壓縮到新的本機資料夾，再安裝該資料夾。Gemini 應用程式若提供技能匯入功能，使用個別 Skill ZIP。

```sh
gemini extensions install "/absolute/path/to/extracted-ziheng-extension"
```

## Skills

- `kumihan-ziheng`
- `kumihan-ziheng-web`
- `kumihan-ziheng-documents`
- `kumihan-ziheng-review`

先備份既有資料夾，校驗 ZIP 後完整替換相同主機與版本的套件，再重新載入。不要混搭不同版本的 references、rules 或 scripts。

原始碼的 active MANIFEST.json 和 SHA256SUMS.txt 描述本次原始碼配布；它可能比網站的正式公開版新。v0.1.0 與 v0.2.0 的舊 ZIP 保留，原 manifest 與 checksum 在 history/<version>/。

- [MANIFEST.json](../downloads%20Gemini/MANIFEST.json)
- [SHA256SUMS.txt](../downloads%20Gemini/SHA256SUMS.txt)

實際主機探索、安裝、技能呼叫與描畫仍需在使用者環境驗收。以 zh-Hant-TW／zh-Hant-HK 及固定原稿測試；直排時分別檢查標點、混排、閱讀順序與 Unicode 序列。
