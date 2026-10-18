# KUMIHAN Thai v0.1.0 implementation plan

Goal: deliver independent Thai guidance skills and trilingual introduction/installation site, then verify and publish the scoped GitHub release.

Architecture: additive Thai product under plugins/kumihan-th, shared resolver adds th-TH only. Reproducible stdlib builder packages complete local support into each skill. Static HTML pages preserve existing site grammar without editing Japanese or ZiHeng artifacts.

Spec: user-adopted packet KUMI-TH-V010-GOAL-RELEASE-20261018-R1 (SHA256 manifest verified, research treated as data).

Constraints: version 0.1.0; display KUMIHAN｜ดุลอักษร; locale th-TH; Apache-2.0; approved logo unchanged. Source text never normalized or rewritten. Rendering and native-host acceptance require observed evidence.

- [x] W00 Fresh-read current main, open PRs, permissions, existing builders. Base 5f4925460e118398f99003ff475bcc686c1c2e76. PR41 already merged before work.
- [ ] W01-W02 Implement explicit Thai context, 32 classified rules, source helper and four skill workflows; positive and deliberate negative integrity tests; 40 individually reported fixture outcomes.
- [ ] W03 Build independent manifests, 5 deterministic ZIPs, inventories and SHA manifest; validate archive paths, local references and approved logo.
- [ ] W04-W05 Follow new entry/web skill source as instructions; implement three actual homepages and nine localized guides with verified matching release asset names.
- [ ] W06-W07 Run Thai/source/distribution/site tests and Japanese/ZiHeng regression checks; inspect Chromium 320/375/768/1280 and 200% text size; independent bounded review.
- [ ] W08 Push scoped branch, create PR, wait exact-head CI; merge verified head when allowed, distinct Thai tag/release, existing Pages route.
- [ ] W09 Fetch published assets and compare SHA, GET all 12 pages, report observed state in KUMIHAN_TH_V010_GOAL_RESULT.md and JSON.

Review focus: Unicode mark changes, shifted protected ranges, emoji UTF-16 boundaries, unsupported host workflows, 320px/200% heading and guide overflow.

Execution: three nonoverlapping writers for core, packaging and site; one independent final reviewer. Continuous execution requested explicitly; redundant design/plan approval omitted. No native /goal tool exists (GOAL_NATIVE_UNAVAILABLE).
