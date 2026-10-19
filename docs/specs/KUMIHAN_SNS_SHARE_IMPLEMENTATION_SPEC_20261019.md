# KUMIHAN SNSシェア機能 実装仕様書

- Document ID: KUMIHAN-SHARE-SPEC-20261019
- Version: 1.0
- 作成日: 2026-10-19（JST）
- 状態: 実装指示用仕様書。仕様書作成時点ではサイト本体への実装・公開は未実施
- 対象リポジトリ: https://github.com/landco-llc/kumihan
- 公開サイト: https://landco-llc.github.io/kumihan/
- 参照基点: main / 88fb6436ec57866aed690da3121bac9e623bc393（着手時に必ず Fresh Read）
- 実装優先度: A
- 作業方法: Codex Cloud/App の /goal 相当の単一目標で W00〜W06 を自律継続。HumanによるWork間のMD/ZIP受け渡しは求めない

## 1. 結論と実装原則

KUMIHAN公式サイトの言語ゲートウェイと各言語版ランディングページに、共通の「シェア」UIを導入する。

対応先は以下の7操作。

1. 端末・ブラウザの標準共有機能（Web Share API）
2. X
3. Threads
4. LINE
5. Facebook
6. LinkedIn
7. URLコピー

静的サイトのみで実装し、外部フォームサービス、独自送信サーバー、SNS OAuth、SNS投稿API、APIキー、データ収集サービスを使用しない。各SNSの共有画面を開き、投稿完了は利用者自身に委ねる。

**重要:** 配布スキル/プラグインの仕様変更・バージョン更新・ZIP再作成は本案件の対象外。サイトの新規UIのみを扱う。

## 2. 現行構成から確定した実装前提

2026-10-19時点のGitHub実読に基づく。

- リポジトリ: landco-llc/kumihan、既定ブランチ main、GitHub Pages公開中
- 言語ゲートウェイ: index.html と top-*.html。実際の生成元は tools/build_gateways.py、表示コピーは assets/gateway-copy.json、スタイルは assets/gateway.css
- ゲートウェイ生成の検査: python tools/build_gateways.py --check
- 日本語版ランディング: kumihan.html、en.html、zh-tw.html はJekyllレイアウト _layouts/landing.html を使用
- 複数の言語別ランディング: kumihan-*.html。多くは tools/build_*_site.py と共通レンダラー tools/product_site.py による生成ファイル
- 言語版ごとに独立した生成元・CSSが存在する。全ページが一つのテンプレートのみで生成されると仮定しない
- 言語版ランディングの一部には既にOGPがあるが、ゲートウェイにはOGP一式が存在しない
- 正式な配布物のソース、導入ページ、プレビューZIPには原則触れない

**生成HTMLの直接編集だけで終了しないこと。** 各ページの生成元を修正し、生成後チェックで再現性を確認する。

## 3. 適用範囲

### 必須・P0

- 言語ゲートウェイ全ページ。着手時点の tools/build_gateways.py の GATEWAYS 登録項目すべて
- 日本語KUMIHANの3表示言語ランディング（kumihan.html / en.html / zh-tw.html）
- 既に公開されている各言語版の製品/版紹介ランディング（kumihan-*.html、翻訳ページ *.en.html / *.ja.html 等）。生成元に変更を反映
- URLごとの共有対象はそのページ自身。トップに強制転送しない

### 本リリース対象外・P1候補

- docs/以下のインストール方法・マニュアルへのシェアUI一括追加
- GitHub README・Release・ZIP内のSNSボタン
- シェア数カウンター、クリック計測、分析タグ
- SNSアカウント連携、自動投稿、投稿成功の検知
- 常時浮遊するシェアボタン、追従UI、過剰な装飾アニメーション

新言語版が増えた際は共通生成部を再利用し、言語ごとの新たな独自実装を増やさない。

## 4. UI/UX仕様

### 4.1 画面上の位置と見た目

- 既存Heroの主CTAを妨げない、副次的な「シェア」アクションを1つ配置
- サイト全体の可読性、文字組、余白、コントラストを既存KUMIHAN基準に合わせる
- サイトの文脈上、Hero内でCTAが過密になる場合はHeroの末尾または本文とフッターの間に配置。各テンプレート内で位置を統一する
- 目立つSNSロゴ群を横一列に常設しない。ポップオーバー/開閉リストで共有先を表示
- 既存のKUMIHANらしいタイポグラフィ優先。カード、グラデーション、過度な丸角等の新設を避ける
- SVGなどのブランドロゴ追加は必須としない。まずは文字ラベルで確実に機能すること
- 固定配置、スクロール追従、共有を促すポップアップの自動表示はしない

