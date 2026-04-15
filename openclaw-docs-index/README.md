# OpenClaw Docs Index - Universal Skill

A unified documentation reference skill for **Codex**, **CodeBuddy**, and **OpenClaw**.

## Purpose

Provides quick navigation and troubleshooting reference for OpenClaw architecture, enabling consistent understanding across all AI tools.

## Directory Structure

```
openclaw-docs-index/
├── SKILL.md                    # Skill definition (universal)
├── README.md                   # This file
├── INSTALL.md                  # Installation guide
├── index.md                    # Full documentation index (from Codex)
├── quick-reference.md          # Common commands and paths
│
├── sections/                   # Per-module deep dives
│   ├── Gateway.md             # Gateway core
│   ├── Channels.md            # Chat platform integration
│   ├── Agents.md              # Multi-agent management
│   ├── Models.md              # AI model configuration
│   ├── Nodes.md               # Device/node capabilities
│   └── Configuration.md       # Config management
│
├── reference/                 # Quick lookup tables
│   ├── config-fields.md       # Configuration field reference
│   ├── api-patterns.md        # Common API patterns
│   └── orchestrator-routing.md # Task routing reference
│
└── troubleshooting/           # Problem solving
    ├── common-issues.md       # Frequent problems
    └── diagnostic-commands.md # Debug procedures
```

## Usage by Runtime

### Codex (Code Review)

Uses this skill to:
- Understand OpenClaw architecture during review
- Verify configuration patterns
- Identify potential issues

**Access**: Read-only, via `~/.codex/skills/user/openclaw-docs-index/`

### CodeBuddy (Development)

Uses this skill to:
- Generate OpenClaw-compatible code
- Understand agent patterns
- Follow configuration conventions

**Access**: Read from shared location or `~/.codebuddy/skills/`

### OpenClaw (Runtime)

Uses this skill to:
- Orchestrate agent tasks
- Route messages correctly
- Manage multi-agent workflows

**Access**: Via `~/.openclaw/skills/openclaw-docs-index/`

## Quick Start

```bash
# Install for all three runtimes
cd ~/shared-skills/openclaw-docs-index
cat INSTALL.md

# Or use shared-skill-bridge
powershell -ExecutionPolicy Bypass -File "$HOME/shared-skills/tools/register-shared-skill.ps1" -SkillName "openclaw-docs-index" -Init
```

## Key Information

| Item | Value |
|------|-------|
| **Dashboard** | http://127.0.0.1:18789/ |
| **Config File** | ~/.openclaw/openclaw.json |
| **Main Protocol** | ~/protocols/openclaw/runtime-protocol-v1.md |
| **CodeBuddy Protocol** | ~/protocols/codebuddy/codebuddy-protocol-v1.md |
| **Codex Protocol** | ~/codex-review-protocol-v1.md |

## Maintenance

- **Source**: https://docs.openclaw.ai/
- **Last Updated**: 2026-04-05
- **Version**: 1.0
- **Update Frequency**: Monthly check for major doc changes

## Cross-References

- `agent-handoff-protocol` skill: Task routing details
- `shared-skill-bridge` skill: Registration patterns
- OpenClaw workspaces: `~/.openclaw/workspace-*/`

## License

Internal reference documentation. Based on https://docs.openclaw.ai/
