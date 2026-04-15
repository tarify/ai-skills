---
name: dev-workflow
description: 通用开发流程规范技能。提供任务分级、角色分工、工具组合和流程阶段的标准指南。适用于：(1) 需要规范化开发流程的场景 (2) 多代理协作任务 (3) 需要明确任务级别和执行策略 (4) 构建遵循 L0-L3 分级的任务流程 (5) 需要选择合适的执行和审查工具 (6) 创建任务状态文件序列。触发关键词：开发流程、任务分级、L0/L1/L2/L3、协调者、规划者、执行者、审查者、任务信封、BUILDER_COMPLETE、CRITIC_COMPLETE。
---

# Dev Workflow

通用开发流程规范，提供任务分级、角色分工、工具组合和流程阶段的标准指南。

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

## 环境检测

运行环境检测脚本获取当前配置：

```bash
python scripts/detect-environment.py
```

输出示例：

```yaml
environment:
  mode: main_agent
  tools:
    execution_tool: available  # 用户配置的执行工具
    review_tool: available     # 用户配置的审查工具
    git: available
    python: available
  recommendations:
    execution_backend: <用户配置的执行工具>
    review_backend: <用户配置的审查工具>
```

> **首次使用提醒**：如果是第一次使用此 skill，请先配置您的执行工具和审查工具。
> 详见 [初始化配置](#初始化配置) 章节。

详细检测逻辑参见 [references/environment-detection.md](references/environment-detection.md)。

## 运行模式选择

根据环境检测结果选择执行模式：

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
> 配置方法参见 [用户配置模板](references/user-config-template.md)。

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

## 首次使用

> **🎯 首次使用提醒**：使用此 skill 前需要进行工具配置。
> 运行以下命令进行初始化：
>
> ```bash
> python scripts/detect-environment.py --init
> ```
>
> 此命令将创建默认配置文件（subagent 模式），无需安装额外工具。

### 配置文件位置

**默认位置**：`~/.config/dev-workflow.yaml`（跨平台通用）

**可选位置**：
- `~/.dev-workflow.yaml`（简化版，放在 home 目录）
- `./.dev-workflow.yaml`（项目级别，放在当前工作目录）

> **说明**：检测脚本会依次查找：项目目录 → home 目录 → .config 目录

### 默认配置（Subagent 模式）

```yaml
# 默认配置 - 使用 subagent 执行和审查
# 无需安装额外的 CLI 工具

tool_priority:
  execution:
    primary: subagent    # 由主代理派发子代理执行
  review:
    primary: subagent    # 由主代理派发子代理审查
```

### 是否需要配置特定工具？

**如果您有以下 CLI 工具**，可以修改配置以获得更好的体验：

| 工具 | 用途 | 配置值 |
|------|------|--------|
| CodeBuddy | 执行工具 | `codebuddy` |
| Codex | 执行/审查 | `codex` |
| Claude Code | 执行工具 | `claude-code` |
| Cursor | 执行工具 | `cursor` |
| Aider | 执行工具 | `aider` |

**配置示例（使用 CodeBuddy + Codex）**：

```yaml
tool_priority:
  execution:
    primary: codebuddy
    fallback: subagent
  review:
    primary: codex
    fallback: subagent
```

> **💡 提示**：如果不清楚自己有哪些工具，保持默认 subagent 模式即可，这是最灵活的选择。

### 支持的工具类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| **Subagent** | 由主代理派发的子代理 | 默认推荐，无需额外安装 |
| **CLI 工具** | 命令行代码助手 | 已安装 CodeBuddy/Codex/Claude Code 等 |
| **自定义脚本** | 用户自定义脚本 | 有特定工作流需求 |

更多配置选项见 [references/user-config-template.md](references/user-config-template.md)。

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
