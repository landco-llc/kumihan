> **Source-design reference (not implemented).** Logical ports and data lifecycle, not MCP public endpoints.
> Public repository copy excludes private-source ledgers and research images. Follow the versioned JSON Schema. Do not infer permission to deploy or publish.

# 論理インターフェースの束縛・データ寿命

0.1.0-design.1 / 2026-10-20。実装対象となるAPIを確定したものではなく、02の内部portをどのtransportへ載せても守る契約を具体化する。

## 1. Port signature

```text
resolve(request: Request,
        modules: Module[],
        capabilities: CapabilityRecord[]) -> Plan | Error

plan(request: Request,
     resolved: Plan,
     measured_inputs: Observation[]) -> Plan | Error

evaluate(request: Request,
         plan: Plan,
         observations: Observation[],
         rules: VersionedRuleReference[]) -> Audit | Error
```

`CapabilityRecord`はschema内のcapabilityと、それを表明した主体・取得時点への外部参照で構成する。manifestの自己申告とObserverによる検証を区別する。`VersionedRuleReference`は識別子・版・出典・適用条件に解決され、入力URLをそのまま実行するものではない。

単一recordのJSONは同梱schemaで検査する。上記の引数集合は呼出側が束縛し、recordのIDを相互参照する。ネットワーク上で束ねるenvelope、HTTP path、MCP tool名はtransport設計時に新しい版付きschemaで定義する。本設計に仮のendpointを実在として記載しない。

## 2. 呼出し前提

request_id、contract_version、source_digests、依存rule/moduleの版が一致すること。planのIDはimmutableな版に紐付く。同じIDの内容を書き換えない。生成候補をやり直す際は新IDと前版参照をtransport側の管理記録に持つ。

すべての`origin_ref`、`artifact_ref`、`font_ref`、`evidence_refs`は識別子である。任意URLをサーバーが取りに行く命令ではない。信頼境界内のresolverが利用者の権限・対象範囲・取得方法を確認して解決する。

## 3. 操作の意味

resolveは適用規則と不足の整理まで。planは表示候補を返すだけ。evaluateは対象を変更しない。いずれも`apply`・`publish`・`translate`操作を含まない。自動修正を将来追加する場合は明示承認・対象範囲・原稿差分を持つ別契約にする。

LLMによる意味改行の判断はassistedとして記録する。文字境界・hash・静的構造の検査はstatic。実hostの画像・geometryを観測した場合のみrendered。言語の自然さをモデルだけで判断したものを独立した母語校閲manualに格上げしない。

## 4. Script解析の位置付け

source範囲へのlanguage_runsは意味メタデータ。UnicodeのScript/Script_Extensionsの解析結果は処理系が別に導出し、使用したUnicode版とともにObservation.factsへ保存する。後者はlanguage_runsを上書きしない。Common/Inheritedを伴う解析に必要な周囲の文字も保持する。

この設計版ではscript解析を依存ライブラリに委譲し、その構造をコアrequestの必須配列にはしていない。高性能な共有キャッシュが必要になった段階で、rangeとUnicode版を持つ専用の版付き観測型を追加できる。言語推定結果をScript解析の代わりに使わない。

## 5. 単位と値

Plan.decisionsのvalueは汎用JSONだが、propertyを解釈するadapterがそのproperty schemaを持つ。例えばfont-sizeは`{"value":18,"unit":"css-px"}`、印刷字級は`{"value":11,"unit":"pt"}`と区別する。line-heightは無単位倍率と絶対長を別にする。viewportはCSS px、画像はdevice pixel、紙はmm/ptを識別し、DPIやzoomのない単位変換をしない。

コアはすべての媒体のpropertyを固定列挙しない。未知propertyは適用せず、必要能力と対応状況を返す。style valueの文字列をCSS/スクリプトとして無検査で実行しない。geometryの制約やunitsの型はadapter schemaで検証し、schema通過とhost適用成功を別に扱う。

## 6. 原稿の送信・保存

共通契約を利用するだけでは、原稿を外部へ送る必要はない。ローカルスキルはローカルに保持でき、MCPでは処理に必要な最小範囲だけを送る設計にする。cloud / localの配置で必要なデータが変わるため、送信範囲はtransport実装時に明示する。

推奨既定は、原稿を永続キャッシュやアクセスログへ自動保存しないこと。evidenceの保存が必要なら対象・保管先・権限・保持期間を明示する。本文のhashも短い機密原稿では推測の手掛かりとなり得るので、匿名情報であると断定しない。private Drive IDや内部承認参照を公開配布ルールへそのまま含めない。

公開版に利用者固有・非公開のDrive識別子や内部承認参照を含めない。研究正本の非公開情報はGitHubへ転記しない。

## 7. 資源と運用負荷

共通基盤にブラウザ・Office・font描画処理をすべて同居させる必要はない。軽量なルール解決と重いhost検証を分ける。全言語の辞書や全フォントを毎回読み込まず、要求範囲と宣言能力で選ぶ。fontファイルをこの研究パッケージやプラグインへ無断同梱しない。

timeouts、入力サイズ、候補数、再試行上限はhost側の宣言値として返す。処理が途中なら範囲を記録し、結果を全件確認へ広げない。既存のPHP/ホスティング構成を変更することや、有料API契約を追加することは今回の設計から自動的には発生しない。

## 8. 適合表示

「入力受入」「ルール提供」「静的検査」「対象host描画」「母語レビュー」「アクセシビリティ確認」を別々に表示する。MCP registryに言語が載っていることだけで、その言語のすべての組版機能を満たすという表示はしない。

規則・辞書・font・hostが更新された場合、影響する検証だけを再試験する。対象のdigestと条件に結び付かない過去の合格は再利用しない。
