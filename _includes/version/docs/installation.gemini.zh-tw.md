<!-- Generated from authored installation Markdown; do not edit. -->
# 在 Gemini 中安裝 KUMIHAN

[日本語](installation.gemini.ja.md) ・ [English](installation.gemini.md) ・ [返回首頁](../README.md)

<br>

這份指南說明如何在 Gemini CLI 或 Gemini 應用程式中使用 KUMIHAN。

> **關於 v0.1.8**
> 此版本供你在自己的環境中試用。各工具的實際運作尚未經過充分驗證，因此部分步驟可能無法如預期使用。

<br>

## 1. 選擇安裝方式

| 使用環境 | 建議方式 |
| --- | --- |
| Gemini CLI（一次安裝四項技能） | [A. 安裝為擴充功能](#a-gemini-cli安裝為擴充功能) |
| Gemini CLI（只安裝需要的技能） | [B. 選擇個別技能安裝](#b-gemini-cli選擇個別技能安裝) |
| Gemini 應用程式（Web、Mac、手機） | [C. 上傳技能](#c-gemini-應用程式上傳技能) |

<br>

## A. Gemini CLI：安裝為擴充功能

一次安裝四項技能的方法：

```sh
gemini extensions install https://github.com/landco-llc/kumihan --ref main
```

若出現確認畫面，請先檢查內容再繼續。擴充功能安裝後會在所有專案啟用。

**更新時**

```sh
gemini extensions update kumihan
```

更新後請重新啟動 Gemini CLI。

**從 ZIP 安裝時**

1. 下載[擴充功能 ZIP](https://github.com/landco-llc/kumihan/releases/download/v0.1.8/kumihan-Gemini-CLI-extension-0.1.8.zip)。
2. 建立空的 `kumihan` 資料夾，並將 ZIP 內容解壓縮到其中。
3. 指定資料夾並安裝。

   ```sh
   gemini extensions install "/absolute/path/kumihan"
   ```

從 ZIP 安裝時不會自動更新。新版本推出後需自行替換 ZIP。

<br>

## B. Gemini CLI：選擇個別技能安裝

此方式可以只在指定專案安裝需要的技能。若已透過 A 安裝，便不必再執行此步驟。

例如在目標專案安裝 `kumihan`：

```sh
gemini skills install https://github.com/landco-llc/kumihan --path skills/kumihan --scope workspace
```

若要安裝其他技能，請將 `--path` 改為：

- `skills/kumihan-web` — 網頁製作
- `skills/kumihan-documents` — 報告與簡報
- `skills/kumihan-review` — 成果檢視

`--scope workspace` 表示只在這個專案使用。若省略，技能將可供所有專案使用。

**更新時**

再次執行相同指令。已安裝的技能會被取代，若曾自行修改請先備份。

<br>

## C. Gemini 應用程式：上傳技能

1. 下載想使用的技能 ZIP。
   - [kumihan](https://github.com/landco-llc/kumihan/releases/download/v0.1.8/kumihan-Gemini-Apps-skill-0.1.8.zip) — 開始使用前的規劃入口
   - [kumihan-web](https://github.com/landco-llc/kumihan/releases/download/v0.1.8/kumihan-web-Gemini-Apps-skill-0.1.8.zip) — 網頁製作
   - [kumihan-documents](https://github.com/landco-llc/kumihan/releases/download/v0.1.8/kumihan-documents-Gemini-Apps-skill-0.1.8.zip) — 報告與簡報
   - [kumihan-review](https://github.com/landco-llc/kumihan/releases/download/v0.1.8/kumihan-review-Gemini-Apps-skill-0.1.8.zip) — 成果檢視
2. 在 Gemini 開啟 **Customize**（若未看到，可先點選 **More**）→ **Skills** → **Upload**。
3. 逐一選擇 ZIP、確認內容後按下 **Create**。

**注意事項**

- 依原始指南所述，此功能目前僅提供給年滿 18 歲的個人 Google 帳號；工作或學校帳號尚不支援。
- 需啟用「Keep Activity」（保留活動紀錄）。
- 功能分階段開放，你可能尚未看到相關選項。請參閱 [Gemini 官方說明](https://support.google.com/gemini/answer/17094296?hl=ja)。
- 此處不能使用 Gemini CLI 的擴充功能 ZIP。
- 上傳的技能不會自動更新。新版本推出時需重新上傳。

<br>

## 2. 開始試用

建議先以不會修改檔案的要求測試：

> 我準備製作一份日文簡報。請告訴我需要注意哪些排版與設計要點，不要修改任何檔案。

<br>

## 驗證下載檔案（選用）

若要檢查下載檔案是否完整，可使用 [SHA256SUMS.txt](https://raw.githubusercontent.com/landco-llc/kumihan/d3d55a344ab5cfe942a640261f9a8760fceee2a2/downloads%20Gemini/SHA256SUMS.txt)。

將檔案放在與下載目錄相同的結構（`extensions/` 和 `skills/`），並在終端機執行以下命令。若無 `shasum`，可使用 Windows PowerShell 的 `Get-FileHash` 等工具檢查 SHA-256：

```sh
cd "downloads Gemini"
shasum -a 256 -c SHA256SUMS.txt
```

若每一行都顯示 `OK`，即表示校驗成功。

<br>

---

其他工具：[ChatGPT／Codex](installation.zh-tw.md) ・ [Claude](installation.claude.zh-tw.md)

介面及功能開放條件可能變更；請以各服務的官方說明為準（原始指南確認日期：2026 年 10 月 14 日）。
