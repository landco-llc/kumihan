# KUMIHAN｜अक्षर-संगति v0.1.0 検証

2026-10-19 JST。Source of truth: docs/hi/GOAL.md / plugins/kumihan-hi / tools/build_hi.py / tools/build_hi_site.py。

- Python 3.12 stdlibで15 ZIPを2回生成し全byte一致。15 ZIP内の4独立Skill/host固有manifest/参照/icon/相対path/size/SHA256を確認。
- Hindi focused 8件、既存root 11件、compasso8件、accord26件、arabic20件、grafia13件、計86件PASS。既存build_dist 128生成物、共通copy/gateway、JA-TYPE-011 11fixtureも確認。
- Chromium 154.0.8037.57、12ページ×320/768/1280px×通常/文字200%/4種spacing同時上書き/webfont失敗 =144観測、修正後overflow 0。文字200%はcomputed font-sizeを2倍にする方法。ブラウザUI zoomとは別。
- 19文字fixtureはDOM原文とUTF-8一致。source byte変更を検出し、NFC同値を原稿一致と扱わない。ZWNJを含むSegmenterの実測境界はqa-results.jsonを参照。
- Q20 PDF抽出は17/19文字列が完全一致、2件不一致。PDF視認/抽出/編集可能原稿は独立した確認。製品にPDF変換保証はない。
- 24 QAは計画・静的・render・operation・native-speakerを個別記録。全24件PASSとは扱わない。
- ja/en gateway×3幅でカード同一寸法、全言語の展開、Hindiリンク、会社リンクtarget=_blankを確認。
- 独立read-only reviewerは梱包、manifest、byte保持、copy、リンクに重大ブロッカーなしと報告。

実ホスト導入、母語校正、Office、Android/iOS、Safari/Firefox、IME/削除、スクリーンリーダー、ブラウザUI zoomは **NOT_CHECKED**。新Hindiコピーは未校正案。限定的な静的・描画検査からWCAG適合、完全な文法・字形保証、公式marketplace承認を表明しない。

公開結果・全12 URL・ReleaseはPUBLICATION.mdで記録する。
