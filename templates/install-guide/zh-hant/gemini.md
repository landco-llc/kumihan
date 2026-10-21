這份指南說明如何在 Gemini CLI 或 Gemini 應用程式中使用 {{brand}}。

> **關於 v{{version}}**
> 此版本供你在自己的環境中試用。各工具的實際運作尚未經過充分驗證，因此部分步驟可能無法如預期使用。

## 1. 選擇安裝方式

| 使用環境 | 建議方式 |
| --- | --- |
| Gemini CLI（一次安裝四項技能） | [A. 安裝為擴充功能](#a) |
| Gemini CLI（只安裝需要的技能） | [B. 選擇個別技能安裝](#b) |
| Gemini 應用程式（Web、Mac、手機） | [C. 上傳技能](#c) |

## A. Gemini CLI：安裝為擴充功能

一次安裝四項技能的方法。

1. 下載[擴充功能 ZIP]({{plugin_url}})。
{{#if plugin_folder}}
2. 解壓縮後會得到 `{{plugin_folder}}` 資料夾。
{{else}}
2. 建立空的 `{{plugin}}` 資料夾，並將 ZIP 內容解壓縮到其中。
{{/if}}
3. 指定資料夾並安裝。

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

若出現確認畫面，請先檢查內容再繼續。擴充功能安裝後會在所有專案啟用。

從 ZIP 安裝時不會自動更新。新版本推出後需自行替換 ZIP。

## B. Gemini CLI：選擇個別技能安裝

此方式可以只在指定專案安裝需要的技能。若已透過 A 安裝，便不必再執行此步驟。

例如要安裝 `{{first}}`，請在目標專案中執行：

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

若要安裝其他技能，請將 `--path` 改為：

{{gemini_paths}}

`--scope workspace` 表示「只在這個專案」使用。若省略，技能將可供所有專案使用。

**更新時**

再次執行相同指令。已安裝的技能會被取代，若曾自行修改請先備份。

## C. Gemini 應用程式：上傳技能

1. 下載想使用的技能 ZIP。
{{skills_list_indented}}
2. 在 Gemini 開啟 **Customize**（若未看到，請改點選 **More**）→ **Skills** → **Upload**。
3. 逐一選擇 ZIP、確認內容後按下 **Create**。

**注意事項**

- 此功能僅提供給年滿 18 歲的個人 Google 帳號；工作或學校帳號目前尚不支援。
- 需啟用「Keep Activity」（保留活動紀錄）。
- 功能分階段開放，你可能尚未看到相關選項。詳見 [Gemini 官方說明](https://support.google.com/gemini/answer/17094296?hl=ja)。
- 此處不能使用擴充功能 ZIP（Gemini CLI 專用）。
- 上傳的技能不會自動更新。新版本推出時需重新上傳。

## 2. 開始試用

建議先以不會修改檔案的要求測試：

> 我準備製作一份中文簡報。請告訴我需要注意哪些要點，不要修改任何檔案。

## 驗證下載檔案（選用）

若要檢查下載的檔案是否完整，可使用 [SHA256SUMS.txt]({{sums}})。

將 SHA256SUMS.txt 放在與下載的 ZIP 檔案相同的資料夾，並在終端機執行以下命令。若無 `shasum`，可使用 Windows PowerShell 的 `Get-FileHash` 等工具檢查 SHA-256。

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

若下載檔案的那一行顯示 `OK`，即表示檔案沒有問題。

---

其他工具：[ChatGPT／Codex]({{page_chatgpt}}) ・ [Claude]({{page_claude}})

介面及功能開放條件可能變更；最新資訊請以各服務的官方說明為準（本頁確認日期：2026 年 10 月 14 日）。
