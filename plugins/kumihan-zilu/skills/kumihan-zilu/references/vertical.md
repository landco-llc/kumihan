# 纵排目的与验证 / Vertical purpose and validation

v0.1.2 strengthens guidance and read-only context lint. It is not an automatic composition engine.

Select `cn-vertical-reading`, `cn-vertical-display`, `cn-vertical-publication-gb` or `cn-classical-reference`. Record region, medium, selected standards, edit authority and actual renderer. Keep horizontal workflows unchanged.

## KH-CN-V001 用途与范围 | Purpose and scope

先记录地区、媒体、目的和修改权限；GB体裁需明确选定版次与条款。 | Record region, medium, purpose and edit authority; select GB editions and clauses explicitly.

## KH-CN-V002 原稿与派生物 | Source and derivatives

保留Unicode、商标、数字和原文；编辑派生物须另有授权与差分。 | Preserve Unicode, brands, numbers and source; authorize and diff editorial derivatives separately.

## KH-CN-V003 真实纵排 | Real vertical composition

连续纵排使用writing-mode: vertical-rl；width:1em或逐字br不是同等实现。 | Use writing-mode: vertical-rl for continuous text; width:1em or per-character BR is not equivalent.

## KH-CN-V004 列方向 | Column direction

通常上到下、列右到左；vertical-lr例外记录目的，不逆转DOM。 | Read top to bottom, columns right to left by default; justify vertical-lr and never reverse the DOM.

## KH-CN-V005 实际字体 | Resolved fonts

检查实际SC字形、缺字和fallback；CSS名称与lang不足以证明。 | Inspect actual SC glyphs, missing characters and fallback; CSS family and lang are not proof.

## KH-CN-V006 字体功能与描画 | Font features and shaping

区分GSUB/GPOS/vert、vmtx/VORG和实际描画；CSS不共同强制vrt2。 | Separate GSUB/GPOS/vert, vmtx/VORG and shaping; do not force vrt2 in shared CSS.

## KH-CN-V007 字体权利 | Font rights

记录字体来源、版本、哈希和使用、嵌入、再分发许可；不附未授权字体。 | Record font source, version, hash and use/embedding/redistribution rights; bundle no unlicensed fonts.

## KH-CN-V008 约物字形 | Punctuation glyphs

在目标输出确认句读、引号、括号、破折号和省略号的纵形位置；不替换原稿码位。 | Inspect vertical punctuation and paired marks in output without replacing source codepoints.

## KH-CN-V009 禁则与双字符号 | Column boundaries and paired marks

实测列上端和下端禁则；——、……内部断开与整个符号的位置分别检查。 | Inspect top/bottom column boundaries; distinguish internal splitting of ——/…… from whole-mark placement.

## KH-CN-V010 书名体裁 | Book-title presentation

保持《》；只在获准GB出版派生物中检查书名左波线，保留语义范围及复制契约。 | Keep 《》; inspect a left wavy title mark only in an authorized GB derivative with semantic range and copy contract.

## KH-CN-V011 着重与专名 | Emphasis and proper names

选定GB体裁时检查着重点在右、专名线在左，分别核对与ruby、波线的碰撞。 | For selected GB presentation inspect emphasis on the right and proper-name line on the left, including annotation collisions.

## KH-CN-V012 数字方向 | Numeric orientation

GB/T 15835-2011选定范围内数字顺时针90度，同一英文数字词方向统一；BCD188型与J12号按词检查。 | Within selected GB/T 15835-2011 scope inspect clockwise 90-degree numbers and consistent alphanumeric words, including BCD188型 and J12号.

## KH-CN-V013 英文与标识符 | Latin words and identifiers

保留URL、型番和英文单词的拼写及空格；不逐字回转或插入换行。 | Preserve URL, identifier, word spelling and spaces; never rotate or break every character by default.

## KH-CN-V014 局部纵中横 | Explicit local text combination

text-combine-upright只作用于明确选定token；2/3/4位分别实测，不按位数自动压成1em。 | Apply text-combine-upright only to explicitly selected tokens; compare 2/3/4 digits at actual size.

## KH-CN-V015 逻辑段落 | Logical paragraphs

