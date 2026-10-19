# 在 Claude 中安裝 KUMIHAN

[日本語](installation.claude.ja.md) ・ [English](installation.claude.md) ・ [返回首頁](../README.md)

<br>

這份指南說明如何在 Claude Code 與 Claude 應用程式中使用 KUMIHAN。

> **關於 v0.1.8**
> 此版本供你在自己的環境中試用。各工具的實際運作尚未經過充分驗證，因此部分步驟可能無法如預期使用。

<br>

## 1. 選擇安裝方式

| 使用環境 | 建議方式 |
| --- | --- |
| Claude Code | [A. 從 GitHub 安裝](#a-claude-code從-github-安裝)（方便後續更新） |
| Claude Code（想使用 ZIP 檔案時） | [B. 從 ZIP 安裝](#b-claude-code從-zip-安裝) |
| Claude（claude.ai 網頁版或應用程式） | [C. 上傳技能](#c-claude-應用程式上傳技能) |

Claude Code 和 Claude 應用程式的安裝方式不同。

<br>

## A. Claude Code：從 GitHub 安裝

1. 在終端機註冊 KUMIHAN 的套件來源。

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. 在 Claude Code 對話中輸入：

   ```text
   /plugin install kumihan@kumihan-marketplace
   ```

3. 確認內容並選擇適用範圍（只供自己使用、只限目前專案等）後安裝。

安裝完成後，可使用下列指令：

- `/kumihan:kumihan`
- `/kumihan:kumihan-web`
- `/kumihan:kumihan-documents`
- `/kumihan:kumihan-review`

更新方式請參閱[更新指南](updates.md#claude-code)。

<br>

## B. Claude Code：從 ZIP 安裝

1. 下載 [Claude Code 外掛 ZIP](../downloads%20Claude/plugins/kumihan-Claude-Code-plugin-0.1.8.zip)。
2. 解壓縮後會得到 `kumihan` 資料夾。
3. 指定該資料夾並啟動 Claude Code。

   ```sh
   claude --plugin-dir "/absolute/path/kumihan"
   ```

**注意事項**

- 請保留資料夾內的完整內容，不要刪除檔案或混入其他檔案。
- 這種方式不會自動更新。新版本推出後，需自行替換 ZIP。

<br>

## C. Claude 應用程式：上傳技能

適用於 claude.ai 或 Claude 應用程式。

1. 下載想使用的技能 ZIP。
   - [kumihan](../downloads%20Claude/skills/kumihan-Claude-skill-0.1.8.zip) — 開始使用前的規劃入口
   - [kumihan-web](../downloads%20Claude/skills/kumihan-web-Claude-skill-0.1.8.zip) — 網頁製作
   - [kumihan-documents](../downloads%20Claude/skills/kumihan-documents-Claude-skill-0.1.8.zip) — 報告與簡報
   - [kumihan-review](../downloads%20Claude/skills/kumihan-review-Claude-skill-0.1.8.zip) — 成果檢視
2. 在 Claude 開啟 **Customize → Skills**，使用新增按鈕選擇 **Upload a skill**。
3. 逐一上傳 ZIP 並啟用技能。

**注意事項**

- 此處不能使用 Claude Code 專用的外掛 ZIP，請上傳個別技能 ZIP。
- 上傳前不要變更 ZIP 檔名。
- 使用技能前必須在設定中啟用「程式碼執行」。請參閱 [Claude 官方說明](https://support.claude.com/en/articles/12512180-use-skills-in-claude)。
- 組織帳號可能受到管理員設定限制。
- 上傳的技能不會自動更新。新版本推出時需重新上傳。

<br>

## 2. 開始試用

建議先以不會修改檔案的要求測試：

> 我準備製作一個日文網頁。請告訴我需要注意哪些排版與設計要點，不要修改任何檔案。

<br>

## 驗證下載檔案（選用）

若要檢查下載檔案是否完整，可使用 [SHA256SUMS.txt](../downloads%20Claude/SHA256SUMS.txt)。

將檔案放在與下載目錄相同的結構（`plugins/` 和 `skills/`），並在終端機執行以下命令。若無 `shasum`，可使用 Windows PowerShell 的 `Get-FileHash` 等工具檢查 SHA-256：

```sh
cd "downloads Claude"
shasum -a 256 -c SHA256SUMS.txt
```

若每一行都顯示 `OK`，即表示校驗成功。

<br>

---

其他工具：[ChatGPT／Codex](installation.zh-tw.md) ・ [Gemini](installation.gemini.zh-tw.md)

介面及功能開放條件可能變更；請以各服務的官方說明為準（原始指南確認日期：2026 年 10 月 14 日）。
