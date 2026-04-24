# Writing Mode Skill

系统化长篇小说创作技能，将创作方法论抽象为可复用的标准化流程。**平台无关、题材无关**，适用于任何 AI 工具和任何小说类型。

## 核心特性

- **任务分级**：L0 即时答复 → L1 单步执行 → L2 流程编排 → L3 后台辅助
- **辩证创作**：多角度分析 + 逻辑检验 + 自我批判，产出更高质量的内容
- **全题材覆盖**：玄幻 / 都市 / 言情 / 悬疑 / 科幻 / 历史 / 奇幻，每种题材有专项规范
- **标准化评审**：四维度评分体系（逻辑一致性 40% / 可读性 30% / 创新性 20% / 完整性 10%）
- **自动归档**：章节正文、章节简介、评审报告、设定文档全部自动归档
- **上下文连贯**：创作前自动读取前 3 章简介，保持长篇叙事一致性

## 适用工具

OpenClaw / CodeBuddy / Cursor / Claude / ChatGPT 等任意 AI 工具

## 触发词

```
写小说 / 帮我写 / 续写 / 创作章节 / 写第X章
评审章节 / 评审第X章 / 创作并评审
辩证创作 / 多角度分析
查看进度 / 小说待办
使用写作模式 / 系统化创作
```

## 安装

**方式一：Git clone**
```bash
git clone https://github.com/tarify/ai-skills.git
```

**方式二：只下载本 skill**
```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/tarify/ai-skills.git
cd ai-skills
git sparse-checkout set xiaoye-writing-mode
```

### 注册到 CodeBuddy
```bash
mkdir -p ~/.codebuddy/skills/xiaoye-writing-mode
cp -r xiaoye-writing-mode/* ~/.codebuddy/skills/xiaoye-writing-mode/
```

### 注册到 OpenClaw
```bash
mkdir -p ~/.openclaw/skills/xiaoye-writing-mode
cp -r xiaoye-writing-mode/* ~/.openclaw/skills/xiaoye-writing-mode/
```

## 初始化工作空间

### 方式一：脚本自动初始化（推荐）

```bash
node xiaoye-writing-mode/init-workspace.js /your/novel/project
```

脚本会自动检查目标目录，**只复制缺失的文件**，已有文件不会被覆盖。执行结果示例：

```
[writing-mode] 检查工作区配置: /your/novel/project
[writing-mode] 创建目录: rules
[writing-mode] 创建目录: writing-archive
[writing-mode] 创建文件: AGENTS.md
[writing-mode] 创建文件: rules/写作规范.md
[writing-mode] 工作区初始化完成 ✅
```

不传路径时默认初始化当前目录：

```bash
cd /your/novel/project
node /path/to/xiaoye-writing-mode/init-workspace.js
```

也可以在代码中调用：

```js
const { initWorkspace } = require('./xiaoye-writing-mode/init-workspace.js');
await initWorkspace('/your/novel/project');
```

### 方式二：手动复制

```bash
cp -r xiaoye-writing-mode/scaffold/* /your/novel/project/
```

初始化后工作区结构：

```
your-project/
├── AGENTS.md         # AI 架构配置
├── SOUL.md           # 写作助手身份（可自定义角色名）
├── MEMORY.md         # 长期记忆模板
├── modules/          # 功能模块定义
├── rules/            # 创作规则
├── templates/        # 常用模板
├── writing-archive/  # 章节正文归档（运行时自动创建内容）
└── memory/           # 评审报告与进度追踪
```

> `SOUL.md` 底部有自定义说明，可以为你的项目配置专属角色名称和风格。

## 文件结构

```
xiaoye-writing-mode/
├── SKILL.md                    # 技能定义（触发词、架构、流程）
├── README.md                   # 本文件
└── scaffold/                   # 工作区配置模板
    ├── AGENTS.md               # AI 架构与任务分级
    ├── SOUL.md                 # 写作助手身份模板
    ├── MEMORY.md               # 长期记忆模板
    ├── modules/
    │   ├── writer-module.md    # 创作模块
    │   ├── reviewer-module.md  # 评审模块
    │   └── coordinator-module.md # 管理模块
    ├── rules/
    │   ├── 写作规范.md          # 通用规范 + 各题材专项规范
    │   ├── 评审标准.md          # 四维度评分体系
    │   └── 管理流程.md          # 归档与进度管理
    └── templates/
        ├── 辩证分析模板.md      # 辩证创作思考框架
        ├── 评审报告模板.md      # 评审报告格式
        ├── 大纲模板.md          # 故事大纲
        ├── 人物卡模板.md        # 人物设定
        ├── 项目看板模板.md      # 进度看板
        └── 后台任务指南.md      # L3 后台任务说明
```

## 工作区归档结构

skill 运行后会在工作区自动创建以下目录：

```
your-project/
├── writing-archive/
│   └── {项目名}/
│       ├── 章节/
│       │   ├── 第1章-{标题}.md
│       │   └── 章节简介/        # 每章独立简介，创作前自动读取
│       └── 设定/
│           ├── 人物/
│           ├── 世界观/
│           └── 情节/
└── memory/
    └── projects/
        └── {项目名}/
            ├── reviews/         # 评审报告
            ├── progress.md      # 进度追踪
            └── todo.md          # 待办事项
```

## 快速上手

```
# 查看项目进度
进度

# 创作新章节
写第三章，推进主角成长，目标3000字

# 创作并自动评审
创作并评审第三章

# 辩证创作（多角度分析后产出）
用辩证方法写第三章的转折点

# 评审已有章节
评审第二章
```

## 题材专项规范

`rules/写作规范.md` 包含以下题材的专项规范：

| 题材 | 核心规范要点 |
|------|------------|
| 玄幻 / 奇幻 | 力量体系描写、境界感官化、世界观渐进揭示 |
| 都市 / 现实 | 爽点铺垫、对话口语化、生活细节真实感 |
| 言情 | 情感节奏分层、误会合理性、甜虐平衡 |
| 悬疑 / 推理 | 线索预埋、信息节奏、推理透明度 |
| 科幻 | 科技感营造、禁用现代工业词汇、设定一致性 |
| 历史 / 古风 | 时代感对话、称谓制度、架空逻辑自洽 |

## License

MIT
