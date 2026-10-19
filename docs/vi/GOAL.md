# /goal — KUMIHAN｜Nhịp Chữ v0.1.0

Owner decision: 2026-10-19 JST · Status: approved for end-to-end implementation and public release.

**Product**: KUMIHAN｜Nhịp Chữ
**Repository**: https://github.com/landco-llc/kumihan
**Research source**: https://drive.google.com/drive/folders/1wAY2IuUR5wMpoSdZ_fNyCpqwyFgNmT7Y
**License**: Apache-2.0 · **Distribution**: free / all countries
**Publisher**: L&Co. LLC

## Non-negotiable owner requirements

- Vietnamese-first implementation (vi-VN) with **Vietnamese and English** skill/plugin descriptions. The request's isolated “Russian” language is treated as a copied phrase, not the target language.
- User-visible plugin name is exactly `KUMIHAN｜Nhịp Chữ`; technical host IDs may be ASCII for compatibility.
- ZIP filenames include `v0.1.0`; all distributions contain official KUMIHAN artwork.
- Implement and package four self-sufficient Skills and three host plugins **before** producing the site. Use their design principles on the site.
- Publish Vietnamese, English and Japanese landing pages and corresponding installation guides using the established Japanese KUMIHAN structure and copy principles.
- Avoid burdensome security/governance ritual for this low-risk open-source informational product, but preserve provenance and do not invent evidence.
- Keep source files intact during read-only review. Mark native host/browser/font/editorial checks not performed as `not-checked`.

## Autonomous Work groups

| Work | Deliverable | Completion condition |
| --- | --- | --- |
| W00 | Fresh-read repository, research and authoritative KUMIHAN design | Existing project structure / language rules confirmed |
| W01 | Four standalone Skills, dedicated 36-rule catalogue, tests and read-only checker | Each Skill independently includes its references, rules and official icon |
| W02 | Host-specific ChatGPT/Codex, Claude and Gemini bundles | 15 versioned archives, checksums and manifest built deterministically |
| W03 | Site design after Skills; VI, EN, JA pages and nine installation guides | 12 pages with Japanese-based structure, local typography, canonical links |
| W04 | Connect VI edition to shared multi-language gateway | Generator changes and all six existing gateway pages in parity |
| W05 | Light test gate: source integrity / website copy / ZIP / shared parity checks | Relevant CI successful before merge |
| W06 | Merge approved branch, publish GitHub Release and GitHub Pages | Tag `kumihan-vi-v0.1.0` plus 15 ZIPs, manifest and SHA present; site responds |

## Repo paths

- `plugins/kumihan-nhip-chu/` — canonical independent product
- `tools/build_nhip_chu.py` — deterministic release distribution
- `tools/build_nhip_chu_site.mjs` — canonical VI/EN/JA site generation/check
- `tools/build_gateways.py` — multi-language gateway generator
- `tests/nhip_chu/` — behavioral, metadata and parity checks
- `.github/workflows/nhip-chu.yml` — CI and release automation
- `kumihan-vi.html`, `kumihan-vi.en.html`, `kumihan-vi.ja.html`
- `docs/install-nhip-chu-*.html` — three hosts × three languages

## Verification boundaries

Static code tests and deterministic package checks are not real-world host activation. Running one agent's checker over a static file does not prove browser rendering, font coverage, Vietnamese copy accuracy or official marketplace acceptance. Publishing source on GitHub does not equal installing or officially listing a plugin.

## Owner Result Gate

Record actual merge SHA, GitHub Release URL, ZIP count, GitHub Pages availability and CI status in the PR / release notes after publication. If an external publishing permission or CI failure blocks any step, report the exact blocker rather than treating the operation as complete. Do not reopen permission requests unnecessarily.
