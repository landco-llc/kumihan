> Historical v0.1.0 report retained below. v0.2.0 execution evidence and unresolved integration checks are recorded separately in the repository at docs/development/zh-hant-v020-20261020/TEST_REPORT.md; these old counts are not current-run results.

# 字衡：測試範圍與結果

2026-10-18。Cloud Linux，Python 3.12.14，zlib 1.3.2；JSON Schema 測試使用 jsonschema 4.26.0。
這是靜態產品／配布測試摘要，不是原生主機或排版引擎的認證。

| 檢查 | 實際執行命令或範圍 | 結果 |
| --- | --- | --- |
| locale／日本語歷史 profile | unittest test_locale.py；6 個既有媒體的 ID 順序一致，拒絕未知／缺少地區 | passed |
| 原稿保存 | test_checks.py；專名、金額、URL、全半形、IVS、分解字元、emoji ZWJ、BOM／CRLF；差異必須被識別 | passed，僅提供的 bytes |
| 區域正／負／例外 | 22 件原創 fixture；受保護的 name/url/code/english-quote/protected 不作正文標點判定 | passed，靜態候選符合預期 |
| JSON／rule schema | test_package.py；15 條新規則和16條共通政策、schema 格式與來源 ID | passed |
| profile／report／context schema | 離線參照驗證；拒絕地區不一致與缺乏證據的 passed | passed |
| 獨立版號／唯讀 check | 隔離目錄升版，拒絕非法版本；check 失敗不覆寫產物 | passed |
| 整包插件 | ZIP 本地文件路徑與 manifest 身分一致 | passed |
| 4 Skills 單獨展開 | test_package.py；本地 Markdown 參考、inventory digest、LICENSE、helper import、不含 JA-TYPE | passed |
| 字衡 build／check | python3 tools/build_ziheng.py；python3 tools/build_ziheng.py --check | passed |
| 重建一致 | 同一 Python／zlib 下兩次 plan_outputs 完整 bytes 比對 | passed；非跨版本保證 |
| 日本語配布 | python3 tools/build_dist.py --check | passed，128 個既有生成檔；0.1.4-preview |

負例測試的 passed 表示候選／差異被正確辨識，不表示負例的排版本身合格。
規則 coverage：字衡15條，其中5條 implemented 僅限 notes 記載的靜態子功能、10條 guidance-only；共通16條維持原有 guidance-only 狀態。
早期研究52候選／28案例原本未取得，未宣稱移植；本次22件fixture獨立撰寫。

未執行：原生 ChatGPT／Codex 安裝、探索與呼叫；Claude／Gemini 字衡專屬配布與主機驗收；瀏覽器實際行端、字形、320px重排與200%放大；Office／PDF、直排與注音／ruby。
以上保持 not-checked；套件未提供的 renderer／extractor 屬 unsupported。
香港機構別標點體例 needs-review。來源與版次見 sources.json，各規則的 source_sections 描述採用範圍。

目前單元測試：11項；日本語 JA-TYPE-011 的8件既有 specification fixture 靜態一致性檢查通過，不代表啟用該規則或完成描畫驗證。

最終檢查亦包含整包插件 ZIP 的所有本地文件連結、離線 report/profile/context schema、獨立版號更新、非法版號拒絕和 check 的非覆寫行為。報告 schema 曾有一處遺留日本語 method 參照，已由失敗案例定位並改為字衡本地參照，完整11項重新通過。
獨立一次審查無 blocking finding，詳見 LIGHT_REVIEW.md。CI 結果以 Draft PR 的當前 HEAD checks 為準；本檔的本地 passed 不代表未觀察的遠端執行已通過。