### 4.2 操作順序

1. 利用者が「シェア」を押す
2. 小さな共有先リストが開く
3. Web Share APIが利用可能なら最上段に「端末で共有 / Share via device」等を表示
4. 次に X / Threads / LINE / Facebook / LinkedIn / URLコピーを表示
5. 利用者が選択する。対応SNSは共有画面を別タブで開く。URLコピーは現在のページに結果表示
6. Escape、外側クリック、閉じる操作でリストを閉じられる

**ネイティブ共有の優先:** モバイルでは最上段をネイティブ共有にする。共有ボタンの1回目のクリックだけで無条件にネイティブ共有を開く仕様にはしない（個別SNSボタンへの到達性を優先）。端末識別はUser-Agentでなく機能検出で行う。

### 4.3 共有成功の表現

- URLコピー成功時のみ「リンクをコピーしました」と表示
- Web Share APIのPromise解決やSNS画面表示だけで「投稿しました」「シェア完了」とは表示しない
- Web Share API の AbortError（キャンセル）は正常操作として扱い、エラー表示しない
- その他の共有API失敗時は閉じずに既存のSNS/コピー方法を使えるようにする
- 同一ページでシェアUIが重複しないこと

## 5. 共有URL・文言の規則

### 5.1 URL

優先順位:

1. 現在のHTMLの link[rel="canonical"] の絶対URL
2. canonical不在/不正時は location.origin + location.pathname

適用条件:

- https プロトコル、landco-llc.github.io ホスト、/kumihan/ 以下のパスを検証
- hashやutm等の追跡クエリ、表示切替クエリは持ち込まない
- 共有URLは訪問中の言語ページ固有のURL
- canonical / og:url / 実際の共有先URLが一致すること
- index.html と /kumihan/ はcanonicalに従って一本化
- 任意の外部ドメインのcanonicalをそのまま共有しない
- Jekyll系の相対URLや下層ディレクトリのアセットパスを壊さない

### 5.2 共有文言

- 各ページの表示言語を基準とする。ブラウザの言語設定で突然共有文言を切り替えない
- タイトル: ページの静的OGPタイトルを優先し、なければ document.title
- 本文: 各ページで短いローカライズされた紹介文を用いる。既存のmeta descriptionを代用する場合は全文の機械的切断を避ける
- 原稿、商品名、アクセント記号、結合文字、約物、RTL表記を保護。強制的なUnicode正規化や不適切な省略をしない
- Xの文字数制限とURLを考慮して短文とする。本文を長文化しない
- HTMLにmetaタグを含む場合はOGPとして事前生成し、SNSクローラが読めるようにする（JS実行だけに依存しない）

## 6. SNS別の技術仕様

| 操作 | URL/API | 値 | 備考 |
| --- | --- | --- | --- |
| 標準共有 | navigator.share({title,text,url}) | ページ固有タイトル/本文/URL | HTTPS・ユーザー操作による起動。対応がなければ項目を隠す |
| X | https://x.com/intent/tweet | text, url | /intent/tweetを使用。/intent/postに固定しない |
| Threads | https://www.threads.com/intent/post | text, url | 2026年のthreads.comを優先。投稿画面で内容を利用者が編集 |
| LINE | https://social-plugins.line.me/lineit/share | url, text | LINE公式のカスタム共有リンク。利用規約・表示ガイドに準拠 |
| Facebook | https://www.facebook.com/sharer/sharer.php | u | 本文の事前設定を保証しない。OGPからカードを構成 |
| LinkedIn | https://www.linkedin.com/sharing/share-offsite/ | url | title/summaryの事前入力を保証しない。OGPに依存 |
| URLコピー | navigator.clipboard.writeText(url) | URL | 失敗時は手動選択可能なテキスト欄を表示 |

実装要件:

- 共有先のURLは URL / URLSearchParams で組み立てる。未エンコード文字列の連結は禁止
- 外部リンクは新規タブ（target="_blank", rel="noopener noreferrer"）
- 任意の第三者スクリプト・SNS SDKをサイト閲覧時に自動ロードしない
- SNSログイン、投稿内容の手修正、最終公開は各サービスの画面に委ねる
- 各SNSのURL形式は将来変更され得るため設定を1箇所に集約
- Threadsの投稿URLは「公式APIによる自動公開」ではなく、共有用のWeb Intentである

