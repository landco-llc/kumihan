# SEO Validation and Change Log

This log is the permanent record of actual runs. **A planned test is not a PASS.**

## 2026-10-19 — Initial instruction placement

| Item | Observation |
| --- | --- |
| Status | NOT STARTED — implementation has not been run |
| Base observed main | `fce40015abaa1f5f309cf9e977f55e41537c13aa` |
| Instruction source | `docs/specs/KUMIHAN_SEO_FOUNDATION_IMPLEMENTATION_20261019.md` |
| Scope | Technical SEO, multilingual sites, sitemap and JSON-LD |
| Tests | NOT EXECUTED |
| Site deployment | NOT EXECUTED |
| Search Console ownership/submit | NOT EXECUTED |
| Next action | Codex Cloud/App executes W00–W08 on the feature branch |

## Append-on-each-PR template

### YYYY-MM-DD — [work / PR]

- Executor:
- Branch / HEAD:
- Baseline / freshness check:
- Changed sources:
- Generated pages / URLs checked:
- Commands executed:
- PASS:
- FAIL:
- NOT TESTED (with reason):
- Sitemap entries / excluded pages:
- Canonical/hreflang coverage:
- JSON-LD/OGP image check:
- Human Owner actions pending:
- Reviewer / result:
- PR URL / merge status:

Do not overwrite prior entries. Publish only observed outcomes; do not infer indexation, rich results, or SNS preview success from a valid metadata syntax test.

## 2026-10-19 (JST) — W00–W07 implementation and review

