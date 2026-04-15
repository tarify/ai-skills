# 用户配置模板

## 首次使用

> **🎯 快速初始化**：运行以下命令创建配置文件（默认 subagent 模式）
>
> ```bash
> python scripts/detect-environment.py --init
> ```

---

## 配置文件位置

配置文件按以下优先级查找：

| 优先级 | 位置 | 说明 |
|--------|------|------|
| 1 | `./.dev-workflow.yaml` | 项目级别配置 |
| 2 | `~/.dev-workflow.yaml` | Home 目录配置 |
| 3 | `~/.config/dev-workflow.yaml` | 默认位置（XDG 标准） |

> **提示**：可以运行 `--init --path /自定义/路径/config.yaml` 指定配置位置。

---

## 默认配置（Subagent 模式）

```yaml
# 默认配置 - 无需安装额外工具

tool_priority:
  execution:
    primary: subagent    # 由主代理派发子代理执行
  review:
    primary: subagent    # 由主代理派发子代理审查
```

> **💡 提示**：Subagent 模式由 orchestrator 通过 sessions_spawn 派发子代理执行，无需配置 CLI 工具。这是最灵活的默认选择。

---

## 是否有特定工具？

**如果您已安装以下 CLI 工具**，可以修改配置以使用它们：

| 工具 | 用途 | 配置值 | 说明 |
|------|------|--------|------|
| CodeBuddy | 执行/审查 | `codebuddy` | 腾讯代码助手 |
| Codex | 执行/审查 | `codex` | OpenAI Codex CLI |
| Claude Code | 执行 | `claude-code` | Anthropic Claude Code |
| Cursor | 执行 | `cursor` | Cursor AI |
| Aider | 执行 | `aider` | Aider AI Pair Programming |

**配置示例**：

```yaml
# 示例：使用 CodeBuddy + Codex
tool_priority:
  execution:
    primary: codebuddy
    fallback: subagent
  review:
    primary: codex
    fallback: subagent
```

---

## 支持的工具类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| **Subagent** | 由主代理派发的子代理 | 默认推荐，无需安装 |
| **CLI 工具** | 命令行代码助手 | 已安装 CodeBuddy/Codex 等 |
| **自定义脚本** | 用户自定义脚本 | 特定工作流需求 |

---

## 配置示例

### 示例 1：使用 CodeBuddy + Codex

```yaml
tool_priority:
  execution:
    primary: codebuddy
    fallback: local
  review:
    primary: codex
    fallback: codebuddy
    skip_if_unavailable: false

  models:
    codebuddy:
      default: kimi-k2.5
      fallback: glm-5
    codex:
      default: gpt-5.4-mini
```

### 示例 2：使用 Claude Code + Codex

```yaml
tool_priority:
  execution:
    primary: claude-code
    fallback: local
  review:
    primary: codex
    skip_if_unavailable: false

  models:
    claude-code:
      default: claude-sonnet-4
    codex:
      default: gpt-5.4-mini
```

### 示例 3：使用 Subagent 执行

```yaml
tool_priority:
  execution:
    primary: subagent  # 通过子代理执行
  review:
    primary: codex     # 仍使用 Codex 审查
    skip_if_unavailable: false
```

### 示例 4：全 Subagent 模式

```yaml
tool_priority:
  execution:
    primary: subagent
  review:
    primary: subagent
```

### 示例 5：自定义工具

```yaml
tool_priority:
  execution:
    primary: my-code-assistant  # 自定义 CLI 工具
    fallback: local
  review:
    primary: my-review-script.py  # 自定义脚本
    skip_if_unavailable: false
```

---

## 任务分级规则

```yaml
task_level_rules:
  # 自动分级规则
  auto_upgrade:
    # 包含敏感关键词时自动升级到 L3
    security_keywords:
      - "密码"
      - "密钥"
      - "token"
      - "credential"
      - "password"

    # 涉及关键路径时自动升级到 L3
    critical_paths:
      - "production"
      - "release"
      - "deploy"

  # 默认级别（未匹配规则时）
  default_level: L2
```

---

## 工作区配置

```yaml
workspace:
  # 默认工作区
  default: ~/.openclaw/workspace

  # 任务状态文件存储位置
  state_dir: ~/.openclaw/tasks

  # 临时文件清理策略
  cleanup:
    enabled: true
    keep_days: 7
```

---

## 通知配置

```yaml
notifications:
  # 任务完成时是否通知
  on_complete: true

  # 任务阻塞时是否通知
  on_blocked: true

  # 审查失败时是否通知
  on_review_failed: true

  # 通知渠道（如果配置了飞书/QQ 等）
  channels:
    - feishu
```

---

## 完整配置示例

### 个人开发者

```yaml
task_level_rules:
  auto_upgrade:
    security_keywords: []
    critical_paths: []
  default_level: L2

tool_priority:
  execution:
    primary: codebuddy
    fallback: local
  review:
    primary: codex
    fallback: codebuddy

workspace:
  default: ~/projects
  state_dir: ~/.openclaw/tasks
  cleanup:
    enabled: true
    keep_days: 30
```

### 团队协作

```yaml
task_level_rules:
  auto_upgrade:
    security_keywords:
      - "密码"
      - "生产环境"
    critical_paths:
      - "production"
      - "main"
      - "master"
  default_level: L3  # 团队默认严格模式

tool_priority:
  execution:
    primary: codebuddy
  review:
    primary: codex
    skip_if_unavailable: false  # 必须审查

notifications:
  on_complete: true
  on_blocked: true
  on_review_failed: true
  channels:
    - feishu
```

---

## 配置文件验证

目前配置文件采用 YAML 格式，可通过以下方式验证：

1. 使用 YAML linter 工具（如 `yamllint`）检查语法
2. 使用 `detect-environment.py` 检测环境工具可用性：

```bash
python scripts/detect-environment.py --json
```

检测输出会显示：
- 配置文件是否存在
- 执行工具是否已配置
- 审查工具是否已配置
- 工具可用性状态

> **首次使用提示**：如果检测结果显示配置文件不存在或工具未配置，请先创建配置文件并设置您的执行和审查工具。