### 6.1 URL生成の参考コード

~~~javascript
function socialShareLinks(url, text) {
  function intent(base, params) {
    const target = new URL(base);
    for (const [key, value] of Object.entries(params)) {
      target.searchParams.set(key, value);
    }
    return target.href;
  }
  return {
    x: intent("https://x.com/intent/tweet", { text, url }),
    threads: intent("https://www.threads.com/intent/post", { text, url }),
    line: intent("https://social-plugins.line.me/lineit/share", { url, text }),
    facebook: intent("https://www.facebook.com/sharer/sharer.php", { u: url }),
    linkedin: intent("https://www.linkedin.com/sharing/share-offsite/", { url })
  };
}
~~~

このコードはURL構築の参照実装であり、ローカライズ、UI、canonical検証、ネイティブ共有、コピー、エラー処理は別途実装する。

## 7. 共通コンポーネント構成

推奨ファイル（最終命名は既存構造と衝突しない範囲で調整可）:

- assets/kumihan-share.js — 共有UI、Web Share API、URLコピー、リンク生成、フォーカス制御
- assets/kumihan-share.css — 既存配色に従った最小UI、レスポンシブ、フォーカス表示
- assets/kumihan-share-locales.json — 共有ボタン、端末共有、コピー完了、手動コピー案内等のUI文言
- tools/share_ui.py — 生成スクリプトでの共通HTML/assetタグ生成ヘルパー（必要な場合）
- assets/kumihan-share-og-1200x630.png — KUMIHAN公式ロゴと既存ブランドトーンを使った共通OGP画像（存在しない場合に新規生成）
- tests/test_social_share.py 等 — 静的出力/URL/OGPの検証

### 7.1 HTMLの最小実装案

~~~html
<section class="kumihan-share" aria-label="ページをシェア" data-kumihan-share>
  <details class="kumihan-share__details">
    <summary class="kumihan-share__trigger">シェア</summary>
    <div class="kumihan-share__panel" data-kumihan-share-panel>
      <!-- 共通JSが端末共有、SNS別リンク、URLコピーを構成 -->
    </div>
  </details>
  <p class="kumihan-share__status" role="status" aria-live="polite"></p>
</section>
~~~

- HTMLの例はJA版。各言語版ではローカライズしたラベルを設定
- 必要な機能がある場合だけJavaScriptで強化する（プログレッシブ・エンハンスメント）
- JavaScript無効でも空の装飾的なシェアUIを表示しない。共有リンクの静的出力または非表示でフォールバック
- data属性は共有コンポーネント専用の名前空間とし、既存Jekyll/ゲートウェイ機能に干渉しない
- <details>利用時は標準のキーボード操作・状態を利用し、不要なARIA menuロールを付けない

## 8. OGP・SNSカード仕様

### 8.1 必須meta

公開する各対象ページのHTMLソース（head）に以下を静的出力:

- title / meta name="description"
- link rel="canonical"
- og:type = website
- og:locale
- og:title
- og:description
- og:url
- og:image （絶対HTTPS URL）
- og:image:width = 1200、og:image:height = 630（画像サイズが実際に一致する場合のみ）
- og:image:alt（各言語ページに適切な表現）
- twitter:card = summary_large_image
- twitter:title / twitter:description / twitter:image
- 既存のhreflangを保持

### 8.2 共通画像

- 基本は 1200 × 630 px PNG のOGP画像を用意し、全言語に共通使用可
- 原稿は公式KUMIHANロゴと既存サイトのブランドトーンから制作
- 既存マスター画像 assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png を素材に使う
- ロゴを引き伸ばさない。白場、トリミング、安全マージンを意識
- 「AIっぽい」装飾・派手なグラデーション・根拠のないアイコン装飾を増やさない
- 制作後にブラウザ等で実寸と視認性を確認
- SNSのクローラはJSを実行しない場合があるためOGPをJSで後付けしない
- 既に正しいOGPがあるページは既存値を尊重し、無差別な上書きや内容劣化を避ける

## 9. 多言語方針

