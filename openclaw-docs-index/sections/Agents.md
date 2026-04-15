# Agents

## Overview

多 Agent 管理和隔离。每个 agent 有独立的 workspace、auth、sessions、persona。

## Key Concepts

- **Agent**: 独立的 AI brain/personality
- **Workspace**: 隔离的工作目录 (`~/.openclaw/workspace-<name>/`)
- **Bindings**: 渠道/账号/发送者到 agent 的映射
- **Session**: 对话上下文
- **Auth Profile**: 模型认证配置

## Directory Structure

```
~/.openclaw/
├── workspace-default/
│   ├── AGENTS.md          # Agent rules
│   ├── MEMORY.md          # Long-term memory
│   ├── sessions/          # Session storage
│   └── skills/            # Agent-specific skills
├── workspace-planner/
├── workspace-builder/
└── workspace-critic/
```

## CLI Commands

```bash
# 列出 agents
openclaw agents list

# 创建 agent
openclaw agents create --name planner

# 查看状态
openclaw agents status --agent planner

# 切换默认
openclaw agents default --agent planner
```

## Configuration

```json
{
  "agents": {
    "defaults": {
      "models": {
        "primary": "gpt-4",
        "fallbacks": ["claude-3", "gpt-3.5"]
      }
    },
    "planner": {
      "agentDir": "~/.openclaw/workspace-planner",
      "models": {...}
    }
  }
}
```

## Bindings

Route messages to specific agents:

```json
{
  "bindings": [{
    "channel": "telegram",
    "accountId": "@mybot",
    "peer": "@username",
    "agentId": "planner"
  }]
}
```

## Multi-Agent Patterns

1. **Persona separation**: Work vs Personal
2. **Task routing**: Planner → Builder → Critic
3. **Channel isolation**: Different agents per channel

## Official Docs

- Multi-Agent: https://docs.openclaw.ai/concepts/multi-agent
- Agent Runtime: https://docs.openclaw.ai/concepts/agent
- CLI: https://docs.openclaw.ai/cli/agents
