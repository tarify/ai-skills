# OpenClaw Docs Index

生成时间: 2026-04-03
来源主站: https://docs.openclaw.ai/

## 目的

这份索引用于后续设计和排查时快速定位 OpenClaw 文档，不追求逐页摘录，重点是:

- 每个模块是干什么的
- 遇到某类问题应该先查哪里
- 常用入口页和概念页分别在哪

## 总览

OpenClaw 的核心是一个 Gateway。

- Gateway 是单一事实源，负责:
  - 渠道接入
  - 会话和路由
  - 节点连接
  - 配置与控制面
- 其他模块基本都围绕 Gateway 展开:
  - Channels 负责消息入口
  - Agents 负责不同 AI 脑/人格/工作区
  - Models 负责模型和认证
  - Nodes 负责外设和远端设备能力
  - Configuration / Ops 负责运行、热更新、诊断、服务化

## 模块索引

### 1. Overview / What is OpenClaw

作用:

- 解释 OpenClaw 是什么
- 说明核心架构: 单个 Gateway 连接多个聊天平台和 AI agent
- 给出快速开始、Dashboard、本地默认端口、配置文件位置

适合查:

- OpenClaw 的定位
- 初始上手流程
- 默认地址和基础概念

入口:

- https://docs.openclaw.ai/
- 锚点: https://docs.openclaw.ai/#what-is-openclaw

关键点:

- 默认 Dashboard: `http://127.0.0.1:18789/`
- 配置文件: `~/.openclaw/openclaw.json`
- 默认架构关键词: self-hosted, multi-channel, agent-native

### 2. Gateway

作用:

- OpenClaw 的运行核心
- 提供 WebSocket 服务、会话管理、渠道连接、节点接入、hooks
- 负责前台/后台运行、服务化、重启、状态探测

适合查:

- `openclaw gateway ...` 命令
- 服务启动失败
- 计划任务/daemon/service 相关问题
- 网关是否在监听、状态是否正常

入口:

- CLI: https://docs.openclaw.ai/cli/gateway
- 配置: https://docs.openclaw.ai/gateway/configuration
- 配置参考: https://docs.openclaw.ai/gateway/configuration-reference

常见任务去向:

- 启动/停止/前台运行: `cli/gateway`
- 监听、模式、reload、校验: `gateway/configuration`
- 字段级别配置说明: `gateway/configuration-reference`

### 3. Configuration / Ops

作用:

- 统一定义 `~/.openclaw/openclaw.json`
- 管理渠道、模型、agent、tools、sandbox、cron、web、UI 等
- 定义热更新策略和严格校验规则

适合查:

- 配置文件怎么写
- 某个字段是否合法
- 改配置后是否需要重启
- `doctor` / `status` / `health` 相关排障

入口:

- 概览: https://docs.openclaw.ai/gateway/configuration
- 全量字段: https://docs.openclaw.ai/gateway/configuration-reference

关键点:

- 配置格式是 JSON5
- 未知字段会导致 Gateway 拒绝启动
- 多数配置支持 hot reload

### 4. Channels

作用:

- 定义 OpenClaw 接入哪些聊天平台
- 说明每个渠道支持的能力、差异、登录方式、群组行为
- 管理多账号、渠道状态、能力探测、名称解析

适合查:

- Telegram / WhatsApp / Discord / Slack / Signal / WeChat 等接入
- 多账号配置
- 某渠道支持哪些能力
- 某渠道消息为什么收不到/发不出

入口:

- 渠道总览: https://docs.openclaw.ai/channels
- CLI: https://docs.openclaw.ai/cli/channels
- 路由: https://docs.openclaw.ai/channels/channel-routing

关键点:

- Channels 是消息入口
- 一个 Gateway 可同时跑多个渠道
- 可按 `channel + accountId + peer` 路由

子模块职责:

- `channels`
  - 看支持哪些聊天平台、每个平台大致特点
- `cli/channels`
  - 管理账号、登录、状态、capabilities、resolve
- `channels/channel-routing`
  - 看消息如何确定回哪个渠道、哪个账号、哪个会话

### 5. Agents / Multi-Agent

作用:

- 管理多个隔离 agent
- 每个 agent 有独立 workspace、auth、sessions、persona
- 通过 bindings 把不同渠道/账号/发送者路由到不同 agent

适合查:

- 一个网关里跑多个 AI
- 家庭/工作 agent 分离
- 不同 WhatsApp/Telegram 账号绑定不同 agent
- workspace、session、auth profile 如何隔离

入口:

- 概念页: https://docs.openclaw.ai/concepts/multi-agent
- 别名页: https://docs.openclaw.ai/multi-agent
- CLI agents: https://docs.openclaw.ai/cli/agents
- 运行时概念: https://docs.openclaw.ai/concepts/agent

关键点:

- 一个 agent = 一个独立 brain
- 隔离项:
  - workspace
  - `agentDir`
  - sessions
  - auth profiles
- Skills 来源:
  - `~/.openclaw/skills`
  - `<workspace>/skills`

### 6. Models

作用:

- 定义默认模型、fallback 模型、图片模型
- 管理 provider 认证和模型 allowlist/catalog
- 支持 provider failover 和模型扫描

适合查:

