# Equilibrio — design application receipt

W07 contract recorded before site generation, 2026-10-19 JST.
Authority: Owner's current /goal explicitly authorizes Italian/English/Japanese site production, canonical KUMIHAN design reuse and publication. No new approval gate is introduced.

Read after the WG02 15-ZIP gate: plugins/kumihan-equilibrio/skills/kumihan-equilibrio-web/SKILL.md, references/web.md and workflow.md, local rules/catalog.json and sources/public-sources.json. Product sources are the current feat/equilibrio-v0.1.0 worktree based on a588f07; first implementation commit will bind these files. Also read skills/kumihan-web/SKILL.md, references/web-recipes.md and design-contract.md, canonical _layouts/landing.html / installation.html, tools/product_site.py / install_frame.py / base_copy.py, assets/kumihan-install.css and .js.

Purpose: let Italian-speaking designers understand the skills, distinguish production from review, and choose an actual host-specific archive. English/Japanese readers receive the same brand principles from shared copy. Primary action: open the correct installation guide, then select plugin or standalone skill. The canonical eight-section structure supports that sequence: purpose → four priorities → principles → four comparable skills → three host choices → evidence/limits → source. Four skill cards and three host rows compare real peers with real links.

Type roles: system Latin sans for navigation/body, canonical display scale for headings, existing serif specimen for accents/quotes. Japanese uses strict line breaking and existing system/fallback stacks. Official logo only; no new font/image assets or national-color aesthetic. Keep the canonical paper/ink/red tokens and spacing. Optional balance is a layout aid, never semantic proof.

Applied Italian rules: R01/R02/R14/R16 source accents/foreign names/bytes; R09 quotation alternatives; R17 apostrophe wrapping is legal; R19 actual lang plus explicit it-IT product context; R20 dictionary behavior not-checked; R21 local wrapping; R22/R23 hierarchy/line length as proposals; R24 accent and fallback inspection; R25/R26 locale separate from house style and values; R32 purposeful design; R35 visible action names; R37/R38/R39 enlargement/reflow/spacing. Japanese JA-TYPE-011: compare natural phrase wrapping; preserve source text and avoid introducing arbitrary break fragments.

Italian headline: “Il design in italiano, più naturale”; specimen phrase “Ogni parola al suo posto”. Adopted for the product's focus on natural reading and contextual form. Native Italian editorial review: NOT-CHECKED; this is authored copy, not a claim of native certification. The 40/48 research inventory is never advertised as automatic pass coverage.

CSS scope: inherit canonical_css; Italian-only natural wrapping/manual hyphenation, multiline controls and header/grid min-width safeguards. No paragraph-wide nowrap, break-all, new gradient system or content deletion. No intentional brand exceptions.

Verification pending W09: 12 pages × 320/375/768/1280; ordinary/doubled computed font sizes (CSS simulation ≠ native zoom), spacing overrides, fallback, focus and links. Native text zoom, Safari/Windows, Office/PDF, screen reader and dictionary remain NOT-CHECKED unless separately measured.

## W09 observed results
- Chromium 154.0.8037.57 on Linux, Python 3.12.14 / Playwright. External fonts blocked deliberately; system/fallback rendering checked, not Google font success. 192 combinations of 12 pages × four widths × normal/doubled computed font sizes × normal/overridden spacing. Initial run: one transient Japanese landing scrollWidth 341 at 320/2×/spacing; direct diagnostic and full repeat: 320 and 0 failures. Stabilized measurement waits two animation frames; final full matrix: 192, 0 failures. Initial failure retained in evidence/browser-initial.json; final in evidence/browser-final.json. No production CSS workaround or source deletion used.
- Visible focus on “Vai al contenuto”, Tab→Enter reaches #main. Mobile and accent regular/bold/italic specimens visually inspected: original diacritics, caporali/English quotes and currency/ordinal symbols visible. See evidence/it-mobile-keyboard.png and it-accent-fallback.png. These specimens are fallback evidence, not all-font coverage.
- Review caught the inherited “Deutsch” install-language label; a failing regression was added, label corrected to “Italiano” and all nine guides regenerated. Corporate external footer link also added with a failing regression. A final CI browser matrix will cover those regenerated guides.
- Shared JA/EN copy checks PASS. Specific exceptions are feature 01 Italian orthography/locale, feature 03 exact-byte protection, entry context and factual release/install limits. Japanese canonical title/h1 and English title/h1 exactly follow base_copy.
- NOT-CHECKED: native browser text-only zoom, Google font loading, Safari/Windows, screen readers, dictionary hyphenation, native provider import/icon UI, native Italian editorial review and Office/PDF. CSS simulation is not native zoom; semantic line quality is manual judgment, not measured by balance support.


Final font integration: explicitly register it in the shared Latin selector group (tools/web_fonts.py); preserve every other stack. Earlier rendered evidence predates that selector registration. The final local and CI browser runs below/at publication validate the registered stack separately. Native font loading/zoom/hosts remain outside the measured scope.
