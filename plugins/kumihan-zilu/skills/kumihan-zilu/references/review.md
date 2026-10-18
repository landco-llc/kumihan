# KUMIHAN｜字律

## 只读审查 / Read-only review
默认不修改、不发布、不安装依赖、不联网发送原稿。把候选修改与原文并列，并说明影响与授权。
Audit is read-only. Do not edit, publish, install dependencies or send source externally without task authorization.

每项结果记录 rule_id、位置、原文、证据、环境、依据版本、例外、状态和候选方案。状态为 passed/failed/needs-review/not-checked/unsupported/waived/not-applicable；未执行不可标通过。
Return positions, source, evidence, environment, source version, exceptions, status and proposed changes. No unexecuted check becomes passed.

“最”等广告词只能提出法律/编辑确认，不能自动断定违法。CTA、错误恢复、术语和语气需业务上下文；标点候选也可能位于代码或引用。
Advertising language requires contextual legal/editorial review, never an automatic legality verdict. UI copy and static warnings require context.

helper 只提供完整文本字节比较与两种上下文候选；它不覆盖全部36规则、不计算行框、不检测全部字素、不证明WCAG/GB符合性。
The helper compares complete UTF-8 text and flags two contextual patterns only. It does not certify all 36 rules, grapheme segmentation, line boxes or accessibility.

