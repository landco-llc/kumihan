# W07 independent lightweight review

One fresh read-only reviewer examined BASE `fe36ef38ba8cb03bb45d24b93649339782237113` through implementation commit `8fb68175da04054c43c2f3b11a0a4847e3ea8311` (tree `5c800742058e9fd0e5b8dbde05b5f9349c4a42ed`). Scope: admission, synchronization, shared renderers, Jekyll fragments, tests and Actions. Synthetic read-only reproductions; no remote writes, Release mutations, network verification or native-host claims. No P0/P1 found.

| Finding | Resolution and regression |
| --- | --- |
| P2: ZIP count/prefix checks allowed a required role to be replaced by an unrelated same-product ZIP | Exact per-edition normalized filename contracts now require every host/plugin/skill role. Test replaces the fixture ZIP with an unrelated same-product name while keeping manifest/checksums consistent: rejected. Source-only ZiHeng has an unconfigured flat contract because plugin and entry Skill share a basename; no invented release names. |
| P2: removed/draft/prerelease current Release could silently keep published facts while synchronization reported success | Current admitted stable tag must still exist in the full API response. Removed, draft, prerelease or older-only lists now raise before replacing facts. Tests assert the original snapshot is unchanged. |

Both reproductions failed before their fixes and pass as rejection regressions afterward. The fixes received producer verification, not a second independent review. This was the single bounded independent review requested by the Work.
