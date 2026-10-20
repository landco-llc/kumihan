# KUMIHAN Universal — OpenAI公開申請管制

状態: `PUBLICATION_PRE_SUBMISSION_HOLD`。最新指示は [publication-20261020/START_HERE.md](publication-20261020/START_HERE.md)。

## 2026-10-20 JST 照合

- 制御文書から継承: L&Co. LLC法人認証済み、ZIP登録済み、4 Skill Checks passed、Domain verified。再申請・再登録・再検査しない。今回Platformへのアクセスがなく、現画面の独立読戻しは未完。
- 既存4 Skill: kumihan-start / kumihan-web / kumihan-documents / kumihan-review。
- GitHub main 8b647cc、Draft PR #101 d3dff4e、未マージ。
- 接続済みMCPから21モジュール/749ルールを実測。全件preview_unverified。文字，排版。の自動判定はja/kanaのままFAIL。別管制へ留保。
- サイト/Privacy HTTPS 200。Privacyは静的Skill中心でMCP運用と不整合。terms.htmlは404。
- 過去の明示的Findings: Terms of service URL is required. / Incomplete review information。最新スキャン最終結果はNOT_CHECKED。
- 現登録ZIPの実体・SHA未取得。旧DRAFT_r02（1 Skill）をアップロードしない。
- 法務公開、本番MCP変更、審査提出、一般公開の各Owner Gateは未承認。NO-GO。

## 過去記録（現行実行手順ではない）

以下は引き継ぎ前の記録を監査用に残す。未アップロード・未認証・1 Skill・認証や登録の実行を促す記述は失効し、上記照合とSTART_HEREを優先する。再実行しない。

# KUMIHAN Universal — OpenAI public Plugin submission track

## Scope and authority

- User explicitly requested public ChatGPT plugin publication as **L&Co. LLC**. Use the OpenAI Platform public plugin submission portal, not personal private-plugin creation.
- Separate automatic-language-detection fix is **OUT OF SCOPE for this publication chat**; handoff: [`HANDOFF_LANGUAGE_ROUTER_OTHER_CONTROL_CHAT.md`](HANDOFF_LANGUAGE_ROUTER_OTHER_CONTROL_CHAT.md). Do not deploy router changes from this track.
- Do not merge PR #101 or publish public directory listing before review approval and explicit Owner release gate.

## Operator-prepared ZIP, not yet uploaded

- Name: `KUMIHAN_Universal_ChatGPT_Public_Submission_v0.1.0_DRAFT_r02.zip` (ChatGPT conversation attachment, not committed to repository).
- SHA-256: `55fc968145176759cbf5d6106a2e1a2ea45833ad8a69b6b28a49da64d460348f`.
- Structure: portable root `plugin.json`, `mcp.json`, one `skills/kumihan-universal/SKILL.md`, 21-language info snapshot, two resized official KUMIHAN favicon-based square assets and Apache-2.0 license.
- Publisher in package: `L&Co. LLC`; Platform organization visible as L&Co. LLC, but **Business Verification status not yet evidenced**.
- MCP endpoint: `https://mcp-kmhn.landco.co.jp/mcp`, public TLS1.3.
- Review cases: five positive and three negative, included as **drafts** (test every case before submitting).
- `publication.countries=[]` represents no country restrictions; EN primary listing, JA translation.

## Evidence and gaps

- User earlier reported ChatGPT directly connected and listed 21 modules / 729 catalog rules. Live KUMIHAN MCP `kumihan_list_languages` currently returns 21 modules whose per-module `rule_count` values sum to **749**, not 729. Reconcile after controlled server changes; package notes current snapshot and avoids promising fixed totals in listing.
- Website `https://landco-llc.github.io/kumihan/` was HTTP 200; privacy `https://landco-llc.github.io/kumihan/privacy.html` was HTTP 200, but its current text describes static skills/plugins and explicitly says it will be updated before introducing a hosted MCP. **Update privacy before review submission** to explain user-text handling, hosting, logs/retention, external processors and contact channels based on actual implementation.
- Support link `https://github.com/landco-llc/kumihan/issues` was HTTP 200. It is a public issue tracker; advise users not to put personal data in public issues. Consider a dedicated private corporate support channel.
- **No publicly accessible Terms of Service** was verified; `/terms.html` and `/terms-of-service.html` both returned HTTP 404. Do not invent a terms URL or repurpose the Apache-2.0 LICENSE as service terms.
- Live MCP tool metadata currently does **not** advertise explicit `readOnlyHint`, `openWorldHint` or `destructiveHint` annotations. All four tools appear read-only from code behavior, but changes must be made on server and validated with portal `Scan Tools` before reviewer submission.
- No public video walkthrough URL is known; OpenAI requires demo recording for initial MCP review.
- Domain verification token must come from the portal and be placed verbatim at `https://mcp-kmhn.landco.co.jp/.well-known/openai-apps-challenge`. Do not pre-generate token or commit it.
- The full FTP `/web` symlink scan was permission-limited; scoped `kmhn` check PASS and Owner manually reviewed all host mappings. This limit remains NOT_CHECKED, not PASS.
- Pricing: free, open-source Apache-2.0. Hosted read-only endpoint currently anonymous, without per-user rate limits; need abuse and logging policy before full release.

## Next operator steps

1. Open `https://platform.openai.com/plugins` in Organization `L&Co. LLC` and verify Business Identity selected (not implied by org title alone). Ensure Apps Management Write or org-owner status.
2. Click `Upload new or existing plugin`, select verified Developer Identity, upload ZIP `...DRAFT_r02.zip` and save as draft. **Do not submit for review yet.** Public portal upload may show required-field findings; copy errors exactly.
3. Check `Metadata & Skills` automated findings, resolve package issues with a replacement ZIP.
4. `MCPs` → `Connect` with Universal fixed URL + None auth; complete domain verification challenge and `Scan Tools`, verify 4 tools, schema and annotations.
5. Publish correct privacy and approved terms URLs; upload corrected ZIP, review positive and negative test cases and a demo recording URL, verify corporate identity.
6. Only after all blockers pass, complete attestations → `Submit for review`. Publish after approval and a separate Owner release decision.

Official docs: https://developers.openai.com/plugins/deploy/submission and https://developers.openai.com/plugins/deploy/submission-errors.
