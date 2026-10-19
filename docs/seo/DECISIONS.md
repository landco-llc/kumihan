# KUMIHAN SEO Architecture Decisions

**State:** Implementation decisions for W00–W08. Execution evidence and outstanding validation remain in VALIDATION_LOG.md. Update this record when code diverges.

## ADR-SEO-001 — Centralized source, generated outputs

- Date: 2026-10-19
- Decision: Use existing page generators/copy files as the source of truth and reuse common SEO helpers.
- Rationale: KUMIHAN has independent generators for gateways, product pages, Jekyll pages, and special language editions. Direct HTML edits alone will be overwritten.
- Consequence: Generator `--check` and cross-page SEO validation are required for every new language.

## ADR-SEO-002 — Canonical multilingual policy

- Date: 2026-10-19
- Decision: The site home canonical is `https://landco-llc.github.io/kumihan/`. Every translated page has its **own** self-canonical. Language alternates must be reciprocal and scoped to the same content.
- Consequence: Never canonicalize a French/Polish/Chinese page to the English or Japanese page solely because they are translations.

## ADR-SEO-003 — Sitemap rather than misleading project robots

- Date: 2026-10-19
- Decision: Generate a root-level`sitemap.xml` for the project path, with only valid canonical URLs. Do not add a misleading `/kumihan/robots.txt` as if it controlled `landco-llc.github.io` at the host root.
- Consequence: Sitemap discovery through Search Console (Owner-managed) and documented URL. Project/host control must be reconsidered on domain changes.

## ADR-SEO-004 — No artificial SEO signals

- Date: 2026-10-19
- Decision: Implement structured data grounded in published content; do not invent review ratings, offers, FAQs, prices, modification dates, or AIO-only meta keywords.
- Consequence: No "rich results guaranteed" or "AI search ranking achieved" claims.

## ADR-SEO-005 — Independent analytics scope

- Date: 2026-10-19
- Decision: GA4/GTM/Consent Mode and tracking are separate from technical SEO.
- Consequence: SEO deployment does not add cookies or analytics scripts.

## ADR-SEO-006 — SNS-share coordination

- Date: 2026-10-19
- Decision: SEO owns OGP/canonical truth. SNS share component should consume canonical and published OG title/description.
- Consequence: Coordinate with `feature/sns-share-spec-20261019` before altering same head templates.

## ADR-SEO-007 — Fresh main and concurrent gateway work

- Date: 2026-10-19 (JST)
- Evidence: W00 fetched latest main `ba1c50fdf2de8f920257d417e6213cd9ea0a2443`, merged at `2ea293f5db838e85817c934625d9b9cf0ab30ac4`. Mizani increased root candidates from 69 to72 and docs from150 to159.
- Decision: Use latest main as protection baseline; implement all231 candidates. Keep open PR #92 gateway CSS/menu changes independent and preserve both generator changes when subsequently reconciling.
- Consequence: Inventory and protected-file checks compare against current `origin/main`, rather than treating newly merged language distributions as SEO modifications.

## ADR-SEO-008 — Source-authored and Jekyll pages use the same SEO contract

- Date: 2026-10-19 (JST)
- Evidence: Korean and Japanese pages are Jekyll frontmatter/body inputs. Bangla has authored HTML, not an independent site builder. `scripts/build_bn_release.py` builds protected distributions and must not be used for SEO regeneration.
- Decision: Reuse common SEO metadata for generated HTML, generated Jekyll SEO includes, and the authored-HTML adapter. Keep each existing body/copy source. Whole-site orchestration verifies every independent generator, including Node/Vietnamese and special templates.
- Consequence: A common product renderer alone does not establish complete coverage. Validate built Jekyll HTML separately from source/include contracts; maintain exact source→output inventory.

## ADR-SEO-009 — Discover pages; do not maintain a second translation registry

