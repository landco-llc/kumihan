# Independent review — SEO foundation

Reviewed 2026-10-19 against `origin/main`, on `feature/seo-foundation-20261019`. Fresh-read binding specification `docs/specs/KUMIHAN_SEO_FOUNDATION_IMPLEMENTATION_20261019.md`. Review covers the working diff and untracked SEO implementation, all 231 discovered HTML contracts, generator adapters, source templates, sitemap, CI, and actual Jekyll output. Reviewer did not modify implementation files.

## Findings at review time

### P2 — Public HTML outside root/docs silently escapes discovery

`tools/seo_inventory.py:public_paths` enumerates only root `*.html` and `docs/**/*.html`. Jekyll also publishes ordinary HTML below other nonexcluded directories. A future `guides/new.html` is therefore absent from metadata audit and sitemap; its missing SEO produces no CI failure. `tools/build_jekyll_seo.py:outputs` has the same discovery restriction for frontmatter pages. This violates future-page coverage and allows false green checks.

Reproduction: in a temporary root, create valid `index.html` and `guides/new.html` using `render_metadata`; `len(pages(root))` returns 1 and `audit(root, False)` returns `[]`. Removing all SEO from `guides/new.html` also remains invisible. Discover public HTML recursively using explicit source/package/Jekyll exclusions, and reuse that policy for frontmatter include generation. Add a nested-page regression fixture. Parent notified and is implementing a fix; this entry records the original independently observed behavior.

### P2 — Comma-separated robots `none` is treated as indexable

`tools/seo_inventory.py:Page.noindex` normalizes commas for `noindex`, but checks `none` using whitespace-only splitting. `none` means `noindex, nofollow`; a valid combined directive such as `<meta name="robots" content="none, max-snippet:-1">` is thus incorrectly included in the canonical sitemap.

Temporary-file reproduction: construct an otherwise valid index page with that robots tag. `Page(...).noindex` returns `False`; `sitemap(root).count('<loc>')` returns 1. Normalize separators once and match both `none` and `noindex` on the resulting tokens; test both robots and googlebot forms. No current committed page was observed to use this directive; consequence concerns future exclusion correctness.

## Independent validation and evidence

- `python -m unittest discover -s tests/seo -v`: 13 tests PASS.
- `python tools/build_seo.py --check`: every Python/Node generator and Jekyll include check PASS; sitemap 231 URLs; source audit 231 pages PASS.
- Independently SHA-256 snapshotted repository files before/after `python tools/build_seo.py --check` (excluding `.git` and Python bytecode): exit 0, zero content changes.
- Compared every existing static public HTML body suffix (`<body` through EOF) with `git show origin/main:PATH`: no body changes. Four layout diffs only replace head metadata with includes; authored Bengali and Ziheng templates preserve existing bodies.
- `JEKYLL_NO_BUNDLER_REQUIRE=true /tmp/kumihan-jekyll3 build --destination /tmp/kumihan-independent-site --trace`: Jekyll 3.10 build PASS.
- `python tools/check_seo.py --site-dir /tmp/kumihan-independent-site`: actual rendered HTML PASS, 231 pages. This is distinct from source includes, which synthesize their language from JSON-LD.
- Direct local Jekyll invocation without that environment override failed because the temporary Ruby installation lacks lockfile dependency `eventmachine-1.2.7`. The override allows the installed Jekyll 3.10 runtime to run, but does not reproduce Bundler/CI dependency installation. Hosted workflow status remains separate evidence.
- Existing tests verify JSON script-closing escaping and Unicode roundtrip, idempotence, disjoint gateway/product groups, wrong canonicals, reciprocal links, external/noindex exclusion, metadata duplicates, JSON-LD mismatch, and sitemap drift. Current hreflang audit confirms existing groups target canonical pages with compatible languages. It does not independently infer semantic translation relationships; group source review remains necessary.
- Shared OG config declares the existing PNG as 1254×1254 with Twitter `summary`; actual built-image signature and dimensions pass the checker. No invented reviews, offers, or software sales claims were found in generated JSON-LD; Organization/WebSite/WebPage describe configured publisher and actual URLs.
- `git diff --name-only origin/main` showed no changed ZIP, SKILL.md, plugin manifest, VERSION, or package.json. No new tracking code or project-root robots.txt was observed.

## Limits and follow-up

The 13 tests initially omitted nested public-page discovery and comma-separated robots `none`; both gaps are demonstrated above. The rendered-output audit uses the same discovery helper as source audit, so its 231-page PASS does not resolve the discovery gap. Verify fixes with adversarial fixtures and rerun source/build checks before closing findings. Live production deployment, browser display, social crawler caches, Google validators, Search Console ownership/submission, and hosted CI success were not independently verified by this reviewer.

### Implementer resolution (after independent review)

Both P2 findings fixed. `test_new_directory_is_discovered_and_sources_excluded` and `test_comma_delimited_robots_none_is_not_indexable` each failed against the reviewed implementation, then passed after scanner/tokenization fixes. Full SEO suite15/15 PASS. Jekyll include generation now shares recursive public discovery. These are implementer verification results, not an additional reviewer sign-off.
