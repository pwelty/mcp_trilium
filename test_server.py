#!/usr/bin/env python3
"""
Simple test script to verify the MCP server is working
"""

import asyncio
import json
import os
from dotenv import load_dotenv
from services.trilium import TriliumService

# Load environment variables
load_dotenv()

async def test_connection():
    """Test connection to Trilium server"""
    try:
        # Load config from environment variables first
        base_url = os.getenv("TRILIUM_BASE_URL")
        api_token = os.getenv("TRILIUM_API_TOKEN")
        
        if not base_url or not api_token:
            # Fall back to config.json
            with open('config.json', 'r') as f:
                config = json.load(f)
            base_url = config["trilium"]["base_url"]
            api_token = config["trilium"]["api_token"]
        
        # Create service
        trilium = TriliumService(
            base_url=base_url,
            api_token=api_token
        )
        
        # Test app info
        print("Testing connection to Trilium...")
        print(f"URL: {trilium.base_url}")
        print(f"Token: {trilium.api_token[:20]}...")
        result = await trilium.get_app_info()
        
        if "error" in result:
            print(f"❌ Connection failed: {result['error']}")
            return False
        else:
            print("✅ Connection successful!")
            print(f"App version: {result.get('appVersion', 'Unknown')}")
            print(f"DB version: {result.get('dbVersion', 'Unknown')}")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_search():
    """Test search functionality"""
    try:
        # Load config from environment variables first
        base_url = os.getenv("TRILIUM_BASE_URL")
        api_token = os.getenv("TRILIUM_API_TOKEN")
        
        if not base_url or not api_token:
            # Fall back to config.json
            with open('config.json', 'r') as f:
                config = json.load(f)
            base_url = config["trilium"]["base_url"]
            api_token = config["trilium"]["api_token"]
        
        # Create service
        trilium = TriliumService(
            base_url=base_url,
            api_token=api_token
        )
        
        # Test search
        print("\nTesting search functionality...")
        results = await trilium.search_notes("*", fast_search=True)
        
        if results and "error" in results[0]:
            print(f"❌ Search failed: {results[0]['error']}")
            return False
        else:
            print(f"✅ Search successful! Found {len(results)} notes")
            if results:
                print(f"First note: {results[0].get('title', 'Untitled')}")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_debug_endpoints():
    """Debug test to find working endpoints"""
    try:
        # Load config from environment variables first
        base_url = os.getenv("TRILIUM_BASE_URL")
        api_token = os.getenv("TRILIUM_API_TOKEN")
        
        if not base_url or not api_token:
            # Fall back to config.json
            with open('config.json', 'r') as f:
                config = json.load(f)
            base_url = config["trilium"]["base_url"]
            api_token = config["trilium"]["api_token"]
        
        # Create service
        trilium = TriliumService(
            base_url=base_url,
            api_token=api_token
        )
        
        # Test endpoints
        print("\nTesting various API endpoints...")
        results = await trilium.debug_endpoints()
        
        for endpoint, result in results.items():
            status = "✅" if result["success"] else "❌"
            print(f"{status} {endpoint}: {result['error'] if not result['success'] else 'Success'}")
        
        return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    """Run tests"""
    print("=" * 50)
    print("Trilium MCP Server Test")
    print("=" * 50)
    
    # Test connection
    connection_ok = await test_connection()
    
    if connection_ok:
        # Test endpoints
        await test_debug_endpoints()
        
        # Test search
        await test_search()
    
    print("\nTest complete!")

if __name__ == "__main__":
    asyncio.run(main())