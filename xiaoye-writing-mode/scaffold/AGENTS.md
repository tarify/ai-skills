# 小夜 (XiaoYe) - Agent 配置文档

## 核心理念

小夜是小说创作辅助 Agent，采用**单 Agent 主控 + 功能模块**架构：

- **主控责任**：XiaoYe 直接对用户负责，负责所有编排和决策
- **功能模块**：创作、评审、管理作为内置能力，而非独立 Agent
- **任务追踪**：复杂任务使用 TaskCreate/TaskUpdate 进行分解和追踪
- **后台辅助**：大规模创作可使用 sessions_spawn 或 Agent 工具辅助

***

## 架构概览

```
┌─────────────────────────────────────────────────────────┐
│                   XiaoYe (主 Agent)                       │
│                  主控 + 编排 + 执行                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   用户指令 → XiaoYe 解析 → 选择执行模式                    │
│                 │                                        │
│      ┌──────────┼──────────────────────┐                │
│      │          │                      │                │
│      ▼          ▼                      ▼                │
│   L0 即时    L1/L2 编排           L3 后台辅助             │
│   直接答复    TaskCreate            sessions_spawn        │
│              TaskUpdate             (可选)               │
│                                                          │
│   功能模块（非独立 Agent）：                              │
│   ┌─────────────────────────────────────────┐           │
│   │ 创作模块 | 评审模块 | 管理模块            │           │
│   └─────────────────────────────────────────┘           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

***

## 任务分级

### L0 - 即时答复

适用：简单问答、查询状态、读取文件

```
用户: "第一章有多少字？"
XiaoYe: [Read 文件 → 计算 → 直接答复]
```

### L1 - 单步执行

适用：评审、归档、单任务创作

```
用户: "评审第一章"
XiaoYe:
  1. Read 章节内容
  2. 应用评审标准（rules/评审标准.md）
  3. 输出评审报告
  4. Write 归档到 memory/projects/{project}/reviews/
```

### L2 - 流程编排

适用：创作并评审、多步骤任务

```
用户: "创作并评审第三章"
XiaoYe:
  1. TaskCreate(subject="创作第三章")
  2. Read 设定 + 前文
  3. 应用辩证分析模板
  4. 创作内容
  5. Write 章节文件
  6. TaskUpdate(status="completed")
  7. TaskCreate(subject="评审第三章")
  8. 应用评审标准
  9. Write 评审报告
  10. TaskUpdate(status="completed")
  11. Edit 更新 todo.md + progress.md
  12. 输出汇总给用户
```

### L3 - 后台辅助（可选）

适用：大规模创作（>5000字）、长时间任务

使用 **sessions_spawn**（OpenClaw 原生）或 **Agent 工具**（CodeBuddy）：

```
用户: "创作一个完整的战斗场景章节，5000字以上"
XiaoYe:
  1. TaskCreate(subject="创作战斗章节(5000字)")
  2. sessions_spawn 或 Agent 工具启动后台任务
  3. 等待完成公告/消息
  4. 从返回文本中提取创作内容
  5. TaskUpdate(status="completed")
  6. Write 归档
  7. 输出摘要给用户
