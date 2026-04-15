# Shared Skills

通用 AI 技能集合，支持 Codex、CodeBuddy 和 OpenClaw 多运行时环境。

## 技能列表

### 1. dev-workflow (开发流程规范)

**描述**: 通用开发流程规范技能，提供任务分级、角色分工、工具组合和流程阶段的标准指南。

**核心功能**:
- 任务分级: L0(问答) → L1(规划) → L2(产物) → L3(高风险)
- 角色分工: 协调者、规划者、执行者、审查者
- 工具组合: 执行工具 + 审查工具的搭配策略
- 流程阶段: Intake → Planning → Confirmation → Building → Reviewing → Delivery

**触发关键词**: 开发流程、任务分级、L0/L1/L2/L3、协调者、规划者、执行者、审查者、任务信封

**目录结构**:
```
dev-workflow/
├── SKILL.md                    # 主技能文件
├── references/
│   ├── agent-team-mode.md      # 代理团队模式
│   ├── environment-detection.md # 环境检测
│   ├── subagent-mode.md        # 子代理模式
│   ├── user-config-template.md # 用户配置模板
│   └── workflow-spec.md        # 完整流程规范
└── scripts/
    └── detect-environment.py   # 环境检测脚本
```

---

### 2. openclaw-docs-index (OpenClaw 文档索引)

**描述**: OpenClaw 文档导航和故障排除的通用参考技能。

**适用运行时**: Codex (代码审查)、CodeBuddy (开发)、OpenClaw (运行时)

**提供内容**:
- Gateway、Channels、Agents、Models、Nodes、Configuration 快速查找
- 故障排除指南
- 快速参考命令

**目录结构**:
```
openclaw-docs-index/
├── SKILL.md
├── index.md
├── quick-reference.md
├── sections/
│   ├── Agents.md
│   ├── Channels.md
│   ├── Gateway.md
│   └── ...
└── troubleshooting/
```

---

### 3. github (GitHub CLI 交互)

**描述**: 使用 `gh` CLI 与 GitHub 交互。

**支持操作**:
- Issues: `gh issue create/list/view`
- Pull Requests: `gh pr create/list/view/merge`
- CI Runs: `gh run list/view`
- API 查询: `gh api`

**使用示例**:
```bash
gh issue list --repo owner/repo
gh pr create --title "Fix bug" --body "Description"
```

---

## 工具脚本

`tools/` 目录包含用于管理共享技能的 PowerShell 脚本：

| 脚本 | 功能 |
|------|------|
| `register-shared-skill.ps1` | 注册 skill 到 Codex/OpenClaw（创建 Junction 链接，自动同步更新） |
| `install-universal-skill.ps1` | 安装 skill 到 Codex/OpenClaw/CodeBuddy（复制文件，独立副本） |

### 使用示例

```powershell
# 注册 dev-workflow 到 Codex 和 OpenClaw（创建符号链接）
./tools/register-shared-skill.ps1 -SkillName "dev-workflow" -Force

# 安装到所有三个运行时（复制文件）
./tools/install-universal-skill.ps1 -SkillName "dev-workflow" -Force
```

**区别**:
- **register**: 创建 Junction 链接，源文件改动自动同步到目标
- **install**: 复制文件，各环境独立，适合需要定制化的场景

---

## 安装指南

### 安装单个 Skill 到 CodeBuddy

```bash
# 复制到 CodeBuddy skills 目录
mkdir -p ~/.codebuddy/skills/<skill-name>
cp -r ~/shared-skills/<skill-name>/* ~/.codebuddy/skills/<skill-name>/
```

### 安装单个 Skill 到 Codex

```bash
mkdir -p ~/.codex/skills/user/<skill-name>
cp -r ~/shared-skills/<skill-name>/* ~/.codex/skills/user/<skill-name>/
```

### 安装单个 Skill 到 OpenClaw

```bash
mkdir -p ~/.openclaw/skills/<skill-name>
cp -r ~/shared-skills/<skill-name>/* ~/.openclaw/skills/<skill-name>/
```

---

## 目录结构

```
shared-skills/
├── README.md                           # 本文件
├── dev-workflow/                       # 开发流程规范
├── openclaw-docs-index/                # OpenClaw 文档索引
├── github/                             # GitHub CLI 交互
└── tools/                              # 管理脚本
    ├── register-shared-skill.ps1
    └── install-universal-skill.ps1
```

---

## 添加新 Skill

1. 在 `shared-skills/` 下创建新目录
2. 添加 `SKILL.md`（必须包含 YAML frontmatter: name 和 description）
3. 可选添加 `references/` 和 `scripts/` 子目录
4. 使用工具脚本安装到目标运行时

**SKILL.md 最小模板**:
```markdown
---
name: my-skill
description: 描述这个 skill 的功能和触发条件
---

# My Skill

## 使用场景

何时使用这个 skill...

## 工作流程

1. 步骤一
2. 步骤二
```

---

## 许可证

MIT License - 自由使用和修改
