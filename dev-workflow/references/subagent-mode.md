# Subagent 模式指南

## 概述

Subagent 模式是 OpenClaw 运行时为特定任务派发的孤立执行单元。每个 subagent 有明确的生命周期和职责边界。

---

## 生命周期

```
创建 → 执行 → 输出结果 → 终止
```

### 创建条件

- Orchestrator 派发任务
- 需要 Builder/Critic 执行具体工作
- 任务需要独立环境隔离

### 执行规则

1. **专注单一任务** - 只做 TASK_ENVELOPE 定义的工作
2. **不与用户交互** - 所有对话通过 Orchestrator
3. **不发起主动操作** - 无心跳、无定时任务、无外部消息
4. **必须提供证据** - 输出结构化报告

### 终止条件

- 正常完成：输出 BUILDER_COMPLETE 或 CRITIC_COMPLETE
- 超时：运行时间超过限制
- 阻塞：无法继续执行

---

## 输入规范

### TASK_ENVELOPE 结构

```yaml
TASK_ENVELOPE:
  task_id: "T-xxx"           # 唯一标识
  stage: "building" | "reviewing"  # 当前阶段
  level: L0-L3               # 任务级别

  context:
    objective: "任务目标描述"
    constraints: []          # 约束条件
    plan_steps: []           # 执行步骤
    acceptance_criteria: []   # 验收标准

  from_handoff: "上下文信息"

  output_requirement: |
    必须输出的结构和字段
```

### 读取方式

任务信封通过注入方式提供，无需主动读取。

---

## 输出规范

### Builder 输出

最后一条消息必须包含 `BUILDER_COMPLETE`：

```yaml
BUILDER_COMPLETE:
  protocol_version: "2.0"
  task_id: "T-xxx"
  status: success | partial | blocked

  execution_result:
    artifacts_created: []     # 创建的文件
    artifacts_modified: []    # 修改的文件
    execution_notes: []       # 关键决策和偏差
    backend_calls: []         # 工具调用证据

    plan_adherence: []        # 计划执行对照

  against_criteria: []        # 验收标准对照

  quality_gates:
    syntax_check: passed | failed | not_applicable
    lint_check: passed | failed | not_applicable
    test_status: passed | failed | partial | not_applicable

  next_recommended_action: return_to_orchestrator | request_planning_revision
  handoff_ready: true
```

### Critic 输出

最后一条消息必须包含 `CRITIC_COMPLETE`：

```yaml
CRITIC_COMPLETE:
  protocol_version: "2.0"
  task_id: "T-xxx"

  verdict: approved | needs_revision | rejected

  findings:
    - severity: high | medium | low
      category: "问题类型"
      description: "具体描述"
      location: "文件:行号"

  recommendations: []

  review_summary:
    strengths: []
    weaknesses: []

  artifacts_reviewed: []
```

---

## 工具调用证据

### 必须记录

```yaml
backend_calls:
  - backend: "codebuddy" | "codex" | "local"
    mode: "develop" | "analyze" | "review"
    command: "完整命令行"
    evidence: "输出摘要或文件路径"
    result: success | failed | skipped
```

### 证据要求

- **L2 任务**：至少一条工具调用记录
- **L3 任务**：
  - Builder: 工具调用记录
  - Critic: 独立审查记录

---

## 约束清单

### 允许的操作

- ✅ 读取/写入指定工作区的文件
- ✅ 调用 CodeBuddy/Codex CLI
- ✅ 执行 shell 命令（探测、测试）
- ✅ 读取 references 文档

### 禁止的操作

- ❌ 与用户直接对话
- ❌ 发送外部消息（邮件、通知）
- ❌ 创建定时任务
- ❌ 修改系统配置
- ❌ 访问非指定工作区

---

## 错误处理

### 遇到阻塞

1. 设置 `status: blocked`
2. 记录阻塞原因到 `execution_notes`
3. 设置 `next_recommended_action: blocked_needs_clarification`

### 发现计划问题

1. 不要直接修改 plan
2. 记录问题到 `execution_notes`
3. 设置 `next_recommended_action: request_planning_revision`
4. 提供上下文帮助 planner 理解问题

### 工具调用失败

1. 记录错误到 `backend_calls[].result: failed`
2. 尝试 fallback（如 Codex 失败 → CodeBuddy review）
3. 无可用 fallback → 设置 `status: partial`
