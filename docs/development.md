# Product development

This branch is a documentation and contract draft. Rules, profiles, sources, skills, packaging scripts, fixtures and CI from separate implementation branches are not integrated here. Commands below describe the frozen packaging interface and become runnable only with those inputs; do not add placeholder files to satisfy links or commands.

Development uses Python 3.12+, `unittest` and pinned `jsonschema` development dependencies. Follow the integrated `requirements-dev.lock` when available; consumers do not install those dependencies. Do not install unpinned packages to make a draft appear complete.

After integration, run the available scoped tests with `python -m unittest discover -s tests`. Use offline schema registration and original synthetic fixtures. Inspect failures and actual outputs; do not describe missing checks as passes.

The frozen packaging commands are:

```sh
python scripts/build_skills.py --root . --output-dir dist --version 0.1.0 --source-epoch 0
python scripts/verify_bundle.py --archive dist/kumihan-0.1.0.zip --expected-version 0.1.0
```

The output directory must not exist before building. Choose and record a fixed source epoch appropriate to the candidate; `0` above is a deterministic example, not release metadata. Version arguments identify package format intent, not publication. Validate complete integrated inputs before building. Bundle checks cover inventories, digests, safe relative paths and self-contained references, not actual host behavior or authenticity.

Future release/report/public-boundary commands remain proposed until their implementations and CLI interfaces are available. Do not advertise them as executable. For documentation-only work, review bilingual facts, relative links, owned-path diff, LICENSE byte identity and public boundaries. Product-wide build/link checks that need pending files must be reported as deferred with the missing inputs named.

Keep rules canonical and let the builder generate standalone copies. Never hand-edit generated output. [Contributing](../CONTRIBUTING.md), [repository instructions](../AGENTS.md) and the [release checklist](release-checklist.md) describe public development boundaries.
