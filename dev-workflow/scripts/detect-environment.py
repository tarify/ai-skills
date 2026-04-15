#!/usr/bin/env python3
"""
Environment Detection Script for Dev Workflow Skill

Detects the current execution environment and recommends appropriate tools.

Usage:
    python detect-environment.py              # 检测当前环境
    python detect-environment.py --json       # JSON 格式输出
    python detect-environment.py --init       # 初始化配置文件（默认 subagent 模式）

Note: Tools are configured via ~/.openclaw/config/dev-workflow.yaml
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Try to import yaml, but provide fallback if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def check_command(name):
    """Check if a command is available in PATH."""
    if not name:
        return False
    result = shutil.which(name)
    return result is not None


def get_version(name):
    """Get version string for a command, if available."""
    if not name:
        return None
    try:
        result = subprocess.run(
            [name, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip().split("\n")[0]
    except Exception:
        pass
    return None


def get_config_paths():
    """Get possible config file paths in priority order."""
    paths = [
        Path.cwd() / ".dev-workflow.yaml",           # 项目级别
        Path.home() / ".dev-workflow.yaml",          # Home 目录
        Path.home() / ".config" / "dev-workflow.yaml",  # XDG 标准位置
    ]
    return paths


def find_config_file():
    """Find existing config file."""
    for path in get_config_paths():
        if path.exists():
            return path
    return None


def load_user_config():
    """Load user configuration from file."""
    config_path = find_config_file()

    if config_path is None:
        return None

    if not HAS_YAML:
        # Fallback: simple YAML-like parsing for basic config
        try:
            content = config_path.read_text(encoding="utf-8")
            return parse_simple_yaml(content)
        except Exception:
            return None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def parse_simple_yaml(content):
    """Simple YAML parser for basic config structure."""
    config = {}
    current_section = None
    current_subsection = None

    for line in content.split("\n"):
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue

        # Detect indentation level
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if ":" in stripped and not stripped.startswith("-"):
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()

            if indent == 0:
                current_section = key
                config[current_section] = {}
                current_subsection = None
            elif indent == 2 and current_section:
                current_subsection = key
                config[current_section][current_subsection] = {}
            elif indent == 4 and current_section and current_subsection:
                if value:
                    config[current_section][current_subsection][key] = value.strip("\"'")
                else:
                    config[current_section][current_subsection][key] = {}

    return config


def get_configured_tools(config):
    """Extract tool names from user configuration."""
    tools = {
        "execution": None,
        "review": None
    }

    if not config:
        return tools

    tool_priority = config.get("tool_priority", {})

    # Get execution tool
    exec_config = tool_priority.get("execution", {})
    tools["execution"] = exec_config.get("primary")

    # Get review tool
    review_config = tool_priority.get("review", {})
    tools["review"] = review_config.get("primary")

    # Handle subagent as special case
    if tools["execution"] == "subagent":
        tools["execution"] = None  # subagent doesn't need CLI check
        tools["subagent_mode"] = True
    else:
        tools["subagent_mode"] = False

    if tools["review"] == "subagent":
        tools["review"] = None
        tools["subagent_review"] = True
    else:
        tools["subagent_review"] = False

    return tools


def detect_environment():
    """Detect the current environment configuration."""
    # Load user configuration
    config = load_user_config()
    configured_tools = get_configured_tools(config)
    
    # Find config file location
    config_file = find_config_file()

    env = {
        "mode": "main_agent",
        "tools": {},
        "workspace": {},
        "recommendations": {},
        "config_status": {}
    }

    # Core tools (always checked)
    core_tools = ["git", "python"]
    for tool in core_tools:
        available = check_command(tool)
        env["tools"][tool] = {
            "available": available,
            "version": get_version(tool) if available else None
        }

    # User-configured execution tool
    exec_tool = configured_tools.get("execution")
    if exec_tool:
        available = check_command(exec_tool)
        env["tools"]["execution_tool"] = {
            "name": exec_tool,
            "available": available,
            "version": get_version(exec_tool) if available else None
        }
    else:
        env["tools"]["execution_tool"] = {
            "name": configured_tools.get("subagent_mode") and "subagent" or None,
            "available": configured_tools.get("subagent_mode", False),
            "version": None
        }

    # User-configured review tool
    review_tool = configured_tools.get("review")
    if review_tool:
        available = check_command(review_tool)
        env["tools"]["review_tool"] = {
            "name": review_tool,
            "available": available,
            "version": get_version(review_tool) if available else None
        }
    else:
        env["tools"]["review_tool"] = {
            "name": configured_tools.get("subagent_review") and "subagent" or None,
            "available": configured_tools.get("subagent_review", False),
            "version": None
        }

    # Subagent capability
    env["tools"]["subagent"] = {
        "available": True,  # subagent is always available if runtime supports it
        "version": None
    }

    # Workspace detection
    cwd = Path.cwd()
    env["workspace"]["current_dir"] = str(cwd)
    env["workspace"]["has_git"] = cwd.joinpath(".git").exists()

    # Recommendations based on configuration
    exec_tool_info = env["tools"]["execution_tool"]
    review_tool_info = env["tools"]["review_tool"]

    if exec_tool_info.get("name") == "subagent" or configured_tools.get("subagent_mode"):
        env["recommendations"]["execution_backend"] = "subagent"
    elif exec_tool_info.get("available"):
        env["recommendations"]["execution_backend"] = exec_tool_info.get("name", "local")
    else:
        env["recommendations"]["execution_backend"] = "local"

    if review_tool_info.get("name") == "subagent" or configured_tools.get("subagent_review"):
        env["recommendations"]["review_backend"] = "subagent"
    elif review_tool_info.get("available"):
        env["recommendations"]["review_backend"] = review_tool_info.get("name", "skip")
    else:
        env["recommendations"]["review_backend"] = "skip"

    # Config status
    env["config_status"]["config_file_exists"] = config_file is not None
    env["config_status"]["execution_tool_configured"] = exec_tool is not None or configured_tools.get("subagent_mode", False)
    env["config_status"]["review_tool_configured"] = review_tool is not None or configured_tools.get("subagent_review", False)

    return env


def create_default_config(custom_path=None):
    """Create default configuration file (subagent mode)."""
    if custom_path:
        config_path = Path(custom_path)
    else:
        # 默认使用 XDG 标准位置
        config_path = Path.home() / ".config" / "dev-workflow.yaml"
    
    if config_path.exists():
        return {
            "status": "exists",
            "path": str(config_path),
            "message": "配置文件已存在，无需重复创建"
        }
    
    # Create directory if not exists
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Default config content
    default_config = """# dev-workflow Skill 配置文件
