---
name: intake
description: 将模糊需求整理为目标、范围、约束、风险和验收标准。
---

# Intake

读取 `AGENTS.md`、`.agents/project-context.md`、`.agents/rules.md` 与相关代码上下文，然后调用 `product-intake`。

输出：

- 目标用户与问题
- 核心场景与预期结果
- 范围内与范围外事项
- 输入、输出、依赖和约束
- 风险、待确认事项和验收标准

若需求涉及外部账号、真实数据、支付、发布、部署或生产访问，先停止实现并列出需要确认的动作。
