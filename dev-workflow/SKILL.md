---
name: dev-workflow
description: |
  通用开发流程规范技能。当用户请求涉及以下场景时使用：
  
  1. **代码相关任务**：写代码、修改代码、重构、实现功能、添加特性、修复 bug
  2. **配置相关任务**：修改配置文件、设置环境、调整参数
  3. **多步骤任务**：需要规划、执行、验证的复杂任务
  4. **协作任务**：需要协调者、规划者、执行者、审查者角色的任务
  5. **质量保证**：需要审查、验证、验收的任务
  
  触发关键词（包含任一即触发）：
  - 动作：写、修改、实现、重构、添加、创建、构建、开发、修复
  - 对象：代码、功能、特性、文件、配置、模块、系统
  - 流程：规划、计划、执行、审查、验收、交付
  - 级别：L0、L1、L2、L3、任务分级
  - 角色：协调者、规划者、执行者、审查者、Builder、Critic
  - 输出：BUILDER_COMPLETE、CRITIC_COMPLETE、任务信封、TASK_ENVELOPE
---

# Dev Workflow

通用开发流程规范，提供任务分级、角色分工、工具组合和流程阶段的标准指南。

## 首次使用配置

> **⚠️ 重要**：首次使用此 skill 前，需要初始化配置文件。

### 检测配置文件

配置文件查找顺序：
```
1. ./.dev-workflow.yaml        （项目级别）
2. ~/.dev-workflow.yaml        （Home 目录）
3. ~/.config/dev-workflow.yaml （XDG 标准位置）
```

### 没有配置文件时

如果未找到配置文件，询问用户：

```
⚠️ 检测到首次使用，未找到配置文件。

请选择配置文件存放位置：
1. 项目级别：./.dev-workflow.yaml（仅当前项目使用）
2. 用户级别：~/.dev-workflow.yaml（所有项目共享）
3. 标准位置：~/.config/dev-workflow.yaml（XDG 标准）

是否初始化配置？[Y/n]
```

用户确认后，运行：
```bash
python scripts/detect-environment.py --init --path <用户选择的路径>
```

### 配置文件模板

默认使用 `subagent` 模式：

```yaml
# dev-workflow 配置文件
tool_priority:
  execution:
    primary: subagent    # 执行工具
  review:
    primary: subagent    # 审查工具
```

### 支持的工具选项

| 工具 | 用途 | 配置值 |
|------|------|--------|
| Subagent（默认） | 子代理执行/审查 | `subagent` |
| CodeBuddy | 执行工具 | `codebuddy` |
| Codex | 执行/审查 | `codex` |
| Claude Code | 执行工具 | `claude-code` |
| Cursor | 执行工具 | `cursor` |
| Aider | 执行工具 | `aider` |

> **💡 提示**：如果不清楚有哪些工具，保持默认 `subagent` 模式即可。

## 快速参考

```yaml
# 任务分级
纯问答 → L0
需规划无产物 → L1
需产物 → L2（代码/配置修改）
高风险 → L3（安全/关键功能）

# 角色分工
协调者: 接收 + 分级 + 状态管理 + 交付
规划者: 目标 + 计划 + 风险 + 验收标准
执行者: 实现 + 工具调用 + 验证
审查者: 独立验证 + 问题发现 + 结论

# 工具组合
L2 执行: 实现工具 + 审查工具 (可选)
L3 执行: 实现工具 + 审查工具 (必须)
L3 审查: 审查工具 或分析工具

# 文件序列
00-intake → 10-plan → 15-confirmation → 20-build → 30-review → 40-delivery
```

## 核心流程

```
用户请求 → 任务分级 → 规划 → 确认 → 执行 → 审查 → 交付
```

### 分级决策树

```
是否需要产物？
├─ 否 → L0/L1（问答/规划）
└─ 是 → 是否涉及代码/配置？
        ├─ 否 → L1
        └─ 是 → 是否高风险/安全相关？
                ├─ 否 → L2
                └─ 是 → L3
```

### 流程阶段

