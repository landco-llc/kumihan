# KUMIHAN｜字律

## 网页与界面 / Web and interfaces
区别中文正文、英文引用、URL、代码、数学式和商标。核对 “外引号‘内引号’”、书名号《》的语义，不按每段开闭数量机械报错；多段引用可以只在末段闭合。
Separate prose and syntax. Review nested quotes and title brackets in context; multi-paragraph quotations need not balance in every paragraph.

依据 KH-CN-R012/R013 与出处条款，实测行首点号、行末开括号，以及 ——、…… 的内部拆分。双字符号整体的行首策略另行记录。`line-break:strict`、`@supports` 不构成 GB 合格证据。`break-all` 可能切开 Latin/数字；不能说它直接取消所有约物禁则。
Inspect actual line boxes; distinguish internal splitting from whole-mark line placement. CSS parsing and computed styles do not establish conformance.

中英间隔尽量在渲染层讨论，保留已有空格与复制文本。不要插入无意义的不可见字符或统一 0.25em。字体、地区字形、fallback、加载失败须在目标环境检查。
Review text-autospace and spacing-trim separately with support checks; preserve copy text and do not silently insert spaces.

验收 320/375/768/1440 CSS px、200%文字、用户间距覆盖、键盘和焦点、语义标签与语言、CTA实际行为。检查数值单位、URL、长名称与底部内容。不得缩小或裁剪内容来隐藏失败。
Test widths, text resize, spacing overrides, keyboard, semantics and real actions. Record browser, viewport, font and evidence. Static checks, screenshots and human judgment stay separate.

纵排参见 [purpose and target-output checks](vertical.md)。26项分开记录指导、静态与实测范围，未检查不是合格。
