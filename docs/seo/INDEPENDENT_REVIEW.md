# Current final Owner Gate — latest main05c60fd / 2026-10-19 JST

W09–W15 implementation is integrated with current main `05c60fd5d519a3a6d38feb616f60fddd373b635f` (including newly merged PR #103 privacy policy/footer). Current audit is **274 HTML / 273 canonical URLs**, not the earlier272/271. 22 gateways +63 LP +186 guides +2 privacy policies, plus1 excluded alias. Privacy translation group is en/ja/x-default, separate from gateways/products. No body or policy text rewritten by SEO.

Latest-main protection PASS: **257 body suffixes** (253 static +4 layouts),21 original Jekyll sources,2609 protected distribution/skill/manifest files. Root tests62/62 and SEO26/26 PASS. Shared language previews and 1200×630 image retained. Current inventory: [BASELINE_INVENTORY.md](BASELINE_INVENTORY.md).

**Authoritative final SHA / Hosted CI / independent review / Owner Gate state:** [final PR #93 gate record](https://github.com/landco-llc/kumihan/pull/93#issuecomment-6265452330). This stable GitHub record is updated after exact-head CI, avoiding another evidence-only commit that would invalidate its own SHA. Earlier snapshots below remain historical evidence for their explicitly named commits.

Draft remains unmerged, auto-merge disabled. Owner alone may approve merging; then deployed HTML/image/current273-URL Sitemap must be verified before Search Console. SEO does not publish or send sitemap.

---

# W09–W15 independent review — 2026-10-19 JST

A separate reviewer agent independently read the two binding documents, source/diff and tests at `fa9451a` against main `b7a8c83`. Reviewer made no changes and did not share the implementation session context.

| Requirement | Independent assessment |
| --- | --- |
| P0-01 alias | Resolved: exact allowlist, noindex/expected refresh, ordinary description failures |
| P0-02 social | Source resolved: shared localized copy, landscape image, large card, single ownership; built proof required |
| P0-03 English root | Resolved: canonical/OG/WebPage/en/x-default agree |
| P0-04 new languages | Source resolved: 22 gateways/271 URLs; independently compared all 272 public body/frontmatter sources with main: unchanged |
| P0-05 candidates | Resolved: skill/plugin/ZIP/MANIFEST/SHA/README/CHANGELOG diff empty; hash protection passes |
| P1-06 Jekyll locales | Resolved: unknown language and missing/stale committed data explicitly fail |
| P1-07 built/idempotence | One important blocker: residual 4 hreflang links in landing layout duplicated generated alternates for kumihan/en/zh-tw |

Reviewer independently ran 22 SEO tests, all generator checks, web-font checks, source audit (272), Sitemap (271), preservation audit. Ruby unavailable locally; reviewer did not claim an actual build.

Parent fix pass: `d395e14` removed residual landing alternates. Two new regression tests were observed FAIL then PASS. Hosted Jekyll logs also identified nil page.lang on the 3 legacy Japanese install pages after removing implicit fallback: generator now captures effective lang and explicitly passes it to share.html. No frontmatter/body changes. Suite: SEO24/24 and root59/59 PASS; preservation PASS. Exact new-head Hosted CI is the gate for actual rendering. No second author-only review is represented as independent sign-off.

Historical independent W00–W08 review and old 231-page results remain in Git history and are not acceptance evidence for this integration.

## Fix-pass acceptance

After merging upstream release-documentation main a08fd66, integrated code6c4ecbf passed Hosted CI23/23. Both exact push and PR synthetic-merge jobs ran actual Jekyll3.10 and audited272 built pages successfully; preservation and271 Sitemap also PASS. This closes the review's important hreflang finding and the default-language handoff defect identified by Hosted CI. Parent regression verification, not a second independent reviewer sign-off. Evidence: `evidence/20261019-integrated-checks.json`, `evidence/20261019-integrated-jekyll-hosted.json`. Owner Gate remains; no main merge.

## Focused independent review — privacy/footer main05c60fd

The independent reviewer was separately tasked to inspect the new upstream privacy/footer scope (not repeat the prior fix pass). Review performed read-only on the final privacy integration working tree against05c60fd. **No new actionable findings.** Independently compared all274 public files:253 static HTML body byte sequences and21 complete Jekyll sources unchanged. Privacy source copy/footer implementation/data/styles/fonts match upstream. Each privacy page has one metadata set/JSON-LD, reciprocal independent en/ja/x-default group and self-canonical. Common pipeline includes privacy builder. Preservation2609/257/21, SEO26, all build checks, source274/Sitemap273 PASS. Prior layout-duplicate/effective-language fixes confirmed present; no P0/P1 source regression. Reviewer did not edit, commit, push or comment to GitHub. New exact-head Hosted Jekyll/browser acceptance is tracked in the final gate comment linked above.
