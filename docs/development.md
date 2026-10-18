# Development

The four skill folders under `skills/` share every file except `SKILL.md` and `inventory.json`. Edit shared files only in `skills/kumihan`; the build script copies them to the other three folders.

## Rebuild after a change

```sh
python3 tools/build_dist.py
```

This syncs the shared files, regenerates each `inventory.json`, rebuilds every ZIP in the three `downloads` folders, and rewrites their `MANIFEST.json`, `SHA256SUMS.txt` and `README.md`. Output is deterministic: running it twice produces identical bytes.

## Release a new version

The latest published preview is `0.1.5-preview` (tag `v0.1.5-preview`). Release tags and their downloaded assets are immutable release snapshots. For a subsequent release, choose a new version rather than rebuilding or moving the published tag.

```sh
python3 tools/build_dist.py --set-version 0.1.6-preview
```

This updates the version in all plugin and extension manifests, in `README.md` and `docs/*.md`, then rebuilds. Old-version ZIPs are removed from the `downloads` folders; Git history keeps them.

## Check before committing

```sh
python3 tools/build_dist.py --check
```

Exits with an error if any generated file is out of date. Python 3.9 or newer, standard library only. The skills themselves need no Python.
