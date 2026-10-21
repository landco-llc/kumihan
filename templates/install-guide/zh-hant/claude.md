這份指南說明如何在 Claude Code 與 Claude 聊天中使用 {{brand}}。

> **關於 v{{version}}**
> 此版本供你在自己的環境中試用。各工具的實際運作尚未經過充分驗證，因此部分步驟可能無法如預期使用。

## 1. 選擇安裝方式

| 使用環境 | 建議方式 |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. 從 GitHub 安裝](#a)（方便後續更新） |
{{/if}}
| Claude Code（想使用 ZIP 檔案時） | [{{L_zip}}. 從 ZIP 安裝](#{{l_zip}}) |
| Claude 聊天（claude.ai 網頁版或應用程式） | [{{L_chat}}. 上傳技能](#{{l_chat}}) |

Claude Code 和 Claude 聊天的安裝方式不同。

{{#if marketplace}}
## A. Claude Code：從 GitHub 安裝

1. 在終端機註冊 KUMIHAN 的套件來源。

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. 在 Claude Code 對話中輸入：

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. 確認內容並選擇適用範圍（只供自己使用、只限目前專案等）後安裝。

安裝完成後，可使用下列指令：

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code：從 ZIP 安裝

1. 下載 [Claude Code 外掛 ZIP]({{plugin_url}})。
{{#if plugin_folder}}
2. 解壓縮後會得到 `{{plugin_folder}}` 資料夾。
{{else}}
2. 建立空的 `{{plugin}}` 資料夾，並將 ZIP 內容解壓縮到其中。
{{/if}}
3. 指定該資料夾並啟動 Claude Code。

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**注意事項**

- 請保留資料夾內的完整內容，不要刪除檔案或混入其他檔案。
- 這種方式不會自動更新。新版本推出後，需自行替換 ZIP。

## {{L_chat}}. Claude 聊天：上傳技能

適用於 claude.ai 或 Claude 應用程式。

1. 下載想使用的技能 ZIP。
{{skills_list_indented}}
2. 在 Claude 開啟 **Customize → Skills**，使用新增按鈕選擇 **Upload a skill**。
3. 逐一上傳 ZIP 並啟用技能。

**注意事項**

- 此處不能使用 Claude Code 專用的外掛 ZIP，請上傳個別技能 ZIP。
- 上傳前不要變更 ZIP 檔名。
- 使用技能前必須在設定中啟用「程式碼執行」。請參閱 [Claude 官方說明](https://support.claude.com/en/articles/12512180-use-skills-in-claude)。
- 組織帳號可能受到管理員設定限制而無法使用。
- 上傳的技能不會自動更新。新版本推出時需重新上傳。

## 2. 開始試用

建議先以不會修改檔案的要求測試：

> 我準備製作一個中文網頁。請告訴我需要注意哪些要點，不要修改任何檔案。

## 驗證下載檔案（選用）

若要檢查下載的檔案是否完整，可使用 [SHA256SUMS.txt]({{sums}})。

將 SHA256SUMS.txt 放在與下載的 ZIP 檔案相同的資料夾，並在終端機執行以下命令。若無 `shasum`，可使用 Windows PowerShell 的 `Get-FileHash` 等工具檢查 SHA-256。

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

若下載檔案的那一行顯示 `OK`，即表示檔案沒有問題。

---

其他工具：[ChatGPT／Codex]({{page_chatgpt}}) ・ [Gemini]({{page_gemini}})

介面及功能開放條件可能變更；最新資訊請以各服務的官方說明為準（本頁確認日期：2026 年 10 月 14 日）。
