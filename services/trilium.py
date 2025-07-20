import httpx
import json
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class TriliumService:
    """Service for interacting with TriliumNext via ETAPI (External API)"""
    
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.headers = {
            "Authorization": api_token,
            "Content-Type": "application/json"
        }
        
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to TriliumNext API"""
        url = f"{self.base_url}/etapi/{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
                response = await client.request(method, url, headers=self.headers, **kwargs)
                response.raise_for_status()
                
                # Handle different response types
                if response.headers.get("content-type", "").startswith("application/json"):
                    return response.json()
                else:
                    return {"content": response.text}
                    
        except httpx.HTTPError as e:
            logger.error(f"HTTP error in {method} {endpoint}: {e}")
            return {"error": f"HTTP error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error in {method} {endpoint}: {e}")
            return {"error": f"Unexpected error: {str(e)}"}
    
    async def search_notes(self, query: str, fast_search: bool = False, include_archived: bool = False) -> List[Dict[str, Any]]:
        """Search for notes containing the query string"""
        # Use the notes API with a search query parameter
        params = {
            "search": query
        }
        
        result = await self._make_request("GET", "notes", params=params)
        
        if "error" in result:
            return [result]
        
        return result.get("results", result if isinstance(result, list) else [])
    
    async def get_note(self, note_id: str) -> Dict[str, Any]:
        """Get a note by its ID"""
        result = await self._make_request("GET", f"notes/{note_id}")
        
        if "error" not in result:
            # Also get the note content
            content_result = await self._make_request("GET", f"notes/{note_id}/content")
            if "error" not in content_result:
                result["content"] = content_result.get("content", "")
        
        return result
    
    async def create_note(self, parent_id: str, title: str, content: str = "", note_type: str = "text") -> Dict[str, Any]:
        """Create a new note"""
        data = {
            "parentNoteId": parent_id,
            "title": title,
            "type": note_type,
            "content": content
        }
        
        result = await self._make_request("POST", "create-note", json=data)
        
        if "error" not in result:
            return {
                "success": True,
                "message": f"Note '{title}' created successfully",
                "note_id": result.get("note", {}).get("noteId"),
                "data": result
            }
        else:
            return {
                "success": False,
                "error": result["error"]
            }
    
    async def update_note(self, note_id: str, title: Optional[str] = None, content: Optional[str] = None) -> Dict[str, Any]:
        """Update an existing note"""
        # Update note metadata if title provided
        if title:
            title_result = await self._make_request("PATCH", f"notes/{note_id}", json={"title": title})
            if "error" in title_result:
                return {"success": False, "error": title_result["error"]}
        
        # Update note content if provided
        if content is not None:
            content_result = await self._make_request("PUT", f"notes/{note_id}/content", json={"content": content})
            if "error" in content_result:
                return {"success": False, "error": content_result["error"]}
        
        return {
            "success": True,
            "message": f"Note {note_id} updated successfully",
            "note_id": note_id
        }
    
    async def delete_note(self, note_id: str) -> Dict[str, Any]:
        """Delete a note"""
        result = await self._make_request("DELETE", f"notes/{note_id}")
        
        if "error" not in result:
            return {
                "success": True,
                "message": f"Note {note_id} deleted successfully"
            }
        else:
            return {
                "success": False,
                "error": result["error"]
            }
    
    async def get_note_tree(self, note_id: str = "root") -> Dict[str, Any]:
        """Get the note tree structure"""
        # Get the note and its children
        result = await self._make_request("GET", f"notes/{note_id}")
        
        # If successful, try to get children
        if "error" not in result:
            # Try to get children - this might be available as a separate endpoint
            children_result = await self._make_request("GET", f"notes/{note_id}/children")
            if "error" not in children_result:
                result["children"] = children_result
        
        return result
    
    async def get_note_attributes(self, note_id: str) -> Dict[str, Any]:
        """Get note attributes (labels, relations)"""
        # Get the note data which includes attributes
        note_data = await self._make_request("GET", f"notes/{note_id}")
        
        if "error" in note_data:
            return note_data
            
        # Extract attributes from the note data
        attributes = note_data.get("attributes", [])
        return {"attributes": attributes}
    
    async def add_note_attribute(self, note_id: str, attribute_type: str, name: str, value: str = "") -> Dict[str, Any]:
        """Add an attribute to a note"""
        # Try different endpoints for adding attributes
        endpoints_to_try = [
            f"notes/{note_id}/attributes",
            f"notes/{note_id}/attribute",
            f"attributes",
            f"attribute"
        ]
        
        data = {
            "type": attribute_type,  # "label" or "relation"
            "name": name,
            "value": value,
            "noteId": note_id
        }
        
        for endpoint in endpoints_to_try:
            result = await self._make_request("POST", endpoint, json=data)
            
            if "error" not in result:
                return {
                    "success": True,
                    "message": f"Attribute '{name}' added to note {note_id}",
                    "data": result
                }
            
            # If we get a 404, try the next endpoint
            if "404" in str(result.get("error", "")):
                continue
            else:
                # If it's not a 404, return the error
                return {
                    "success": False,
                    "error": result["error"]
                }
        
        # If all endpoints failed
        return {
            "success": False,
            "error": "No working endpoint found for adding attributes. Your Trilium version might not support ETAPI attribute operations."
        }
    
    async def get_app_info(self) -> Dict[str, Any]:
        """Get application info and statistics"""
        result = await self._make_request("GET", "app-info")
        return result
    
    async def export_note(self, note_id: str, format_type: str = "html") -> Dict[str, Any]:
        """Export a note in specified format"""
        params = {"format": format_type}
        result = await self._make_request("GET", f"notes/{note_id}/export", params=params)
        return result
    
    async def get_recent_notes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recently modified notes"""
        # Since we don't have a search endpoint, let's try to get notes from root
        # and traverse to find recent ones
        
        try:
            # Get root note and its children
            root_result = await self._make_request("GET", "notes/root")
            if "error" in root_result:
                return [root_result]
            
            # This is a simplified version - in a real implementation,
            # we would need to traverse the tree to find all notes
            recent_notes = []
            
            # Add the root note if it has useful info
            if root_result.get("title") and root_result.get("noteId"):
                recent_notes.append(root_result)
            
            return recent_notes[:limit]
            
        except Exception as e:
            return [{"error": f"Failed to get recent notes: {str(e)}"}]
    
    async def backup_note(self, note_id: str) -> Dict[str, Any]:
        """Create a backup of a note"""
        result = await self._make_request("POST", f"notes/{note_id}/backup")
        
        if "error" not in result:
            return {
                "success": True,
                "message": f"Backup created for note {note_id}",
                "data": result
            }
        else:
            return {
                "success": False,
                "error": result["error"]
            }
    
    async def debug_endpoints(self) -> Dict[str, Any]:
        """Debug function to test different API endpoints"""
        endpoints_to_test = [
            "notes",
            "notes/root",
            "notes/root/children",
            "search", 
            "search-notes",
            "note-search",
            "calendar/notes",
            "tree"
        ]
        
        results = {}
        for endpoint in endpoints_to_test:
            try:
                result = await self._make_request("GET", endpoint)
                results[endpoint] = {
                    "success": "error" not in result,
                    "error": result.get("error", "None"),
                    "has_data": bool(result and result != {"error": result.get("error", "")})
                }
            except Exception as e:
                results[endpoint] = {
                    "success": False,
                    "error": str(e),
                    "has_data": False
                }
        
        return results