# Development checks

Install the development-only JSON Schema validator and run all checks:

```sh
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
python3 tools/check_ja_type_011_cases.py
python3 tools/build_dist.py --check
```

The contract tests validate all rule objects with Draft 2020-12, unique catalog
and schema ID sets in four Skills, six profiles, and the contents, manifests and
inventories of all 15 distribution ZIPs. Negative tests cover the missing
JA-TYPE-011 enum entry, duplicate IDs, invalid types/enums, and missing fields.
These checks establish source and packaging consistency, not rendered typography
or host compatibility. JSON Schema is a development dependency; the Skills and
standard-library distribution builder do not require it.
