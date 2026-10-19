# PUBLISHED — KUMIHAN｜अक्षर-संगति v0.1.0

公開検証: 2026-10-19 JST。実装main SHA `5b7057366621ace37fd36185450bfe0d7282846c`。

実装PR [#71](https://github.com/landco-llc/kumihan/pull/71)、公開経路PR [#73](https://github.com/landco-llc/kumihan/pull/73) はmerge済。

タグ/Release: [kumihan-hi-v0.1.0](https://github.com/landco-llc/kumihan/releases/tag/kumihan-hi-v0.1.0)。タグは上記実装SHAを固定し、以後の公開記録・workflow修正で移動しない。

## 公開ページ（全12 URLがHTTP 200）

- [kumihan-hi.html](https://landco-llc.github.io/kumihan/kumihan-hi.html)
- [kumihan-hi.en.html](https://landco-llc.github.io/kumihan/kumihan-hi.en.html)
- [kumihan-hi.ja.html](https://landco-llc.github.io/kumihan/kumihan-hi.ja.html)
- [docs/install-kumihan-hi-chatgpt.html](https://landco-llc.github.io/kumihan/docs/install-kumihan-hi-chatgpt.html)
- [docs/install-kumihan-hi-chatgpt.en.html](https://landco-llc.github.io/kumihan/docs/install-kumihan-hi-chatgpt.en.html)
- [docs/install-kumihan-hi-chatgpt.ja.html](https://landco-llc.github.io/kumihan/docs/install-kumihan-hi-chatgpt.ja.html)
- [docs/install-kumihan-hi-claude.html](https://landco-llc.github.io/kumihan/docs/install-kumihan-hi-claude.html)
- [docs/install-kumihan-hi-claude.en.html](https://landco-llc.github.io/kumihan/docs/install-kumihan-hi-claude.en.html)
- [docs/install-kumihan-hi-claude.ja.html](https://landco-llc.github.io/kumihan/docs/install-kumihan-hi-claude.ja.html)
- [docs/install-kumihan-hi-gemini.html](https://landco-llc.github.io/kumihan/docs/install-kumihan-hi-gemini.html)
- [docs/install-kumihan-hi-gemini.en.html](https://landco-llc.github.io/kumihan/docs/install-kumihan-hi-gemini.en.html)
- [docs/install-kumihan-hi-gemini.ja.html](https://landco-llc.github.io/kumihan/docs/install-kumihan-hi-gemini.ja.html)

## 配布物と検証

Releaseに15 ZIP＋SHA256SUMS.txt＋MANIFEST.json。全17assetのremote API size/SHA256とローカル再現ビルドが一致し、全asset URLがHTTP 200。内部24resourceもHTTP 200。全asset名・size/hash・URLはpublication-results.jsonに記録。

自動テスト92件（Hindi8/root11/compasso8/accord26/arabic20/grafia13/nhip-chu6）。Chromium144条件で修正後overflow 0。最終gatewayはHindi/Vietnameseを含む11カードを6画面条件で同一寸法・normal Hindi tracking・overflowなし。Claude/Gemini CLI validators PASS。

24 QA全体のPASSとは扱わない。PDF抽出は17/19文字列が完全一致し、Q03/Q09に差がある。編集可能原稿を正本とし、PDFからの再利用を保証しない。

母語校正、モバイル実機、Office、IME/削除、支援技術、Safari/Firefox、ブラウザUI zoom、実ホストモデル呼び出しはNOT_CHECKED。新Hindiコピーは未校正案。

## 公開経路の実測

Cloudからuploads.github.comへの直接uploadは接続先制限で失敗。GitHub Actionsは全17assetをdraftへuploadできたが、draftをtag endpointで取得する段階で404となった。authenticated release IDで全size/digest一致を確認して公開APIを実行し、その後全URLを実確認。workflowはdraftも取得できるauthenticated listへ修正し、既存public/添付済assetは上書きせず検証だけを行う。

詳細: [VALIDATION.md](VALIDATION.md)、[WORK_LOG.md](WORK_LOG.md)、browser-results.json / qa-results.json / host-validation.json / publication-results.json。
