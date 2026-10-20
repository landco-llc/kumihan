# W03 — 実呼出しQA / 2026-10-20 JST

対象: https://mcp-kmhn.landco.co.jp/mcp （接続済みKUMIHAN MCP connector経由）。生応答と引数は [evidence/live-mcp.json](evidence/live-mcp.json)。本番の配備commitは未特定。GitHubソースHEADとの同一性を主張しない。入力は合成例。

## 正常系5件と異常系3件

| ID | 再現引数・期待ツール | 合格条件 | 観測 | 結果 |
|---|---|---|---|---|
| P1 | list_languages({}) | count=21 | 21 / 全preview_unverified / rule_count合計749 | PASS |
| P2 | review_text(text=日本語の組版を確認します。, language=ja, medium=web) | ja明示優先、source_unchanged=true、checked=[]、visual_rendering未検証 | guidance-only / ja、期待フィールド一致 | PASS（返却契約） |
| P3 | review_text(text=文字，排版。, language=zh-Hant, medium=document) | zh-Hant明示優先、原稿不変宣言、未検証明示 | guidance-only / zh-Hant。ただしscriptsに誤ったkanaが残る | PASS（明示locale契約のみ） |
| P4 | review_text(text=مرحبا بالعالم, language=ar, medium=web) | ar明示優先、原稿不変宣言、未検証明示 | guidance-only / ar、checked=[] | PASS（返却契約） |
| P5 | get_guidance(language=th, medium=presentation, mode=review, limit=3) | guidance_only、medium=presentation | 一致、3候補返却 | PASS（取得契約） |
| N1 | get_guidance(language=xx-XX) | 未登録localeを確定扱いしない | unsupported_or_ambiguous / needs_review=true | PASS |
| N2 | get_guidance(language=ja, medium=invalid) | 不正mediumを拒否、パス・トークン・入力を漏らさない | isError=true / -32603 / Error while executing tool、機密露出なし | PASS（拒否・限定非露出） |
| N3 | detect_language(text=Hello world) | Latinだけでは言語確定しない | und / needs_review=true / source_unchanged=true | PASS |

N2は利用者向けの入力エラー区別として不十分。SDK例外とエラーコードをW02で検討し、不正UTF-8・HTTP本文長・WAF・障害時の非露出を別途試験する。上の8件のみで全異常系合格とはしない。

## 21モジュール取得スモーク

ar / bn / de / es / fa / fr / hi / id / it / ja / km / ko / pl / pt / ru / sw / th / vi / zh-Hans / zh-Hant / zu に対し get_guidance(language=<id>, medium=web, mode=review, limit=1)。全21件でエラーなし、language一致、status=guidance_only、rulesが1件。21/21 PASS。これは取得のスモークであり、現地語品質・RTL実表示・複雑スクリプトの描画検証ではない。

## 公開を止める別管制依存

detect_language(text=文字，排版。) → language=ja / scripts=[han,kana]。正しい保守的判定を満たさずFAIL。別管制の修正commit、適用版、同入力の本番回帰、関連locale/混在文字の回帰、復旧証跡を受領するまで公開No-Go。

## ソース/環境検証

`python3 -m unittest discover -s universal/tests -v`: 29件中28 PASS / 1 FAIL。test_deployment_target_is_planned_not_live が public_bootstrap_installed=false を要求し、既存target=trueと矛盾。PR #101ベースにも同じ期待値/値がある。ログはevidence/python-tests.log。PHP/Composer未導入のためPHP lint/SDK/HTTP smoke/依存auditはNOT_CHECKED。

## 未確認・次アクション

原稿不変はサーバー返却宣言とソース読解による限定証拠で、外部文書のbyte比較ではない。全媒体関連性、ルール妥当性、現地語編集、レンダリング、実登録4 Skillを用いたホスト操作、最終版の8件再実測は未完。古いテストの修正は現行状態との整合を調べてから行い、PASSにするためにtargetを未導入へ巻き戻さない。
