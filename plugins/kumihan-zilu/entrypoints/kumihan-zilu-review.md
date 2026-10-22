---
name: kumihan-zilu-review
description: "用于简体中文只读审查，保护原稿并区分静态与实测证据。 Use for Simplified Chinese read-only review, preserving source text and separating static from rendered evidence."
---

# KUMIHAN｜字律

只读审查 / Read-only review。独立安装，无需其他语言插件。 / Independently installable; no other language plugin required.

1. 从请求确定模式、zh-Hans-CN或明确地区、媒体与修改范围。未知地区不得推定。 / Establish mode, locale, medium and authorized changes; do not infer unknown regions.
2. 读取 [流程](references/workflow.md)、[本任务指引](references/review.md)、[只读审查](references/review.md) 与 [范围](references/coverage.md)。 / Read workflow, task guidance, review limits and coverage.
3. 读取 [规则](rules/catalog.json)、[依据](sources/public-sources.json) 和所需 `profiles/*.json`。保留原文、数字、商标、Unicode；禁止隐式繁简转换、NFKC或添加空格。 / Consult rules, sources and medium profile. Never silently normalize, convert scripts or edit text.
4. 制作时按当前项目的 Design Contract 选择结构、字体许可与验收条件；审查默认只读。 / Build under the project's Design Contract; audit remains read-only.
5. 返回实际执行的证据与未检查项，候选文字修改需单独呈现。 / Return performed evidence and untested scope; keep editorial proposals separate.

可选离线辅助：`python scripts/checks.py original.txt --candidate candidate.txt`。输出 JSON；不渲染或改写。 / Optional offline helper compares complete text and prints JSON; it does not render or edit.

示例：请保留原文检查这个页面。 / Example: Review this page while preserving its source text.

纵排任务先选择目的，再读 [纵排指引](references/vertical.md) 与 `rules/vertical.json`；使用 `profiles/cn-vertical-*.json` 或 `profiles/cn-classical-reference.json`。保留原稿，按媒体实测。 / For vertical tasks select a purpose, consult vertical guidance and rules, preserve source and validate target output.
