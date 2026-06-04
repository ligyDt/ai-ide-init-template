---
name: trae-project-workflow
description: 在 TRAE 项目中编排 Rules、Commands、.agents Skills 以及 SOLO Spec/Plan 工作流。用于需要判断应使用项目规则、斜杠命令、/spec、/plan 或通用研发 Skills 的任务。
---

# TRAE 项目工作流编排

将 TRAE 原生项目能力和通用 Agent Skills 串起来，避免在不合适的任务中直接实现。

## 使用场景

- 用户提出新功能、重构、发布、安全审查、PR 总结或复杂交付任务。
- 需要判断使用 `/spec`、`/plan`、项目命令或 `.agents/skills/` 中的研发流程 Skill。
- 需要把 `.trae/rules/` 的约束落实到当前实现、审查或交付总结中。

## 指令

1. 先读取 `AGENTS.md`、`.trae/rules/`、`.agents/project-context.md` 和与任务相关的 Skill。
2. 系统级新建、大规模重构、多人协作、高稳定性或长期维护任务，建议使用 `/spec` 并等待用户确认 `spec.md`、`tasks.md`、`checklist.md`。
3. 中小型功能、模块级重构或有限范围交付，建议使用 `/plan` 或 `plan-delivery` 命令生成执行计划。
4. 模糊需求先调用 `product-intake`；多角色协同调用 `delivery-orchestration`；体验、质量、安全、发布和集成任务分别调用对应 Skill。
5. 高风险外部动作必须先输出风险与审批项，不直接执行。

## 输出

- 推荐工作流：`/spec`、`/plan`、项目命令或具体 Skill
- 触发理由
- 需要读取或生成的文件
- 执行顺序、验证方式和人工确认点
