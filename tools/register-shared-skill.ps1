param(
    [Parameter(Mandatory = $true)]
    [string]$SkillName,

    [string]$SourcePath,

    [switch]$Init,

    [switch]$Force,

    [ValidateSet("codex", "openclaw", "both")]
    [string]$Target = "both"
)

$ErrorActionPreference = "Stop"

$homeDir = [Environment]::GetFolderPath("UserProfile")
$sharedRoot = Join-Path $homeDir "shared-skills"

if (-not $SourcePath) {
    $SourcePath = Join-Path $sharedRoot $SkillName
}

$sourceFullPath = [System.IO.Path]::GetFullPath($SourcePath)
$skillFile = Join-Path $sourceFullPath "SKILL.md"

if ($Init) {
    New-Item -ItemType Directory -Path $sourceFullPath -Force | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $sourceFullPath "references") -Force | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $sourceFullPath "scripts") -Force | Out-Null

    if (-not (Test-Path $skillFile)) {
        $template = @"
---
name: $SkillName
description: Shared skill for Codex and OpenClaw. Update this description so the skill triggers on the right tasks.
---

# $SkillName

## When To Use

Use this skill when the task matches the description above.

## Workflow

1. Read only the references you need.
2. Prefer bundled scripts for repeatable operations.
3. Keep changes in this shared skill compatible with both Codex and OpenClaw.
"@
        Set-Content -Path $skillFile -Value $template -Encoding UTF8
    }
}

if (-not (Test-Path $sourceFullPath)) {
    throw "Source skill directory does not exist: $sourceFullPath"
}

if (-not (Test-Path $skillFile)) {
    throw "Missing SKILL.md in source skill directory: $skillFile"
}

$targets = switch ($Target) {
    "codex" { @("codex") }
    "openclaw" { @("openclaw") }
    default { @("codex", "openclaw") }
}

function Ensure-Junction {
    param(
        [string]$LinkPath,
        [string]$DestinationPath,
        [switch]$ForceReplace
    )

    $parent = Split-Path -Parent $LinkPath
    New-Item -ItemType Directory -Path $parent -Force | Out-Null

    if (Test-Path $LinkPath) {
        $existing = Get-Item -LiteralPath $LinkPath -Force
        if ($existing.LinkType -eq "Junction" -or $existing.LinkType -eq "SymbolicLink") {
            if ($ForceReplace) {
                Remove-Item -LiteralPath $LinkPath -Force -Recurse
            } else {
                Write-Host "Skip existing link: $LinkPath"
                return
            }
        } else {
            if ($ForceReplace) {
                Remove-Item -LiteralPath $LinkPath -Force -Recurse
            } else {
                throw "Target path exists and is not a link: $LinkPath. Re-run with -Force to replace it."
            }
        }
    }

    New-Item -ItemType Junction -Path $LinkPath -Target $DestinationPath | Out-Null
    Write-Host "Linked $LinkPath -> $DestinationPath"
}

foreach ($item in $targets) {
    switch ($item) {
        "codex" {
            $link = Join-Path $homeDir ".codex\skills\user\$SkillName"
            Ensure-Junction -LinkPath $link -DestinationPath $sourceFullPath -ForceReplace:$Force
        }
        "openclaw" {
            $link = Join-Path $homeDir ".openclaw\skills\$SkillName"
            Ensure-Junction -LinkPath $link -DestinationPath $sourceFullPath -ForceReplace:$Force
        }
    }
}

Write-Host ""
Write-Host "Done."
Write-Host "Source: $sourceFullPath"
Write-Host "Targets: $($targets -join ', ')"
