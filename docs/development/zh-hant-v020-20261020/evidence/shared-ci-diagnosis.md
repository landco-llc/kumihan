# PR 122 ZiLu CI diagnosis

Read-only diagnosis at fixed HEAD `3d7a892613cdec0f04259bacc00becbe5c61c70f`, branch `feat/zh-hant-v020-research-20261020`, repository `landco-llc/kumihan`, Draft PR 122. Parent owns lifecycle. No repository changes, commits, pushes or lifecycle transitions performed.

## Observed failure

Hosted run `39373267987`, job `118465630717`, workflow `ZiLu product and site`, event `pull_request`, failed in `Other-language regression`. Checkout was synthetic merge `7822061`, merging the exact candidate into main `8b647cc752d7a9bc3db48356fa0ab7b221bb66d6`.

ZiLu's own 10 tests, `build_zilu.py --check` and `build_zilu_site.py --check` succeeded. Other-language root suite 118 tests, Ziheng 26 tests and Geuljjaim 9 tests succeeded. Thai suite ran 22 tests and failed in 12 subtests of `tests/thai/test_core.py:40`, `LocaleTests.test_existing_locale_outputs_match_base`: zh-Hant-TW and zh-Hant-HK across all six media. Later commands in that shell and Host manifest/browser steps did not execute because the shell failed. Their status must not be inferred from earlier success.

Workflow source `.github/workflows/zilu.yml` was not changed. Shared integration changed `top-zh-cn.html`, which matches its existing path trigger. Thus previously unexercised cross-locale regression is now visible. Root unittest discovery does not recurse into these nested suites because they are not packages; its green result did not cover Thai.

## Exact cause and unchanged boundaries

`tests/thai/locale-baseline.json` was introduced by Thai commit `06d196c1fe6b8cac9e084f5e6d27723872b5d26f` to preserve outputs from base `5f4925460e118398f99003ff475bcc686c1c2e76`. It contains 18 locale/medium records and SHA-256 of canonical JSON (`ensure_ascii=False`, sorted keys, compact separators). No committed fixture-generation command was found; consumers must preserve this historical fixture rather than fabricate a new baseline.

Fixture SHA-256 remains `52307ccadbe04ced592d2854c4d4ecfbb15551ba281d70a104cec6eb750b4f3a`, byte-identical to main and candidate baseline. `tools/locale_resolver.py` also remains unchanged. For zh-Hant it selects Japanese common content/design/evidence records plus the regional records from `plugins/kumihan-ziheng/rules/zh-hant.json`.

The Ziheng rule source changed from main SHA-256 `a478e959f8521843c28ab57f848f0c2614d7768cfbddc30f1546cda5627442ef` to candidate SHA-256 `5079baacb1b0093e9b8fdec095232a79c152a3671a2cc3b4675be2fabefd7555`. The latter is already identical at `773289a1dc7d04627a7cd3b539eb640f65c40fa8` and current HEAD. Existing `docs/development/zh-hant-v020-20261020/source-transition.json` explicitly registers this path and exact before/after file hashes.

All 15 ZH-HANT rule records change exactly two metadata fields: revision 1 to 2, and empty case_ids to the reviewed Fxx mappings. IDs, ordering, all requirements and all other fields remain equal to main. Japanese common rule data is unchanged. All 18 context hashes and all six Japanese output hashes still match the historical fixture.

## Exact current digest admission

Each row below applies separately to the listed three media, making exactly 12 allowed transitions.

| Locale | Media | Historical rules SHA-256 | Current rules SHA-256 |
| --- | --- | --- | --- |
| zh-Hant-TW | web-editorial, web-marketing, web-ui | `6df7ec87d1cd08159f05b9d6b531c1ec0b0985c2e19bc91ba23156299a54db8d` | `80483b225146cad3cb9dd14eaebccc424c4b52dc8cf2de2f6d94eeca174d2274` |
| zh-Hant-TW | report-document, presentation, display-copy | `b3ebeed3ab1ee647130640950b92839252aaa06371e99a71c704baa7357ec510` | `405c76f81898ea981628fb0219a29c656beec420a654e24cbb2daae359ebe3cd` |
| zh-Hant-HK | web-editorial, web-marketing, web-ui | `755880562622602c17dc6b384d0752fefe8cd90fff4d7d0582e98ca5b849782b` | `d7f3834a7e516c8102ebb92535edf3c98bc8dca1902ca830c6620c7139615892` |
| zh-Hant-HK | report-document, presentation, display-copy | `9d4637679e22ba4830470a7a455ad1f242716a2f81ec85de9d319caf83f10008` | `8e75b02d95a15c7f1ca85d9cf6cc700398ce28c10bd533e93e7ad31bfc03e29b` |

## Reproduction and bounded correction recommendation

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/thai -v` reproduced the same 22 tests / 12 failed subtests locally. A read-only Python comparison loaded old source via `git show 8b647cc:path`, compared all 15 records, asserted only revision/case_ids differ, then deep-copied each resolved current output and restored only those two ZH-HANT metadata fields. The resulting canonical digest matched every historical fixture record across all 18 locale/medium combinations. Current output digests were independently computed and match the hosted failure values above. This projection is diagnostic evidence; generic metadata stripping is not an acceptable production admission.

Parent accepted a bounded correction direction: preserve the original fixture bytes, base identity, records and every context hash; add exact Ziheng transition evidence and a minimal admission in the shared regression consumer `tests/thai/test_core.py`. Require the original fixture SHA, exact locale/medium/before keys, the registered source path with exact old/new file hashes, existing frozen transition baseline/authority checks, and full current resolver-output equality against the explicit after digest. Preserve every Japanese original assertion. Reject missing, additional or modified transition rows, changed original fixtures, unknown locale/media, unknown before digest, changed source/ledger/baseline, and mutated current guidance output. The new evidence must describe this specific transition, not claim a new historical baseline.

Add focused negative regression coverage under Ziheng integration tests. No workflow trigger/command removal, skip, xfail, broad locale bypass, dynamic expected digest from current output, baseline regeneration or fixture replacement is needed. No ZiLu/Thai plugin source or other-language distribution changes are needed. Full ZiLu workflow and separately triggered Thai workflow remain necessary after correction, because later hosted steps were not reached in this run.

This is a debugging result and bounded recommendation, not formal independent audit or CI acceptance for a corrected candidate.
