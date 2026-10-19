# WG01 — Satzbild 製品本体、ドイツ語ルール、独立4 Skills

Part of [GOAL_SATZBILD_V010.md](GOAL_SATZBILD_V010.md)
Execution order: W00 → W01 → W02 → W03。W03完了後は自律的にWG02へ進む。品質確保を理由に無関係なコードや共通フレームワークを大改変しない。

## W00 — Fresh Read / scope lock

- 最新 main と実際の branch HEAD、AGENTS.md／repoルール、既存4 Skills・各言語のパッケージングを実読。
- 参考実装は最も新しい品質確認済み独立版を選ぶ。現行の plugins/kumihan-grafia と tools/build_grafia.py、plugins/kumihan-compasso、tools/base_copy.py を比較。古い設計の非互換をコピーしない。
- 他言語成果物のdigestと現行stateを固定。並列他言語PRを見て対象外の変更を避ける。
- docs/de/EXECUTION_LEDGER.md に BASE_SHA、Work、入力参照、採用ディレクトリ、環境、done/not-checkedを記入。
- 日本語版にある共通目的・原稿保護・品質検証・anti-generic AI designを継承し、ドイツ語固有規則を共通JA rulesに混ぜない。

## W01 — de-DE / de-AT / de-CH 設定とルール

ルール原本の候補44件・fixture候補48件は [RESEARCH_RULES_V010.md](RESEARCH_RULES_V010.md) を利用。外部の文面やフォントファイルを無断取り込みせず、参照URLと仕様の版を持つ独自の要約・テストだけ実装する。

- plugins/kumihan-satzbild 内に自己完結の locale/resolver、rule catalog、evidence/source index、media profiles、fixture ledger、必要な JSON Schemaを整備。
- locale defaults: de-DE, de-AT, de-CH。ただし country によって通貨・timezone・呼称・ハウススタイル・政治的表記・フォントを勝手に決めない。既存データ・利用者の明示設定を優先。
- typesetting_only/proofread/rewrite、Web/editorial/UI/report/presentation/displayの媒体を区別。reviewモードは必ず非破壊。
- 正書法: ß、ẞ、SSの変換禁止。スイス標準ドイツ語のssは地域的な設定として扱い、固有名/ブランド語彙や明示原稿は変更しない。
- 文字: äöü、ÄÖÜ、結合文字、開閉引用符（DE/ATの„“・CHの«»と許容別形式）、引用入れ子、ダッシュ、アポストロフィ、SI数値・単位、長い複合語、任意分綴を扱う。既存文字を暗黙のNFKCや一括正規化で書き換えない。
- Content/data: prices, decimal values, dates, timezone, IDs, German+English mixed content を source protected。Intl runtimeの値と編集ハウススタイルを区別。
- du/Sieとジェンダー表記、Leichte Sprache（専門的検証なしに適合とは宣言しない）、地域語 Jänner 等は policy/locale候補であってオートリライト対象ではない。
- ルールごとに ID, source_ref, authority_type, impact, scope, recommended_action, machine_check, render_check, editorial_review, exception を最低限明示。
- 44件を記録したことと静的checkerが実装済みであることを厳密に分ける。checkerは偽陽性が小さい選定例のみ。任意の正書法全面訂正エンジンは作らない。

## W02 — 四つの自己完結 Skills

- skills/kumihan-satzbild/SKILL.md — 入口。文脈/権限/locale/媒体/保護原文を設定。
- skills/kumihan-satzbild-web/SKILL.md — Web・LP・UIのリフロー、長語、ハイフネーション、アクセシビリティ。固定文字数を全媒体へ強制しない。
- skills/kumihan-satzbild-documents/SKILL.md — Word/PDF/スライド、ページ・表の見切れ、文字保持。
- skills/kumihan-satzbild-review/SKILL.md — 変更しないレビュー。static/render/editorialと根拠・未検査の区別。

各SKILL.md:
- frontmatterのtechnical nameはASCII。descriptionは独語と英語だけ、両方が同じ機能を示す。
- 見出しに正式ブランドKUMIHAN｜Satzbild、導入できる範囲と限制約。内部 links/references/rules/schemaが4つそれぞれのSkill配布ディレクトリ内で閉じる。
- 実ファイルの仕様・Hostに非対応な操作はツール呼出可のように書かない。
- design contract: 読者と目的、情報構造・視線誘導、書体/余白の理由を持たせる。Hero→3 cards→CTAの無理由反復、架空実績、架空数字、意味のない装飾を避ける。カードやグラデーションを一律禁止せず理由による。
- typography-onlyでは原稿やブランド名を変更しない。変更可能な場合はbefore/afterの明示diffと確認。
- 原稿保護・not-checked / needs-review / failed / passedの状態は共通方式。

### メタデータ草案（自然な表現に校閲して採用）

- Plugin DE: „Offene KI-Skills für deutsche Typografie und durchdachte Gestaltung – mit Schutz des Originaltexts und nachvollziehbarer Prüfung.“
- Plugin EN: “Open-source AI skills for German typography and purposeful design, preserving original content and providing evidence-based review.”
- Entry DE: „Projektziel, Sprachvariante, Medium und erlaubte Änderungen klären, ohne Inhalte ungefragt umzuschreiben.“
- Entry EN: “Define purpose, German locale, medium, and authorized edits without silently rewriting content.”
- Web DE: „Deutschsprachige Websites und Oberflächen mit lesbarer Typografie, sinnvollen Umbrüchen und begründetem Design gestalten.“
- Web EN: “Design German websites and interfaces with readable typography, considered line breaks, and purposeful layout.”
- Documents DE: „Deutsche Berichte, Dokumente und Präsentationen lesbar setzen und ohne Inhaltsverlust prüfen.“
- Documents EN: “Typeset German reports, documents, and presentations for readability while preserving their content.”
- Review DE: „Deutsche Texte und Layouts auf Typografie und Lesbarkeit prüfen, ohne die Originaldateien zu verändern.“
- Review EN: “Review German typography and layouts for readability without changing the original files.”

## W03 — 製品manifest・軽量チェック・引継ぎゲート

- plugin.json、.claude-plugin/plugin.json、.codex-plugin/plugin.json、gemini-extension.json、GEMINI.md、四つのSkill metadataを整備。Codex実行時点の各Host仕様が優先。
- 表示名全箇所は厳密に KUMIHAN｜Satzbild。technical slugは kumihan-satzbild。authorは L&Co. LLC。version 0.1.0。URLは予定地 kumihan-de.html を指定。
- 公式ロゴパスは既存 assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png。必要なロゴを配布構成へ後続WG02でコピーし、各manifestパスを検査。
- 必要なら小さな offline read-only checker だけ実装。データ差分・保護原稿と設定逸脱を観測し、機械判定不能な美的/言語判断はneeds-reviewへ。過大な「自動修正」は入れない。
- 代表ケース（少なくとも15件）として ß/ẞ/SS、CHの固有名、複合語、引用符入れ子、メール/URL、数値と単位、locale指定、長UIラベル、許可外書き換え防止、ソースのbyte preservationをテスト。
- 独立Skill4種のリンク閉包とmanifest構文を検査し、docs/de/EXECUTION_LEDGER.mdへ W00-W03 result, test command, status, commitを記録。
- この時点ではサイト制作に着手せず、WG02の15 ZIP構築・検証へ進む。

WG01 Done gate: 4独立Skill実体＋地域ルール基盤＋manifest原本＋検証証拠が存在。調査候補44/48を全検出済と誤表示していない。
