---
name: openclaw-docs-index
description: |
  Universal reference skill for OpenClaw documentation navigation and troubleshooting.
  Used by: Codex (review), CodeBuddy (develop), OpenClaw (runtime).
  Provides quick lookup paths for Gateway, Channels, Agents, Models, Nodes, Configuration.
type: universal
supported_runtimes:
  - codex
  - codebuddy
  - openclaw
version: "1.0"
---

# OpenClaw Docs Index - Universal Skill

## Purpose

This skill provides a unified documentation index for OpenClaw, enabling:
- **Codex**: Understand OpenClaw architecture during code review
- **CodeBuddy**: Navigate OpenClaw patterns when generating code
- **OpenClaw**: Runtime reference for agent orchestration

## Quick Decision Tree

```
User mentions Gateway issue?
  → Read: sections/Gateway.md
  → Key: cli/gateway, gateway/configuration

User mentions chat platform (Telegram/WhatsApp/Discord)?
  → Read: sections/Channels.md
  → Key: channels, cli/channels

User mentions multi-agent / workspace isolation?
  → Read: sections/Agents.md
  → Key: concepts/multi-agent, channels/channel-routing

User mentions model configuration?
  → Read: sections/Models.md
  → Key: concepts/models, gateway/configuration

User mentions device/node capabilities?
  → Read: sections/Nodes.md
  → Key: nodes, cli/nodes

User mentions config validation / hot reload?
  → Read: sections/Configuration.md
  → Key: gateway/configuration, gateway/configuration-reference
```

## Runtime-Specific Usage

### For Codex (Review Mode)

When reviewing OpenClaw-related code:
1. Check `sections/` for architectural context
2. Verify against `reference/config-fields.md` for valid configuration patterns
3. Use `troubleshooting/common-issues.md` to identify potential problems

**Constraints**:
- Only read, do not modify skill files
- Use this skill for context, not as authoritative source (check official docs for latest)

### For CodeBuddy (Develop Mode)

When generating OpenClaw-compatible code:
1. Check `reference/api-patterns.md` for common patterns
2. Use `sections/Configuration.md` to understand config structure
3. Follow `quick-reference.md` for command examples

**Output Location**:
- Generated code reports → `d:/protocols/codebuddy/task-executions/`
- Analysis results → `d:/protocols/codebuddy/code-analysis/`

### For OpenClaw (Runtime)

When orchestrating agent tasks:
1. Use `orchestrator-routing.md` to determine task routing
2. Check `sections/Agents.md` for multi-agent patterns
3. Reference `handoff-patterns.md` for inter-agent communication

## Key Files

| File | Purpose | Access Frequency |
|------|---------|------------------|
| `index.md` | Full documentation index | Low (reference) |
| `quick-reference.md` | Common commands and paths | High (daily use) |
| `sections/*.md` | Per-module deep dives | Medium (as needed) |
| `reference/*.md` | Config fields, API patterns | High (lookup) |
| `troubleshooting/*.md` | Common issues and solutions | Medium (debugging) |

## Canonical Sources

This skill indexes but does not replace:
- **Official Docs**: https://docs.openclaw.ai/
- **Runtime Protocol**: `d:/protocols/openclaw/runtime-protocol-v1.md`
- **CodeBuddy Protocol**: `d:/protocols/codebuddy/codebuddy-protocol-v1.md`
- **Codex Protocol**: `~/codex-review-protocol-v1.md` (用户主目录下)

## Maintenance

**Update Frequency**: Check official docs monthly for major changes
**Last Updated**: 2026-04-05
**Version**: 1.0

## Cross-References

- Links to `agent-handoff-protocol` skill for task routing details
- Links to `shared-skill-bridge` for skill registration patterns
- Used by all agents in `~/.openclaw/workspace-*/`