- lang/dirと表示されるサイトコピーから共有UIの言語を解決
- ゲートウェイに存在する全言語、言語別サイトで公開中の言語をサポート
- 例: ja, en, zh-Hant-TW, zh-Hans-CN, ko-KR, th-TH, ar, hi, bn, vi, fr, es, pt, de, it, id, pl, ru
- 不足時は英語へフォールバック。未確認のローカライズは「検証済み」と主張しない
- UIラベルは短く自然な定型語で統一。社会的・商業的に誇張する紹介文を新作しない
- KUMIHANの各言語版で文字組のチェックを適用。RTLは論理CSSプロパティを使用
- URL・プロジェクト名・言語固有の結合文字やダイアクリティクスを壊さない
- スキル未検証の言語・環境はレポートに明記
- 各言語ページを共有したら、同じ言語ページに着地すること

## 10. アクセシビリティ・安全性・運用負荷

### 必須

- キーボードのみで開閉とすべての操作が可能
- フォーカス可視化、Escapeによる閉鎖、開閉トリガーへの復帰
- 音声読み上げで各リンクの共有先が区別できる
- 320px幅、CSS 200%拡大、長い言語名でも文字切れ/画面外はみ出しなし
- スマートフォンでタップ対象44×44px程度を確保
- RTL・日本語・繁体字・タイ語・デーヴァナーガリー等を確認
- reduced-motion設定を尊重
- URLに任意のJavaScriptスキームを通さない
- innerHTMLへの未検証パラメータ直挿入を避ける
- 外部ページを開く場合はnoopener/noreferrer
- SNS SDK、外部分析ツール、Cookie、APIキー、SNS認証は追加しない
- URLコピーAPIに失敗しても、選択可能なURL文字列を表示
- OGP画像と各ページはHTTPSの公開URLでアクセス可能
- ページの既存ナビ、導入リンク、ダウンロードリンクの動作を維持

### 過剰対応しないこと

- 法務画面、設定コンソール、ユーザーDB、許諾管理の新設は不要
- 認証や厳格なセキュリティ監査は不要。ただしXSS/外部リンク/機能劣化の最小確認は必須
- 再利用可能な小規模静的UIに留める

## 11. Codex実行 Work群

### W00 — Fresh Read・対象棚卸し

- mainの最新HEAD、生成スクリプト、共通テンプレート、既存テストを実読
- index/top-*/kumihan*の生成元一覧を作成
- 既存の並行開発差分と衝突しない範囲を特定
- 既存サイトのCTA、Footer、CSS/JS、SEOメタを検査
- ファイル一覧を作成し、生成物直接修正のみにならない計画を確定

### W01 — 共通UIの実装

- share.js / share.css / UI多言語辞書 / canonical解決
- 7操作の実装と外部URL構築
- Web Share API利用可否、キャンセル、URLコピー失敗のフォールバック
- JavaScript無効時の設計とキーボード/読み上げを整備
- テスト可能な依存関係のない構成にする

### W02 — 言語ゲートウェイへ統合

- tools/build_gateways.py と必要な正本の変更
- index.html、すべてのtop-*.htmlを再生成
- assets/gateway-copy.jsonは既存コピーを保持し、新しい共有UIコピーのみ追加
- CSSと見出しの衝突防止
- python tools/build_gateways.py --check PASS

### W03 — 製品/各言語ランディングへ統合

- _layouts/landing.html と tools/product_site.py で共通導入可能な経路を優先
- 個別の tools/build_*_site.py や固有ジェネレータは必要範囲だけ追加改修
- kumihan*.html系の公開ランディング各言語に1つずつシェア機能を配置
- 各言語の正本コピーファイル・生成物を整合
- スキル/プラグインの配布内容・版番号は変えない

### W04 — OGP整備

- ゲートウェイのOGP一式を静的生成
- 既存ランディングのOGP不足とcanonical/og:url不一致を補正
- KUMIHANブランドの共通OGP画像を用意し、1200×630サイズと公開URLを確認
- SNS別カードのタイトル/説明文/画像を確認
- 既存メタ情報の意味を勝手に改変しない

### W05 — 回帰テスト・公開検証

- 対象ページと生成物の差分・内部リンク・canonical・OGPを自動点検
- 可能な限り対象ジェネレータの --check を実行
- 共有先URL構築のエンコード、ロケール、フォールバックを単体テスト
- 320/390/768/1440px、200%ズーム、RTL、キーボード操作を確認
- iOS Safari/Chrome、Android Chrome、Desktop Chrome/Safari/Firefox/Edge は実機/ブラウザが使える分だけ確認。未実施は未実施と明記
- 共有画面を開けたことと投稿完了を混同しない。SNSへの実投稿は禁止
- 必要に応じて画像・HTMLソースの静的検査を実施

