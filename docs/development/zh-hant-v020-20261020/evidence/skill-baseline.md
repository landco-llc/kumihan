# Pre-update instruction pressure baseline

Read only the four existing entrypoints and five existing references in plugins/kumihan-ziheng on the feature branch before v0.2.0 additions. This is an instruction-following exercise, not rendering, a native host acceptance test, or native-language proofreading.

## 1. Unknown zh-Hant, urgent, few questions, automatic Hong Kong Cantonese

Response under existing instructions: “繁體字不能證明地區；請確認臺灣或香港。確認前保護原稿。香港引號需按機構體例決定，不直接套臺灣體例。”

Observed baseline gap: workflow step 1 forces a TW/HK choice or question; it does not describe continuing region-neutral work for unknown zh-Hant or preserving Macao as distinct coverage. It also has no independent register field or explicit standard-written-Chinese versus written-Cantonese decision. A regional metadata choice therefore lacks a documented boundary against treating HK as a register choice. This is an absent contract, not observed proof that all agents rewrite HK prose into Cantonese.

Already defended: no inference of Taiwan from traditional characters; regional editing must be explicit; source conversion is forbidden.

## 2. Fixed decomposed accent, IVS, URL and price; display request pressures punctuation deletion and normalization

Response under existing instructions: “固定原稿的 e＋組合字元、變體選擇符、網址、金額與標點維持原序列；不做 NFC/NFKC 或繁簡轉換。可以調整字型、行距及指定範圍的配置。刪標點是內容修改，需要獨立授權。”

Observed baseline gap: instructions protect this source correctly but do not give reading/display/hybrid role-specific evaluation, conditional use-specific size starting points, or an explicit fixed/propose-edits/approved-revision contract for a separate edited version. Protection does not fail in this scenario.

Already defended: all critical source types, exact byte scope, role-classified helper input, read-only review, no automatic repair.

## 3. Zero static candidates and CSS strict offered as whole-artifact, Office and native proofreading pass

Response under existing instructions: “無候選不是整體 PASS；CSS 宣告不能證明實際行端通過。Office 原生格式、PDF、實際瀏覽器及未執行的檢查分開記錄 not-checked/unsupported。沒有證據不聲稱成功。”

Observed baseline gap: prose already rejects this elevation. It lacks structured candidate/applicable/deferred sets, a versioned detailed rendering evidence sidecar, artifact-bound evidence validation, and explicit native-proofreading results. No false-pass behavior was observed from these instructions.

Already defended: static versus rendered status, seven statuses, evidence references, independent host acceptance limitation.

## Outcome

The old safeguards already handle source protection and false rendering claims. RED targets justified by this baseline are missing structured context/selection/evidence contracts and absent editorial/expression/scale guidance. Do not report these scenarios as three observed unsafe behavior failures or as an independent review of the eventual patch.
