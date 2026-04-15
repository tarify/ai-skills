# Channels

## Overview

聊天平台接入层。管理多平台、多账号、消息路由。

## Supported Platforms

- Telegram
- WhatsApp
- Discord
- Slack
- Signal
- WeChat
- Lark/Feishu
- QQ

## Key Concepts

- **Channel**: 聊天平台类型
- **Account**: 平台内的账号
- **Peer**: 对话对象（用户/群组）
- **Routing**: 消息路由规则
- **Capabilities**: 平台能力检测

## CLI Commands

```bash
# 列出渠道
openclaw channels list

# 查看账号
openclaw channels accounts --channel telegram

# 检查能力
openclaw channels capabilities --channel telegram --account @bot

# 状态探测
openclaw channels status --probe

# 解析名称
openclaw channels resolve --channel telegram --name @username
```

## Configuration

```json
{
  "channels": {
    "telegram": {
      "accounts": [{
        "token": "BOT_TOKEN",
        "allowFrom": ["*"],
        "groupPolicy": "smart"
      }]
    }
  }
}
```

## Routing

Messages are routed by:
- `channel + accountId + peer`
- Bindings map to specific agents

## Common Issues

| Issue | Check | Solution |
|-------|-------|----------|
| Message not received | Token valid? | Regenerate bot token |
| Can't send to group | Privacy mode | Disable privacy or add bot |
| Webhook fails | HTTPS required | Use reverse proxy |

## Official Docs

- Overview: https://docs.openclaw.ai/channels
- CLI: https://docs.openclaw.ai/cli/channels
- Routing: https://docs.openclaw.ai/channels/channel-routing
