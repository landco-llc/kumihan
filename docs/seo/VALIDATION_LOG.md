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

### Final hosted CI and handoff — all checks green

- Verified final implementation HEAD: `54458d301ac618bdcf81344157461c2475813a3c`. Hosted checks **20/20 PASS**, including both SEO push/PR runs, existing language/distribution checks, Korean/ZiLu Jekyll/browser checks and Grafía's browser measurements. No failed/pending check remains for this implementation SHA.
- Dedicated SEO PR run: https://github.com/landco-llc/kumihan/actions/runs/39205956034 . Includes15 tests, non-writing regeneration, pinned Jekyll3.10 build,231 actual-page/Sitemap audit, and unpublished fixture/source-directory checks. All steps PASS.
- Exact hosted check names, URLs and completion timestamps: [evidence/20261019-hosted-checks.json](evidence/20261019-hosted-checks.json). Local regression commands and official28-gem dependency audit are retained beside it.
- This final documentation/evidence-only commit follows the verified implementation above. Resolve final submission HEAD at [PR #93](https://github.com/landco-llc/kumihan/pull/93) (`head.sha` / `git rev-parse feature/seo-foundation-20261019`); its code and generated public files are identical to the verified implementation. PR checks rerun for that log-only HEAD.
- W00–W08 implementation, independent review, tests, runbooks and Draft PR delivered. Branch preserved for review; `draft=true`, `merged=false`, target=`main`. Owner merge and subsequent production verification/Search Console submission remain unperformed. External Rich Results/Schema Validator submission and SNS cache refresh remain unperformed as stated above.

## 2026-10-19 JST — Current main re-evaluation (reconciliation pending)

- Mode: GitHub connector read-only fresh inspection; **not a code reconciliation, test rerun or production deployment**.
- Latest observed main: `db14de27b4b7e8ffd298bd3ab4a940ba2a623bca`.
- Old PR #93 HEAD before this documentation update: `0cfadad8dba7aff4ca0c97c31cbdf5fa9846c8ce`, draft/open, mergeable=false; old Hosted checks 20/20 PASS **only on prior code**.
- Current main root HTML: 86 candidates = 22 true top gateways, 60 trilingual additional product pages, Japanese landing 3, and one legacy noindex `top-en.html`; docs HTML 186. Total candidate HTML 272. Expected indexable URL count 271 **subject to an audit** (one noindex alias, other exclusions not yet audited).
- English gateway now `index.html`; Japanese `top-ja.html`; legacy English `top-en.html` redirects and has `noindex`. New top languages: Swahili/sw, isiZulu/zu, Khmer/km, Persian/fa.
- Main PR #99 currently owns share OGP/Twitter metadata, 1200×630 preview and language-matched combined description; old SEO PR's 1254×1254 and equality checks conflict with it.
- Main already merged #94/#95/#96/#97/#98/#99; PR #100 open Draft (not part of observed main).
- Production/branch output HTTP and Search Console changes: **NOT EXECUTED/NOT VERIFIED**. Web fetch could not verify live Pages in this inspection. Do not submit old 231-URL sitemap.
- Next required work: [W09–W15 reconciliation](RECONCILIATION_20261019_EN_TOP_NEW_LANGS.md), final SHA hosted CI, independent review, owner merge gate.

## 2026-10-19 JST — W09–W15 second review / NOT EXECUTED

- Reviewer: GitHub Fresh Read, code-path/static review; no code integration or local execution.
- Main HEAD: `73d2b01d2f604608360beabe364f59af72b8b66c` including merged PR #100.
- SEO PR #93: Draft/open, pre-review HEAD `861bd3346ecd218cf45bf0b2c4cbbbfab6b3823f`, mergeable=false. Later documentation commits are NOT implementation tests.
- Current HTML discovery: 22 top gateways, 63 LP, 186 docs, 1 legacy noindex alias = 272 HTML candidates; indexable candidate ~271, not audited.
- Confirmed critical risks: `top-en.html` lacks normal description but old `seo_metadata.enrich_html` requires it; #99 `site_share.py` OGP/Twitter copy and 1200×630 previews conflict with old SEO metadata's square image/default copy; root/index canonical/OGP path mismatch; new sw/zu/km/fa pages absent from old sitemap; #100 v0.1.8-preview candidate packages protected.
- PR #101 (Universal MCP) and #102 (QA docs) remain open Draft, not merged.
- Actions performed: updated W09–W15 instruction, [review file](REVIEW_REFRESH_20261019_MAIN_73D2B01.md), runbook/ADR/PR hold notes. Actual code/HTML/sitemap regeneration, Jekyll rendered validation, new Hosted CI, independent post-reconciliation review: **NOT EXECUTED**.
- Latest web-hosted GitHub Pages HTTP/Sitemap validation: **NOT VERIFIED**; live fetch unavailable through current web tool.
- Owner gate: merged publication and Search Console submission remain prohibited before integration is validated and explicitly approved.

## 2026-10-19 JST — W09–W15 reconciled execution

- Binding docs Fresh Read from PR head `accbf832021ba29022a2b1c79098cd07d19c2d72`.
- Initial main `b7a8c83` (#100/#102 merged) safely integrated at `fa9451a`. Later main `a08fd66` (#104 release announcement) Fresh Read and merged, protecting current README/CHANGELOG. #101 is still Draft/unmerged. No main merge or release changes by this work.
- Sources: SEO adapter/metadata/audit, gateway/new fa/hlela/lumnung builders, shared site_share parsing/data, authored BN/ZiHeng templates refreshed from current main, Jekyll layout heads and generated captures/share include; existing source→output paths in current inventory.
- `python tools/build_seo.py`: all Python/Node/Jekyll metadata builders and Sitemap regenerated successfully. `python tools/build_seo.py --check`, `python tools/build_sitemap.py --check`, `python tools/check_seo.py`, `python tools/web_fonts.py --check`: PASS. Check mode leaves tracked files unchanged.
- Actual source audit **272 pages**, indexable **271 URLs**, 22 gateway languages. top-en alias excluded, root once, top-ja once. No external/noindex exclusions beyond alias. Source simulation explicitly distinguished from actual Jekyll.
- `python -m unittest discover -s tests/seo -v`: **24 PASS** after fixes. Added alias, invalid alias, normal description missing, mixed quote/idempotence/localized share, all gateway languages/root, unknown locale, missing Jekyll data, effective JA language handoff, duplicate layout-alternate tests. Initial 6 regressions reproduced missing behaviors before implementation. Review-fix regressions both observed FAIL then PASS.
- `python -m unittest discover -s tests -v`: **59 PASS**. Initial root59 run found13 layout/footer/font regressions while resolving merge; restored main layout bodies/font expressions and reran green. No failure omitted.
- Broad initial49-command run recorded in `evidence/20261019-local-checks-initial.json`: all language content suites except id/sw/km/zu passed; those four require untracked generated ZIP/MANIFEST prerequisites. In `/tmp/kumihan-seo-package-tests` only, existing builders created those prerequisites; id9/sw6/km5/zu6 then PASS. Working branch distributions untouched. 9 exploratory distribution `--check` commands were unsupported CLI options, not product failures; valid builders use --out or isolated copies. Existing supported distribution checks PASS in initial record.
- `python tools/check_seo_preservation.py`: **PASS** against latest-main a08fd66 immutable snapshot: protected2609, static/layout body255, original Jekyll sources21. `git diff origin/main -- plugins skills 'downloads *' README.md CHANGELOG.md .codex-plugin .claude-plugin plugin.json gemini-extension.json`: empty.
- Local Chromium at320px: English/JA tops, FA top+LP, KM top+LP, ZU/SW tops, top-en redirect: HTTP200, no JavaScript errors, scrollWidth=320 all; FA rtl. External fonts/network blocked; this is system-font smoke of local static HTML, not full multilingual font/render proof. `evidence/20261019-browser-320.json`.
- Local Ruby/Bundler unavailable; apt install attempt stopped by read-only system path. No local Jekyll claim. Hosted SEO CI does actual Bundler/Jekyll3.10 rendering and checks output.
- First integrated Hosted CI at fa9451a: actual Jekyll build succeeds, audit FAIL on3 landing duplicate hreflang +3 legacy JA install missing share language. Independent reviewer separately found duplicate hreflang. Fixed at d395e14 with regressions. Push SEO run [39238730392](https://github.com/landco-llc/kumihan/actions/runs/39238730392) **SUCCESS** including actual Jekyll audit272/Sitemap271. PR run [39238744625](https://github.com/landco-llc/kumihan/actions/runs/39238744625) failed because concurrent main #104 changed README/CHANGELOG; preservation check detected stale upstream baseline. Fresh merge and hashes updated only for those upstream files.
- Independent review at fa9451a: P0 five source requirements resolved, one P1 built issue requiring fix. Parent fix pass d395e14 verified SEO24/root59 and push actual Jekyll; see independent report. Final exact-head checks after current main merge will be recorded below and on existing Draft PR #93; no use of old 20/20 as new evidence.
- NOT DONE by SEO: production deployment, branch publication to Pages, external Rich Results/Schema submission, social posting/cache refresh, Search Console ownership/submission/indexation. Owner may merge only after fresh exact-head checks and review resolution, then validate deployed production before sending current sitemap. Old231 sitemap must not be submitted.