保留标题、段落、多段引用、古籍原文和注释关系；视觉改列不是文本分段。 | Preserve headings, paragraphs, multi-paragraph quotations, classical source and annotation relations.

## KH-CN-V016 间距参数 | Separate spacing controls

字间、约物压缩、纵向送进与列间分别调整；不靠全局负字间修补禁则。 | Control letter spacing, punctuation compression, vertical advance and column gap separately.

## KH-CN-V017 混排空白 | Mixed-script spacing

混排间距在显示层处理，保留原有空格与复制结果，检查双重间距。 | Adjust mixed-script spacing in display only; preserve existing spaces and check duplicated spacing.

## KH-CN-V018 文案目的 | Copy purpose

区别阅读与图形目的；纵排不授权四字化、缩短、删标点或繁体化。 | Distinguish reading from graphic purposes; vertical layout does not authorize rewriting or removing punctuation.

## KH-CN-V019 纵横配置 | Mixed layout

列长、字号、字距和列间按媒体实测；纵标题配横价格、日期、CTA只是条件方案。 | Choose column length, size and gaps by medium; vertical headings with horizontal prices/dates/CTA are conditional options.

## KH-CN-V020 支给注音 | Supplied annotations

仅用支给拼音、ruby与侧注映射，不创作人名读音；检查方向和跨列碰撞。 | Use supplied pinyin/ruby/side-note mappings only; check orientation, splitting and collisions.

## KH-CN-V021 逐媒体确认 | Per-medium validation

Web、Word、幻灯片和PDF逐一检查实际字体、列序、裁切、选择、复制、抽取与嵌入。 | Validate Web, Word, slides and PDF separately for actual fonts, columns, clipping, selection, copy, extraction and embedding.

## KH-CN-V022 语义顺序 | Semantic order

分别比较视觉顺序、DOM、无障碍树、复制、朗读和键盘操作；自动检测不等于读屏验收。 | Compare visual, DOM, accessibility-tree, copy, speech and keyboard order independently.

## KH-CN-V023 文字放大 | Text enlargement

选用WCAG2.2 SC1.4.4时测至200%文字放大，记录例外、丢失和重叠。 | Where WCAG2.2 SC1.4.4 applies test up to 200% text enlargement and record exceptions and overlap.

## KH-CN-V024 按轴重排 | Reflow by scroll axis

SC1.4.10按滚动轴：横向滚动内容高度256 CSS px，纵向滚动内容宽度320 CSS px；不按字向猜轴。 | For SC1.4.10 use height 256 CSS px for horizontally scrolling content and width 320 CSS px for vertically scrolling content.

## KH-CN-V025 用户间距 | User spacing overrides

SC1.4.12适用范围内测试用户间距覆盖，纵排line-height为横向列间；未支持CSS另行记录。 | Test applicable SC1.4.12 spacing overrides; vertical line-height changes horizontal column spacing; record unsupported CSS.

## KH-CN-V026 证据与限制 | Evidence and limits

规范、字体表、浏览器样本、产品验收和编辑判断分开；not-run不得升级为GB/WCAG或全媒体通过。 | Separate standards, font tables, browser samples, product acceptance and judgment; never promote not-run to universal certification.

## Read-only context helper / 只读上下文辅助

`python scripts/checks.py original.txt --candidate candidate.txt --context context.json`

Example context: `{"profile":"cn-vertical-reading","writing_mode":"vertical-rl"}`.
Optional fields: `direction_reason`, `selected_standards` (array), `css` (string), `per_character_breaks` (boolean). CSS input is a supplied snippet for bounded lint, not a stylesheet parser or DOM renderer. Reports keep all vertical rendering checks `not-checked`. Never infer GB compliance, glyph selection, WCAG conformance or native installation.

## Target-output checklist / 输出检查

Record browser/application version, source SHA, actual font files and fallback, glyphs, punctuation, column boundaries, numeric/Latin direction, annotations, logical order, selection/copy/extraction, 200% text enlargement, correct reflow axis, spacing overrides and unsupported features. Office/PDF/native hosts require their own evidence. Supply readings instead of inventing them. Review stays read-only; return proposed editorial changes separately.
