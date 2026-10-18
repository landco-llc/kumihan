# KUMIHAN｜字衡: Claude and Gemini

Source-of-truth is the ZiHeng standalone skill directory, generated from shared
CONTENT/DESIGN/EVIDENCE and the zh-Hant TW/HK rule catalog. The host packaging
builder reads existing stand-alone ZiHeng skill folders without touching Japanese
KUMIHAN files.

```
python3 tools/build_ziheng.py --check
python3 tools/build_ziheng_hosts.py
python3 tools/build_ziheng_hosts.py --check
python3 -m unittest discover -s tests/ziheng -v
```

- Claude: Marketplace uses the *same existing repository*, new relative plugin
  `./plugins/kumihan-ziheng`; 1 bundle ZIP and 4 Claude chat skill ZIPs.
- Gemini: 1 standalone CLI extension ZIP with extension manifest at ZIP root,
  plus 4 flat skill ZIPs for supported Gemini Apps.
- Gemini CLI's direct GitHub monorepo-root install selects the *Japanese* KUMIHAN
  root extension. ZiHeng's CLI bundle must be installed from a locally extracted
  folder, or use supported individual CLI skill install commands.
- Source text and regional profiles remain unchanged; no automatic conversion.
- Platform detection/invocation is *not-checked* until tested in Claude/Gemini.

The official brand separator stays U+FF5C (`｜`). The plugin's display name is
`KUMIHAN｜字衡`; distribution ZIPs contain versions in filenames.
