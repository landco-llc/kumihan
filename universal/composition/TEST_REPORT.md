# Test report — bounded static scope

Environment: Python 3.12 / jsonschema 4.26.0; PHP 8.5.11 CLI in official Docker image, digest in evidence/php-image-digest.json. All container test runs use `--network none`, read-only repository and read-only temporary generated registry. Host PHP/Composer initially absent. No Composer install, live endpoint, native Office or rendering run.

## Composition candidate

`PYTHONPATH=universal/composition python3 -m unittest discover -s universal/composition/tests -v`: **48 tests passed** (evidence/final-review-green.log after the independent review fix pass). Includes six record kinds; strict unknown fields/version; exact source hashes; combining marks, CRLF, NBSP, ZWJ/ZWNJ, selectors, RTL/LTR, astral/empty; invalid UTF8/surrogate; byte split/off-by-one; duplicate/reference/range/coverage/cycle; critical extension/resource limits; locale/metadata; stale plan/observation; source-bound evidence; forged statuses/waivers; exact target pre/post bytes. Initial RED logs are retained as historical failures, not current regressions.

Selected P01–P07/P09/P14/P16–P19/P23–P26/P28–P30/P40 each run a separate static test. **21 partial, 19 not-run, 0 full product passes**. Matrix in evidence/P01-P40-matrix.json is complete. Host layout, dictionary/shaping, fonts, actual hidden CTA failure, scoped logo approval, native-language correctness and accessibility remain pending even where static preservation passes.

## Original repo suites

302 tests across 24 commands: **298 passed, 1 failure and 3 errors**, all four reproduced on original70727ff archive with unchanged files. Universal29/29 and default root21/21 passed. Root discovery does not include nested edition tests automatically; all nested suites were explicitly run.

| Exact command | Tests | Result |
| --- | ---: | --- |
| `python3 -m unittest discover -s tests -v` | 21 | PASS |
| `python3 -m unittest discover -s tests/accord -v` | 26 | PASS |
| `python3 -m unittest discover -s tests/arabic -v` | 20 | PASS |
| `python3 -m unittest discover -s tests/bn -v` | 10 | PASS |
| `python3 -m unittest discover -s tests/compasso -v` | 8 | PASS |
| `python3 -m unittest discover -s tests/equilibrio -v` | 16 | PASS |
| `python3 -m unittest discover -s tests/fa -v` | 8 | PASS |
| `python3 -m unittest discover -s tests/geuljjaim -v` | 9 | PASS |
| `python3 -m unittest discover -s tests/geuljjaim_adapter -v` | 2 | PASS |
| `python3 -m unittest discover -s tests/geuljjaim_site -v` | 3 | PASS |
| `python3 -m unittest discover -s tests/grafia -v` | 13 | PASS |
| `python3 -m unittest discover -s tests/hi -v` | 8 | PASS |
| `python3 -m unittest discover -s tests/id -v` | 9 | BASE FAILURE (reproduced) |
| `python3 -m unittest discover -s tests/km -v` | 5 | BASE FAILURE (reproduced) |
| `python3 -m unittest discover -s tests/lad -v` | 8 | PASS |
| `python3 -m unittest discover -s tests/nhip_chu -v` | 7 | PASS |
| `python3 -m unittest discover -s tests/satzbild -v` | 22 | PASS |
| `python3 -m unittest discover -s tests/sw -v` | 6 | BASE FAILURE (reproduced) |
| `python3 -m unittest discover -s tests/szyk -v` | 8 | PASS |
| `python3 -m unittest discover -s tests/thai -v` | 22 | PASS |
| `python3 -m unittest discover -s tests/ziheng -v` | 26 | PASS |
| `python3 -m unittest discover -s tests/zilu -v` | 10 | PASS |
| `python3 -m unittest discover -s tests/zu -v` | 6 | BASE FAILURE (reproduced) |
| `python3 -m unittest discover -s universal/tests -v` | 29 | PASS |

Base failures (evidence/base-failure-confirmation.json and baseline-*.log):
- tests/id: test_laras.Laras.test_archives — expected15 archives, observed0.
- tests/km: test_lumnung.Khmer.test_archives — missing plugins/kumihan-lumnung/downloads/MANIFEST.json.
- tests/sw: test_mizani.Mizani.test_released_archives — missing plugins/kumihan-mizani/downloads/MANIFEST.json.
- tests/zu: test_hlela.Hlela.test_packages — missing plugins/kumihan-hlela/downloads/MANIFEST.json.

These pre-existing distribution failures remain outside authorized edits; no suite was skipped or relaxed.

Additional observed commands:
- `python3 tools/build_dist.py --check`: exit0; 128 existing generated files up to date.
- `python3 tools/check_ja_type_011_cases.py`: exit0;11 internally consistent spec fixtures, no rendered claim.
- `python3 universal/tools/build_registry.py --output /tmp/kmc-evidence/registry.json`, then same command with `--check`: exit0,21 modules, deterministic unchanged snapshot. No committed/runtime registry rewritten.
- PHP8.5 Docker: lint7 PHP files (5 existing,2 composition) all clean; original `php /tmp/server/tests/smoke.php` PASS modules21; `php universal/composition/tests/php_resolver_smoke.php /evidence/registry.json` PASS14 cases. Existing server copied only inside disposable container to supply temporary registry, preserving repo byte-for-byte.

PHP command reproduction from repo root after registry generation:

```sh
env -u DOCKER_HOST -u DOCKER_CONTEXT -u DOCKER_TLS -u DOCKER_TLS_VERIFY -u DOCKER_CERT_PATH docker --host=unix:///var/run/docker.sock run --rm --network none --mount type=bind,src=/workspace/kumihan,dst=/repo,readonly --mount type=bind,src=/tmp/kmc-evidence,dst=/evidence,readonly -w /repo php:8.5-cli sh -c 'php -v; find universal/server/src universal/server/public universal/server/tests universal/composition -name "*.php" -exec php -l {} \;; cp -a universal/server /tmp/server; cp /evidence/registry.json /tmp/server/runtime/registry.json; php /tmp/server/tests/smoke.php; php universal/composition/tests/php_resolver_smoke.php /evidence/registry.json'
```

Public PHP SDK HTTP/Composer validation is **NOT RUN locally**: dependency lock belongs to #118 and vendor is absent. Upstream successful #101/#118 CI is separately inventoried; it is not claimed as candidate execution evidence. Full PHP Draft2020-12 runtime validation remains a separate gate; Python is the complete development validator.

Protection: 3,243 original tracked paths hashed; zero changes. Existing 21 module source trees, four MCP registrations/signatures, deployment, Composer/workflows, site and distribution outputs all zero diff. Immutable gzip and schema copy match approved uncompressed SHA256. See protected-comparison.json and manifest.

Independent review at1451aa0 identified two Important defects despite46 green tests. Both added regressions were observed RED and fixed in one pass; final48 green includes forged fact value/provenance and malformed registry. No second independent review claimed. Review artifact: evidence/independent-review.md.
