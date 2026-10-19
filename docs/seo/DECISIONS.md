# KUMIHAN SEO Architecture Decisions

**State:** Design decisions for implementation W00–W08. Update when verified code diverges.

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
