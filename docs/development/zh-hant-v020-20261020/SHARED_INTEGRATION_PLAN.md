# Shared integration plan — PR #122

Owner approved this dedicated branch for the six shared Ziheng changes, generated displays, tests and evidence. Runtime Parent owns lifecycle and publication. No main merge or production publication is authorized.

Inputs: HEAD `773289a1dc7d04627a7cd3b539eb640f65c40fa8`, TREE `148a93f3de8c80ad2b40bafee3d3962c50540e84`; main `8b647cc752d7a9bc3db48356fa0ab7b221bb66d6`; read-only PR #120 `ce2fd8d23e4afb0816b5870625e02af3aa7a96b8`. Main is already an ancestor; no synchronization is needed. Git remote is `landco-llc/kumihan`; branch is `feat/zh-hant-v020-research-20261020`. No unidentified working-tree edits were present. Global AGENTS guidance applies; no repository AGENTS file exists.

The unapplied patch blob is `e77d8353f68bc67180d905a0a3fa1016cd3d7e2a`; `git apply --check` passed. Three-way record inspection confirms its zh-hant source-only JSON change retains all publication fields and other editions. The proposed overlay adds exact Ziheng protected hashes and changes only generated display after-values; existing non-Ziheng protected/body records remain. The original patch remains evidence; implementation applies its six shared source changes then regenerates HTML and the overlay from generators. No HTML patching by hand.

Root baseline reproduced 112 tests / 4 failures, matching the four previously recorded failures exactly; see `evidence/shared-root-before.log`. Add six named regression contracts before integration and observe their source/display RED. Reuse existing packaging/transition negative tests and extend unknown-path, baseline, history tamper, legacy deletion and version-label coverage.

`evidence/shared-integration-baseline.json` fixes all edition records, all tracked distribution ZIPs and download metadata, the original SEO snapshot, frozen source-transition preimages and inactive release contract before implementation. Fifteen current and fifteen historical Ziheng ZIPs are distinct fixed sets. No package regeneration is planned. All other-language distribution bytes must remain equal.

Shared source ceiling: README ZH-HANT row only; assets edition source_version for zh-hant only; additive transition hooks in build_version_site/check_seo_preservation; generated preservation overlay; strict retained-manifest and current-version assertions in test_version_naming. Linked helper correction only upon reproduced bug. New boundary tests: tests/test_ziheng_v020_shared_integration.py. Evidence ceiling: this development directory. Transition after-values will be derived from actual generated pages; frozen preimages remain unchanged.

Original patch paths (six shared paths and authorized derived gateway/LP/install displays):

- `top-zh-han.html`
- `top-ja.html`
- `top-pl.html`
- `top-th.html`
- `top-hi.html`
- `kumihan-zh-han.html`
- `top-de.html`
- `top-ko.html`
- `top-pt.html`
- `README.md`
- `top-fr.html`
- `top-it.html`
- `kumihan-zh-han.en.html`
- `top-km.html`
- `top-sw.html`
- `top-id.html`
- `top-zh-cn.html`
- `kumihan-zh-han.ja.html`
- `top-ru.html`
- `top-es.html`
- `top-fa.html`
- `top-zu.html`
- `top-bn.html`
- `index.html`
- `top-ar.html`
- `top-vi.html`
- `tools/check_seo_preservation.py`
- `tools/build_version_site.py`
- `docs/install-ziheng-claude.ja.html`
- `docs/install-ziheng.ja.html`
- `docs/install-ziheng.html`
- `docs/install-ziheng-gemini.en.html`
- `docs/install-ziheng-claude.en.html`
- `docs/install-ziheng-claude.html`
- `docs/install-ziheng-gemini.ja.html`
- `docs/install-ziheng-gemini.html`
- `docs/install-ziheng.en.html`
- `assets/edition-versions.json`
- `tests/test_version_naming.py`
- `docs/version-automation/preservation.json`

## Reproduced display dependency

Before integration, old LP ZIP links said “Download latest” / “最新版のダウンロード” or generic source ZIP while their URL remained v0.1.0. With source0.2.0 the old/new distinction would be ambiguous. The new link-label regression reproduced this missing version label. Necessary Ziheng generator source dependencies are `tools/build_ziheng_site.py`, version-state fields in `assets/ziheng-site-copy.json` and the six `templates/ziheng/docs/install-ziheng-{claude,gemini}{,.en,.ja}.html` status paragraphs. The generator labels exact Ziheng legacy ZIP anchors v0.1.0 before the existing shared metadata decorator; generic shared version_display is unchanged. Only obsolete pending-integration/version phrases are replaced; other prose and every URL remain. Applied kumihan-ziheng scoped zh-Hant-TW web refine/source protection.

## Implementation verification before review

Root suite: 118 tests PASS, no skipped tests; isolated version naming: 7 PASS; six new boundary methods PASS after source/display RED. Full SEO generator check PASS (274 source pages, sitemap272 URLs); preservation and whitespace checks PASS. Logs are `evidence/shared-{root-before,root-after,regression-red,regression-green,naming-after,seo-after}.log`. Isolated naming initially reproduced a missing tools import path for the newly added retention import; explicit sys.path setup corrected it, then isolated and full root suites passed.

All 255 fixed files retain bytes/size/digest, including old15/current15 ZIPs, other-language distributions, original SEO snapshot, frozen preimages and inactive Release contract. Existing preservation overlay rows removed:0; changed rows are README +12 Ziheng bodies +22 gateway Ziheng cards. Masking the Ziheng card proves every other byte in each changed gateway unchanged. Exact edition comparison proves zh-hant source_version is the only edition fact change. No ZIPs were rebuilt. Publication facts remain unpublished; no v0.2.0 main URL is reported working.

This is writer-run implementation evidence, not an independent audit or hosted CI acceptance. Runtime Parent will obtain one bounded read-only review, independent verification, read-only PR #120 coexistence evidence and final-head CI. Final lifecycle RESULT/NEXT_GATE/TEST_REPORT/MCP_HANDOFF/revision are owned by the later publication worker.

## Hosted cross-locale consumer correction

The first real hosted run on3d7a892 completed8 workflows successfully, including all four originally failing workflows, but newly triggered ZiLu Other-language regression exposed12 zh-Hant rule-output digest mismatches in the Thai suite. Raw failures and all9 checkout identities are in evidence/hosted-ci-first.json and associated logs. The resolver and original Thai fixture remain unchanged; all15 Ziheng rule records differ from main only in already-reviewed revision/case_ids metadata. Exact diagnosis: evidence/shared-ci-diagnosis.md.

Necessary shared regression dependency added to scope: tests/thai/test_core.py. It keeps the original18 contexts, six Japanese full output assertions and twelve complete Ziheng output assertions. A pinned locale-output-transition.json records exactly12 old→new output hashes; admission pins the original Thai baseline bytes, fixed originalbase, exact12 locale/media entries, originalcontext/old output hashes, exact registered Ziheng rules source old/new hashes and existing frozen source-transition validation. Full current output must match the explicit after digest; no metadata stripping, fixture rebaseline, skip or workflow modification. New negative coverage in the existing Ziheng integration test rejects unknown locale/media/hash/context, missing/additional/modified fixture entries, altered originalbaseline, oldhash, candidatebytes and matched candidate/ledger tampering. This bounded correction was validated separately after the single source review; no additional formal review is claimed.
