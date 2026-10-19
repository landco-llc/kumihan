# KUMIHAN SEO v1.0 — 英語トップ切替・新言語版統合（W09–W15）

- Created: 2026-10-19 JST
- Status: **RECONCILIATION REQUIRED / NOT YET IMPLEMENTED**
- Scope: Update existing Draft PR #93; do **not** create a parallel SEO PR without need
- PR: https://github.com/landco-llc/kumihan/pull/93
- Work branch: `feature/seo-foundation-20261019`
- Original SEO PR HEAD observed: `0cfadad8dba7aff4ca0c97c31cbdf5fa9846c8ce`
- Latest main HEAD observed: `db14de27b4b7e8ffd298bd3ab4a940ba2a623bca`
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
- PR #100 is still Draft/open; not on main when inspected, so do not treat it as merged.

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

- Fetch latest `origin/main`, SEO PR #93 branch, merged PR #94–#99, open PR #100.
- Record refreshed SHA, ahead/behind, conflicts, all tracked site generators and HTML pages.
- Resolve main→SEO feature branch conflicts while retaining **current main body/footer/visual content** and existing SEO contract/tests. Do not force-push main or auto-merge PR.
- Do not resolve HTML conflicts by keeping old SEO-generated bodies or old `gateway-copy.json`.
- Save a source→output map and conflict resolution ledger in `docs/seo/`.

### W10 — English-first gateway and redirect

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

- Reconcile `seo_metadata.py`, `site_share.py`, Jekyll includes/data, all Python/Node generators, special authored pages with one canonical/OGP/JSON-LD contract.
- Do not clobber language-matched preview text or replace current 1200×630 share image with outdated square card output.
- Update locales correctly (`fa_IR`, `km_KH`, `zu_ZA`, `sw_TZ` as used by current site share code). Respect existing page.lang and region variants.
- Adjust validators/tests to check correct OG description contract, not old standalone description equality.
- Verify `_config.yml`, latest footer/site_share generation and Jekyll built pages.
- Preserve existing SEO's idempotent, non-writing `--check`, and duplicate tag protection.

### W13 — Regenerate sitemap & run comprehensive checks

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

- `docs/seo/BASELINE_INVENTORY.md`: record **refreshed** page count/source map, aliases, actual languages; stop presenting 231 as current.
- `docs/seo/DECISIONS.md`: append design decisions for English-first root, alias, OGP share ownership, fa/km/zu/sw adapter.
- `docs/seo/ADD_LANGUAGE_OR_PAGE.md`: new language addition must register site_share locale/about + appropriate Jekyll data when needed; mapping from product generators to gateway. New canonical/OGP compatibility checks.
- `docs/seo/VALIDATION_LOG.md`: run commands, branch SHA, true test results, remaining limitations, and production/Search Console Owner actions.
- Append file/URL inventories and CI URLs to the PR body. Do not fabricate PASS or production deployment.

### W15 — Fresh final CI and independent review

- Obtain fresh Hosted CI on **new final PR HEAD**. Old `0cfadad` 20/20 PASS no longer sufficient.
- Independent reviewer inspect: correct English/Japanese URLs, 22 top hreflang group, new 3-language product groups, 271ish-page sitemap, Jekyll and pre-existing page body preservation, main #99 social previews.
- Any conflicts/FAIL remain reported, PR left Draft; do not claim merge readiness.
- After all gates pass, submit updated Draft PR #93 (same PR). Do NOT merge or publish.
- Owner Gate: only after new green CI and independent review, merge to main; then production HTTP/HTML/sitemap check and Search Console submission.

## 4. Status and immediate risk

- **Baseline verification**: old SEO HEAD `0cfadad` passed 20/20 hosted CI.
- **Current integration**: new main differs and PR #93 is `mergeable=false`.
- **Technical conflict**: new main #99 owns social card generation while old SEO PR would override that content.
- **Work completed in this current handoff**: read-only fresh inspection, this reconciliation document and review handoff. **W09–W15 code reconciliation and new CI are not yet executed**.
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
