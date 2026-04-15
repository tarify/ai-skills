# 环境检测指南

## 目的

识别当前运行环境，选择合适的工具和执行模式。

---

## 配置文件位置

配置文件按优先级查找：

| 优先级 | 位置 | 说明 |
|--------|------|------|
| 1 | `./.dev-workflow.yaml` | 项目级别配置 |
| 2 | `~/.dev-workflow.yaml` | Home 目录配置 |
| 3 | `~/.config/dev-workflow.yaml` | 默认位置（XDG 标准） |

---

## 检测维度

### 1. 运行模式检测

```python
# 判断依据
is_subagent = "TASK_ENVELOPE" in context
is_agent_team = "AGENT_TEAM" in context
is_main_agent = not (is_subagent or is_agent_team)
```

| 模式 | 标识 | 特征 |
|------|------|------|
| **主代理** | 默认 | 无特殊标识 |
| **子代理** | TASK_ENVELOPE | 有明确的任务信封 |
| **代理团队** | AGENT_TEAM | 多代理协作标识 |

### 2. 工具可用性检测

> **说明**：工具检测基于用户配置，非硬编码特定工具。

| 检测类型 | 检测方式 | 用途 |
|---------|---------|------|
| **用户配置的执行工具** | 从配置文件读取后检测 | 代码实现 |
| **用户配置的审查工具** | 从配置文件读取后检测 | 代码审查 |
| **Git** | `git --version` | 版本控制 |
| **Python** | `python --version` | 脚本执行 |

#### 从配置文件读取工具设置

```python
# 按优先级查找配置文件
config_paths = [
    Path.cwd() / ".dev-workflow.yaml",
    Path.home() / ".dev-workflow.yaml",
    Path.home() / ".config" / "dev-workflow.yaml",
]

for config_path in config_paths:
    if config_path.exists():
        config = yaml.safe_load(config_path.read_text())
        execution_tool = config.get("tool_priority", {}).get("execution", {}).get("primary")
        review_tool = config.get("tool_priority", {}).get("review", {}).get("primary")
        break
```

### 3. 工作区检测

```python
# 检测工作区类型
has_git = Path.cwd().joinpath(".git").exists()
```

---

## 执行策略

### 主代理模式

```yaml
流程: 用户请求 → 任务分级 → 选择执行模式
工具链:
  - 使用用户配置的执行工具
  - 使用用户配置的审查工具
文件操作: 直接读写
```

### 子代理模式

```yaml
流程: TASK_ENVELOPE → 执行 → 输出 BUILDER_COMPLETE
工具链:
  - 根据配置约束选择
  - 必须提供执行证据
文件操作: 在指定工作区内
输出: 结构化 YAML 报告
```

### 代理团队模式

```yaml
流程: 接收分工 → 执行 → 协作交付
工具链: 根据角色选择
通信: 通过共享状态文件
```

---

## 检测脚本

运行 `scripts/detect-environment.py` 获取当前环境报告：

```bash
# 检测当前环境
python scripts/detect-environment.py

# 初始化配置文件
python scripts/detect-environment.py --init

# 指定配置文件位置
python scripts/detect-environment.py --init --path /path/to/config.yaml

# JSON 格式输出
python scripts/detect-environment.py --json
```

输出格式：

```yaml
environment:
  mode: main_agent | subagent | agent_team
  tools:
    execution_tool: <工具名> (available | unavailable)
    review_tool: <工具名> (available | unavailable)
    subagent: available
    git: available | unavailable
    python: available | unavailable
  workspace:
    has_git: true | false
    current_dir: /path/to/current/dir
  recommendations:
    execution_backend: <用户配置的执行工具> | local | subagent
    review_backend: <用户配置的审查工具> | subagent | skip
  config_status:
    config_file_exists: true | false
    execution_tool_configured: true | false
    review_tool_configured: true | false
```
