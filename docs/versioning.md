# KUMIHAN Version Naming Policy / 全言語版バージョン表記方針

**Owner decision:** 2026-10-19 JST — remove the `-preview` suffix from active version names for **every KUMIHAN language edition**.

## Normative current-version naming

- **User-facing version:** `vMAJOR.MINOR.PATCH`, for example `v0.1.8` and `v0.1.0`. Do not append `-preview`, ` preview`, `プレビュー` or `預覽版` to a current version label.
- **Canonical plugin manifests:** `MAJOR.MINOR.PATCH` without a leading `v` and without prerelease/build suffixes. Existing language-specific distribution manifest formats may contain `vMAJOR.MINOR.PATCH` for compatibility; treat it as the same numeric version, and do not introduce any suffix.
- **GitHub tags:** Japanese KUMIHAN uses `vMAJOR.MINOR.PATCH`; an independent language product uses its **existing product-specific slug** and `-vMAJOR.MINOR.PATCH`, such as `kumihan-ko-v0.1.0`. Do not force all languages to share a number.
- **ZIP filenames:** Preserve the already adopted per-product host/bundle/Skill filename patterns while removing the `-preview` suffix; include the product's actual version number. Do not silently change an `@mention` display name to include a version.
- **Platform and language independence:** Japanese, Traditional Chinese, Korean, Thai and all other editions retain their own version number and release lifecycle. A shared naming rule is **not** simultaneous publishing or version bumping.
- **Website/installation labels:** New/current distribution links, size/hash displays, site generator source text, update guides and metadata must point to the currently generated name and digest. Do not change localized customer copy except to reflect the new current version/status label.
- **Verification limits:** Removing “preview” from a name does **not** establish wider runtime, native host, print or accessibility acceptance. Continue to state genuine `not-checked` or other limitations accurately, without inventing qualifications.
- **Historical immutability:** Older published `*-preview` tags/releases and their ZIP contents are kept as historical artifacts. Do not force-move/delete old tags or silently replace their attachments. Prior release notes and validation reports may cite their exact historical original names.
- **Version release process:** Release artifacts are built from a fixed, verified source commit; verify manifests, ZIP members, sizes and SHA-256; create a *new* tag; publish only with Owner's approval; read back all public artifacts. When a language product has no release, renaming its active manifest does not authorize a first marketplace or GitHub release.
- **Existing parallel work:** The SEO Draft PR #93 and multilingual MCP Draft PR #101 are independent; incorporate the new naming policy through review/rebase rather than rewriting or merging unrelated branches without their own approval.

## Examples

| Product | Current display | Canonical manifest | Example release tag |
|---|---|---|---|
| Japanese KUMIHAN | `v0.1.8` | `0.1.8` | `v0.1.8` |
| Traditional Chinese KUMIHAN｜字衡 | `v0.1.0` | `0.1.0` | `kumihan-ziheng-v0.1.0` (if separately released) |
| Thai KUMIHAN｜ดุลอักษร | `v0.1.1` | `0.1.1` | `kumihan-th-v0.1.1` |
| Other language modules | Their existing `vX.Y.Z` | Their existing `X.Y.Z` | Keep their product-specific tag slug |

Current active manifests are protected by `tests/test_version_naming.py`. This test distinguishes canonical active package metadata from archived historical versions; it does not relabel past evidence.