### W06 — PRと成果物引き渡し

- 実装差分とテスト結果を整理してPRを作成。mainへ直接push/mergeしない
- 変更ファイル、生成元と生成物の対応、実施/未実施テスト、制限事項を記載
- 既存開発との衝突、未達、外部SNSの確認限界を明記
- ユーザーに追加のMD/ZIP受け渡しを要求せず、GitHub上のコミットとPRを正本とする
- 受入判定前に公開完了と主張しない

## 12. 受入条件（Definition of Done）

- [ ] ゲートウェイの全対象ページに1つのシェアトリガーがある
- [ ] 日本語版ランディング3言語に共有機能がある
- [ ] 公開済み各製品/言語版ランディングに共有機能がある（対象一覧と除外理由が記録済み）
- [ ] SNS 5種とネイティブ共有、URLコピーの7操作が実装されている
- [ ] ネイティブ共有非対応でもSNS別共有とURLコピーに進める
- [ ] X/Threads/LINEは本文とURLを正しくURLエンコードして渡す
- [ ] Facebook/LinkedInのプレビューが有効な静的OGPに依存している
- [ ] 表示中の言語版と共有URLの言語版が一致する
- [ ] query/hashや不正canonicalを誤って共有しない
- [ ] OGPのtitle/description/url/imageが全対象ページにあり、同ページの値と整合
- [ ] 全対象ページでキーボード/フォーカス/RTL/320px/200%の基本要件を満たす
- [ ] 主要生成元の --check がPASS、変更に伴う既存テストがPASS
- [ ] 配布物、ダウンロードリンク、既存コンテンツ、Release番号を変更していない
- [ ] 自動投稿・新規SNS API権限・Cookie・追跡タグを導入していない
- [ ] ブランチ上に実装と証跡を保存し、PRを提出
- [ ] 未確認端末・SNSの制限は明示し、テスト未実施をPASSとしていない

## 13. 作業範囲の防衛

これはサイト上の配布導線を補助する小規模UI改修であり、SNS運用代行、シェア数分析、マーケティング自動化、SNS投稿予約、ユーザーアカウント管理の開発へ拡大しない。

現在並行しているKUMIHAN各言語版・スキル/プラグインリリース作業を妨げない。対象外の変更は独立した提案に分離し、勝手に同じPRへ入れない。

## 14. 参考一次資料・仕様確認先

- Web Share API (MDN): https://developer.mozilla.org/en-US/docs/Web/API/Web_Share_API
- Navigator.share (MDN): https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share
- Clipboard API (MDN): https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/writeText
- LINE share buttons (official): https://developers.line.biz/en/docs/line-social-plugins/install-guide/using-line-share-buttons/
- X post button (official): https://help.x.com/en/using-x/add-x-share-button
- Threads Web Intents (Meta公式): https://developers.facebook.com/documentation/threads/threads-web-intents
- LinkedIn share plugin (official): https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/plugins/share-plugin
- Open Graph protocol: https://ogp.me/

**注:** 共有先サービスは仕様変更され得る。Threadsは現在のthreads.com Web Intentのテキスト/URL入力を想定。ログインや地域、アプリ導入状態による差は実機検証で確認する。

---

## Codex起動文（本ファイルを読み取った上で実行）

対象: GitHub landco-llc/kumihan  
作業ブランチ: feature/sns-share-spec-20261019  
正本仕様: docs/specs/KUMIHAN_SNS_SHARE_IMPLEMENTATION_SPEC_20261019.md

この仕様書をFresh Readし、/goalでW00〜W06を一気通貫で進めてください。Parentは作業指示・結果統合・ゲート管理を担当し、実装/テストを専門Childへ委任して構いません。サイト生成元を必ず修正し、生成済みHTMLのみの手修正で終わらせないでください。KUMIHANの文字組/デザインルールを適用してください。SNS5種、Web Share API、URLコピー、OGP、多言語アクセシビリティを実装し、生成再現性と機能を検証してください。既存のスキル/プラグイン配布物や版番号を変更せず、mainへ直接マージしないでください。途中でHumanへMD/ZIPの受け渡しを要求せず、実行可能なWorkを自律継続してPR・証跡・未達一覧を最終報告してください。
