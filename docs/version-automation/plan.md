# Version automation Work plan

Spec: [Owner instruction](https://drive.google.com/file/d/19001jWMwFT7Qfz65V8RcaEJT9om70N6K/view), KUMI-VERSION-AUTO-WG00-WG04-20261019-01.
Execution: native autonomous WG00–WG04; one independent bounded read-only review at W07.

- [x] W00: fetch main, fix BASE fe36ef38ba8cb03bb45d24b93649339782237113, inspect generators and open PRs.
- [x] W01–W03: catalogue 21 source manifests and tag prefixes; verify complete per-product Release ZIP contracts against manifest, API, actual bytes, and pinned source. Store facts in assets/edition-versions.json. Test synthetic promotion, older/draft/prerelease/incomplete/unrelated/mismatch/failure/duplicate cases before implementing sync.
- [x] W04–W05: shared version renderer at existing builder boundaries, generated Jekyll fragments and README sections; no HTML hand-patching. Keep templates/copy and historical artifacts intact. Test coverage and idempotence.
- [x] W06: generators --check, complete unittest suite with baseline comparison of failures, representative Chromium 320/390/desktop/RTL and language switching.
- [x] W07: one independent read-only reviewer; fix actionable findings with focused regressions.
- [x] W08: fixed revision evidence, feature commit/push, Draft PR, current HEAD CI, Owner Gate.

Architecture: immutable verified published facts are separate from source versions. A release-published/manual workflow validates all bytes before changing anything, renders from shared facts, and uploads a proposed patch artifact with read-only repository permissions. Owner applies the patch through a reviewed PR; no main writes, merge, deploy, tags or releases.

Review focus: partial assets and changed release manifests; stale source versus published version; duplicate and out-of-order events; language-specific tag/file naming; stale copyable download commands and untranslated status labels. Offline tests and actual API/ZIP readback distinguish these from unverified live workflow delivery and native hosts.

Closeout: Draft PR #115. PR CI execution observed (final HEAD conclusions recorded in PR; Actions-permissions inspection 403), ZiHeng flat first-Release contract pending Owner, and publication remains Owner-controlled. See result.md for complete evidence and limits.
