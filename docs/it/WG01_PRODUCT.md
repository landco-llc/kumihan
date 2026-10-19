# WG01 — Equilibrio core / 4 Skills（W00–W03）

Parent: [GOAL_EQUILIBRIO_V010.md](GOAL_EQUILIBRIO_V010.md)。完了時は確認質問を挟まずWG02へ進む。

## W00 Fresh Read / scope
- main HEAD・他言語PR・CI・Release状態をfresh read。AGENTSやローカル指示があれば適用、conflicting changesはrebase。現時点の正本docs/it/ITALIAN_RESEARCH_20261019_JA.mdを実読する。
- 現行のFrench/Spanish/German/Polish版の実装とその最新差分、toolsの生成器/共通コピーを照合。新規言語 edition のみを追加。既存ZIP/タグ/manifestは変更しない。
- 40規則/48提案fixtureを実装対象、設計判断、未実装判定、実測対象に分類し、採用予定と検証可能性をledgerに記載。

## W01 Locale / scope / evidence
- tech slug: kumihan-equilibrio、product folder: plugins/kumihan-equilibrio。4 skillsは独立したSKILL.mdと同梱のlocale/rules/referenceで成立。
- locale=it-ITを基準。it-CHやhouse-style（EU・連邦官房・出版社等）を別の設定軸にする。language, medium, content_role, house_style, source_policy, intended audience, evidenceを別フィールドとして保持し、未指定を勝手に確定しない。
- 音節分割/分綴・ウェブ描画・読み上げを静的判定と混同しない。CSSだけ、辞書なし、実機未確認ならstatus not-checked。美的提案はproposal、断定できない文法はneeds-review。
- 生成レポートにrule id、reference、scope、before/after proposal、edit permission、status、observed environmentを残す。

## W02 Grammar / typography / source protection
- 主なA順位: é/èと大文字、perché、caffè、qual è、po’、文脈依存e/è・da/dà・si/sì、正式固有名と外国語を守る。
- quote styles: caporali/英式二重/原典忠実の複数方式を許す。アポストロフィ直後の本文折返しは許容（Crusca）しerrorにしない。見出しでは意味上の改善案として示せる。ハイフン・ダッシュ・範囲・負号を役割で区別。
- フォント/見出しはaccent glyphやfallbackと文字拡大を確認。意味を保持し、単語切断を目的としたbreak-all/overflow hidden/段落nowrapの乱用は避ける。styleを「イタリアらしい固定配色」へ一本化しない。
- 数字・価格・単位・date/timeに暗黙型推定や再解釈をしない。元値を保持して、明示的なデータ型とlocale/house-styleで表示層だけフォーマット。
- Unicode NFD/NFC、コード、URL、JSON、ISBN/ID、名称、引用、商標、署名等のbyte-preservation例をfixtureに含める。reviewは絶対に書込みしない。

## W03 Skills / manifests / light QA
- 4 Skills: kumihan-equilibrio[-web|-documents|-review]。entrypointsや各SKILL.md frontmatterは技術slug + IT | ENの説明。referencesとrules/sources/locales/fixtures/testは参照が外へ漏れない閉包。
- Product rootの plugin.json, .claude-plugin/plugin.json, .codex-plugin/plugin.json, gemini-extension.json, GEMINI.md, entrypoints, license, README, referencesを構築。人間向けプラグイン表示名は KUMIHAN｜Equilibrio の完全一致、version=0.1.0、developer L&Co. LLC、公式PNG参照。
- オフラインのread-only helperは必要最小限。元入力とcandidateを比較・報告するだけ。辞書検証していない綴りをregexで誤修正したと宣言しない。
- 代表ケースを先に実装し、研究48 fixtureの各評価状態を記録。少なくとも16の保護/正例/反例をfocused testsに含める。実行していないfixtureのstatusをPASSにしない。
- docs/it/EXECUTION_LEDGER.mdへW00-W03のpath、SHA、tests実行条件、PASS/FAIL/NOT-CHECKEDを記録。

Done gate: 4独立Skill実体、IT localeと編集方針の区別、原稿保護契約、plugin metadata、軽量core tests。サイトを作らずWG02へ。
