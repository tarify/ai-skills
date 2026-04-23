# 小夜创作模式 Skill

这个 skill 将小说创作方法论抽象成了可复用的标准化创作模式，不依赖任何特定平台或工具。

## 核心特性

- **任务分级体系**：L0即时答复 → L1单步执行 → L2流程编排 → L3后台辅助
- **功能模块化**：创作、评审、管理三大模块
- **流程编排**：标准化的创作并评审流程
- **后台辅助**：支持大规模创作任务的并行处理
- **完整归档**：自动化的文件管理体系

## 使用方法

### 1. 安装 Skill

**方式一：通过 Git 克隆**
```bash
git clone https://github.com/tarify/ai-skills.git
cd ai-skills
```

**方式二：下载压缩包**
直接下载 `xiaoye-writing-mode` 文件夹到你本地的 skill 目录。

### 2. 注册到 CodeBuddy / OpenClaw

**Windows (PowerShell):**
```powershell
# 以管理员身份运行 PowerShell
./register-shared-skill.ps1 -SkillName "xiaoye-writing-mode"
```

**手动注册（符号链接）：**
```bash
# Codex
cd ~/.codex/skills/user
ln -s ~/shared-skills/xiaoye-writing-mode xiaoye-writing-mode

# OpenClaw
cd ~/.openclaw/skills
ln -s ~/shared-skills/xiaoye-writing-mode xiaoye-writing-mode
```

### 3. 初始化工作空间

首次激活 skill 时，系统会自动检查并初始化配置。如需手动运行：

```bash
node init-workspace.js
```

这会在当前工作目录创建以下配置文件：
- `AGENTS.md` - Agent 配置
- `SOUL.md` - 角色设定
- `MEMORY.md` - 用户偏好记忆
- `rules/` - 创作规则文档
- `templates/` - 常用模板
- `modules/` - 功能模块文档

## 触发词

使用以下关键词激活 skill：
- `小夜，开启创作模式`
- `进入写作模式`
- `开始创作`
- `写一篇小说`

## 文件结构

```
xiaoye-writing-mode/
├── SKILL.md              # 技能定义和完整方法论
├── README.md             # 使用说明
├── init-workspace.js     # 初始化脚本
└── scaffold/             # 配置模板
    ├── AGENTS.md         # Agent 配置
    ├── SOUL.md           # 角色设定
    ├── MEMORY.md         # 记忆模板
    ├── modules/          # 功能模块
    │   ├── writer-module.md
    │   ├── reviewer-module.md
    │   └── coordinator-module.md
    ├── rules/            # 创作规则
    │   ├── 写作规范.md
    │   ├── 评审标准.md
    │   └── 管理流程.md
    └── templates/        # 模板文件
        ├── 大纲模板.md
        ├── 人物卡模板.md
        ├── 辩证分析模板.md
        ├── 评审报告模板.md
        ├── 项目看板模板.md
        └── 后台任务指南.md
```

## 适用场景

适用于任何小说创作项目，特别是：
- 长篇小说的章节创作
- 多人协作的创作项目
- 需要标准化流程的出版级作品
- 学习系统化写作方法的作者