- 用哪个模型
- 为什么模型不可用
- OpenRouter / OpenAI / Anthropic 等 provider 怎么配
- `models status` / `models scan` / `models list`

入口:

- 概念页: https://docs.openclaw.ai/concepts/models
- 短路径页: https://docs.openclaw.ai/models

关键点:

- 模型选择顺序: primary -> fallbacks
- provider 内部也可能发生 auth failover
- `agents.defaults.models` 决定 allowlist / alias

### 7. Nodes

作用:

- 让 iOS / Android / macOS / headless 设备作为 Gateway 的外设加入
- 通过 Gateway 暴露 camera、canvas、device、notifications、system 等能力

适合查:

- 手机节点配对
- Android 设备能力调用
- 远端设备执行命令
- companion device / node host 的区别

入口:

- 概览: https://docs.openclaw.ai/nodes
- CLI: https://docs.openclaw.ai/cli/nodes
- 单机 node host: https://docs.openclaw.ai/cli/node

关键点:

- Node 不是 Gateway
- Node 连接到 Gateway 的 WS
- Gateway 收消息, Node 提供设备能力

子模块职责:

- `nodes`
  - 配对、能力模型、设备类别、协议概念
- `cli/nodes`
  - 配对审批、列表、状态、invoke
- `cli/node`
  - 启动一个 headless node host，让这台机器对 Gateway 暴露执行能力

### 8. Reference / CLI

作用:

- 查具体命令怎么用
- 查某个子命令支持哪些参数
- 适合做落地操作而不是理解架构

适合查:

- `openclaw xxx --help` 对应的文档页
- 参数细节
- 命令组合和日常运维操作

常用入口:

- `cli/gateway`
- `cli/channels`
- `cli/agents`
- `cli/nodes`
- `cli/node`

使用策略:

- 先看概念页确定模块
- 再看 CLI 页确定命令和参数

### 9. Help / Troubleshooting / Diagnostics

作用:

- 用于诊断配置错误、渠道问题、启动失败、连通性异常
- 是排障入口，不是架构入口

适合查:

- Gateway 起不来
- 配置校验失败
- 渠道状态异常
- 节点配对或连接异常

入口:

- 首页 Help hub: https://docs.openclaw.ai/
- 与问题最接近的模块页内 Troubleshooting 段落
- 常用诊断命令:
  - `openclaw doctor`
  - `openclaw status --deep`
  - `openclaw health`
  - `openclaw logs`
  - `openclaw channels status --probe`
  - `openclaw nodes status`

## 按需求查找

### 我要接一个聊天平台

先查:

- `channels`
- 再看对应平台页或 `cli/channels`

关键词:

- token
- QR pairing
- accounts
- allowFrom
- groupPolicy

### 我要做多人格 / 多工作区 / 多账号路由

先查:

- `concepts/multi-agent`
- `cli/agents`
- `channels/channel-routing`

关键词:

- `agentId`
- `accountId`
- `bindings`
- `workspace`
- `agentDir`

### 我要改模型或 provider

先查:

- `concepts/models`
- `gateway/configuration`

关键词:

- primary
- fallbacks
- imageModel
- providers
- auth profiles

### 我要改 OpenClaw 运行方式

先查:

- `cli/gateway`
- `gateway/configuration`

关键词:

- local mode
- daemon/service
- restart
- reload
- status

### 我要让手机或别的机器提供能力

先查:

- `nodes`
- `cli/nodes`
- `cli/node`

关键词:

- pairing
- `node.invoke`
- camera
- notifications
- `system.run`

### 我要查某个配置字段到底是什么

直接查:

- `gateway/configuration-reference`

这是字段级别最权威入口。

## 我后续设计时的检索顺序

如果你后面让我设计一个基于 OpenClaw 的东西，我会按这个顺序查:

1. 先用 Overview 确定边界
2. 用对应概念页确定架构模块
3. 用 Configuration 确认落地配置面
4. 用 CLI 页确认操作方式
5. 有问题再回到 Troubleshooting / doctor / status

## 当前记忆重点

我后面优先把需求映射到这几个模块:

- 接消息: Channels
- 跑核心服务: Gateway
- 分 brain: Agents
- 选模型: Models
- 接设备能力: Nodes
- 落配置: Configuration
- 排故障: Help / Diagnostics

## 已记录的高频入口

- Overview: https://docs.openclaw.ai/
- What is OpenClaw: https://docs.openclaw.ai/#what-is-openclaw
- Configuration: https://docs.openclaw.ai/gateway/configuration
- Configuration Reference: https://docs.openclaw.ai/gateway/configuration-reference
- Channels: https://docs.openclaw.ai/channels
- Channel Routing: https://docs.openclaw.ai/channels/channel-routing
- Gateway CLI: https://docs.openclaw.ai/cli/gateway
- Channels CLI: https://docs.openclaw.ai/cli/channels
- Multi-Agent: https://docs.openclaw.ai/concepts/multi-agent
- Agent Runtime: https://docs.openclaw.ai/concepts/agent
- Models: https://docs.openclaw.ai/concepts/models
- Nodes: https://docs.openclaw.ai/nodes
- Nodes CLI: https://docs.openclaw.ai/cli/nodes
- Node Host CLI: https://docs.openclaw.ai/cli/node