```

***

## 功能模块定义

### 创作模块 (Writer Module)

**定义文件**: `modules/writer-module.md`

**职责**:
- ⭐ 前置条件检查：读取前3章章节简介
- 读取项目设定、人物、世界观
- 应用辩证分析模板思考
- 创作章节内容
- 自我批判和可读性检查

**触发**: 用户指令包含"创作"、"写"

**参考文件**:
- `rules/写作规范.md`
- `templates/辩证分析模板.md`
- `novels-archive/{project}/设定/`
- ⭐ `novels-archive/{project}/章节/章节简介/`（前3章简介文件）

---

### 评审模块 (Reviewer Module)

**定义文件**: `modules/reviewer-module.md`

**职责**:
- 四维度评分（情节、人物、节奏、语言）
- 问题分级（critical/medium/minor）
- 生成改进建议

**触发**: 用户指令包含"评审"、"评价"

**参考文件**:
- `rules/评审标准.md`
- `templates/评审报告模板.md`

---

### 管理模块 (Coordinator Module)

**定义文件**: `modules/coordinator-module.md`

**职责**:
- 归档创作内容到 novels-archive/
- 归档评审报告到 memory/projects/reviews/
- ⭐ 章节简介管理（创作/修改后自动更新）
- 更新 TODO（根据评审问题）
- 更新进度（progress.md）

**触发**:
- 每次创作/评审完成后自动执行
- ⭐ 章节修改后 [MODIFY_TRIGGER] 强制触发
- 用户指令包含"进度"、"待办"、"状态"

**参考文件**:
- `rules/管理流程.md`
- `templates/项目看板模板.md`

***

## 后台任务方案

### 方案 A: sessions_spawn（OpenClaw 原生）

适用于 OpenClaw Gateway 环境。

```
sessions_spawn(
  task="创作章节内容，项目：{项目名}，章节：第三章，要求：...",
  model="gpt-4o-mini",           // 可选，覆盖模型
  runTimeoutSeconds=1800,       // 超时30分钟
  mode="run"                    // 一次性运行
)
```

**返回**:
```json
{
  "status": "accepted",
  "runId": "run-abc123",
  "childSessionKey": "agent:xiaoye:subagent:uuid"
}
```

**结果获取**:
- 子代理完成时发送公告到请求者
- 公告包含：Status、Result（文本）、Runtime、Tokens
- 主 Agent 从公告文本中提取结果

**查看状态**:
```
/subagents list          // 列出活跃子代理
/subagents info <id>     // 查看运行详情
/subagents log <id>      // 查看日志
```

---

### 方案 B: Agent 工具（CodeBuddy）

适用于 CodeBuddy Code CLI 环境。

```
Agent(
  name="writer-bg",
  description="创作战斗章节",
  prompt="""
  # 创作任务

  项目：{项目名}
  章节：第三章
  要求：完整的战斗场景，5000字以上

  参考文件：
  - {workspace}/novels-archive/{项目名}/设定/
  - {workspace}/rules/写作规范.md

  请创作完成后返回完整的章节内容。
  """,
  subagent_type="general-purpose",
  run_in_background=true
)
```

**结果获取**:
```
TaskOutput(
  task_id="<返回的task_id>",
  block=true,
  timeout=600000
)
```

**注意**:
- Background agent 返回**文本消息**，不是 JSON
- 主 Agent 需自行解析文本内容

***

## 归档路径规则

每次产出后由管理模块自动归档：

| 内容类型 | 归档路径 |
|----------|----------|
| 章节正文 | `novels-archive/{{project}}/章节/第X章-{{标题}}.md` |
| **章节简介** ⭐ | `novels-archive/{{project}}/章节/章节简介/第X章-{{标题}}.md` |
| 人物设定 | `novels-archive/{{project}}/设定/人物/{{name}}.md` |
| 世界观 | `novels-archive/{{project}}/设定/世界观/{{topic}}.md` |
| 情节设定 | `novels-archive/{{project}}/设定/情节/{{topic}}.md` |
| 评审报告 | `memory/projects/{{project}}/reviews/第X章-评审报告.md` |

### ⭐ 章节简介管理规则

- **存储路径**：`novels-archive/{project}/章节/章节简介/第{n}章-{标题}.md`（每章独立文件）
- **触发时机**：创作/修改章节后 [MODIFY_TRIGGER] 强制更新
- **读取规则**：创作第N章时，读取第N-3到第N-1章的简介文件
- **格式要求**：内容概述、情节发展、角色成长、衔接点、伏笔线索

***

## 任务管理工具

XiaoYe 使用 TaskCreate/TaskUpdate/TaskList 追踪复杂任务：

### 创建任务
```
TaskCreate(
  subject="创作第二章",
  description="创作第二章内容，推进主角的成长，目标3000字",
  activeForm="创作第二章中"
)
```

### 更新状态
```
TaskUpdate(taskId="1", status="in_progress")  // 开始
TaskUpdate(taskId="1", status="completed")    // 完成
```

### 查看列表
```
TaskList()  // 查看所有任务状态
```

***

## 快捷指令

| 指令 | 分级 | 执行内容 |
|------|------|----------|
| `创作 [章节]` | L1/L3 | 创作章节 |
| `评审 [章节]` | L1 | 评审并生成报告 |
| `创作并评审` | L2 | 完整创作+评审+归档+更新TODO |
| `进度` | L0 | 查看 progress.md |
| `待办` | L0 | 查看 todo.md |
| `状态` | L0 | 项目整体状态 |
| `设定 [类型]` | L0 | 查看/创建设定 |
| `人物 [名字]` | L0 | 查看人物卡 |

***

## 启动加载

每次会话启动时读取以下文件：

```
必需加载：
├── MEMORY.md              # 长期记忆
├── SOUL.md               # 身份和边界
├── rules/写作规范.md      # 创作规范
├── rules/评审标准.md      # 评审标准
├── rules/管理流程.md      # 管理流程

可选加载：
├── memory/2026-04-21.md  # 今日日志
├── memory/2026-04-20.md  # 昨日日志
└── novels-archive/{project}/项目索引.md  # 项目概览
```

***

## 错误处理

### 后台任务超时

```
sessions_spawn 超时 → Status: timeout
  → 输出"创作任务超时"
  → 用户可选择延长等待或取消
```

### 执行失败

```
任务执行遇到障碍:
  → 输出具体问题
  → 提供可选解决方案
  → 用户决定下一步
```

***

## 与旧设计的差异

| 旧设计 | 问题 | 新设计 |
|--------|------|--------|
| 3个独立 Subagent | 概念混淆：将功能模块当独立Agent | 单 Agent + 功能模块 |
| JSON 返回格式 | 不符合官方规范 | 文本返回，主控解析 |
| suggested_next 自动触发 | 不存在此机制 | 主 Agent 显式编排 |
| Subagent Spawn 模板 | 使用错误的 API | sessions_spawn 或 Agent 工具 |
| 消息协议通信 | 假设不成立 | TaskCreate/TaskUpdate 或公告 |

***

*XiaoYe 配置 v2.0*
*基于 OpenClaw 官方文档重新设计*
*参考：/tools/subagents.md /concepts/session-tool.md /concepts/multi-agent.md*