- Date: 2026-10-19 (JST)
- Decision: Discover public HTML under root and docs, consume the existing page canonical/translation information, and require complete SEO. Missing metadata is an error, rather than a silent sitemap omission. Intentional noindex/external canonical is excluded from Sitemap, with errors for malformed or contradictory canonical information.
- Consequence: New public HTML is automatically audited. `tests/seo/fixtures/test-fixture-new-language` exercises future-language detection without publishing a fixture. Templates, layouts, plugins and tests are outside public HTML discovery.

## ADR-SEO-010 — Existing square logo and conservative structured data

- Date: 2026-10-19 (JST)
- Decision: Reuse the existing official1254×1254 PNG without changing brand artwork. Emit actual width/height and Twitter `summary`, not a fictitious1200×630 large-image card.
- Decision: Organization uses published `L&Co. LLC` and `https://landco.co.jp/`; WebPage URLs equal canonical. Do not add SoftwareApplication offers or speculative SoftwareSourceCode/review data merely for rich-result eligibility.
- Consequence: Structured data describes public facts; external rich-result tooling may report no eligible rich result without implying invalid WebPage/Organization markup. Record external checks and their limits separately.

## ADR-SEO-011 — Deterministic Sitemap and publication boundary

- Date: 2026-10-19 (JST)
- Decision: Commit simple `loc`-only Sitemap in stable order. Omit lastmod because no reliable per-page update source is established; omit priority/changefreq and duplicate hreflang XML.
- Consequence: Rebuilds are independent of wall-clock time. Branch source/Jekyll preview validation establishes reviewable implementation; production retrieval, Search Console ownership and submission remain Owner actions after publication. No analytics tags, robots policy or AI-training permissions are changed.

## ADR-SEO-012 — Independent-review fixes and language granularity

- Date: 2026-10-19 (JST)
- Finding/fix: Root/docs-only discovery missed a future `guides/new.html`. Discovery now recursively covers new public directories; the Jekyll include builder uses that same scanner. Hidden/underscore directories and tools/scripts/tests/templates/plugins/skills/vendor/node_modules, host download trees, docs/specs and docs/seo are intentionally outside the indexable page inventory. Package/direct-download availability is unchanged.
- Finding/fix: `robots="none, max-snippet:-1"` must exclude the page just as `noindex` does. Both directives now share comma-token normalization. Regression tests failed before these fixes and passed afterward.
- Decision: Accept compatible BCP47 granularity (existing Thai `lang="th"` and `hreflang="th-TH"`) while rejecting conflicting primary language, script, or region. Preserve existing source language markup rather than rewriting visible copy or source contracts.
- Cost if wrong: New publishing conventions require an exclusion-policy update; regional translations must use explicit matching region/script tags when differences matter.

## ADR-SEO-013 — Reproducible Ruby dependencies and existing preview jobs

- Hosted CI exposed Debian-patched gem metadata in the locally generated lock: kramdown's rexml constraint and listen's macOS dependency differed from official RubyGems. Audit all28 locked versions against official exact-version metadata and retain the official dependency graph.
- Existing Korean/ZiLu preview workflows intentionally install distro Jekyll4 and previously had no Gemfile. Their Jekyll commands now explicitly set `JEKYLL_NO_BUNDLER_REQUIRE=true` to continue using that installed preview runtime. SEO's dedicated job separately uses the pinned Bundler/Jekyll3.10 GitHub Pages-compatible runtime. Neither preview check is removed.
- Cost: Two runtime variants remain intentional; the dedicated3.10 build is the Pages reference. Workflow/runtime version changes must rerun built-HTML and browser checks.

## ADR-SEO-014 — English first, legacy alias and current share-preview authority (integration pending)

