#!/usr/bin/env powershell
# Install Universal Skill to Codex, CodeBuddy, and OpenClaw

param(
    [Parameter(Mandatory=$true)]
    [string]$SkillName,
    
    [switch]$Force,
    [switch]$Init
)

$ErrorActionPreference = "Stop"

# Paths
$sharedSkillsDir = "$env:USERPROFILE\shared-skills"
$skillSource = "$sharedSkillsDir\$SkillName"
$codexDir = "$env:USERPROFILE\.codex\skills\user\$SkillName"
$openclawDir = "$env:USERPROFILE\.openclaw\skills\$SkillName"
$codebuddyDir = "$env:USERPROFILE\.codebuddy\skills\$SkillName"

function Test-SkillValid {
    param([string]$path)
    if (-not (Test-Path "$path\SKILL.md")) {
        Write-Error "Invalid skill: $path\SKILL.md not found"
        return $false
    }
    return $true
}

function Install-ToCodex {
    Write-Host "Installing to Codex..." -ForegroundColor Cyan
    
    if (-not (Test-Path "$env:USERPROFILE\.codex")) {
        Write-Warning "Codex not installed, skipping"
        return
    }
    
    if (Test-Path $codexDir) {
        if (-not $Force) {
            Write-Warning "Codex skill exists, use -Force to overwrite"
            return
        }
        Remove-Item -Recurse -Force $codexDir
    }
    
    # Copy files (not symlink, for Windows compatibility)
    Copy-Item -Recurse $skillSource $codexDir
    Write-Host "✓ Installed to: $codexDir" -ForegroundColor Green
}

function Install-ToOpenClaw {
    Write-Host "Installing to OpenClaw..." -ForegroundColor Cyan
    
    if (-not (Test-Path "$env:USERPROFILE\.openclaw")) {
        Write-Warning "OpenClaw not installed, skipping"
        return
    }
    
    if (Test-Path $openclawDir) {
        if (-not $Force) {
            Write-Warning "OpenClaw skill exists, use -Force to overwrite"
            return
        }
        Remove-Item -Recurse -Force $openclawDir
    }
    
    Copy-Item -Recurse $skillSource $openclawDir
    Write-Host "✓ Installed to: $openclawDir" -ForegroundColor Green
}

function Install-ToCodeBuddy {
    Write-Host "Installing to CodeBuddy..." -ForegroundColor Cyan
    
    # CodeBuddy can use shared location directly
    # But also create a reference for clarity
    
    if (-not (Test-Path "$env:USERPROFILE\.codebuddy")) {
        New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codebuddy" | Out-Null
    }
    
    if (Test-Path $codebuddyDir) {
        if (-not $Force) {
            Write-Warning "CodeBuddy skill exists, use -Force to overwrite"
            return
        }
        Remove-Item -Recurse -Force $codebuddyDir
    }
    
    # Create junction/symlink or copy
    # For simplicity, copy on Windows
    Copy-Item -Recurse $skillSource $codebuddyDir
    Write-Host "✓ Installed to: $codebuddyDir" -ForegroundColor Green
    Write-Host "  Note: CodeBuddy also reads from shared location: $skillSource" -ForegroundColor Gray
}

# Main
Write-Host "Installing Universal Skill: $SkillName" -ForegroundColor Yellow
Write-Host "Source: $skillSource" -ForegroundColor Gray
Write-Host ""

if (-not (Test-SkillValid $skillSource)) {
    exit 1
}

Install-ToCodex
Write-Host ""

Install-ToOpenClaw
Write-Host ""

Install-ToCodeBuddy
Write-Host ""

Write-Host "Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Verification:" -ForegroundColor Yellow
Write-Host "  Codex:    Test with 'openclaw gateway status' query"
Write-Host "  OpenClaw: Run 'openclaw skills list'"
Write-Host "  CodeBuddy: Check ~/.codebuddy/skills/$SkillName"
