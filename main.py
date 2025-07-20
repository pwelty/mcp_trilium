#!/usr/bin/env python3

import asyncio
import json
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp import stdio_server
import mcp.types as types

from services.trilium import TriliumService

# Load environment variables from .env file
load_dotenv()

# Load configuration from environment variables or config file
def load_config():
    """Load configuration from environment variables or config.json"""
    
    # Try environment variables first
    base_url = os.getenv("TRILIUM_BASE_URL")
    api_token = os.getenv("TRILIUM_API_TOKEN")
    
    if base_url and api_token:
        return {
            "trilium": {
                "base_url": base_url,
                "api_token": api_token
            }
        }
    
    # Fall back to config.json
    config_path = Path(__file__).parent / "config.json"
    if not config_path.exists():
        print(f"No config found. Please set TRILIUM_BASE_URL and TRILIUM_API_TOKEN environment variables")
        print(f"Or create a config.json file at {config_path}")
        sys.exit(1)
    
    with open(config_path) as f:
        return json.load(f)

config = load_config()

# Initialize Trilium service
trilium = TriliumService(
    base_url=config["trilium"]["base_url"],
    api_token=config["trilium"]["api_token"]
)

# Create MCP server
server = Server("trilium-mcp")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="search_trilium_notes",
            description="Search for notes in Trilium using full-text search",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find in note titles and content"
                    },
                    "fast_search": {
                        "type": "boolean",
                        "description": "Use fast search (default: false)",
                        "default": False
                    },
                    "include_archived": {
                        "type": "boolean",
                        "description": "Include archived notes in search (default: false)",
                        "default": False
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="get_trilium_note",
            description="Get a specific Trilium note by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "The ID of the note to retrieve"
                    }
                },
                "required": ["note_id"]
            }
        ),
        types.Tool(
            name="create_trilium_note",
            description="Create a new note in Trilium",
            inputSchema={
                "type": "object",
                "properties": {
                    "parent_id": {
                        "type": "string",
                        "description": "ID of the parent note (use 'root' for root level)"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title of the new note"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content of the note",
                        "default": ""
                    },
                    "note_type": {
                        "type": "string",
                        "description": "Type of note (text, code, file, image, search, book, relationMap, render)",
                        "default": "text"
                    }
                },
                "required": ["parent_id", "title"]
            }
        ),
        types.Tool(
            name="update_trilium_note",
            description="Update an existing Trilium note",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "ID of the note to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the note (optional)"
                    },
                    "content": {
                        "type": "string",
                        "description": "New content for the note (optional)"
                    }
                },
                "required": ["note_id"]
            }
        ),
        types.Tool(
            name="delete_trilium_note",
            description="Delete a Trilium note",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "ID of the note to delete"
                    }
                },
                "required": ["note_id"]
            }
        ),
        types.Tool(
            name="get_trilium_note_tree",
            description="Get the tree structure of notes from a specific note",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "ID of the note to get tree from (default: 'root')",
                        "default": "root"
                    }
                }
            }
        ),
        types.Tool(
            name="get_recent_trilium_notes",
            description="Get recently modified notes",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of recent notes to return (default: 10)",
                        "default": 10
                    }
                }
            }
        ),
        types.Tool(
            name="get_trilium_note_attributes",
            description="Get attributes (labels and relations) of a note",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "ID of the note to get attributes for"
                    }
                },
                "required": ["note_id"]
            }
        ),
        types.Tool(
            name="add_trilium_note_attribute",
            description="Add an attribute (label or relation) to a note",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "ID of the note to add attribute to"
                    },
                    "attribute_type": {
                        "type": "string",
                        "description": "Type of attribute: 'label' or 'relation'"
                    },
                    "name": {
                        "type": "string",
                        "description": "Name of the attribute"
                    },
                    "value": {
                        "type": "string",
                        "description": "Value of the attribute (optional for relations)",
                        "default": ""
                    }
                },
                "required": ["note_id", "attribute_type", "name"]
            }
        ),
        types.Tool(
            name="get_trilium_app_info",
            description="Get Trilium application info and statistics",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="export_trilium_note",
            description="Export a note in specified format",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "ID of the note to export"
                    },
                    "format": {
                        "type": "string",
                        "description": "Export format (html, markdown, etc.)",
                        "default": "html"
                    }
                },
                "required": ["note_id"]
            }
        ),
        types.Tool(
            name="backup_trilium_note",
            description="Create a backup of a specific note",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "ID of the note to backup"
                    }
                },
                "required": ["note_id"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""
    
    if name == "search_trilium_notes":
        query = arguments.get("query", "")
        fast_search = arguments.get("fast_search", False)
        include_archived = arguments.get("include_archived", False)
        
        results = await trilium.search_notes(query, fast_search, include_archived)
        
        if results and "error" in results[0]:
            return [types.TextContent(type="text", text=f"Error: {results[0]['error']}")]
        
        if not results:
            return [types.TextContent(type="text", text=f"No notes found matching '{query}'")]
        
        response = f"Found {len(results)} notes matching '{query}':\n\n"
        for result in results:
            response += f"**{result.get('title', 'Untitled')}**\n"
            response += f"Note ID: {result.get('noteId', 'N/A')}\n"
            response += f"Type: {result.get('type', 'N/A')}\n"
            if result.get('dateCreated'):
                response += f"Created: {result['dateCreated']}\n"
            if result.get('dateModified'):
                response += f"Modified: {result['dateModified']}\n"
            response += "\n"
        
        return [types.TextContent(type="text", text=response)]
    
    elif name == "get_trilium_note":
        note_id = arguments.get("note_id", "")
        result = await trilium.get_note(note_id)
        
        if "error" in result:
            return [types.TextContent(type="text", text=f"Error: {result['error']}")]
        
        response = f"# {result.get('title', 'Untitled')}\n\n"
        response += f"**Note ID:** {result.get('noteId', 'N/A')}\n"
        response += f"**Type:** {result.get('type', 'N/A')}\n"
        response += f"**Created:** {result.get('dateCreated', 'N/A')}\n"
        response += f"**Modified:** {result.get('dateModified', 'N/A')}\n\n"
        
        if result.get('content'):
            response += "**Content:**\n"
            response += result['content']
        
        return [types.TextContent(type="text", text=response)]
    
    elif name == "create_trilium_note":
        parent_id = arguments.get("parent_id", "")
        title = arguments.get("title", "")
        content = arguments.get("content", "")
        note_type = arguments.get("note_type", "text")
        
        result = await trilium.create_note(parent_id, title, content, note_type)
        
        if result.get("success"):
            return [types.TextContent(type="text", text=f"✅ {result['message']}\nNote ID: {result['note_id']}")]
        else:
            return [types.TextContent(type="text", text=f"❌ {result.get('error', 'Unknown error')}")]
    
    elif name == "update_trilium_note":
        note_id = arguments.get("note_id", "")
        title = arguments.get("title")
        content = arguments.get("content")
        
        result = await trilium.update_note(note_id, title, content)
        
        if result.get("success"):
            return [types.TextContent(type="text", text=f"✅ {result['message']}")]
        else:
            return [types.TextContent(type="text", text=f"❌ {result.get('error', 'Unknown error')}")]
    
    elif name == "delete_trilium_note":
        note_id = arguments.get("note_id", "")
        result = await trilium.delete_note(note_id)
        
        if result.get("success"):
            return [types.TextContent(type="text", text=f"✅ {result['message']}")]
        else:
            return [types.TextContent(type="text", text=f"❌ {result.get('error', 'Unknown error')}")]
    
    elif name == "get_trilium_note_tree":
        note_id = arguments.get("note_id", "root")
        result = await trilium.get_note_tree(note_id)
        
        if "error" in result:
            return [types.TextContent(type="text", text=f"Error: {result['error']}")]
        
        response = f"**Note Tree from {note_id}:**\n\n"
        
        def format_tree(nodes, indent=0):
            tree_text = ""
            for node in nodes:
                prefix = "  " * indent + "- "
                tree_text += f"{prefix}**{node.get('title', 'Untitled')}** (ID: {node.get('noteId', 'N/A')})\n"
                if node.get('children'):
                    tree_text += format_tree(node['children'], indent + 1)
            return tree_text
        
        if isinstance(result, list):
            response += format_tree(result)
        else:
            response += str(result)
        
        return [types.TextContent(type="text", text=response)]
    
    elif name == "get_recent_trilium_notes":
        limit = arguments.get("limit", 10)
        results = await trilium.get_recent_notes(limit)
        
        if results and "error" in results[0]:
            return [types.TextContent(type="text", text=f"Error: {results[0]['error']}")]
        
        response = f"Recent {len(results)} notes:\n\n"
        for result in results:
            response += f"**{result.get('title', 'Untitled')}**\n"
            response += f"Note ID: {result.get('noteId', 'N/A')}\n"
            response += f"Type: {result.get('type', 'N/A')}\n"
            if result.get('dateModified'):
                response += f"Modified: {result['dateModified']}\n"
            response += "\n"
        
        return [types.TextContent(type="text", text=response)]
    
    elif name == "get_trilium_note_attributes":
        note_id = arguments.get("note_id", "")
        result = await trilium.get_note_attributes(note_id)
        
        if "error" in result:
            return [types.TextContent(type="text", text=f"Error: {result['error']}")]
        
        response = f"**Attributes for note {note_id}:**\n\n"
        
        if isinstance(result, list):
            for attr in result:
                response += f"- **{attr.get('name', 'N/A')}** ({attr.get('type', 'N/A')})"
                if attr.get('value'):
                    response += f": {attr['value']}"
                response += "\n"
        else:
            response += str(result)
        
        return [types.TextContent(type="text", text=response)]
    
    elif name == "add_trilium_note_attribute":
        note_id = arguments.get("note_id", "")
        attribute_type = arguments.get("attribute_type", "")
        name = arguments.get("name", "")
        value = arguments.get("value", "")
        
        result = await trilium.add_note_attribute(note_id, attribute_type, name, value)
        
        if result.get("success"):
            return [types.TextContent(type="text", text=f"✅ {result['message']}")]
        else:
            return [types.TextContent(type="text", text=f"❌ {result.get('error', 'Unknown error')}")]
    
    elif name == "get_trilium_app_info":
        result = await trilium.get_app_info()
        
        if "error" in result:
            return [types.TextContent(type="text", text=f"Error: {result['error']}")]
        
        response = "**Trilium Application Info:**\n\n"
        for key, value in result.items():
            response += f"{key.replace('_', ' ').title()}: {value}\n"
        
        return [types.TextContent(type="text", text=response)]
    
    elif name == "export_trilium_note":
        note_id = arguments.get("note_id", "")
        format_type = arguments.get("format", "html")
        
        result = await trilium.export_note(note_id, format_type)
        
        if "error" in result:
            return [types.TextContent(type="text", text=f"Error: {result['error']}")]
        
        response = f"**Exported note {note_id} in {format_type} format:**\n\n"
        if isinstance(result, str):
            response += result
        else:
            response += str(result)
        
        return [types.TextContent(type="text", text=response)]
    
    elif name == "backup_trilium_note":
        note_id = arguments.get("note_id", "")
        result = await trilium.backup_note(note_id)
        
        if result.get("success"):
            return [types.TextContent(type="text", text=f"✅ {result['message']}")]
        else:
            return [types.TextContent(type="text", text=f"❌ {result.get('error', 'Unknown error')}")]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdin/stdout streams
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, 
            write_stream, 
            InitializationOptions(
                server_name="trilium-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())