- Date: 2026-10-19 JST; status: **pending implementation**, following main `db14de27b4b7e8ffd298bd3ab4a940ba2a623bca`.
- Observation: PR #94 moved English gateway to `index.html`, Japanese gateway to `top-ja.html`; `top-en.html` is a noindex redirect. New top languages include sw, zu, km and fa.
- Decision: Homepage canonical and x-default resolve to `https://landco-llc.github.io/kumihan/`; Japanese top self-canonical is `/kumihan/top-ja.html`; legacy `top-en.html` stays out of Sitemap.
- Observation: Merged PR #99 introduced `tools/site_share.py`, `assets/kumihan-share.png` (1200×630), and Jekyll `_includes/share.html`. These now own localized OG/Twitter previews. Old SEO PR assumed square 1254×1254 image and meta-description equality.
- Decision: **Do not overwrite** main #99's localized combined share description/OGP image; SEO owns canonical/hreflang/JSON-LD/sitemap, share component owns social previews; audit their alignment after integration.
- Outcome: Existing PR #93 has `mergeable=false`; do not merge before reconciliation and new Hosted CI. Implementation instructions: [RECONCILIATION_20261019_EN_TOP_NEW_LANGS.md](RECONCILIATION_20261019_EN_TOP_NEW_LANGS.md).

## ADR-SEO-015 — 2026-10-19 v2 refresh after design/skills merge

- Baseline: latest main `73d2b01d2f604608360beabe364f59af72b8b66c`. PR #100 is merged. PR #101 (Universal MCP PHP) and PR #102 (Rendered QA documentation) remain Draft/unmerged at this observation.
- Decision: treat all `v0.1.8-preview` candidate skills, plugin manifests, packages/ZIPs and content that PR #100 merged into main as protected. SEO work must not restore older candidate versions or alter them.
- Decision: noindex/meta-refresh `top-en.html` is an explicit alias. SEO enrichment must skip such allowlisted aliases while preserving a hard failure for malformed ordinary pages.
- Decision: social preview text, landscape image and Twitter card remain under main's `tools/site_share.py`; SEO only supplies canonical/alternate/JSON-LD contract. Jekyll `page.url` must not reintroduce a mismatched OG URL.
- Decision: CI must flag future Jekyll languages missing `site_share` locale data rather than silently falling back to Japanese.
- Evidence: [2026-10-19 second review](REVIEW_REFRESH_20261019_MAIN_73D2B01.md). W09–W15 code integration and new hosted CI have not run; decisions are guidance, not verified fixes.

## 2026-10-19 — W09–W15 current-main reconciliation

- Root English route canonicalizes physical index.html to `/kumihan/` in canonical, en/x-default, OG URL, WebPage URL and Sitemap. `top-ja.html` stays Japanese; only allowlisted `top-en.html` with noindex and expected refresh skips ordinary metadata requirements.
- `site_share.py` owns OG/Twitter presentation, combined localized descriptions, locale, 1200×630 image and large card. SEO calls its renderer after canonical/translation groups/JSON-LD. Shared cards are emitted last so applying either hook twice is stable. SEO image config mirrors the actual shared image and audit verifies bytes/dimensions.
- Jekyll generated includes own metadata and compute title, description, canonical and effective language captures. Layouts pass those values to `share.html`, which has no implicit JA share-data fallback. Missing frontmatter language retains the established explicit JA default in the generator; unknown languages or missing/stale committed language data fail generation. All registered share languages are generated from gateway copy.
- Current-main `fa`, `km`, `zu` builders use the same SEO output decorator; `sw` coverage retained. Page discovery remains recursive and unknown metadata/generator/layout fails verification. Persian RTL, ZWNJ and original bodies remain byte-stable.
- Existing authored BN/ZiHeng templates were refreshed from current main instead of overwriting newer body/footer. All four Jekyll layout bodies retain current main. Baseline hashes cover skill/plugin/package candidates including v0.1.8-preview. Package prerequisite tests run in isolated copies only.
- Actual Hosted Jekyll audit caught residual landing alternates and missing effective-language handoff after JA fallback removal. Fixed via two regression tests; source simulation alone is not a build acceptance gate.
