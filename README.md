# Trilium MCP Server

A Model Context Protocol (MCP) server for interacting with TriliumNext/Trilium Notes via the ETAPI (External API).

## Features

- **Search Notes**: Full-text search across all notes with fast search and archived notes options
- **Note Management**: Create, read, update, and delete notes
- **Tree Navigation**: Browse note hierarchies and tree structures
- **Attributes**: Manage note attributes (labels and relations)
- **Recent Notes**: Get recently modified notes
- **Export**: Export notes in various formats
- **Backup**: Create backups of specific notes
- **App Info**: Get application statistics and information

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd mcp_trillium
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

Add this to your Claude Desktop configuration file:

### macOS
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "trilium": {
      "command": "python",
      "args": ["/path/to/mcp_trillium/main.py"],
      "env": {
        "PYTHONPATH": "/path/to/mcp_trillium"
      }
    }
  }
}
```

### Windows
Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "trilium": {
      "command": "python",
      "args": ["C:\\path\\to\\mcp_trillium\\main.py"],
      "env": {
        "PYTHONPATH": "C:\\path\\to\\mcp_trillium"
      }
    }
  }
}
```

## Available Tools

### Search and Navigation
- `search_trilium_notes` - Search for notes using full-text search
- `get_trilium_note` - Get a specific note by ID
- `get_trilium_note_tree` - Get the tree structure from a note
- `get_recent_trilium_notes` - Get recently modified notes

### Note Management
- `create_trilium_note` - Create a new note
- `update_trilium_note` - Update an existing note
- `delete_trilium_note` - Delete a note

### Attributes and Metadata
- `get_trilium_note_attributes` - Get note attributes (labels/relations)
- `add_trilium_note_attribute` - Add an attribute to a note

### Utilities
- `get_trilium_app_info` - Get application info and statistics
- `export_trilium_note` - Export a note in specified format
- `backup_trilium_note` - Create a backup of a note

## Example Usage

Once configured, you can use these tools in Claude Desktop:

- "Search for notes about 'machine learning'"
- "Show me the tree structure starting from the root"
- "Create a new note called 'Meeting Notes' under the 'Work' folder"
- "Get the recent notes I've been working on"
- "Add a label 'important' to note ID abc123"

## Development

### Running Tests
```bash
# Activate virtual environment
source venv/bin/activate

# Run the server directly for testing
python main.py
```

### Adding New Features

1. Add new methods to `TriliumService` class in `services/trilium.py`
2. Add corresponding tools in `main.py`
3. Update this README with new tool documentation

## Troubleshooting

### Common Issues

1. **Connection refused**: Check that your Trilium server is running and accessible
2. **Authentication failed**: Verify your API token is correct and has proper permissions
3. **Note not found**: Ensure the note ID exists and is accessible

### Debug Mode

Set environment variable for debug logging:
```bash
export PYTHONPATH=/path/to/mcp_trillium
python main.py
```

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## API Reference

This server uses the TriliumNext ETAPI. For more information about the underlying API, see the [TriliumNext documentation](https://github.com/TriliumNext/Notes/wiki/ETAPI).