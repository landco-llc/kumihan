# Universal MCP — ZiHeng v0.2.0 source handoff (source candidate only)

This draft branch is stacked on PR #101's implementation branch. It copies the merged, publicly reviewed KUMIHAN｜字衡 v0.2.0 product source from main at `de6ec7d6c393a832ffff8f842be47a5335d3ecd0`; existing unrelated language module sources are left untouched.

The canonical `universal/languages.json` already registers `zh-Hant` as `plugins/kumihan-ziheng`. Rebuilding the ephemeral `universal/server/runtime/registry.json` via `python3 universal/tools/build_registry.py` now yields 21 modules and ZiHeng version `0.2.0`, 15 regional rules, regional locale identifiers and updated module checksum. The runtime registry is intentionally Git-ignored and must be built in authorized deployment staging, not committed with private server configuration.

The registry builder currently ingests plugin metadata, entry Skill Markdown and structured rules; it is **not** a direct executor of v0.2.0 context/evidence helpers. TW/HK applicable/deferred rule semantics cannot be claimed as a live MCP feature until the consumer contract is explicitly implemented and tested. No edits to the MCP server, production PHP, credentials, deployment configuration, or other module code are made.

The connected live MCP observed in this session still reports ZiHeng `0.1.0` with SHA `7e3980c292521b97f6606b23fe819eb670e3b4dd55eecfb644a8c60c62fc4ab4`; source CI/PR merge does not update the live service.

**Verification:** `python3 universal/tools/build_registry.py` and `python3 -m unittest discover -s universal/tests -p test_ziheng_v020_registry.py -v`. Existing macOS `universal/tests` full suite cannot be used to claim Linux deployment acceptance; several tests require remote Linux and fail with `NOT_REMOTE_LINUX`.

**Next Owner Gate:** after source tests on PHP 8.5 Linux and a review of PR #101 integration, rebuild the private runtime registry, pin its SHA, deploy only through authorized private non-web root, check protocol and rollback path. No tag/Release/Marketplace or common document creation is authorized. PR #120 is unchanged.
