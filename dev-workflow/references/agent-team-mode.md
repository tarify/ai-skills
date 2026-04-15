# Agent Team 模式指南

## 概述

Agent Team 模式适用于多代理协作场景，通过角色分工完成复杂任务。

---

## 角色分工

### Orchestrator（协调者）

**职责**：
- 接收用户请求
- 任务分级判断
- 分派任务给其他角色
- 管理任务状态
- 交付最终结果

**输入**：
- 用户原始请求

**输出**：
- 任务信封（TASK_ENVELOPE）
- 状态文件（YAML）

### Planner（规划者）

**职责**：
- 分析任务目标
- 制定执行计划
- 识别风险
- 定义验收标准

**输入**：
- TASK_ENVELOPE

**输出**：
- Plan 文件（含步骤、风险、验收标准）

### Builder（执行者）

**职责**：
- 代码实现
- 文件操作
- 工具调用
- 验证执行结果

**输入**：
- Plan 文件 + Confirmation 文件

**输出**：
- Build 文件（含产物、工具调用证据）

### Critic（审查者）

**职责**：
- 独立验证执行结果
- 发现遗漏问题
- 质量评估
- 给出审查结论

**输入**：
- Build 文件

**输出**：
- Review 文件

---

## 协作流程

```
用户
  │
  ↓
Orchestrator (接收 + 分级)
  │
  ├──→ Planner (规划)
  │       │
  │       ↓
  │     用户确认
  │       │
  │       ↓
  ├──→ Builder (执行)
  │       │
  │       ↓
  └──→ Critic (审查) [L3]
          │
          ↓
      交付用户
```

---

## 状态文件管理

### 文件序列

```
{T-任务ID}/
├── 00-intake.yaml       # Orchestrator
├── 10-plan.yaml         # Planner
├── 15-confirmation.yaml # Orchestrator (等待用户)
├── 20-build.yaml        # Builder
├── 30-review.yaml       # Critic [L3]
└── 40-delivery.yaml     # Orchestrator
```

### 状态转换

```yaml
created → completed → confirmed → built → reviewed → delivered
                ↓           ↓          ↓
              rejected   blocked   partial
```

---

## 通信机制

### 任务派发

Orchestrator 通过 TASK_ENVELOPE 派发任务：

```yaml
TASK_ENVELOPE:
  task_id: "T-xxx"
  stage: "planning" | "building" | "reviewing"
  level: L0-L3
  context:
    objective: "任务目标"
    constraints: []
    plan_steps: []
    acceptance_criteria: []
```

### 结果回传

Agent 通过结构化输出回传结果：

```yaml
BUILDER_COMPLETE:
  task_id: "T-xxx"
  status: success | partial | blocked
  artifacts_created: []
  backend_calls: []
  next_recommended_action: return_to_orchestrator
```

---

## 最佳实践

### Orchestrator

- 保持轻量，不做具体规划/执行
- 记录每个阶段的进入和退出时间
- 维护任务状态机

### Planner

- 提供可执行的步骤，而非模糊描述
- 明确验收标准
- 识别所有已知风险

### Builder

- 必须留下工具调用证据
- 对照验收标准逐项检查
- 记录偏离计划的原因

### Critic

- 独立验证，不预设结论
- 明确给出 verdict
- 提供可执行的改进建议
