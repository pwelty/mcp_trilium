#!/usr/bin/env python3
"""
Test MCP server protocol
"""

import asyncio
import json
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_mcp_protocol():
    """Test MCP protocol communication"""
    print("Testing MCP protocol...")
    
    # Start the MCP server
    process = await asyncio.create_subprocess_exec(
        sys.executable, "main.py",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Initialize connection
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send initialization
        init_json = json.dumps(init_request) + "\n"
        process.stdin.write(init_json.encode())
        await process.stdin.drain()
        
        # Read response
        response_line = await process.stdout.readline()
        if response_line:
            response = json.loads(response_line.decode())
            print(f"Initialize response: {response}")
            
            # Send initialized notification
            initialized_request = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {}
            }
            
            init_notif_json = json.dumps(initialized_request) + "\n"
            process.stdin.write(init_notif_json.encode())
            await process.stdin.drain()
            
            # List tools
            tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
            
            tools_json = json.dumps(tools_request) + "\n"
            process.stdin.write(tools_json.encode())
            await process.stdin.drain()
            
            # Read tools response
            tools_response_line = await process.stdout.readline()
            if tools_response_line:
                tools_response = json.loads(tools_response_line.decode())
                print(f"Tools response: {tools_response}")
                
                if "result" in tools_response:
                    tools = tools_response["result"]["tools"]
                    print(f"✅ Found {len(tools)} tools:")
                    for tool in tools:
                        print(f"  - {tool['name']}: {tool['description']}")
                else:
                    print("❌ No tools found in response")
            else:
                print("❌ No tools response received")
        else:
            print("❌ No initialization response received")
            
    except Exception as e:
        print(f"❌ Error during MCP test: {e}")
        # Read stderr for more details
        stderr_output = await process.stderr.read()
        if stderr_output:
            print(f"Server stderr: {stderr_output.decode()}")
        
    finally:
        # Clean up
        try:
            process.terminate()
            await process.wait()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_mcp_protocol())