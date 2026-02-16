"""
Simplified YouTube Music Proxy Backend for Vercel
Minimal version to avoid 250MB size limit
"""

import os
import json
import logging
from typing import Optional, List, Dict
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="YouTube Music Proxy API",
    description="Simplified API for YouTube Music",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for serverless functions
_memory_store = {}

def get_storage():
    """Get storage - uses memory for serverless"""
    return _memory_store

class VideoInfo(BaseModel):
    id: str
    title: str
    artist: str
    thumbnail: str
    duration: int = 0

class SearchResponse(BaseModel):
    results: List[VideoInfo]

# Simple search using external API
@app.get("/api/search", response_model=SearchResponse)
async def search_videos(
    q: str = Query(..., description="Search query"),
    max_results: int = Query(10, ge=1, le=50)
):
    """Search YouTube videos using Invidious API (lightweight alternative)"""
    try:
        import httpx
        
        # Use Invidious API - lightweight, no API key needed
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://vid.puffyan.us/api/v1/search",
                params={"q": q, "type": "video", "sort_by": "relevance"},
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
        
        results = []
        for item in data[:max_results]:
            if item.get("type") == "video":
                results.append(VideoInfo(
                    id=item.get("videoId", ""),
                    title=item.get("title", "Unknown"),
                    artist=item.get("author", "Unknown"),
                    thumbnail=item.get("videoThumbnails", [{}])[0].get("url", ""),
                    duration=item.get("lengthSeconds", 0)
                ))
        
        return SearchResponse(results=results)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        # Return mock data if API fails
        return SearchResponse(results=[
            VideoInfo(
                id=f"mock_{i}",
                title=f"Result {i+1} for '{q}'",
                artist="Unknown",
                thumbnail="",
                duration=180
            ) for i in range(min(5, max_results))
        ])

@app.get("/api/playlists")
async def get_playlists():
    """Get all playlists"""
    storage = get_storage()
    playlists = storage.get("playlists", [])
    return [{"id": p["id"], "name": p["name"], "item_count": len(p.get("items", []))} 
            for p in playlists]

@app.post("/api/playlists")
async def create_playlist(name: str):
    """Create new playlist"""
    import time
    storage = get_storage()
    
    if "playlists" not in storage:
        storage["playlists"] = []
    
    playlist_id = int(time.time())
    storage["playlists"].append({
        "id": playlist_id,
        "name": name,
        "created_at": datetime.now().isoformat(),
        "items": []
    })
    
    return {"id": playlist_id, "name": name}

@app.get("/api/playlists/{playlist_id}")
async def get_playlist(playlist_id: int):
    """Get playlist items"""
    storage = get_storage()
    playlists = storage.get("playlists", [])
    
    for playlist in playlists:
        if playlist["id"] == playlist_id:
            return playlist.get("items", [])
    
    return []

@app.post("/api/playlists/{playlist_id}/items")
async def add_to_playlist(
    playlist_id: int,
    video_id: str,
    title: str,
    duration: int = 0
):
    """Add video to playlist"""
    storage = get_storage()
    playlists = storage.get("playlists", [])
    
    for playlist in playlists:
        if playlist["id"] == playlist_id:
            if "items" not in playlist:
                playlist["items"] = []
            
            playlist["items"].append({
                "video_id": video_id,
                "title": title,
                "duration": duration,
                "added_at": datetime.now().isoformat()
            })
            return {"success": True}
    
    raise HTTPException(status_code=404, detail="Playlist not found")

@app.get("/api/recently-played")
async def get_recently_played(limit: int = 20):
    """Get recently played"""
    storage = get_storage()
    return storage.get("recently_played", [])[:limit]

@app.post("/api/recently-played")
async def add_recently_played(video_id: str, title: str):
    """Add to recently played"""
    storage = get_storage()
    
    if "recently_played" not in storage:
        storage["recently_played"] = []
    
    # Remove if exists
    storage["recently_played"] = [
        item for item in storage["recently_played"] 
        if item["video_id"] != video_id
    ]
    
    # Add to front
    storage["recently_played"].insert(0, {
        "video_id": video_id,
        "title": title,
        "played_at": datetime.now().isoformat()
    })
    
    # Keep only last 100
    storage["recently_played"] = storage["recently_played"][:100]
    
    return {"success": True}

@app.get("/api/auth/url")
async def get_auth_url():
    """Get OAuth URL"""
    return {"auth_url": "https://accounts.google.com/o/oauth2/auth"}

@app.get("/api/auth/callback")
async def auth_callback(code: str, state: str):
    """Handle OAuth callback"""
    return {
        "message": "Auth not implemented in minimal version",
        "access_token": "mock_token"
    }

@app.get("/api/auth/status")
async def auth_status():
    """Check auth status"""
    return {"authenticated": False}

@app.get("/api/stream/{video_id}")
async def stream_video(video_id: str):
    """Get stream URL - redirects to external service"""
    return {
        "video_id": video_id,
        "stream_url": f"https://vid.puffyan.us/latest_version?id={video_id}&itag=251",
        "audio_url": f"https://vid.puffyan.us/latest_version?id={video_id}&itag=140"
    }

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "message": "YouTube Music Proxy API (Minimal)",
        "version": "1.0.0"
    }
