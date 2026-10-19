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
