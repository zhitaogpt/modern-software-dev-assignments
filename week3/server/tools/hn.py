import httpx
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Algolia API Endpoints
HN_SEARCH_API = "https://hn.algolia.com/api/v1/search_by_date"
HN_ITEM_API = "https://hn.algolia.com/api/v1/items"

async def fetch_hot_stories(hours: int = 24, min_points: int = 50, limit: int = 20) -> str:
    """
    Fetch hot stories from Hacker News using Algolia API.
    Returns a JSON string containing the list of stories.
    """
    # Calculate cutoff timestamp
    threshold_time = int((datetime.now() - timedelta(hours=hours)).timestamp())
    
    # Construct query parameters
    # tags=story ensure we only get top-level posts, not comments
    params = {
        "tags": "story",
        "numericFilters": f"created_at_i>{threshold_time},points>={min_points}",
        "hitsPerPage": limit
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(HN_SEARCH_API, params=params, timeout=15.0)
            response.raise_for_status()
            data = response.json()
            
            stories = []
            for hit in data.get("hits", []):
                stories.append({
                    "id": hit.get("objectID"),
                    "title": hit.get("title"),
                    "url": hit.get("url"),
                    "points": hit.get("points"),
                    "num_comments": hit.get("num_comments"),
                    "author": hit.get("author"),
                    "created_at": hit.get("created_at")
                })
            
            return json.dumps(stories, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

async def fetch_story_details(story_id: str) -> str:
    """
    Fetch detailed context for a specific story, including top comments.
    Returns a JSON string.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{HN_ITEM_API}/{story_id}", timeout=15.0)
            response.raise_for_status()
            data = response.json()
            
            context = {
                "id": data.get("objectID"),
                "title": data.get("title"),
                "text": data.get("text"),  # Handles "Ask HN" or "Show HN" text content
                "url": data.get("url"),
                "top_comments": []
            }
            
            # Extract top 10 comments to provide context without overwhelming the token limit
            children = data.get("children", [])
            for child in children[:10]:
                if child.get("text"):
                    context["top_comments"].append({
                        "author": child.get("author"),
                        "text": child.get("text")[:1000]  # Truncate very long comments
                    })
            
            return json.dumps(context, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})
