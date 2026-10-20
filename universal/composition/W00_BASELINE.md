# W00 — Fresh baseline (2026-10-20)

Implementation starts at `70727ff81ef0e14403f6145244b134ed3729a120`, tree `b55b77d07b2c0bfa18c9599a3067ada1b2818729`, clean working tree. Remote: landco-llc/kumihan. Branch: feat/universal-composition-core-20261020. No AGENTS.md found in repository or workspace ancestry. START_HERE.md, GOAL.md and all four reference documents freshly read. Approved gzip decompressed in /tmp; exact uncompressed SHA-256 `14d9226833c8ff1af8a92f8da56de4c852f003e87803f78c3ec8bf45c8c75cda`. Schema ID and Draft2020-12 verified. Reference archive immutable.

Fresh fetched main: `8b647cc752d7a9bc3db48356fa0ab7b221bb66d6`; latest commits #115 version display, #114 Search Console, #112/#111 site and #93 SEO. Initial local remote ref was stale; it was refreshed, never used as current baseline.

## Parallel ownership (all open Draft at inspection)

| PR | HEAD | Responsibility |
| --- | --- | --- |
| #101 | 5d32ea64618e33a171705363c223fe43060c31e1 | stack base, Universal runtime |
| #118 | 4b07ac069af688892595e1cf56934ecf40901dac | Composer lock / workflow |
| #116 | 839f7b492a8ab1578717b7938f6d4de73035d3c7 | publication control |
| #87 | df0c2929f66adab29628a7c7eb86cad0a9a7f4f3 | architecture |
| #120 | ce2fd8d23e4afb0816b5870625e02af3aa7a96b8 | JA research |
| #123 | 384f073ba122abde42f5836b15650c055928e724 | JA QA |
| #122 | 4f51a8a063abf7bc8bc5586575bff5304ee588b1 | ZH-Hant research |
| #125 | 1f205124cee538235f4cee384ca67f414c5e0e26 | JA W09 follow-up |

PR bodies and changed paths freshly read, recorded in evidence/fresh-pr-read.json. #101 reported checks successful (one event skip); #118 registry-and-php successful. This is upstream CI evidence, not our candidate's local runtime evidence.

## Existing interface and dependencies

Four registrations unchanged in server/public/index.php:
- kumihan_list_languages → listLanguages()
- kumihan_detect_language → detectLanguage(string text, string language='auto', string documentLang='')
- kumihan_get_guidance → getGuidance(string language, string medium='web', string mode='review', int limit=12)
- kumihan_review_text → reviewText(string text, string language='auto', string documentLang='', string medium='web')

Registry built only into /tmp: 21 modules, each preview_unverified; declared reference_guidance and source_preserving_review. Module locale arrays come from actual source locale files plus module IDs, not language prefixes. See evidence/registry-inventory.json. JA root catalog and Universal module rule scope remain distinct; no rule IDs/counts merged. Existing LanguageRouter offsets are bytes; sidecar offsets will be scalars.

composer.json declares PHP ^8.5, ext-json/fileinfo, mcp/sdk ^0.9.0, php-http/discovery ^1.20, nyholm/psr7 ^1.8, laminas/laminas-httphandlerrunner ^2.14, symfony/finder ^7.3 || ^8.0, platform 8.5.0. composer.lock and vendor absent; #118 NOT integrated. No dependency resolution/install attempted in its ownership scope.

Observed commands before implementation:
- python3 -m unittest discover -s universal/tests -v: exit 0, 29 tests.
- python3 -m unittest discover -s tests -v: exit 0, 21 tests (default discovery; nested editions separately checked in W08).
- python3 universal/tools/build_registry.py --output /tmp/kmc-evidence/registry.json: exit 0, 21 modules; repeat --check exit 0.
- php -v: exit 127 (binary unavailable); Composer likewise exit 127. PHP lint/smoke and SDK HTTP unavailable locally at baseline.
- jsonschema 4.26.0 already installed, matches requirements-dev.txt.

No observed baseline Python failures. No claim that local source matches deployed MCP. All pre-existing tracked files protected by evidence/protected-baseline.json, including public tool registration, deployment, workflow, module trees, published site and ZIPs. New code restricted to universal/composition/. W00 gate: isolation feasible without any shared-file edits.
