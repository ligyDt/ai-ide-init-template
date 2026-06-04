---
description: TRAE 项目通用协作、上下文读取和交付规则。
alwaysApply: true
---

# 通用协作规则

- 开始任务前先读取 `AGENTS.md`、`.agents/project-context.md`、`.agents/rules.md`、`.agents/memory.md` 与 `.agents/errors.md`。
- 新需求先明确目标用户、输入输出、范围边界、风险和验收标准；需求不清晰时先调用 `product-intake`。
- 涉及多角色、多模块或跨阶段交付时，先用 `delivery-orchestration` 拆分阶段、职责、依赖和交接物。
- 复杂系统级任务优先使用 `/spec` 生成 `.trae/specs/<任务名>/spec.md`、`tasks.md`、`checklist.md` 后再执行。
- 中小型功能或模块级重构优先使用 `/plan` 生成 `.trae/documents/plan.md`，确认后按计划推进。
- 所有面向人的沟通、说明、交付总结和项目 Markdown 默认使用中文；代码标识、命令和协议字段保持原文。
