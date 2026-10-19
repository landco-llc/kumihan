# W09–W15 current execution status — 2026-10-19 JST

**W09–W15 implementation/review gates complete: integrated HEAD 6c4ecbf Hosted CI23/23 PASS. Draft retained / Owner Gate / DO NOT MERGE. Final evidence-only HEAD checks are recorded on PR #93.**

- Initial Fresh Read main b7a8c83 and PR accbf83; safely merged at fa9451a. During validation main advanced to `a08fd66fcb58d70dd448dfcb51745c0c91d03d4f` (PR #104 release docs), refreshed/read/merged and baseline protections updated.
- PR #100 and #102 are merged. #101 remains independent Draft/unmerged. Main now announces the already-published v0.1.8-preview; all upstream release/docs and 2609 protected distribution/skill/manifest files retained.
- P0/P1 integration: exact noindex alias handling; English root; 22 gateways/63 LP/186 guides; shared language-matched 1200×630 previews; canonical/JSON-LD/Sitemap consistency; fail-closed Jekyll share language/data checks.
- Actual inventory: **272 HTML / 271 indexable URLs**. Alias excluded; root once; no guessed pages. Static/layout body hashes255 and Jekyll source hashes21 unchanged against latest main.
- Independent review at fa9451a found one important duplicate Jekyll hreflang issue. Parent fixed it and a Hosted-CI-discovered default-language handoff at `d395e14`. SEO24/root59 PASS; push Hosted Jekyll3.10 actual output audit PASS. Initial failures remain recorded. PR CI then caught upstream README/CHANGELOG freshness; merge of a08fd66 resolves the baseline mismatch.
- Current evidence: [validation log](VALIDATION_LOG.md), [review resolution](REVIEW_REFRESH_20261019_MAIN_73D2B01.md), [independent review](INDEPENDENT_REVIEW.md), [conflict/ruling ledger](RECONCILIATION_LEDGER_20261019.md), [current inventory](BASELINE_INVENTORY.md).
- No SEO production deployment, main merge, release mutation, SNS posting/cache reset or Search Console submission. Integrated code CI23/23 PASS; final evidence-only HEAD checks must also be green on PR #93 before Owner action.

The original handoff below is preserved as historical instructions. Its NOT EXECUTED statuses, old SHA/counts and PR #102 Draft claim are superseded by this execution status and linked evidence.

---

# KUMIHAN SEO v1.0 — 英語トップ切替・新言語版統合（W09–W15）

> **Updated review — 2026-10-19 JST / main `73d2b01`:** This W09–W15 instruction has **NOT been executed**. Use the fresh critical review [REVIEW_REFRESH_20261019_MAIN_73D2B01.md](REVIEW_REFRESH_20261019_MAIN_73D2B01.md) before starting. Its P0/P1 fixes and newest main protections override older factual examples in this document. Review/WIP docs are not implementation evidence. Treat PR #100 as **already merged**, PR #101/#102 as independent Draft, and the old PR #93 20/20 as **stale for merge**. W09 must Fresh Read again.


- Created: 2026-10-19 JST
- Status: **RECONCILIATION REQUIRED / NOT YET IMPLEMENTED**
- Scope: Update existing Draft PR #93; do **not** create a parallel SEO PR without need
- PR: https://github.com/landco-llc/kumihan/pull/93
- Work branch: `feature/seo-foundation-20261019`
- Original SEO PR HEAD observed: `0cfadad8dba7aff4ca0c97c31cbdf5fa9846c8ce`
- Latest main HEAD at the second review: `73d2b01d2f604608360beabe364f59af72b8b66c` (refresh on entry); previous baseline `db14de27b4b7e8ffd298bd3ab4a940ba2a623bca`
- **Refresh both refs before the work.** PR #93 is `draft=true`, `merged=false` and `mergeable=false` at time of observation
- Prior Hosted CI 20/20 PASS applies to the **old** SEO HEAD only. It is **not** acceptance evidence for current main

## 1. Confirmed facts from current GitHub main

### 1.1 Site routes

| Role | Current page | Required SEO canonical |
| --- | --- | --- |
| Default English top | `index.html` | `https://landco-llc.github.io/kumihan/` |
| Japanese top | `top-ja.html` | `https://landco-llc.github.io/kumihan/top-ja.html` |
| Legacy English top | `top-en.html` | alias / meta refresh to new English top; `noindex`; must NOT be in sitemap |
| Other language tops | `top-<code>.html` | self-canonical on actual current path |

The current `top-en.html` file deliberately holds `<meta name="robots" content="noindex">`, refresh to `index.html`, and a canonical to `.../index.html`. Preserve its **redirect/noindex intent**. Prefer the site-root canonical if the canonical policy is changed. Do not silently turn it into an indexable second English page.

`x-default` should resolve to the English site root, not the Japanese page. Homepage `/kumihan/index.html` and `/kumihan/` must not be two sitemap entries. Update main site share generator so all URLs/OGP and JSON-LD remain consistent.

### 1.2 New content

New top languages since the prior SEO PR baseline: `sw` (Swahili), `zu` (isiZulu), `km` (Khmer), `fa` (Persian). Swahili product pages existed in the old SEO PR baseline; the other three have new trilingual products plus nine install guides each. Reflect all *actual* published paths, not guessed filenames.

From GitHub main tree at `db14de2`:

| Category | Count | Note |
| --- | ---: | --- |
| Gateway tops | 22 | `index.html` + 21 `top-*.html` excluding the legacy alias |
| Product landings | 63 | 20 products ×3 + Japanese KUMIHAN's 3-language landing |
| Install guides / docs HTML | 186 | Inspect indexability and canonical for each |
| Old redirect alias | 1 | `top-en.html` explicitly `noindex` |
| Total root/docs HTML files | 272 | 86 root + 186 docs |
| Expected indexable URLs if no other exclusion | **271** | **Do not treat this inference as an audited pass** |

New-product versions/names and language-preserving typography must follow current code sources. Read the current generator `tools/build_gateways.py`, `assets/gateway-copy.json`, footer data, product builders and doc sources. Do not invent localizations.

### 1.3 Main merged changes to protect

- PR #94: English homepage, Japanese top, shared footer, Swahili top, Vietnamese fixes.
- PR #95: Zulu edition and its package/site.
- PR #96: Khmer edition and its package/site.
- PR #97: Persian edition and its package/site.
- PR #98: copy parity for Khmer/Persian.
- **PR #99: shared language-matched previews and dedicated 1200×630 OG image.**
- **PR #100 is now merged into main** at `73d2b01`. It updates KUMIHAN core skills/plugin manifests, versioned candidate v0.1.8-preview distributions, README/CHANGELOG and design-quality rules. Treat those main files as protected latest authority and **never restore old artifacts**. PR #101 (Universal MCP) and PR #102 (rendered QA documentation) are open Draft and not part of observed main.

Other languages, style, footer, fonts and package artifacts in main must remain unchanged apart from necessary SEO metadata and integration changes.

## 2. Critical newly discovered OGP owner conflict — PR #99

Main already implements social preview logic:

- `tools/site_share.py` owns share title, localized **combined** description, locale, `og:*`, `twitter:*`, and the logo preview image.
- `assets/kumihan-share.png` is the **current** 1200×630 source image.
- Jekyll previews are generated via `_includes/share.html` and `_data/site_share.json`.
- Relevant generators, including `tools/web_fonts.py`, `tools/build_gateways.py`, `tools/product_site.py`, `tools/install_frame.py`, Vietnamese Node and special language builders, call or mirror the shared preview logic.

Old SEO PR #93 instead:
- `tools/seo_metadata.py` generates OGP/Twitter using `assets/seo-config.json` with **square** logo dimensions 1254×1254 and `twitter:card=summary`.
- `tools/check_seo.py` assumes `og:description == meta[name=description]`, which conflicts with PR #99's **localized combined** share description.
- Old SEO metadata will overwrite PR #99 previews if blindly merged.

**Integration policy: preserve the latest merged #99 behavior**, not the older square-card output. Establish one source of truth:
1. `seo_metadata.py` owns canonical, language alternate URLs, organization/webpage JSON-LD and sitemap contracts.
2. `site_share.py` owns OGP/Twitter display text, image, locale and social card output. Maintain its idempotence.
3. Implement a stable generation order/hook so **one** OGP/Twitter tag set exists. The `og:url` must match SEO canonical. Source/Jekyll output must agree. Avoid import cycles.
4. Update `assets/seo-config.json` and tests to point to the actual 1200×630 `assets/kumihan-share.png`. If SEO config no longer owns share image, remove redundant image config and have audit read the shared asset constants.
5. Replace old equality tests: validate social description against `site_share.description(lang, page_description)`, not blindly against standalone meta description.
6. Preserve original language-specific title, combined share copy, square official logo within the landscape image, source body and font behavior.
7. Existing `_includes/share.html` computes OG URL from `page.url`; reconcile so English home OG URL uses the canonical root and all pages have matching canonical/og:url/JSON-LD WebPage.url.
8. Confirm the Facebook/LinkedIn/Threads/X preview standards without claiming actual posting or indexation. **No GA4 or social tracking**.

## 3. Execution Work群 — /goal and Codex Cloud/App

### W09 — Fresh Read and safe branch integration

**追加受入:** latest main `73d2b01` (or newer) already contains PR #100 changes. Before merging, capture current versions/checksums for protected core skills, plugin manifests, `downloads *` ZIP/MANIFEST/SHA256SUMS, README and CHANGELOG. Do not downgrade v0.1.8-preview candidate artifacts or touch release tags. Confirm PR #101/#102 status without conflating them with main. Existing PR #93 will require resolving genuine conflicts; do not force push stale main content.



- Fetch latest `origin/main`, SEO PR #93 branch, merged PR #94–#99, open PR #100.
- Record refreshed SHA, ahead/behind, conflicts, all tracked site generators and HTML pages.
- Resolve main→SEO feature branch conflicts while retaining **current main body/footer/visual content** and existing SEO contract/tests. Do not force-push main or auto-merge PR.
- Do not resolve HTML conflicts by keeping old SEO-generated bodies or old `gateway-copy.json`.
- Save a source→output map and conflict resolution ledger in `docs/seo/`.

### W10 — English-first gateway and redirect

**新規P0:** main `top-en.html` is a noindex/meta refresh alias with no description. Existing SEO `enrich_html` requires description and will fail if blindly applied to the alias. Explicitly recognize allowlisted redirect/noindex pages and skip normal metadata enrichment, without suppressing missing description errors on real content pages. Add negative tests and assert the alias is NOT included in sitemap, while the root is exactly once. Canonical, OGP URL, JSON-LD and hreflang en/x-default should agree on the English **root URL**.



- Update `tools/build_gateways.py` and any shared registries to `en:index.html`, `ja:top-ja.html`.
- All 22 top pages must have correct self-canonical, language tag, 22-way reciprocal hreflang and English root x-default.
- `top-en.html` remains nonindex redirect; generated SEO adapter must skip/handle aliases without trying to require normal title/description/JSON-LD, and sitemap must exclude it.
- All internal brand/footer/dropdown and metadata links point to current main paths.
- The default homepage `/kumihan/` should have one root canonical; old `/index.html` is a valid physical file alias to same page, not a separate indexable URL.

### W11 — Cover new languages and product guides

- Integrate `sw`, `zu`, `km`, `fa` tops and `zu`/`km`/`fa` trilingual product & install guide paths.
- In addition, preserve existing `sw` product/guide coverage.
- Ensure fa RTL (direction, Unicode ZWNJ), Khmer combining clusters, isiZulu morphology and Swahili apostrophes stay byte-stable in rendered body.
- New page families must be discovered automatically without manual SEO file whitelist; existing actual `PRODUCTS`/copy source is authoritative.
- Do not regenerate or change packaging ZIPs, Plugin metadata, versions or Releases.

### W12 — Shared metadata + OGP merge

**新規P0/P1:** Main's `tools/site_share.py` is OGP/Twitter presentation authority. Never overwrite its language-matched combined description with plain meta description, its 1200×630 PNG with the old square PNG, or `summary_large_image` with `summary`. Remove duplicated ownership from `seo_metadata.py`. Jekyll `_includes/share.html` currently constructs og:url from page.url; make it consume the computed canonical, including the root URL. `_data/site_share.json` is currently a subset of language names; add detection so missing Jekyll locales cannot silently get Japanese OGP. Verify idempotency, mixed quote-attribute meta removal, one copy of every required tag, and no import cycle across seo_metadata/site_share/web_fonts/build_gateways.



- Reconcile `seo_metadata.py`, `site_share.py`, Jekyll includes/data, all Python/Node generators, special authored pages with one canonical/OGP/JSON-LD contract.
- Do not clobber language-matched preview text or replace current 1200×630 share image with outdated square card output.
- Update locales correctly (`fa_IR`, `km_KH`, `zu_ZA`, `sw_TZ` as used by current site share code). Respect existing page.lang and region variants.
- Adjust validators/tests to check correct OG description contract, not old standalone description equality.
- Verify `_config.yml`, latest footer/site_share generation and Jekyll built pages.
- Preserve existing SEO's idempotent, non-writing `--check`, and duplicate tag protection.

### W13 — Regenerate sitemap & run comprehensive checks

**追加受入:** Test separately (1) script alias missing ordinary meta description but `noindex` remains, (2) normal HTML missing description fails, (3) main #99 language-specific OG copy and landscape dimensions survive, (4) root/index canonical x-default consistency, (5) new page/Jekyll locale missing share config fails CI, (6) no edits to #100 main packaged v0.1.8-preview files. Old job outputs and documentation-only green checks are NOT integrated-code evidence.



- Run all builders and `python tools/build_seo.py` (or updated equivalent) after resolving main conflicts. Commit source and generated output together.
- `python tools/build_seo.py --check` (nonwriting)
- `python tools/build_sitemap.py --check`
- `python tools/check_seo.py`
- `python -m unittest discover -s tests/seo -v`
- Jekyll 3.10 (GitHub Pages compatible) actual built HTML audit; source-only checks are not enough.
- Re-run existing relevant language/preview/packaging prerequisite CI jobs.
- Assert `top-en.html` absent from sitemap, root present once, `top-ja.html` present once, every new language page and new product/guide included when indexable.
- Expected **271 URL** is a comparison target only; report actual audited count and explain any change/exclusion.
- Verify old site body bytes versus fresh main for pre-existing files (allow only SEO head adjustments). Preserve #99 OG preview output. 320px RTL spot checks.
- Fail on unrecognized source builders or missing metadata instead of silently hiding pages.
- Check `git diff origin/main -- plugins skills` and `*.zip` to confirm protected distributions remain unchanged.
- Verify new `guides/` directory fixture and comma-separated `robots=none` negative cases still pass.

### W14 — Update durable sources and evidence

**追加受入:** Update [REVIEW_REFRESH_20261019_MAIN_73D2B01.md](REVIEW_REFRESH_20261019_MAIN_73D2B01.md) with real resolution evidence and record the current main's PR #100 merged baseline; the previous 231-page table is historical. No invented live HTTP validation, Search Console result or Jekyll proof.



- `docs/seo/BASELINE_INVENTORY.md`: record **refreshed** page count/source map, aliases, actual languages; stop presenting 231 as current.
- `docs/seo/DECISIONS.md`: append design decisions for English-first root, alias, OGP share ownership, fa/km/zu/sw adapter.
- `docs/seo/ADD_LANGUAGE_OR_PAGE.md`: new language addition must register site_share locale/about + appropriate Jekyll data when needed; mapping from product generators to gateway. New canonical/OGP compatibility checks.
- `docs/seo/VALIDATION_LOG.md`: run commands, branch SHA, true test results, remaining limitations, and production/Search Console Owner actions.
- Append file/URL inventories and CI URLs to the PR body. Do not fabricate PASS or production deployment.

### W15 — Fresh final CI and independent review

**追加受入:** The CI must run after code reconciliation on the exact new HEAD, not just a documentation commit. Reviewer must independently check the five P0 issues documented in the 2026-10-19 refresh, and explicitly mark them resolved / not resolved. Keep Draft if PR remains merge-conflicted, stale, or checks incomplete.



- Obtain fresh Hosted CI on **new final PR HEAD**. Old `0cfadad` 20/20 PASS no longer sufficient.
- Independent reviewer inspect: correct English/Japanese URLs, 22 top hreflang group, new 3-language product groups, 271ish-page sitemap, Jekyll and pre-existing page body preservation, main #99 social previews.
- Any conflicts/FAIL remain reported, PR left Draft; do not claim merge readiness.
- After all gates pass, submit updated Draft PR #93 (same PR). Do NOT merge or publish.
- Owner Gate: only after new green CI and independent review, merge to main; then production HTTP/HTML/sitemap check and Search Console submission.

## 4. Status and immediate risk

- **Baseline verification**: old SEO HEAD `0cfadad` passed 20/20 hosted CI.
- **Current integration**: new main differs and PR #93 is `mergeable=false`.
- **Technical conflict**: new main #99 owns social card generation while old SEO PR would override that content.
- **Work completed in this current handoff**: fresh review and corrected GitHub instructions only. **W09–W15 code reconciliation, regeneration, post-reconciliation tests and new CI are NOT executed**.
- **Review status:** reviewed against main `73d2b01` after PR #100 merge; see [REVIEW_REFRESH_20261019_MAIN_73D2B01.md](REVIEW_REFRESH_20261019_MAIN_73D2B01.md).
- User must not submit an old 231-page sitemap to Search Console. Use the new version **after** a successful main merge and production validation.

## 5. Codex Cloud/App 起動文

```text
/goal
対象Repo: landco-llc/kumihan
対象PR: https://github.com/landco-llc/kumihan/pull/93
作業ブランチ: feature/seo-foundation-20261019
指示正本: docs/seo/RECONCILIATION_20261019_EN_TOP_NEW_LANGS.md

この指示書をFresh Readし、W09〜W15を自律継続してください。最新mainへの安全な整合（英語index・日本語top-ja・旧top-en noindex）、新規のスワヒリ語/ズールー語/クメール語/ペルシア語ページ、PR #99の多言語SNSプレビュー、SEO JSON-LDとSitemapを両立させてください。現在のmainの既存コピー・フッター・フォント・スキル・配布ZIPを保護し、生成元/生成物/実ビルド/CI/独立レビューを確認。古い20/20 CIは新HEADの合格とみなさない。仕上げは同じDraft PR #93に差分・証跡をまとめ、mainへマージせずにOwner Gateで停止。HumanにMD/ZIPの再添付を求めない。
```
