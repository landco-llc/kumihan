# WG02 — 3ホスト配布・15 ZIP（W04–W06）

Parent: [GOAL_EQUILIBRIO_V010.md](GOAL_EQUILIBRIO_V010.md)。WG01の製品/4Skill完成が前提。終端ではWG03へ自動進行。

## W04 Host adapters / official branding
- ChatGPT/Codex: portable agent plugin (.codex-plugin + plugin.json / schemaに合うinterface)。Claude: .claude-plugin/plugin.json。Gemini: gemini-extension.json / GEMINI.md。既存 kumihan-satzbild と他言語の生成器をfresh readし、現時点のHost仕様に合わせる。
- displayName等のユーザー向け欄は KUMIHAN｜Equilibrio のみ。technical nameは kumihan-equilibrio、versionは0.1.0。全description, shortDescription, longDescription, Skill frontmatter descriptionは意味の対応するItalian | English。author/developerは L&Co. LLC。
- assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png を各対応ZIPに配置しmanifestの相対パスから参照できること。PNG digestのcanonical一致、ZIP破損なし。native UIのアイコン表示は未検証ならnot-checked。
- 他言語製品や海外のプラグインマーケットへの登録・公開・権限変更はしない。

## W05 15 archives / deterministic metadata
- 各hostグループに plugin/extension 1 と standalone skills 4、計5ずつの3群＝15 ZIP。すべて -v0.1.0.zipで終える。例えば:
  - kumihan-equilibrio-GPT-Codex-plugin-v0.1.0.zip
  - kumihan-equilibrio-Claude-Code-plugin-v0.1.0.zip
  - kumihan-equilibrio-Gemini-CLI-extension-v0.1.0.zip
  - kumihan-equilibrio-web-Claude-skill-v0.1.0.zip
  - kumihan-equilibrio-review-Gemini-Apps-skill-v0.1.0.zip
  全ファイルはbuilderで一意生成、絶対pathや相対逸脱なし。
- tools/build_equilibrio.py を作り、offline・決定論的順序、固定ZIP timestamp/permission、UTF-8、必要最低限の同梱でbyte-identical。--checkはファイル非書込。入力のsymlinkやパストラバーサル、未同梱reference、欠損fileを拒否。
- plugins/kumihan-equilibrio/downloads/に15ZIP＋MANIFEST.json＋SHA256SUMS.txtを保存。MANIFESTにhost/filename/byte length/digest/member summary/official logo/reference checks等。SHA256SUMSは15ZIPとMANIFESTをカバーし自己hashを含めない。
- 4 standalone skills×3ホストに各SKILL.mdとローカルassets/rules/fixtures/locale/sources/licenseの参照閉包を構築。各ホストのinstall手順は実際の製品適合先のみ示す。
- README/INSTALL/UPDATES/LICENSE/THIRD_PARTY_NOTICESに無料・オープンソース・ライセンスと対応範囲、実Install手順、native-host未確認事項を明記する。ChatGPT plugin登録成功・公式Marketplace掲載とGitHub ZIP公開を混同しない。

## W06 Focused QA / distribution gate
- tests/equilibrio/ 以下へ構文、metadata、displayName、IT/EN description、4 skills closure、15 ZIP、CRC、path、SHA、--checkの非書込、icon実体とdigest、研究ケースと原稿保護、locale独立などのfocused testsを追加。
- 研究40規則は規則候補として配置できても全てを自動検出実装と主張しない。48 fixtureは全件を ledger に取り込んでも、未実行はnot-checked、手動判断はneeds-reviewを保持。
- Python/Node等の実行版を固定記録。it-IT/it-CHのIntl baselineは正本調査に記載したNode24/ICU78.3/CLDR48との環境差を容認し、無条件の定数比較を避ける。NFC/NFDとURL/引用/数値のbyte preserving testsを含める。
- 関係する既存日本語版/他言語の回帰と、この変更で既存配布物のbyte digestが変わらないことを軽く確認。Native Hostが使えない場合はstatic PASSだけを報告。
- docs/it/EXECUTION_LEDGER.mdにW04–W06の成果物と実tests/数/digest/environment/NOT-CHECKEDを記録。

Done gate: 4実体skills、3 adapter、15 ZIP、MANIFEST/SHA、配布内容の検査PASS、重要blockerなし。**完了前にWeb制作禁止**。
