# /goal · KUMIHAN｜Accord v0.1.0

## Goal

Implement, test, package and publicly release French typography guidance in the existing landco-llc/kumihan repository, keeping other language editions unchanged.

## Fixed owner constraints

Display name KUMIHAN｜Accord; descriptions Español + English; technical IDs ASCII; ZIP filenames v0.1.0; gratis/free Apache-2.0; lightweight audit only; owner authorized public GitHub source and assets. Do not claim an external marketplace listing.

## Self-contained workgroups

- W00: Fresh read repository main and FR research in /RESEARCH/FR.
- W01: Region, institution and medium choice, rule catalog and sources.
- W02: Preserve source and build bounded, read-only text checker.
- W03: Four independent skills with embedded instructions and data.
- W04: ChatGPT/Codex plugin, Claude Code plugin and Gemini CLI extension.
- W05: Deterministic 15 ZIP releases, SHA-256 and manifest.
- W06: Unit checks, public French landing, install guides and bilingual metadata.
- W07: PR/CI, merge, public GitHub Release and HTTP/asset readback.

Finish workgroups end-to-end without human ZIP handoffs; stop only on an actual external Gate. Static QA is enough for initial OSS release, but keep native-host, browser, Office/PDF, French editor review and 48-case acceptance marked NOT_RUN if not performed.

## Environment / Placement

Repository: https://github.com/landco-llc/kumihan
Work branch: feat/accord-v0.1.0
Source: plugins/kumihan-accord/
Python build: tools/build_accord.py
QA: tools/check_accord.py, tests/accord/
Site: kumihan-fr.html
Automation: .github/workflows/accord.yml
Release tag: kumihan-fr-v0.1.0

## No work on unrelated products

Do not mutate files under other plugins or package identities. Homepage may add an Accord link; Claude marketplace may append its source entry. Never infer unperformed runtime verification.
