# Gateway

## Overview

OpenClaw 的运行核心。提供 WebSocket 服务、会话管理、渠道连接、节点接入、hooks。

## Key Concepts

- **Single source of truth**: Gateway 是单一事实源
- **WebSocket Server**: 处理实时连接
- **Session Management**: 管理用户会话
- **Channel Integration**: 连接聊天平台
- **Node Access**: 外设能力接入

## CLI Commands

```bash
# 启动/停止
openclaw gateway start
openclaw gateway stop
openclaw gateway restart

# 状态检查
openclaw gateway status
openclaw health
openclaw doctor

# 配置重载
openclaw gateway reload
```

## Configuration

Key files:
- Main config: `~/.openclaw/openclaw.json`
- Dashboard: `http://127.0.0.1:18789/`

Important sections:
- `gateway.listen`: WebSocket 监听地址
- `gateway.mode`: local/daemon/service
- `gateway.hotReload`: 热更新策略

## Common Issues

| Issue | Check | Solution |
|-------|-------|----------|
| Gateway won't start | `openclaw doctor` | Check config validation |
| Port 18789 in use | `lsof -i :18789` | Change listen port |
| WS connection fails | Firewall rules | Check 18789/tcp |

## Official Docs

- CLI: https://docs.openclaw.ai/cli/gateway
- Config: https://docs.openclaw.ai/gateway/configuration
- Reference: https://docs.openclaw.ai/gateway/configuration-reference
