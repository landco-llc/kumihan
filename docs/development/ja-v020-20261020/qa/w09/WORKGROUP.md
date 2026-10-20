# KUMIHAN 日本語版 v0.2.0 — W09 限定組版修正・再受入 Work群

- Workgroup ID: \`KUMI-JA-V020-W09-20261020-01\`
- Owner approval: 2026-10-20 JST「推奨を承認」。直前の提案「W09の限定修正を実施した後に公開可否を再判定」を採用。
- State: \`AUTHORIZED_FOR_BOUNDED_QA_FIX / NOT_EXECUTED / NO_RELEASE_AUTHORITY\`
- Repository: \`landco-llc/kumihan\`
- 管理: [Issue #121](https://github.com/landco-llc/kumihan/issues/121), [原実装 #119](https://github.com/landco-llc/kumihan/issues/119)
- 候補: [Draft PR #120](https://github.com/landco-llc/kumihan/pull/120)（main向け）, [Draft PR #123](https://github.com/landco-llc/kumihan/pull/123)（PR #120向けのstacked QA）
- 観測時のPR #123 HEAD: \`384f073ba122abde42f5836b15650c055928e724\`
- 観測時のPR #123 TREE: \`a0a937658a24381bf2dd10012f1f977a46be3418\`
- 観測時のmain: \`8b647cc752d7a9bc3db48356fa0ab7b221bb66d6\`
- 指示正本branch: \`control/ja-v020-w09-20261020\`（上記PR #123 HEADから作成）
- 本書path: \`docs/development/ja-v020-20261020/qa/w09/WORKGROUP.md\`
- 推奨実装branch: \`fix/ja-v020-w09-20261020\`。既存同名branchがあれば実体確認・保全し、強制pushをしない。
- 実行: Codex Cloud または Codexアプリ。管制チャットから一般Codexを直接起動する必要はない。Remote Desktop経由のローカルCodex CLIは使用しない。

## 0. 結論・設計境界

今回解決するのは **Web/PDF正常例の日本語改行品質と、PPTX→PDF変換の空白・字間の再現性** に限る。ベースのv0.2.0ソース、利用可能な4スキル・6 profile・39 JA rule IDs・7既存status・既存report schema・20他言語・15配布ZIP・Universal MCPは原則変更しない。根本原因が本体レシピにあると実証された場合に限り、対象ファイルの最小修正と配布物再生成を候補として別に差分・影響を明示する。単に例を修正しただけでKUMIHANエンジン全体の改行性能向上を主張しない。

実測環境・原稿・画像を保持する。見た目の問題はスクリーンショットから確認しているが、ここに挙げる語句分断は原稿コードポイント欠落ではない。**「禁則違反」「文法的誤り」「KUMIHAN runtime破損」と推定で呼ばない。**

- Positive artifacts: 新たな原稿改変・強制1行化・隠すための縮小・過大なnowrap・不要な句読点/空白挿入を禁止。
- Historical evidence: \`qa/RESULT.md\`, \`qa/evidence/\`, \`qa/case-results.json\`, 30ケース原本・負例を上書きしない。W09の出力は \`qa/w09/evidence/\` に別保存。
- Required copy: \`髙﨑さま／料金１,２００円／が\`（濁点分解含む）、\`2026年度・特別会員向けオンライン講座の受講登録を取り消す\`、\`2026年11月3日／文字の広場（架空会場）\` とソースにある注意・見出し・表のデータ。Unicode正規化、文字置換、無断要約禁止。
- Fail status: 違反が確認されたscopeで \`failed\`; 試していなければ \`not-checked\`; 語義/意図判断が未決なら \`needs-review\`; 真正の証拠がある範囲だけ \`passed\`。負例fixtureが狙いどおりfailedであることと、製品がPASSであることは分ける。
- Existing historical baseline: 97 unittest / 29 SEO tests / 15 ZIP integrity / final-head CI success run [39370914128](https://github.com/landco-llc/kumihan/actions/runs/39370914128) は **旧HEAD \`384f07…\` に対する証拠**。W09の変更後HEADへのPASSには流用しない。
- Scope freeze: mainへのmerge、tag、Release、Pages本番公開、Marketplace申請、Universal MCP本番変更は禁止。最終Owner Gateで停止。

## W09-00 — Fresh Read / 対象固定（読取）

1. \`PR #120/#123\`、\`Issue #121/#119\`、mainとPR各HEAD、開いている関連#101/#116/#118を読み直す。staleならHEADを固定し直す。既存作業や未commit差分を保護。
2. \`docs/development/ja-v020-20261020/qa/RESULT.md\`、\`evidence/documents-result.md\`、\`evidence/web-result.md\`、\`evidence/independent-review.md\`、\`evidence/documents/measurements.json\`、関連PNG、QA-V03〜05のPR #123 reviewとIssue #121最新コメントを読む。
3. 下記の実装sourceおよび出力を照合する:
   - \`tools/qa_documents_v020.py\` → \`qa/evidence/documents/report.html\`, \`report.pdf\`, \`presentation.pptx\`, \`presentation.pdf\`
   - \`tools/qa_web_acceptance.py\` → \`qa/evidence/web-positive.html\`, \`web-320-css200.png\` 等
   - \`tools/version_display.py\`, \`tools/render_ja_v020_research.py\` は既解決QA-V01/V02を保全するだけ。再改修は新しい根拠がある場合のみ。
4. \`qa/w09/evidence/baseline.json\` に固定HEAD/TREE、ソースSHA-256、旧レンダリング・原稿digest、使用font/renderer/viewport、環境の可用性を記録。

**Gate:** source/expected/observed/unknownを区分できる。W09-01〜03は並行可能であり毎Workの承認ループは禁止。

## W09-01 — QA-V03：PDF報告書の自然な改行を限定修正

既存のPDF最終画像:
- p2: 「ありません。」が \`ありませ／ん。\` と分断される凡例。
- p2〜4: 表中 \`継続欄\` が \`継／続欄\` に分断される行が反復。
- p5: 注記 \`しない。\` が \`しな／い。\` と分断。
- 既存のPDF source（HTML）は正確で、分割は描画改行である。

作業:
1. 同一原稿、A4、20mm margin、44行継続表、必要な見出し・注記・protected fieldsで旧表示を再現。抽出の改行と画像に見える実際の折返しを別確認。
2. まず対象の\`table\`の列幅・セルpadding・font/style・テキストの収め方、凡例/注記の実幅・行送りを比較。文節・短い語句を必要箇所だけ保つ局所的なwrap候補を試す。長いセル全体の\`nowrap\`や表全体\`break-inside: avoid\`は採用しない。
3. source HTML文字列（DOM \`textContent\`）と最終PDF抽出の保護対象を厳密比較。数値・語順・原稿の文面を編集して直してはいけない。空白やゼロ幅文字・手動改行の挿入で見せかけて解決しない。
4. 同じ比較条件でBEFORE/AFTERを画像化し、全ページのページ番号、表ヘッダー反復、1〜44行、最後のnote/footnote・見出し、本文階層を検査。ページ数の自然な増減は許可するが、元6ページとの変化理由を記録。
5. \`tools/qa_documents_v020.py\` に必要なら \`--output-dir\` を追加して、新規成果物を \`qa/w09/evidence/report/\` 配下に出力し、古いQA画像/結果は上書きしない。修正により既存スクリプトの意味や生成する原稿が変わっていないことを確認。
6. 実ページ画像のテキスト行境界を記録し、\`継／続\`, \`ありませ／ん\`, \`しな／い\` 等の元問題を **その位置の実描画** で解消したか助言者/目視者が判定。単純なPDF文字抽出の改行置換は証拠としない。
7. ページ継続・過長文・フォントfallbackで新たな孤立、表示欠落、全行nowrap、本文の無断縮小を発生させない。

**Acceptance W09-01:** 新規の全PDFページ画像・コピーテキスト・page map・原稿一致と局所的な意味判断の対応。P1元箇所が残った場合は \`needs-review\` または \`failed\` とし、修正済みの認定を禁止。

## W09-02 — QA-V04：Web 320px / CSS200%の語尾・見出しを局所修正

既存 \`qa/evidence/web-320-css200.png\` で以下の改行を確認:
- \`資料を読む前／に\`（見出し）
- \`できませ／ん。\`（本文）
- \`認定しませ／ん。\`（注記）
これは厳密な禁則違反の認定ではなく、意味上の組版品質課題。

作業:
1. 現行正例 \`web-positive.html\` と \`qa_web_acceptance.py\` を同じChromium/使用書体で再現。既に修正したPV-006ボタンは退行させない。
2. 320/375/768/1024/1440 CSS px × normal/CSS200/spacing/fallbackの20状態を再試験し、少なくとも320/375 CSS200で対象の実行line boxesを記録する。可能なら200% native text zoomも別名で実施、できなければnot-checkedのまま。
3. 横余白・可用幅、見出しの幅、見出し・語尾の短い不可分範囲、送りとfontメトリクス、段落の設計を比較。誤分割が改善する最小のローカル構成にする。見出し全文・段落全体のnowrap、global \`overflow-wrap:anywhere\`、縮小による押込を避ける。
4. どの条件でも元の保護文のコードポイント、ボタンの可視性・focus・click、必須date/place/price/name、スクロール軸と可視範囲を保全。狭小画面で語を必ず不可分にできない場合は、実際の制約と代替案を提示して \`needs-review\` として残し、偽のPASSを作らない。
5. BEFORE/AFTER画像を \`qa/w09/evidence/web/\` に20状態分、視覚上の改行map・DOM exact match・overflow・使用font・renderer/buildをJSONに保存。負例 \`web-negative.html\` は意図的な失敗のまま。

**Acceptance W09-02:** 重点行頭・行末、ボタン、形と本文階層、可視必須情報を各状態で目視点検。未実行方式はPASSにしない。

## W09-03 — QA-V05：PPTX→LibreOffice PDFの抽出・字間問題を切り分ける

旧環境: LibreOfficeDev 26.8.0.0.alpha0 / Chromium 154 / PyMuPDF。 \`presentation.pptx\` のXMLにprotected stringsは完全保持。 \`presentation.pdf\` 抽出テキストは \`2026 年11 月3 日\`、\`１, ２００\` と空白を補い、最終画像slide1でも数字と和文の間が広く見える。 **「PDF抽出器が挿入した空白」「PDFコンテンツ/グリフ配置が変化」「実際のcopy/pasteが異なる」のどれかは未確定。**

作業:
1. PPTXパッケージ内の \`a:t\`/paragraphs、\`a:latin\`/\`a:ea\` と使用フォント、runの分割、文字間隔、XML原稿値を記録。保護原稿の曖昧な正規化・空白削除を行わない。
2. LibreOffice旧環境で再現し、同じPDFのPyMuPDF text/rawdict文字座標・可能な別抽出器の結果を比較する。可能ならLibreOffice安定版/別PDFレンダラー/実PowerPointを**独立した環境**として比較。使えない環境はnot-checked、推測で合格にしない。
3. PDF中のテキストオブジェクトが実際に持つUnicodeと描画glyphの字間/advanceを区別。sourceの \`1,200\` とPDF抽出の \`1, 200\` は同値扱いしない。ユーザー操作のコピーは、実操作記録が取れる場合のみ判定する。
4. 原因がPPTX側の書体設定/文字run組み立てにある場合、\`tools/qa_documents_v020.py\` の当該箇所だけ修正。source値は一字も変更せず、編集可能なshape/テキストを維持。単なる描画画像への置換は不可。
5. 再現不可かconverter固有なら「LO alphaによる限定観察・Microsoft Office native未検証・抽出不一致FAILED」を保ったまま、修正可能範囲と代替の出力経路を示す。PDFのみの抜け道でPPTXをPASSとしない。
6. 全8スライドを画像に再出力し、文字の前後間隔、図形との重なり、タイトル/本文の大小、全必要情報、句読点位置を改めて目視点検。\`slide3\` で修正済みの3カラム配置は保全する。
7. 旧PPTX・旧LO出力・新PPTX・新LO出力は \`qa/w09/evidence/presentation/\` にbefore/afterか参照リンクとdigestを並べる。

**Acceptance W09-03:** (A) PPTX source Unicode、(B) PDFテキスト抽出、(C)視覚上の字間、(D)native PowerPointの4scopeを別ステータスで提出。残ったconverter不一致を \`passed\` に昇格しない。

## W09-04 — 回帰fixture・記録分離

1. 新規検証は \`qa/w09/evidence/\` のsidecarに登録。歴史的 \`qa/RESULT.md\`, \`qa/evidence\`, \`case-results.json\`, \`docs/development/ja-v020-20261020/RESULT.md\`、原30ケースの期待と失敗を黙って更新しない。
2. 専用 \`tests/test_ja_v020_w09.py\` 等は元症状に対して先にFAILし、局所変更でPASSする設計にする。文字コード点一致、実幅・PDFページ数の整合、必要情報到達、出典画像パス有効性、必要なrecord schemaを検査。見た目を未観測なのに正規表現で \`passed\` と判定しない。
3. \`evidence-map.json\` に \`source digest/renderer/font/viewport/target region/actual observation/method/status/limitations\` と画像・抽出の対応を収録。
4. \`qa/w09/RESULT.md\` にはW09-01/02/03別の判断・修正path/未検証を記録。QA既存P1の閉鎖は実観測に限定。

## W09-05 — 最終HEAD保全・CI

1. \`git diff\` と保全台帳からQA制限外ファイルの変更が無いことを確認する。20他言語パッケージ・公開版0.1.8のRelease資産・既存JA 39規則/6profile/7status/schema、#101/#116/#118の対象は不変。
2. 既存15 ZIPは新規QAによって変わらない想定だが、raw archiveのpath/CRC/member-list/size/SHA-256を検証。何か差が出たら原因調査・停止。製品の正式source変更が必要になった場合だけ、正本 \`skills/kumihan\` からbuild_distで全ホスト再生成し、影響・hashを明示する。
3. 最終HEADで最低以下を再実行（環境欠落は未実行と明記）:
   - \`python -m unittest discover -s tests -v\`
   - \`python -m unittest discover -s tests/seo -v\`
   - \`python tools/check_ja_type_011_cases.py\`
   - \`python tools/build_dist.py --check\`
   - \`python tools/build_seo.py --check\`
   - \`python tools/check_seo_preservation.py\`
   - \`python tools/web_fonts.py --check\`
   - \`git diff --check\`
   - 実際の \`bundle exec jekyll build\`、生成公開サイトの404・非公開QA資材の除外検査。
4. 変更後の\`qa/w09\` source/evidenceが \`docs/development/\` のPagesとsitemapへ紛れないことを確認。既存QA/W09結果へのリンクはGitHubで提供。
5. 修正ブランチから \`qa/ja-v020-acceptance-20261020\` をbaseとする **新規Draft stacked PR** を作成。CIはその最終HEADで実行/読戻しする（旧緑の流用不可）。

## W09-06 — 独立レビュー・Owner Gate

- read-onlyの独立レビュアーが3課題の旧観測→変更→新観測を照合。各ページ・スライド全体の確認結果を新しい台帳に記入。対象化できない画面/環境は明示。
- 保存PPTXの正確な文字列、LO出力、PDF抽出、視認品質を混同していないか検査。必須原稿、表44行、全8スライド、3カラム整列の保全を再確認。
- \`qa/w09/RESULT.md\` に、実HEAD/TREE、diff、10個程度の重点before/after、Web20状態の評価、PDF全ページ、PPTX全8枚、版/15ZIP、最新CI URL、残るP0/P1、nativeホスト12件の状態、判断案を記録。
- [Issue #121](https://github.com/landco-llc/kumihan/issues/121) と [#119](https://github.com/landco-llc/kumihan/issues/119) に1回ずつ同じ最終結果とDraft PR URLを報告。PR #123と新PRの親子/取込み順を説明する。
- 未確認のnative ChatGPT/Codex/Claude/Gemini、native文字ズーム、Microsoft Office、実投影/サイン・読者実験を無根拠に合格扱いしない。
- **最終Owner Gate:** main merge/tag/Release/Pages更新/Marketplace/本番Universal MCPは行わず停止。残るP1を「解決」「技術的に未解決」「当該scopeを出荷対象から除外」と分け、Ownerに改めて公開判断を返す。

## W09 result contract

| Field | Requirement |
| --- | --- |
| source | previous PR #123 exact HEAD/TREE, control SHA, new W09 final HEAD/TREE |
| changes | all changed paths, purpose, protected-content digest |
| report | before/after exact PDF pages, every page inspected, 44 rows and notes |
| web | 5 widths × 4 states (20 states), highlighted 320 CSS200 and controls |
| presentation | 8-slide before/after visual and separate source/PDF-text/copy/renderer statuses |
| evidence | method, environment, font, element/region, limitations and raw artifact refs |
| tests | actual command lines, exit status, new final-head CI results, 15 ZIP hashes |
| risks | P0/P1/P2 remaining, original30 case counts separated from W09 supplements |
| Gate | proposed publish scope and explicit unverified capabilities; Owner decision needed |

**本書は実行指示であり、W09実装・再テスト完了やv0.2.0公開済みの証拠ではない。**
