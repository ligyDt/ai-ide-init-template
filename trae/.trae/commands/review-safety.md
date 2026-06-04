---
name: review-safety
description: 对当前变更进行安全、质量、凭据和发布风险审查。
---

# Review Safety

读取当前变更、项目规则和相关上下文，组合使用 `quality-gate`、`security-risk-review` 与 `release-readiness`。

优先报告：

- 凭据、真实数据、生产资源和外部写入风险
- 测试、类型检查、Lint、构建和回归缺口
- API、数据模型、权限、支付、发布和回滚风险
- 需要人工确认或阻断交付的事项

结论使用“可继续 / 有条件继续 / 阻断”三类，并给出下一步动作。
