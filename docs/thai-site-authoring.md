# Thai website authoring record

W04/W05 use **instruction-guided**, not native installed-host invocation. Before generating the localized pages, the author read `plugins/kumihan-th/entrypoints/kumihan-th.md`, `kumihan-th-web.md`, `references/workflow.md`, `references/web.md`, and `locales/profiles/web-marketing.json` from the new Thai product.

- Locale: explicit `th-TH`; medium: `web-marketing` for landing, `web-editorial` for installation; mode: build, then read-only audit.
- Purpose: introduce the independent Thai product and explain actual portable delivery formats to Thai readers, with equivalent English/Japanese editions.
- Source: execution packet 03 draft copy imported into `assets/thai-site-copy.json`; technical host prose authored conservatively against the packaged contract. Documents supplied facts and copy, while the user's execution request authorized implementation.
- Protected text: exact product name `KUMIHAN｜ดุลอักษร`, publisher, identifiers, sample `น้ำชา เก่ง ภาษาไทย`, original logo, existing Japanese/ZiHeng files. No normalization or invisible break controls inserted.
- Design: existing KUMIHAN ivory/ink/red tokens, sticky navigation, hero, concept, four features, thesis band, four Skill cards, three host rows, status, final CTA and footer. Source text remains selectable and complete. Thai headings use generous line height with normal wrapping; emergency URL wrapping is confined to identifiers.
- Site-only font stack: Noto Sans Thai, Leelawadee UI, Thonburi, Tahoma, system sans. No fonts redistributed. Actual font/run/rendering evidence is recorded separately by browser QA; a CSS family name is not proof of font use.
- No native host installation or invocation was performed by this author: `not-checked` for ChatGPT/Codex, Claude and Gemini. Gemini documentation clearly describes instruction-guided use; no native Gemini extension is supplied.
- Native Thai editorial review: `needs-review`. No fabricated audience, performance, installation or marketplace claims.
- Publication wording directs readers to actual GitHub Release status. If no Release exists the page explicitly describes the version as a release candidate and assets as unavailable; it makes no unverified released claim.

Rebuild with `python tools/build_th_site.py`; verify determinism with `python tools/build_th_site.py --check`. Static checks are not visual review. Browser evidence must cover actual width, fonts, combining marks and enlarged text separately.

## Enlarged-text correction

The bounded browser run exposed narrow-screen overflow at 200% CSS text enlargement in English/Japanese landing pages. The mobile hero grid now has a zero minimum track, cards/content can shrink, buttons reflow, and section numbers sit above the full-width text column. English headings/card text and mixed identifiers use emergency word wrapping only when their natural token exceeds the available measure. No source text changed and no clipping was added. Static tests remain separate from the browser run recorded by the root QA worker.
