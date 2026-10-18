# 在 ChatGPT 和 Codex 中安裝 KUMIHAN

[日本語](installation.ja.md) ・ [English](installation.md) ・ [返回首頁](../README.md)

<br>

這份指南說明如何在 ChatGPT 或 Codex 中使用 KUMIHAN。

> **關於預覽版（v0.1.5 preview）**  
> 此版本供你在自己的環境中試用。各工具的實際運作尚未經過充分驗證，因此部分步驟可能無法如預期使用。

<br>

## 1. 選擇安裝方式

| 使用環境 | 建議方式 |
| --- | --- |
| ChatGPT（畫面上提供技能上傳功能時） | [A. 逐一新增技能](#a-逐一新增技能至-chatgpt) |
| ChatGPT（希望註冊為自己的專用外掛時） | [B. 將四項技能註冊為外掛](#b-將四項技能註冊為-chatgpt-外掛) |
| Codex（在本機電腦使用時） | [C. 複製技能資料夾](#c-在-codex-中複製技能資料夾) |

**技能（Skill）**是一個獨立功能；**外掛（Plugin）**則是包含四項技能的套件。

<br>

## 2. 下載檔案

檔案位於[下載目錄](../downloads%20GPT-Codex/)。

**外掛套件（包含四項技能）**

- [kumihan-GPT-Codex-plugin-0.1.5-preview.zip](../downloads%20GPT-Codex/plugins/kumihan-GPT-Codex-plugin-0.1.5-preview.zip)

**個別技能**

- [kumihan](../downloads%20GPT-Codex/skills/kumihan-GPT-Codex-skill-0.1.5-preview.zip) — 開始使用前的規劃入口
- [kumihan-web](../downloads%20GPT-Codex/skills/kumihan-web-GPT-Codex-skill-0.1.5-preview.zip) — 網頁製作
- [kumihan-documents](../downloads%20GPT-Codex/skills/kumihan-documents-GPT-Codex-skill-0.1.5-preview.zip) — 報告與簡報
- [kumihan-review](../downloads%20GPT-Codex/skills/kumihan-review-GPT-Codex-skill-0.1.5-preview.zip) — 成果檢視

在 GitHub 開啟檔案後，使用右上角的下載按鈕儲存。

<br>

## A. 逐一新增技能至 ChatGPT

適用於 ChatGPT 畫面中可找到「Skills」與上傳選項的情況。

1. 選擇一個技能 ZIP 檔案並上傳。
2. 確認畫面顯示的內容後新增技能。
3. 需要其他技能時，依序重複上述步驟。

**注意事項**

- 這種方式不能使用外掛套件 ZIP，請選用個別技能的 ZIP。
- 只把檔案附加到聊天對話中，不代表已安裝為技能。
- 若找不到相關功能，可能是你的方案或應用程式尚未開放使用。請參考 [OpenAI 官方說明](https://learn.chatgpt.com/docs/build-skills)。

<br>

## B. 將四項技能註冊為 ChatGPT 外掛

把四項技能合併註冊成自己專用的外掛。

1. 在 ChatGPT 開啟新對話，選擇 `@plugin-creator`。
2. 附上外掛套件 ZIP 檔案。
3. 輸入類似下列的要求：

   > 請將這個套件註冊為我個人使用的私人外掛，不要提交至公開外掛目錄。

4. 若註冊成功，可在 Plugins 的「Personal」或「Created by me」找到 **KUMIHAN Private Install Preview**。
5. 視需要安裝，並在新對話中啟用。

**注意事項**

- 依設定不同，外掛可能建立於團隊工作區。若要只供自己使用，請先確認註冊位置。
- 此功能可能因方案或工作區設定而無法使用。詳見 [Build plugins](https://learn.chatgpt.com/docs/build-plugins) 與 [Plugins](https://learn.chatgpt.com/docs/plugins)。
- 以此方式建立的外掛僅供你的帳號使用，不會出現在公開外掛目錄。

<br>

## C. 在 Codex 中複製技能資料夾

將技能 ZIP 解壓縮後，會得到 `kumihan` 等資料夾。把整個資料夾複製到 Codex 可讀取的位置。

| 使用範圍 | 複製目的地 |
| --- | --- |
| 僅限特定專案 | 專案內的 `.agents/skills/` |
| 所有專案 | 個人主目錄下的 `~/.agents/skills/` |

例如，要在專案中加入 `kumihan`，請使用：

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R kumihan /path/to/your-project/.agents/skills/
```

**注意事項**

- 請連同資料夾內的全部檔案一起複製。缺少部分檔案可能導致無法正常使用。
- 若已有同名資料夾，覆寫前請先檢查內容。

若想從 GitHub 直接安裝，或使用 Codex 市集，請參閱[更新指南](updates.md)。

<br>

## 3. 開始試用

安裝後，開啟新對話並呼叫技能。

| 工具 | 呼叫方式 |
| --- | --- |
| ChatGPT | 由 `@` 選擇 |
| Codex | 使用 `$` 或 `/skills` 選擇 |

建議先用不會修改檔案的要求測試：

> 我準備製作一份日文報告。請告訴我需要注意哪些排版與設計要點，不要修改任何檔案。

<br>

## 驗證下載檔案（選用）

若要檢查下載檔案是否完整，可使用 [SHA256SUMS.txt](../downloads%20GPT-Codex/SHA256SUMS.txt)。

將檔案放在與下載目錄相同的結構（`plugins/` 和 `skills/`），並在 macOS 的終端機執行：

```sh
cd "downloads GPT-Codex"
shasum -a 256 -c SHA256SUMS.txt
```

若每一行都顯示 `OK`，即表示校驗成功。

<br>

---

其他工具：[Claude](installation.claude.zh-tw.md) ・ [Gemini](installation.gemini.zh-tw.md)

介面及功能開放條件可能變更；請以各服務的官方說明為準（原始指南確認日期：2026 年 10 月 14 日）。
