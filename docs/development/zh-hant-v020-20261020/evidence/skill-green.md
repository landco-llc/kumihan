# v0.2.0 instruction pressure check

Read the current four entrypoints, four new references (research-20261020, editorial-registers, expression-and-scale, verification-matrix), and existing workflow.md. Same three scenarios as the pre-update baseline. This is an instruction-following exercise only: no rendering, host invocation, Office, assistive technology or native-language acceptance is claimed. No product files edited.

## 1. Unknown zh-Hant, urgent, few questions, automatic Hong Kong Cantonese

Concrete response using the new contract:

「content_locale=zh-Hant、editorial_region=unknown、register=未指定として記録します。香港だから書面粵語とは推定しません。原稿保全・情報順序・地域中立の確認は進め、香港固有の引號や語體は条件不足としてdeferredに残します。既存metadataを使い、結果に影響する不足だけ確認します。MOならMOを保持し、HKへ統合しません。」

New contract covers the missing regional/register separation and neutral continuation. However this scenario is not fully GREEN yet: all entrypoints first route to existing workflow.md, whose step 1 still requires choosing zh-Hant-TW or zh-Hant-HK and says unknown region must first be asked. This conflicts with the appended v2 section and editorial-registers.md. Step 5 also only describes rules_by_locale rather than the v2 candidate/applicable/deferred split, leaving unknown/MO without an explicit path through the first linked workflow. Update the canonical workflow to route v2 inputs through context.py and reserve the old strict selection for legacy callers.

## 2. Fixed decomposed accent, IVS, URL and price; display request pressures punctuation deletion and normalization

Concrete response:

「source_policy=fixedを維持し、e＋組合字元、IVS、URL、價格與標點を原序列のまま保持します。題字はdisplay、必要情報はreading/hybridとして役割を分け、字級・段幅・余白・配置だけを許可範囲で調整します。句の抜出しや標點削除も文章編集です。提案許可が得られた場合は原版と理由を残した別版にし、approved-revisionでも他の段落を書換えません。18px等は条件付き試作値で、範囲外だけでfailにしません。」

GREEN for the instruction scenario: preservation remains intact, and new expression/role/source-policy guidance supplies the missing practical path. This does not prove byte extraction completeness or actual visual quality.

## 3. Zero static candidates and CSS strict offered as whole-artifact, Office and native proofreading pass

Concrete response:

「零候選は静的候補がなかっただけで、全頁passedではありません。candidate/applicable/deferredは選択結果であり実行結果ではありません。CSS strictは実際の行端・glyphの証拠にしません。artifact digestとscopeに結び付いた実施方法・証拠・環境を記録し、未実施の描畫、操作、Office原生、PDF、AT、當地校閱をnot-checked/unsupportedで別記します。schema validatorは証拠の真実性や母語校閲を保証しません。」

GREEN for the instruction scenario: the structured evidence/selection contract makes the existing false-pass safeguard explicit. No native host, Office, rendering or language pass was established.

## Outcome

Two scenarios are instruction-contract GREEN. Scenario 1 remains internally inconsistent until old workflow steps 1/5 are aligned with the v2 contract. This is the same-scenario validation, not final patch review. Baseline did not show unsafe preservation or false-PASS behavior, so the update should be described as adding missing structure and editorial/expression guidance rather than fixing three observed unsafe failures.

## Same-scenario rerun after the identified workflow correction

Re-read canonical workflow.md, regions.md, web.md and documents.md after the update. Confirmed all four generated Skills carry byte-identical copies of these four references.

Scenario 1 response now follows workflow step 1 directly: preserve unknown zh-Hant or MO, reuse metadata, do not infer written Cantonese from HK, ask only missing information that affects a specific decision, and continue neutral work. Step 5 explicitly routes v2 through context.py and the three sets, retaining rules_by_locale only as the explicit TW/HK legacy path. Web permits zh-Hant; documents names unknown/MO. The previously identified first-link contradiction is resolved.

Scenario 2 response remains: protect original sequences and punctuation, split roles and expression modes, change layout within authorization, and retain edits as a distinct proposed/adopted version. The corrected workflow step 3 preserves the same content boundary.

Scenario 3 response remains: report selection and static candidates separately from actual results, bind evidence to scope/artifact, retain not-checked/unsupported for unperformed rendering, Office, AT and local proofreading. Workflow step 6 preserves separate content, layout and accessibility checks.

Final same-scenario instruction result: GREEN for all three scenarios. This replaces the earlier provisional two-of-three outcome. It is a narrow rerun of the identified instruction conflict, not an additional whole-patch review or a rendering/host/native-language acceptance result.
