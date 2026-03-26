# Trilium MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10--3.13-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/pwelty/mcp_trilium/workflows/CI/badge.svg)](https://github.com/pwelty/mcp_trilium/actions)

🌳 **A powerful Model Context Protocol (MCP) server that brings your Trilium Notes knowledge base directly into Claude Desktop.**

Connect your personal knowledge management system to AI conversations with full-text search, note management, and intelligent content interaction.

*This is a Python implementation. If you prefer JavaScript/TypeScript, check out [triliumnext-mcp](https://github.com/tan-yong-sheng/triliumnext-mcp).*

## ✨ What's new in v0.2.0

- 🚀 **MCP SDK 1.26.0** - Upgraded to the latest stable MCP SDK with improved performance and compatibility
- 🐍 **Python 3.13 support** - Now tested and compatible with Python 3.10 through 3.13
- 📦 **Modern dependencies** - All packages updated to latest stable versions (httpx 0.28.1, aiohttp 3.13.3)
- ✅ **Enhanced CI/CD** - Automated testing across all supported Python versions, automated releases

See the full [changelog](CHANGELOG.md) for details.

## ⚠️ Important: Claude Desktop vs Claude Web

**This MCP server is designed for Claude Desktop and runs locally on your machine.**

| Claude Desktop | Claude Web (claude.ai) |
|----------------|-------------------------|
| ✅ Desktop app you download | ✅ Web browser version |
| ✅ Supports local MCP servers | ✅ Supports remote MCP servers (BETA) |
| ✅ Runs tools locally | ✅ Connects to hosted MCP servers |
| ✅ Can access your local Trilium | ⚠️ Requires publicly accessible Trilium |

**Current Project Scope:**
- This MCP server runs **locally on your machine** via stdio
- Designed for **Claude Desktop** with local Trilium instances
- You **must** download and use [Claude Desktop](https://claude.ai/download) for this implementation

**Network Requirements:**
- Claude Desktop and your Trilium instance must be on the **same network** or **mutually accessible**
- If Trilium is behind Docker/VPN/Tailscale, ensure Claude Desktop can reach it

**🚀 Future Possibilities:**
Both Claude Web and ChatGPT now offer "Custom Connectors" (BETA) that can connect to remote MCP servers via HTTPS. We're exploring creating a hosted version of this MCP server for web-based AI assistants. [Follow development updates →](https://github.com/pwelty/mcp_trilium/discussions)

## Project Goals

This project aims to:

🐍 **Bring MCP to Python developers** - Provide a robust, Pythonic implementation for the growing MCP ecosystem

🌍 **Bring MCP to FOSS tools** - Connect open source applications to AI workflows through Model Context Protocol  

🔗 **Bridge knowledge systems** - Connect personal knowledge bases like Trilium to AI workflows seamlessly

📦 **Production-ready tools** - Deliver polished, well-documented software that works out of the box

*Part of a broader effort to create FOSS MCP servers for popular tools (NocoDB, and more coming soon!)*

## About Trilium Notes

Trilium Notes is an exceptional free and open-source personal knowledge management application for building large personal knowledge bases with hierarchical notes. Originally created by zadam, the project is now actively developed by the community as [TriliumNext](https://github.com/TriliumNext/Trilium).

**Why Trilium?**
- 🏗️ **Hierarchical structure** - Build complex knowledge trees with linking and tagging
- 🔍 **Full-text search** - Find anything in your knowledge base instantly  
- 🎨 **Rich content** - Support for text, code, images, files, diagrams, and more
- 🔌 **Extensible** - Custom scripts, themes, and powerful API access
- 🌐 **Self-hosted & free** - Your data stays under your control, completely open source
- 🔄 **Active development** - Continuously improved by the TriliumNext community

This MCP server works with **both** the original Trilium (maintenance mode) and TriliumNext installations. Thanks to zadam for creating this incredible foundation and to the TriliumNext community for continuing its development - and for providing the ETAPI that makes this integration possible!

➡️ **Get Trilium:** [TriliumNext](https://github.com/TriliumNext/Trilium) | [Original Trilium](https://github.com/zadam/trilium)

### What You Can Do

Talk to Claude naturally about your notes:
- *"Search for my notes about Python programming"*
- *"Create a new meeting note under my Work folder"* 
- *"Show me what I've been working on recently"*
- *"Add a 'priority' label to note abc123"*
- *"Export my research note as HTML"*
- *"What's the structure under my Projects folder?"*

> 💡 **New to MCP Trilium?** Star ⭐ the repo and [try it out](#installation)! Found it useful? We'd love to hear about your use case in the [discussions](https://github.com/pwelty/mcp_trilium/discussions).

## Features

### 🔍 **Search & Discovery**
- `search_trilium_notes` - Full-text search across all notes with fast search and archived notes options
- `get_recent_trilium_notes` - Get recently modified notes with timestamps

### 📝 **Note Management** 
- `get_trilium_note` - Read any note by ID with full content
- `create_trilium_note` - Create new notes with custom titles, content, and parent placement
- `update_trilium_note` - Edit existing note content and metadata  
- `delete_trilium_note` - Remove notes from your knowledge base

### 🌳 **Navigation & Structure**
- `get_trilium_note_tree` - Browse hierarchical note structures and relationships
- Navigate parent-child relationships and folder organization

### 🏷️ **Attributes & Metadata**
- `get_trilium_note_attributes` - View all labels and relations on notes
- `add_trilium_note_attribute` - Add custom labels and relations for organization

### 📤 **Export & Backup**
- `export_trilium_note` - Export notes in various formats (HTML, Markdown, etc.)
- `backup_trilium_note` - Create backups of specific notes

### 📊 **System Information**
- `get_trilium_app_info` - Get application statistics, version info, and system status

## Quick Demo

Once configured, you can interact with your Trilium notes naturally in Claude Desktop:

```
💬 "Search for notes about machine learning"
🔍 Returns relevant notes with content snippets and note IDs

💬 "Show me the tree structure starting from my 'Projects' folder"  
🌳 Displays hierarchical note organization

💬 "Create a new note called 'Meeting Notes' under my Work folder"
✏️ Creates and links the note in the specified location

💬 "What are my most recently modified notes?"
📝 Shows your latest activity with timestamps

💬 "Add a label 'important' to note abc123"
🏷️ Applies the label to organize your content
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/pwelty/mcp_trilium.git
cd mcp_trilium
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the server:
```bash
cp config.json.template config.json
# Edit config.json with your Trilium details
```

## Configuration

You can configure the server using either environment variables or a config file.

### Method 1: Environment Variables (Recommended)

Create a `.env` file in the project root:

```env
TRILIUM_BASE_URL=https://your-trilium-instance.com
TRILIUM_API_TOKEN=your-trilium-api-token-here
```

### Method 2: Config File

Edit `config.json` with your Trilium instance details:

```json
{
  "trilium": {
    "base_url": "https://your-trilium-instance.com",
    "api_token": "your-trilium-api-token-here"
  }
}
```

### Getting Your API Token

1. Open Trilium in your browser
2. Go to Options → ETAPI
3. Create a new API token
4. Copy the token to your `.env` file or config.json

**Note**: The API token should be used directly without "Bearer " prefix.

## Usage with Claude Desktop

### Option 1: Automatic Configuration (Recommended)

1. Generate the Claude Desktop configuration:
   ```bash
   python generate_config.py
   ```

2. Open Claude Desktop and access the configuration:
   - Open Claude Desktop
   - Go to **Settings/Preferences** 
   - Click **Developer** tab
   - Click **Edit Config** (or similar button to open config file)
   - This opens your `claude_desktop_config.json` file in a text editor

3. Add the configuration to your Claude Desktop config file:

   **If the file is empty or only has `{}`:**
   - Copy the entire contents from the generated `claude_desktop_config.json` file

   **If you already have MCP servers configured:**
   - Find the `"mcpServers"` section in your existing config
   - Add the trilium server inside it with a comma:
   ```json
   {
     "mcpServers": {
       "existing-server": { ... },
       "trilium": {
         "command": "...",
         "args": ["..."],
         "env": { ... }
       }
     }
   }
   ```

   **If you have other config but no `mcpServers` section:**
   - Add the entire `"mcpServers"` section from the generated file

4. Save the file and restart Claude Desktop

**Advanced users only:**
```bash
# Automatically merge and install (backup your Claude config first!)
python generate_config.py --merge --install
```

### Option 2: Manual Configuration  

Add this to your Claude Desktop configuration file:

#### macOS
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "trilium": {
      "command": "python",
      "args": ["/path/to/mcp_trilium/main.py"],
      "env": {
        "PYTHONPATH": "/path/to/mcp_trilium"
      }
    }
  }
}
```

#### Windows
Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "trilium": {
      "command": "python",
      "args": ["C:\\path\\to\\mcp_trilium\\main.py"],
      "env": {
        "PYTHONPATH": "C:\\path\\to\\mcp_trilium"
      }
    }
  }
}
```

## Development

### Running tests
```bash
source venv/bin/activate
python test_server.py    # Integration tests (requires running Trilium instance)
python test_mcp.py       # MCP protocol tests
```

### Adding new features

1. Add new methods to `TriliumService` class in `services/trilium.py`
2. Add corresponding tools in `main.py`
3. Update this README with new tool documentation
4. Add entry under `[Unreleased]` in `CHANGELOG.md`

## Troubleshooting

### Common Issues

1. **Connection refused**: Check that your Trilium server is running and accessible
2. **Authentication failed**: Verify your API token is correct and has proper permissions
3. **Note not found**: Ensure the note ID exists and is accessible

### Debug Mode

Set environment variable for debug logging:
```bash
export PYTHONPATH=/path/to/mcp_trilium
python main.py
```

## FAQ

### General Questions

**Q: Can I use this with Claude Web (claude.ai in my browser)?**  
A: **Currently, this version only works with Claude Desktop.** However, both Claude Web and ChatGPT now support "Custom Connectors" (BETA) that can connect to remote MCP servers. This would require hosting the MCP server publicly and ensuring your Trilium instance is accessible via HTTPS. We're exploring this possibility for future versions.

**Q: What is MCP and why should I use this?**  
A: Model Context Protocol (MCP) allows Claude Desktop to directly interact with external tools and data sources. This server lets you search, read, and manage your Trilium notes directly from Claude conversations, making your knowledge base an active part of your AI workflows.

**Q: Do I need TriliumNext or will regular Trilium work?**  
A: Both work! This server uses the ETAPI (External API) which is available in both Trilium and TriliumNext. Just make sure ETAPI is enabled in your instance.

**Q: Is my data sent to Anthropic?**  
A: No. The MCP server runs locally on your machine and connects directly to your Trilium instance. Your notes stay private and are only accessed when you explicitly interact with them in Claude Desktop.

### Setup Issues

**Q: Claude Desktop doesn't show my Trilium tools**  
A: Common fixes:
- Ensure you restarted Claude Desktop after adding the config
- Check that the paths in your config file are correct (use absolute paths)
- Verify your virtual environment is activated if using one
- Run `python generate_config.py` to regenerate a clean config

**Q: I get "Connection refused" errors**  
A: Check:
- Your Trilium server is running and accessible at the configured URL
- ETAPI is enabled in Trilium (Options → ETAPI)
- Your API token is valid and hasn't expired
- No firewall blocking the connection

**Q: Authentication keeps failing**  
A: Verify:
- Your API token is correctly copied (no extra spaces)
- Don't include "Bearer " prefix in the token
- The token has sufficient permissions in Trilium
- Try creating a new API token

### Usage Questions  

**Q: Can I use this with a remote Trilium server?**  
A: Yes! Just set your `TRILIUM_BASE_URL` to your remote server's URL. Make sure the server is accessible from your machine and ETAPI is enabled.

**Q: How do I search for notes with special characters?**  
A: The search uses Trilium's built-in full-text search, so you can use the same syntax you'd use in Trilium itself.

**Q: Can I create nested notes or just top-level ones?**  
A: You can create notes anywhere in your tree structure. Just specify the parent note ID when creating new notes.

## License

This project is licensed under the MIT License.

## Contributing

We'd love your help making MCP Trilium even better! Here are ways you can contribute:

### 🐛 **Report Bugs**
Found an issue? [Create a bug report](https://github.com/pwelty/mcp_trilium/issues/new) with:
- Steps to reproduce the problem
- Expected vs actual behavior  
- Your system info (OS, Python version, Trilium version)

### 💡 **Request Features**
Have an idea? [Open a feature request](https://github.com/pwelty/mcp_trilium/issues/new) and tell us:
- What you'd like to see added
- How it would help your workflow
- Any implementation ideas

### 🔧 **Code Contributions**
Ready to dive in? Check out our [Contributing Guide](./CONTRIBUTING.md) for:
- Development setup instructions
- Code style guidelines
- How to submit pull requests

### 📖 **Improve Documentation**
Help others by:
- Fixing typos or unclear instructions
- Adding examples and use cases
- Translating documentation
- Writing tutorials

### ⭐ **Show Support**
- Star the repository if you find it useful
- Share it with others who use Trilium
- Join discussions in issues and PRs

### 🗣️ **Community**
- Share your use cases and workflows
- Help answer questions from other users
- Suggest improvements based on your experience

## About the Author

This project is developed by **Dr. Paul Welty**, Vice Provost for Academic Innovation at Emory University and founder of [Synaxis, LLC](https://www.synaxis.ai). With a Ph.D. in Philosophy and 25+ years of technology solution experience, Paul specializes in strategic AI implementation and team capability transformation.

At Emory, Paul's major achievements include launching three transformative initiatives: the Center for AI Learning (CAIL), The Hatchery (Emory's Center for Student Innovation and Entrepreneurship), and Facet (Emory's Faculty Information and Action System). Through Synaxis, he helps teams dramatically increase their capacity through practical AI integration - from customer support to market research.

This MCP server reflects Paul's commitment to making AI tools accessible and practical for real-world workflows, bridging the gap between cutting-edge technology and everyday productivity.

🌐 **Learn more:** [paulwelty.com](https://www.paulwelty.com) | [synaxis.ai](https://www.synaxis.ai)

*Interested in team AI implementation or custom MCP server development? Let's talk about transforming your workflow.*

## API Reference

This server uses the TriliumNext ETAPI. For more information about the underlying API, see the [TriliumNext documentation](https://github.com/TriliumNext/Notes/wiki/ETAPI).