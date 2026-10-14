# Development

The four skill folders under `skills/` share every file except `SKILL.md` and `inventory.json`. Edit shared files only in `skills/kumihan`; the build script copies them to the other three folders.

## Rebuild after a change

```sh
python3 tools/build_dist.py
```

This syncs the shared files, regenerates each `inventory.json`, rebuilds every ZIP in the three `downloads` folders, and rewrites their `MANIFEST.json`, `SHA256SUMS.txt` and `README.md`. Output is deterministic: running it twice produces identical bytes.

## Release a new version

Versions are written as `0.1.4-preview` in manifests and file names, and as **v0.1.4 preview** in text. Each release raises the last number: the release after `0.1.4-preview` is `0.1.5-preview`.

```sh
python3 tools/build_dist.py --set-version 0.1.5-preview
```

This updates the version in all plugin and extension manifests, in `README.md` and `docs/*.md`, then rebuilds. Old-version ZIPs are removed from the `downloads` folders; Git history keeps them.

## Check before committing

```sh
python3 tools/build_dist.py --check
```

Exits with an error if any generated file is out of date. Python 3.9 or newer, standard library only. The skills themselves need no Python.
