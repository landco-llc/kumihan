# KUMIHAN｜字律 — v0.1.0 candidate

简体中文的独立Skills与插件；说明和安装指引见本目录。 / Independent Simplified Chinese skills and plugins; see the product documentation in this directory.

- Four self-contained skills; three host bundles and twelve standalone skill ZIPs, all versioned v0.1.0.
- Canonical catalog: 36 items (14 implemented workflow/bounded-static, 20 advisory-only, 2 deferred). Source versions, sections, exceptions, severity and change authority remain separate from implementation priority.
- Original acceptance cases: 3 full pass, 41 not-run; all 44 narrower byte-preservation subchecks pass.
- Product suite: 8 tests pass. Twelve standalone archives execute offline in isolated directories.
- Chromium 154.0.8037.57: twelve pages × four widths × three conditions = 144 passing layout checks; 30 local links checked. Keyboard skip navigation passes. Text resize is simulated from computed sizes, not native browser zoom.
- Existing Japanese, ZiHeng, Korean and Thai representative tests/builders pass. Existing product files are unchanged; the shared landing template adds one product footer link.
- Claude Code 2.1.302 and Gemini CLI 0.64.0 manifest validators pass. Native model calls, icon/display behavior, marketplaces, resolved regional glyphs, Office/PDF, full GB/WCAG conformance and live deployment are unverified.
- One independent read-only review found a missing root evidence path in full bundles; fixed with a failing-then-passing archive regression test. Browser-detected text-resize overflow was also fixed and all layout conditions rerun.

See [TEST_REPORT.md](TEST_REPORT.md), [LIGHT_REVIEW.md](LIGHT_REVIEW.md), [downloads/MANIFEST.json](downloads/MANIFEST.json) and [downloads/SHA256SUMS.txt](downloads/SHA256SUMS.txt). SHA256SUMS covers the 15 ZIPs and manifest; individual inventories cover standalone skill files.

This is a release candidate awaiting final publication approval. A public source branch is not a GitHub Release, deployed Pages site or marketplace listing.
