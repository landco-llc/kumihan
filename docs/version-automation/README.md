# Edition version automation

Authority: [KUMI-VERSION-AUTO-WG00-WG04-20261019-01](https://drive.google.com/file/d/19001jWMwFT7Qfz65V8RcaEJT9om70N6K/view).

`assets/edition-versions.json` is the single machine-readable source for 21 independent editions. `source_version` is read from each edition's active plugin manifest. `published_version`, tag, publication time, pinned source SHA/tree/manifest digest and downloadable ZIPs describe an actually verified stable Release. Unpublished source packages do not become a formal Release or a working native installation through a filename change.

## Synchronize and render

```sh
# Requires complete tag history, HTTPS access to GitHub API and Release assets.
git fetch origin --tags
python tools/sync_edition_versions.py
python tools/build_seo.py
python tools/build_seo.py --check
python tools/check_seo_preservation.py
python -m unittest discover -s tests -p test_edition_versions.py -v
```

`sync_edition_versions.py --check` also re-downloads and verifies without writing. No renderer uses a runtime API. Stable Releases are selected by an edition's exact existing tag prefix and semantic version, never the repository-wide `/latest`. Source versions and published versions can differ.

Admission requires the pinned source manifest version, the exact adopted product-specific host/plugin/skill ZIP-name contract (`assets/edition-release-contracts.json`), exact Release/manifest/checksum asset sets, actual ZIP sizes and SHA-256, API digests when provided, and ZIP CRC integrity. Non-Japanese releases carry `MANIFEST.json` and `SHA256SUMS.txt`; the Japanese Release has 15 ZIPs only, so its three host manifests come from the immutable source tag. Japanese checksum links also point to that pinned source. A network/API/hash/manifest error aborts the entire update before the facts file is replaced. Repeated events produce identical facts; older releases cannot downgrade an edition. A missing, draft or prerelease replacement for the current verified Release aborts verification while retaining the snapshot. Drafts, prereleases and unrelated tags cannot promote it.

The existing HTML generator boundaries consume the shared renderer. Jekyll Japanese/Korean pages consume generated version/body fragments; authored installation Markdown, Korean source pages and translation JSON remain the inputs. ZIP links and copyable commands use verified concrete asset names. Unpublished formal downloads are disabled and labelled while source-repository links remain available. New metadata is Japanese/Chinese where provided and explicitly `lang="en"` otherwise; native metadata translations are not claimed.

README's table and managed status spans use the same facts. `build_version_site.py --preservation` runs last in the shared build pipeline and records exact reviewed before/after hashes for this feature's allowed body/Jekyll/README changes. The original SEO snapshot remains immutable; all other protected bytes, including every existing ZIP and license, stay subject to its original hashes. This overlay is regression evidence, not an independent authorization mechanism.

## Actions and Owner Gate

`.github/workflows/version-automation.yml` listens to `release: published` and manual dispatch. It checks out trusted main, verifies all Releases, regenerates locally, runs checks, then uploads a bounded patch artifact and its fixed base SHA. Its token has **contents: read**. It does not push, merge, create tags/Releases, change secrets/settings or deploy Pages. A no-change run emits an empty patch.

Owner reviews and applies a nonempty artifact through a feature PR. This is the safe alternative to automatic main updates: unattended publication is intentionally **not fulfilled**. The workflow cannot receive real events until Owner merges it. Real Release-event delivery, repository Actions availability, applying the patch, merging and subsequent Pages publication remain human-controlled/unverified. No workflow dispatch or real Release mutation was used in this Work.

## Unpublished ZiHeng first-Release condition

The 15 source ZiHeng archives are verified locally, but its source plugin ZIP and entry Skill ZIP have the **same basename** in different directories. GitHub Release assets require distinct flat names. There is no adopted flat asset-name/role mapping to infer safely. Its release contract is explicitly unconfigured; Owner must adopt unique Release asset names and corresponding source-role mappings before a first formal Release can be admitted. No existing ZIP was renamed. ZiLu's 15 source names are distinct and its future-release contract is configured. Synthetic first-publication tests exercise admission with an adopted contract without creating any real tag/Release.

## Evidence

- [`plan.md`](plan.md): W00–W08 work plan.
- [`unpublished-source-zips.json`](unpublished-source-zips.json): integrity evidence for both unpublished source editions (15 ZIPs each).
- [`preservation.json`](preservation.json): exact permitted body/README changes against the original SEO snapshot.
- [`rendered/report.json`](rendered/report.json): real Chromium measurements; screenshots alongside it.
- [`result.md`](result.md): fixed revisions, coverage, checks, review, CI and remaining limits at closeout.

Native AI-host installation/invocation, all-device rendering, native screen-reader use, Office/PDF output, marketplace acceptance and a live new Release event are not established by these checks.

## WD09–WD12 delta (2026-10-20 JST)

Authority: `KUMI-PR115-OWNER-GATE-DELTA-20261020-01` ([instruction](https://drive.google.com/file/d/1JE7okEGkvcigtzjSgOOFAdKzDC5HOq7f/view)). The original W00–W08 reports remain historical evidence. The delta and current limits are in [wd09-wd12.md](wd09-wd12.md).

Chinese source downloads now have a separate offline admission path: the existing per-host source manifests must match source version, exact full archive path, size, SHA-256 and ZIP CRC. Admitted existing relative/raw-main URLs remain clickable and explicitly labelled `Source ZIP`; the adjacent status still says Release unpublished. No `published_version`, Release asset URL, archive name or marketplace/native-host claim is invented. Full paths distinguish ZiHeng's plugin and entry Skill with identical basenames. Untrusted remote hosts, absent files, other editions and undeclared archive versions are not admitted. Corrupt source bytes abort generation. Formal Release admission and its exact role contract are unchanged.

**Automation mode: PATCH_ONLY_CONSTRAINED / 半自動. 自動公開未実装.** A patch artifact does not update the public HTML/README. Owner must download/check the base SHA, apply through a feature PR, run required CI and review, merge, then verify the legacy main Pages build. No-change events are no-ops; failed verification retains the prior snapshot. Withdrawal of the current Release aborts rather than silently downgrading. Rollback requires an Owner-reviewed revert PR and Pages verification; deleting a Release is not a rollback/deploy operation.
