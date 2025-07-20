#!/usr/bin/env python3
"""Debug script to test Trilium ETAPI endpoints"""

import asyncio
import json
import httpx
from pathlib import Path

async def test_etapi_endpoints():
    """Test various ETAPI endpoints to debug the 404 issue"""
    
    # Load config
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)
    
    base_url = config["trilium"]["base_url"]
    api_token = config["trilium"]["api_token"]
    
    if api_token == "your-trilium-api-token-here":
        print("❌ Please update your API token in config.json")
        return
    
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }
    
    # Test endpoints
    test_cases = [
        # Basic connectivity
        ("GET", "app-info", None, "App info (basic connectivity test)"),
        ("GET", "notes/root", None, "Root note"),
        
        # Note existence tests
        ("GET", "notes/GqGt4xhGpbi8", None, "Note GqGt4xhGpbi8"),
        ("GET", "notes/TLGXBkVmhR2t", None, "Note TLGXBkVmhR2t"),
        
        # Attribute endpoint tests
        ("GET", "notes/GqGt4xhGpbi8/attributes", None, "Attributes for GqGt4xhGpbi8"),
        ("GET", "notes/TLGXBkVmhR2t/attributes", None, "Attributes for TLGXBkVmhR2t"),
        ("GET", "notes/root/attributes", None, "Attributes for root note"),
        
        # Alternative attribute endpoints
        ("GET", "attributes", None, "All attributes endpoint"),
        ("GET", "notes/GqGt4xhGpbi8/attribute", None, "Attribute (singular) endpoint"),
        
        # Search for notes
        ("GET", "notes", {"search": "test"}, "Search notes"),
        ("GET", "search", {"query": "test"}, "Search endpoint"),
    ]
    
    print(f"Testing ETAPI endpoints for: {base_url}")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
        for method, endpoint, params, description in test_cases:
            url = f"{base_url}/etapi/{endpoint}"
            
            try:
                response = await client.request(
                    method, url, 
                    headers=headers, 
                    params=params
                )
                
                status_color = "✅" if response.status_code < 400 else "❌"
                print(f"{status_color} {method} {endpoint} - {response.status_code} - {description}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, dict):
                            print(f"   Keys: {list(data.keys())}")
                        elif isinstance(data, list):
                            print(f"   Items: {len(data)}")
                    except:
                        print(f"   Response: {response.text[:100]}...")
                        
            except Exception as e:
                print(f"❌ {method} {endpoint} - ERROR - {str(e)}")
            
            print()

if __name__ == "__main__":
    asyncio.run(test_etapi_endpoints())