# 创建时间: {created_at}
# 
# 此配置定义您的执行工具和审查工具。
# 默认使用 subagent 模式，无需安装额外工具。

tool_priority:
  # 执行工具：用于代码实现、修改、重构等
  execution:
    primary: subagent    # 默认：使用子代理执行

  # 审查工具：用于独立验证、质量评估
  review:
    primary: subagent    # 默认：使用子代理审查

# ========================================
# 可选：如果您有特定的 CLI 工具
# ========================================
# 
# 取消注释以下配置以使用您的工具：
#
# tool_priority:
#   execution:
#     primary: codebuddy    # 或 codex, claude-code, cursor, aider
#     fallback: subagent
#   review:
#     primary: codex        # 或 codebuddy, claude-code
#     fallback: subagent

# ========================================
# 支持的工具类型
# ========================================
# 
# CLI 工具：codebuddy, codex, claude-code, cursor, aider
# 内置模式：subagent（推荐默认）
# 自定义：脚本路径
#
# 详细配置见：references/user-config-template.md
#
# ========================================
# 配置文件位置（按优先级查找）
# ========================================
# 1. ./.dev-workflow.yaml（项目级别）
# 2. ~/.dev-workflow.yaml（Home 目录）
# 3. ~/.config/dev-workflow.yaml（默认位置）
""".format(created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    config_path.write_text(default_config, encoding="utf-8")
    
    return {
        "status": "created",
        "path": str(config_path),
        "message": "配置文件已创建（默认 subagent 模式）"
    }


def format_output(env, use_json=False):
    """Format environment data for output."""
    if use_json:
        return json.dumps(env, indent=2, ensure_ascii=False)

    lines = ["environment:"]
    lines.append(f"  mode: {env['mode']}")

    lines.append("  tools:")
    for tool, info in env["tools"].items():
        if isinstance(info, dict):
            if "name" in info:
                # User-configured tool
                name = info.get("name") or "not_configured"
                status = "available" if info.get("available") else "unavailable"
                version = f" ({info.get('version')})" if info.get("version") else ""
                lines.append(f"    {tool}: {name} ({status}){version}")
            else:
                status = "available" if info.get("available") else "unavailable"
                version = f" ({info.get('version')})" if info.get("version") else ""
                lines.append(f"    {tool}: {status}{version}")
        else:
            lines.append(f"    {tool}: {info}")

    lines.append("  workspace:")
    for key, value in env["workspace"].items():
        if isinstance(value, bool):
            value = "true" if value else "false"
        lines.append(f"    {key}: {value}")

    lines.append("  recommendations:")
    for key, value in env["recommendations"].items():
        lines.append(f"    {key}: {value}")

    lines.append("  config_status:")
    for key, value in env["config_status"].items():
        if isinstance(value, bool):
            value = "true" if value else "false"
        lines.append(f"    {key}: {value}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Dev Workflow 环境检测和配置工具"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出"
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="初始化配置文件（默认 subagent 模式）"
    )
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="指定配置文件位置（可选）"
    )
    args = parser.parse_args()

    if args.init:
        # 初始化配置文件
        result = create_default_config(custom_path=args.path)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"📁 配置文件: {result['path']}")
            print(f"✅ 状态: {result['message']}")
            print()
            print("📝 默认配置:")
            print("   执行工具: subagent")
            print("   审查工具: subagent")
            print()
            print("💡 如需配置特定工具（如 CodeBuddy、Codex），请编辑配置文件")
            print()
            print("📂 配置文件查找优先级：")
            print("   1. ./.dev-workflow.yaml（项目级别）")
            print("   2. ~/.dev-workflow.yaml（Home 目录）")
            print("   3. ~/.config/dev-workflow.yaml（默认位置）")
        return

    env = detect_environment()
    
    # 添加配置文件位置信息
    existing_config = find_config_file()
    env["config_file"] = {
        "found": existing_config is not None,
        "path": str(existing_config) if existing_config else None,
        "search_paths": [str(p) for p in get_config_paths()]
    }
    
    output = format_output(env, use_json=args.json)
    print(output)
    
    # 首次使用提示
    if not env["config_status"].get("config_file_exists"):
        print()
        print("⚠️  检测到配置文件不存在")
        print("   请运行以下命令初始化配置：")
        print("   python scripts/detect-environment.py --init")
        print()
        print("   或指定配置文件位置：")
        print("   python scripts/detect-environment.py --init --path /path/to/config.yaml")


if __name__ == "__main__":
    main()
