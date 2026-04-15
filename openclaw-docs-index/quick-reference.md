# Quick Reference

## Common Commands

### Gateway
```bash
openclaw gateway start          # 前台启动
openclaw gateway start --daemon # 后台启动
openclaw gateway stop           # 停止
openclaw gateway status         # 状态
openclaw gateway reload         # 热重载配置
openclaw doctor                 # 诊断
openclaw health                 # 健康检查
```

### Channels
```bash
openclaw channels list                    # 列出渠道
openclaw channels accounts                # 查看账号
openclaw channels status --probe          # 状态探测
openclaw channels capabilities            # 能力检测
```

### Agents
```bash
openclaw agents list                      # 列出 agents
openclaw agents status --agent <name>     # 查看状态
openclaw sessions list --agent <name>     # 查看会话
```

### Models
```bash
openclaw models list                      # 列出模型
openclaw models status                    # 模型状态
openclaw models scan                      # 扫描可用模型
```

### Nodes
```bash
openclaw nodes list                       # 列出节点
openclaw nodes status                     # 节点状态
openclaw node start                       # 启动 node host
```

## Key Paths

| Path | Description |
|------|-------------|
| `~/.openclaw/openclaw.json` | 主配置文件 |
| `~/.openclaw/agents/` | Agent 会话存储 |
| `~/.openclaw/workspace-*/` | Agent 工作区 |
| `~/.openclaw/skills/` | 全局技能 |
| `~/.codex/skills/` | Codex 技能 |
| `~/shared-skills/` | 共享技能 |
| `http://127.0.0.1:18789/` | Dashboard |

## Default Ports

| Port | Service |
|------|---------|
| 18789 | Gateway HTTP/WebSocket |
| 18790 | Gateway gRPC (optional) |

## Config Validation

```bash
# 检查配置
openclaw doctor

# 详细诊断
openclaw status --deep

# 查看日志
openclaw logs
openclaw logs --follow
```

## Emergency Recovery

```bash
# Gateway won't start
1. Check: openclaw doctor
2. Validate: openclaw gateway validate-config
3. Reset: mv ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak
4. Restart: openclaw gateway start

# Session stuck
openclaw sessions list
openclaw sessions kill <id>

# Full reset (careful!)
openclaw gateway stop
rm -rf ~/.openclaw/sessions/*
openclaw gateway start
```

## Handoff Runtime Quick Start

```bash
# L2 Task (plan + build)
1. User request → orchestrator
2. Create: handoffs/T-XXX/00-intake.yaml
3. Planner generates: 10-plan.yaml
4. Builder executes: 20-build.yaml
5. Orchestrator delivers: 40-delivery.yaml

# L3 Task (plan + build + review)
Add step 5: Critic reviews: 30-review.yaml
Then step 6: Delivery
```

## Protocol References

- Runtime: `~/protocols/openclaw/runtime-protocol-v1.md`
- CodeBuddy: `~/protocols/codebuddy/codebuddy-protocol-v1.md`
- Codex Review: `~/codex-review-protocol-v1.md`
