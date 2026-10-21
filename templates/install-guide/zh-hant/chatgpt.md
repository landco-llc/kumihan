這份指南說明如何在 ChatGPT 或 Codex 中使用 {{brand}}。

> **關於 v{{version}}**
> 此版本供你在自己的環境中試用。各工具的實際運作尚未經過充分驗證，因此部分步驟可能無法如預期使用。

## 1. 選擇安裝方式

| 使用環境 | 建議方式 |
| --- | --- |
| ChatGPT（畫面上提供技能上傳功能時） | [A. 逐一新增技能](#a) |
| ChatGPT（希望註冊為自己的專用外掛時） | [B. 將四項技能註冊為外掛](#b) |
| Codex（在本機電腦使用時） | [C. 複製資料夾](#c) |

**技能**是一個獨立功能；**外掛**則是包含四項技能的套件。

## 2. 下載檔案

檔案位於[發行頁面]({{release}})。點選連結即可下載 ZIP 檔案。

**外掛（包含四項技能）**

- {{plugin_link}}

**個別技能**

{{skills_list}}

## A. 逐一新增技能至 ChatGPT

適用於 ChatGPT 畫面中可找到「Skills」與上傳選項的情況。

1. 選擇一個技能 ZIP 檔案並上傳。
2. 確認畫面顯示的內容後新增技能。
3. 需要其他技能時，依序重複上述步驟。

**注意事項**

- 這種方式不能使用外掛 ZIP，請選用個別技能的 ZIP。
- 只把檔案附加到聊天對話中，不代表已安裝為技能。
- 若找不到相關功能，可能是你的方案或應用程式尚未開放使用。請參考 [OpenAI 官方說明](https://learn.chatgpt.com/docs/build-skills)。

## B. 將四項技能註冊為 ChatGPT 外掛

把四項技能合併註冊成自己專用的外掛。

1. 在 ChatGPT 開啟新對話，選擇 `@plugin-creator`。
2. 附上外掛 ZIP 檔案。
3. 輸入類似下列的要求：

   > 請將這個套件註冊為我個人使用的私人外掛，不要提交至公開目錄。

4. 若註冊成功，可在 Plugins 的「Personal」或「Created by me」找到 **{{display}}**。
5. 視需要安裝，並在新對話中啟用。

**注意事項**

- 外掛可能會建立於團隊工作區。若要只供自己使用，請在註冊前確認儲存位置。
- 此功能可能因方案或工作區設定而無法使用。詳見 [Build plugins](https://learn.chatgpt.com/docs/build-plugins) 與 [Plugins](https://learn.chatgpt.com/docs/plugins)。
- 以此方式註冊的外掛僅供你的帳號使用，不會出現在公開目錄。

## C. 在 Codex 中複製技能資料夾

將技能 ZIP 解壓縮後，會得到 `{{first}}` 等資料夾。把這個資料夾複製到 Codex 可讀取的位置。

| 使用範圍 | 複製目的地 |
| --- | --- |
| 僅限特定專案 | 專案內的 `.agents/skills/` |
| 所有專案 | 個人主目錄下的 `~/.agents/skills/` |

例如，要在專案中加入 `{{first}}`，請使用：

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**注意事項**

- 請連同資料夾內的全部檔案一起複製。缺少部分檔案將無法正常運作。
- 若已有同名資料夾，覆寫前請先檢查內容。

## 3. 開始試用

安裝後，開啟新對話並呼叫技能。

| 工具 | 呼叫方式 |
| --- | --- |
| ChatGPT | 由 `@` 選擇 |
| Codex | 使用 `$` 或 `/skills` 選擇 |

建議先用不會修改檔案的要求測試：

> 我準備製作一份中文報告。請告訴我需要注意哪些要點，不要修改任何檔案。

## 驗證下載檔案（選用）

若要檢查下載的檔案是否完整，可使用 [SHA256SUMS.txt]({{sums}})。

將 SHA256SUMS.txt 放在與下載的 ZIP 檔案相同的資料夾，並在終端機執行以下命令。若無 `shasum`，可使用 Windows PowerShell 的 `Get-FileHash` 等工具檢查 SHA-256。

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

若下載檔案的那一行顯示 `OK`，即表示檔案沒有問題。

---

其他工具：[Claude]({{page_claude}}) ・ [Gemini]({{page_gemini}})

介面及功能開放條件可能變更；最新資訊請以各服務的官方說明為準（本頁確認日期：2026 年 10 月 14 日）。