- Executor: Codex parent with specialist generator/contract/runtime workers and a fresh independent reviewer.
- Branch: `feature/seo-foundation-20261019`. Initial remote feature HEAD `3f1e2ee`; main Fresh Read `ba1c50f`, safely merged at `2ea293f`. A final freshness check found main advanced to `64a8425` (PR #92); reconciliation and final validation follow below.
- W00: 72 root +159 docs =231 public pages inventoried individually. 210 static output pages +21 Jekyll frontmatter pages. Main distribution additions retained; no protected path changes.
- W01–W03: shared SEO library/config, all Python/Node site output boundaries, Jekyll21 generated includes, Bengali12 and legacy ZiHeng9 authored template pairs. All210 changed static HTML bodies match original main byte-for-byte.
- W04–W06: canonical-only Sitemap231, source and actual-output audit, dedicated PR CI, new-language/new-directory fixtures, source mapping and runbooks.
- `python tools/build_seo.py --check`: PASS all generation checks and231 source contracts. SHA256 before/after independent reviewer check: zero repository content changes.
- `python -m unittest discover -s tests/seo -v`: initial13 PASS; independent-review fixes increased to15 PASS.
- Independent review: [INDEPENDENT_REVIEW.md](INDEPENDENT_REVIEW.md). Two P2 findings fixed: nested-directory discovery and comma-separated robots `none`. Both regression tests observed FAIL before fix, then15/15 PASS. No remaining current-page correctness findings.
- Full existing sweep:20 suites /250 tests before Zilu adaptation =247 PASS, two failures and one error. Zilu's exact raw-template equality was updated to compare enriched source and independently preserve body bytes; its10 tests then PASS. Remaining ID `test_archives` (0 vs15 archives) and SW `test_released_archives` (missing `plugins/kumihan-mizani/downloads/MANIFEST.json`) reproduced unchanged on isolated `origin/main ba1c50f`; do not regenerate protected distributions for this SEO work.
- Existing distribution/site/font `--check` sweep:29/29 PASS. No ZIP writes.
- Actual Bundler/Jekyll3.10.0 +Liquid4.0.4 +Ruby3.3.8 build PASS; `python tools/check_seo.py --site-dir /tmp/kumihan-seo-site`:231 PASS. GFM parser explicitly pinned in Gemfile/lock. Source contracts alone are not treated as rendered evidence.
- Browser/Chromium154 smoke on actual output: `/`, `top-en.html`, `kumihan.html`, `kumihan-ko.html`: HTTP200, correct language, exactly one canonical, no JS page errors.
- Live baseline: GitHub Pages API confirms legacy build main/root. Homepage HTTP200. Official OG PNG HTTP200, `image/png`,1045725 bytes,1254×1254; dimensions match metadata. Host `/robots.txt` HTTP404; no project robots added or crawler policy changed.
- Noindex/external canonical/duplicate/drift checks exercised with nonpublished fixtures. No current231 pages excluded; source/package/template paths are outside the indexable inventory.
- NOT EXECUTED: production deployment of branch, Google Rich Results Test/Schema Markup Validator service submission, Search Console ownership/submission/indexing, authenticated SNS cache refresh. Generic WebPage/Organization syntax PASS is not a rich-result or indexing guarantee.
- Pending Owner actions: review Draft PR; authorize merge separately; after publication verify production Sitemap and submit `https://landco-llc.github.io/kumihan/sitemap.xml` in an owned Search Console property.

### Final main reconciliation and code HEAD

- Verified implementation HEAD: `a38a237` (merge of latest main `64a842585b9a19fbdfa90bffb06b1c7aa8d43d3e`). PR #92 merged while SEO work was running. Resolved all18 generated gateway conflicts by rerunning the merged generator, preserving versioned stylesheet and menu changes.
- Post-merge `python tools/build_seo.py --check`: PASS,231 pages/URLs, no writes; `python -m unittest discover -s tests -v`:18 PASS (includes new main stylesheet regression).
- Post-merge Bundler Jekyll3.10 build: PASS; actual231-page output audit: PASS. SEO15 tests and Zilu10 tests PASS after independent-review fixes.
- Protected plugins/skills/download directories and every ZIP: zero differences versus final `origin/main 64a8425`. Existing static HTML bodies: zero differences.
- Raw-checkout ID/SW archive tests require workflow package-build prerequisites (their existing CI creates packages before tests). Isolated workflow verification is recorded separately; no generated archives will be copied into this branch.

### W08 — Draft PR and workflow-prepared archive tests

- Draft PR: https://github.com/landco-llc/kumihan/pull/93 (main未マージ)。最終コード検証HEAD `a38a237`; initial submission HEAD `abd6c51` is the same code plus validation-log update.
- Existing CI prerequisites faithfully reproduced in isolated current-feature copy: `python tools/build_laras.py` then ID9/9 PASS; `python tools/build_mizani.py` then SW6/6 PASS. The raw-checkout failures above are preparation-dependent, not SEO regressions. Temp-generated ZIPs remain outside the branch and are not copied back.
- Final combined results: all251 existing tests PASS with their established preparation (root18 + language233; Zilu10 rechecked after parity-test adaptation), SEO15 PASS. Existing check29/29 PASS. No remaining local test failure.
- First hosted SEO run: https://github.com/landco-llc/kumihan/actions/runs/39205706993 (submitted HEAD `abd6c51`; completion recorded separately). PR CI reruns on each log-only commit; inspect latest PR check SHA for the final state.

### Hosted CI failure diagnosis and correction

- First hosted SEO job failed in `ruby/setup-ruby`, after all15 tests and all231 source/generator checks passed. Official kramdown2.5.1 requires rexml>=3.3.9; local Debian gemspec had recorded>=3.2. Auditing all28 locked versions against official RubyGems also identified listen's missing rb-fsevent dependency. Corrected the lock to official metadata.
- Korean/ZiLu jobs failed because their apt-installed Jekyll4 automatically activated the newly added Jekyll3.10 Gemfile without bundle install. Explicitly select their existing distro preview runtime with `JEKYLL_NO_BUNDLER_REQUIRE=true`; the dedicated SEO job retains pinned Bundler3.10 validation. Existing checks remain enabled.
