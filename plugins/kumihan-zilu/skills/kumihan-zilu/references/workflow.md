# KUMIHAN｜字律

## 工作流程 / Workflow
先从请求确定 study/build/audit/refine、语言、文字体系、地区、媒体、受众与允许修改的范围。地区未知时保留 unknown，不把所有简体中文视为 CN。记录原稿与保护内容。
Determine mode, language, script, region, medium, audience and authorized changes from context. Unknown region stays unknown. Record supplied text and protected spans.

制定 Design Contract：内容目标、信息层级、原文保护、品牌语气、字体许可、输出环境、验收方式。不要建立固定字体、字号、行高、行长或统一四字标题模板。
Design for this project: hierarchy, brand voice, licensed assets, target environment and evidence. Do not impose a universal aesthetic template.

读取 rules/catalog.json、sources/public-sources.json 与所选 profiles/*.json。规则状态 implemented 指工作流或有限静态功能，绝不代表自动渲染支持。
Read the catalog, public sources and selected profile. Implemented workflow guidance is not automatic rendering support.

如要比较内容，使用 `python scripts/checks.py original.txt --candidate candidate.txt`。可选 helper 只读、离线、仅输出 JSON；不写文件。字节比较保留换行、BOM、Unicode与数字。退出码 1 表示差异。没有 candidate 时不报告原稿保全通过。
Optional offline helper returns JSON to stdout. Exact UTF-8 comparison detects changes, including line endings. It does not inspect glyphs or edit files.

