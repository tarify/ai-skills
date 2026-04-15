# Installation Guide

## Overview

This skill is designed to be used by **Codex**, **CodeBuddy**, and **OpenClaw** simultaneously.

## Installation Methods

### Method 1: Using shared-skill-bridge (Recommended)

This method creates symbolic links so all three runtimes share the same skill source.

```powershell
# 1. Ensure shared-skills tools exist
ls ~/shared-skills/tools/register-shared-skill.ps1

# 2. Register this skill
powershell -ExecutionPolicy Bypass -File "$HOME/shared-skills/tools/register-shared-skill.ps1" -SkillName "openclaw-docs-index" -Force

# 3. Verify installation
ls ~/.codex/skills/user/openclaw-docs-index
ls ~/.openclaw/skills/openclaw-docs-index
```

### Method 2: Manual Installation

#### For Codex

```bash
# Create directory
mkdir -p ~/.codex/skills/user/openclaw-docs-index

# Copy files
cp -r ~/shared-skills/openclaw-docs-index/* ~/.codex/skills/user/openclaw-docs-index/

# Verify
cat ~/.codex/skills/user/openclaw-docs-index/SKILL.md
```

#### For CodeBuddy

CodeBuddy reads skills from multiple locations:

```bash
# Option A: Use shared directory directly (recommended)
# CodeBuddy can read from ~/shared-skills/openclaw-docs-index/

# Option B: Copy to CodeBuddy workspace
mkdir -p ~/.codebuddy/skills/openclaw-docs-index
cp -r ~/shared-skills/openclaw-docs-index/* ~/.codebuddy/skills/openclaw-docs-index/
```

**Note**: CodeBuddy protocols reference this skill at:
- `d:/protocols/codebuddy/codebuddy-protocol-v1.md`

Update your agent configs to reference this path.

#### For OpenClaw

```bash
# Create directory
mkdir -p ~/.openclaw/skills/openclaw-docs-index

# Copy files
cp -r ~/shared-skills/openclaw-docs-index/* ~/.openclaw/skills/openclaw-docs-index/

# Verify
openclaw skills list
```

### Method 3: Git Clone (For Teams)

```bash
# Clone to shared location
git clone https://your-repo/openclaw-docs-index.git ~/shared-skills/openclaw-docs-index

# Then use Method 1 or 2 to link
```

## Verification

### Test in Codex

```
Ask Codex: "What should I check if Gateway won't start?"
Expected: References Gateway.md troubleshooting
```

### Test in CodeBuddy

```
Ask CodeBuddy: "Generate OpenClaw-compatible agent config"
Expected: Uses sections/Agents.md for patterns
```

### Test in OpenClaw

```bash
# List skills
openclaw skills list | grep openclaw-docs-index

# Check skill loaded
cat ~/.openclaw/skills/openclaw-docs-index/SKILL.md
```

## Update Procedure

When the skill is updated:

```bash
# If using shared-skill-bridge (Method 1):
# Re-run registration to refresh links
powershell -ExecutionPolicy Bypass -File "$HOME/shared-skills/tools/register-shared-skill.ps1" -SkillName "openclaw-docs-index" -Force

# If using manual installation (Method 2):
# Re-copy files to all three locations
cp -r ~/shared-skills/openclaw-docs-index/* ~/.codex/skills/user/openclaw-docs-index/
cp -r ~/shared-skills/openclaw-docs-index/* ~/.openclaw/skills/openclaw-docs-index/
# (CodeBuddy uses shared location directly)
```

## Troubleshooting

### Skill not found in Codex

```bash
# Check path
ls ~/.codex/skills/user/openclaw-docs-index/SKILL.md

# Check permissions
chmod 644 ~/.codex/skills/user/openclaw-docs-index/SKILL.md

# Restart Codex session
```

### Skill not found in OpenClaw

```bash
# Check path
ls ~/.openclaw/skills/openclaw-docs-index/SKILL.md

# Reload skills
openclaw skills reload
```

### Encoding issues (Windows)

If you see garbled Chinese characters:
```powershell
# Ensure UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Or convert file encoding
Get-Content file.md -Encoding UTF8 | Set-Content file.md -Encoding UTF8
```

## Uninstall

```bash
# Remove from Codex
rm -rf ~/.codex/skills/user/openclaw-docs-index

# Remove from OpenClaw
rm -rf ~/.openclaw/skills/openclaw-docs-index

# Remove shared source (optional)
rm -rf ~/shared-skills/openclaw-docs-index
```

## References

- Shared Skill Bridge: `~/shared-skills/shared-skill-bridge/SKILL.md`
- OpenClaw Skills: https://docs.openclaw.ai/concepts/skills
- Codex Skills: ~/.codex/skills/README.md (if exists)
