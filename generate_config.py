#!/usr/bin/env python3

import json
import os
import sys
from pathlib import Path
import platform

def get_claude_config_path():
    """Get the Claude Desktop config file path for the current OS"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    elif system == "Windows":
        appdata = os.getenv("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA environment variable not found")
        return Path(appdata) / "Claude/claude_desktop_config.json"
    elif system == "Linux":
        # Common Linux path (may vary by distribution)
        return Path.home() / ".config/claude/claude_desktop_config.json"
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")

def generate_config(project_path=None, server_name="trilium"):
    """Generate Claude Desktop MCP server configuration"""
    
    if project_path is None:
        project_path = Path(__file__).parent.absolute()
    else:
        project_path = Path(project_path).absolute()
    
    # Check if we're in a virtual environment
    venv_python = project_path / "venv" / "bin" / "python"
    if platform.system() == "Windows":
        venv_python = project_path / "venv" / "Scripts" / "python.exe"
    
    # Use venv python if available, otherwise system python
    if venv_python.exists():
        python_cmd = str(venv_python)
    else:
        python_cmd = "python3" if platform.system() != "Windows" else "python"
    
    main_py = project_path / "main.py"
    
    if not main_py.exists():
        raise FileNotFoundError(f"main.py not found at {main_py}")
    
    config = {
        "mcpServers": {
            server_name: {
                "command": python_cmd,
                "args": [str(main_py)],
                "env": {
                    "PYTHONPATH": str(project_path)
                }
            }
        }
    }
    
    return config

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Claude Desktop MCP configuration for Trilium")
    parser.add_argument("--project-path", help="Path to the mcp-trilium project (default: current directory)")
    parser.add_argument("--server-name", default="trilium", help="Name for the MCP server (default: trilium)")
    parser.add_argument("--output", help="Output file path (default: claude_desktop_config.json in project dir)")
    parser.add_argument("--merge", action="store_true", help="Merge with existing Claude config (EXPERIMENTAL - backup first!)")
    parser.add_argument("--install", action="store_true", help="Install directly to Claude config location (DANGEROUS - backup first!)")
    
    args = parser.parse_args()
    
    try:
        # Generate the config
        config = generate_config(args.project_path, args.server_name)
        
        # Determine output path
        if args.output:
            output_path = Path(args.output)
        elif args.install:
            output_path = get_claude_config_path()
        else:
            project_path = Path(args.project_path) if args.project_path else Path(__file__).parent
            output_path = project_path / "claude_desktop_config.json"
        
        # Handle merging with existing config
        if args.merge and output_path.exists():
            print(f"Merging with existing config at {output_path}")
            with open(output_path) as f:
                existing_config = json.load(f)
            
            # Merge mcpServers sections
            if "mcpServers" not in existing_config:
                existing_config["mcpServers"] = {}
            
            existing_config["mcpServers"].update(config["mcpServers"])
            config = existing_config
        
        # Create parent directory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the config
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Configuration generated: {output_path}")
        
        if args.install:
            print("⚠️  Configuration installed directly to Claude Desktop!")
            print("   Restart Claude Desktop to use the new configuration.")
        else:
            print("\nNext steps:")
            print(f"1. Review the generated config: {output_path}")
            print("2. Copy the contents to your Claude Desktop config file:")
            
            claude_path = get_claude_config_path()
            print(f"   {claude_path}")
            print("3. Restart Claude Desktop")
            print("\nOr run with --install to install directly (backup first!)")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()