| 阶段 | 角色职责 | 输出文件 |
|------|---------|---------|
| **Intake** | 协调者：接收请求、分级、创建任务ID | 00-intake.yaml |
| **Planning** | 规划者：制定计划、识别风险、定义验收标准 | 10-plan.yaml |
| **Confirmation** | 协调者：展示计划、等待用户确认 | 15-confirmation.yaml |
| **Building** | 执行者：实现、工具调用、验证 | 20-build.yaml |
| **Reviewing** | 审查者：独立验证、评估质量 (L3) | 30-review.yaml |
| **Delivery** | 协调者：汇总结果、交付用户 | 40-delivery.yaml |

## 运行模式选择

### 主代理模式

- **场景**：直接响应用户请求
- **流程**：用户请求 → 任务分级 → 选择执行模式 → 交付
- **工具链**：使用用户配置的执行工具和审查工具

### 子代理模式

- **场景**：由 Orchestrator 派发的孤立执行单元
- **输入**：TASK_ENVELOPE（包含 task_id、stage、level、context）
- **输出**：BUILDER_COMPLETE 或 CRITIC_COMPLETE 结构化报告
- **约束**：
  - 只做 TASK_ENVELOPE 定义的工作
  - 不与用户直接交互
  - 必须提供工具调用证据

详见 [references/subagent-mode.md](references/subagent-mode.md)。

### Agent Team 模式

- **场景**：多代理协作完成复杂任务
- **角色**：Orchestrator、Planner、Builder、Critic
- **通信**：通过状态文件和任务信封
- **文件序列**：intake → plan → confirmation → build → review → delivery

详见 [references/agent-team-mode.md](references/agent-team-mode.md)。

## 工具调用规范

> **说明**：本 skill 不绑定特定工具，以下为示例性说明。实际工具调用方式取决于用户配置。

### 执行阶段 (Building)

根据用户配置的执行工具调用，示例：

```bash
# 示例：如果配置了 Claude Code
claude-code --print --permission-mode bypassPermissions "<prompt>"

# 示例：如果配置了 Codex
codex exec "<prompt>" --json

# 示例：如果使用 subagent 作为执行方式
# 由 orchestrator 通过 sessions_spawn 派发子代理执行
```

验证执行结果：

- 检查文件是否创建/修改
- 对照验收标准逐项检查

### 审查阶段 (Reviewing)

根据用户配置的审查工具调用，示例：

```bash
# 示例：如果配置了独立审查工具
<review_tool> --mode review "<prompt>"

# 示例：如果使用 subagent 作为审查方式
# 由 orchestrator 派发独立审查代理
```

### 证据记录

```yaml
backend_calls:
  - backend: "<执行工具名称>"  # 如 codebuddy, codex, claude-code, subagent 等
    mode: develop | analyze | review
    command: "完整命令"
    evidence: "输出摘要或文件"
    result: success | failed | skipped
```

> **重要**：无论使用什么工具，都必须记录 `backend_calls` 证据。

## 验收标准

### L2 任务

- [ ] Plan 文件存在
- [ ] Build 文件包含工具调用记录
- [ ] 对照验收标准检查通过

### L3 任务

- [ ] Plan 文件存在
- [ ] Build 文件包含工具调用记录
- [ ] Review 文件存在
- [ ] 审查结论为 approved
- [ ] 对照验收标准检查通过

## 详细参考

- **流程规范**：[references/workflow-spec.md](references/workflow-spec.md) - 完整的任务分级、角色定义、流程阶段
- **环境检测**：[references/environment-detection.md](references/environment-detection.md) - 检测维度和执行策略
- **子代理模式**：[references/subagent-mode.md](references/subagent-mode.md) - 生命周期、输入输出规范
- **Agent Team 模式**：[references/agent-team-mode.md](references/agent-team-mode.md) - 角色分工、协作流程
- **用户配置**：[references/user-config-template.md](references/user-config-template.md) - 配置文件模板

## 检查清单

**Builder 输出前检查**：

- [ ] 是否属于 L2/L3 任务？→ 必须有工具调用证据
- [ ] 是否已调用配置的执行工具？→ 记录到 backend_calls
- [ ] 是否已调用配置的审查工具或有合法 fallback？
- [ ] BUILDER_COMPLETE 是否为最后一条消息？
- [ ] 之后是否还有额外文本？（应该没有）

**Critic 输出前检查**：

- [ ] 是否独立验证？（不预设结论）
- [ ] verdict 是否明确？
- [ ] 是否提供可执行的改进建议？
- [ ] CRITIC_COMPLETE 是否为最后一条消息？
