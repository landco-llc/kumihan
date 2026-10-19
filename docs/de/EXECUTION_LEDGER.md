# KUMIHAN｜Satzbild execution ledger

2026-10-19 UTC. Owner scope: Issue #75 / GOAL_SATZBILD_V010.md. Native execution, W00–W11 sequential; no intermediate approval required.

## Plan and inputs

- W00–W03: read latest main, all WG01–WG04 and research excerpt; implement plugins/kumihan-satzbild/{entrypoints,references,rules,sources,profiles,locales,runtime,schemas,fixtures}; test explicit locale and source preservation.
- W04–W06: tools/build_satzbild.py generates closed skills and 15 ZIPs + manifest/checksums; test deterministic bytes, CRC, safe paths, host identity and no-write check.
- W07–W09: only after distribution gate, read finished Web skill and Japanese skill; reuse product_site/install_frame/base_copy and gateway generator; browser-measure 12 pages.
- W10–W11: focused CI, independent lightweight review, PR/main merge, immutable tag and public Release, Pages/asset readback and final report.

## W00 fresh read — passed

BASE_SHA main: 57c5cafb5fc023a9bc4892e87e21cb4deb682c9a. Workpack origin: bdb852431251d2f7a2e523df1a1746fcf2d48bfa. Latest main merged without conflict. No AGENTS.md present in repository or ancestor instruction directories. Compared Grafía and Compasso manifests and read existing packaging, canonical pages/layouts, base_copy, product_site and install_frame. Existing language packages remain unchanged (compare to origin/main). No private Drive originals or paid DIN text read; public research excerpt used. Unresolved source IDs are explicitly indexed as unresolved, not fabricated links.

Environment: managed Linux / Python 3, Node, Chromium, gh authenticated as repository owner. Cloud runtime skill applied. GitHub access succeeds; no external host installation assumed.

## W01–W06 distribution gate — passed

44 research candidates and 48 proposed cases retained separately from actual tests; 1 bounded CSS candidate rule only. Unknown locale stays unknown; de-DE/de-AT/de-CH explicit profiles, currency/timeZone independent. UTF-8 source bytes protected; helper read-only. Four self-contained skills with local official PNG and host metadata. Three host manifest structures follow existing repository adapters; native schema/import/icon rendering not-checked where no host runtime available.

Commands (2026-10-19 UTC):
- `python tools/build_satzbild.py`: 15 ZIPs and generated skill closures built.
- `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests/satzbild -v`: 21 tests passed (including 20 representative strings across 3 locales, 6 unauthorized mutation comparisons, schema, CLI nonmutation, deterministic ZIP bytes, CRC/member safety, inventories and host identities).
- `python tools/build_satzbild.py --check`: outputs current, mtime and bytes unchanged (tested).
- `python -m unittest discover -s tests -q`: existing root suite 14 passed. Further language regression runs follow at W10.

Native host invocation, provider marketplace listings, native German proofreading, Office/PDF and assistive technology remain not-checked. This gate permits W07 site work; it does not claim all 48 research cases passed.
