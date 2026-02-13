"""
YouTube Music Proxy Backend
FastAPI server for streaming YouTube audio without ads
"""

import os
import asyncio
import logging
from typing import Optional
from pathlib import Path
from fastapi.responses import FileResponse

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from downloader import YouTubeDownloader
from cache import AudioCache
from db import Database
from models import *
from auth import AuthManager
from recommendations import RecommendationEngine
from youtube_api import YouTubeAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# App configuration
app = FastAPI(
    title="YouTube Music Proxy API",
    description="API for streaming YouTube music without ads",
    version="1.0.0"
)

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global services
downloader: Optional[YouTubeDownloader] = None
cache: Optional[AudioCache] = None
db: Optional[Database] = None
auth_manager: Optional[AuthManager] = None
recommendation_engine: Optional[RecommendationEngine] = None
youtube_api: Optional[YouTubeAPI] = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global downloader, cache, db, auth_manager, recommendation_engine, youtube_api

    # Initialize database
    db = Database()
    await db.init()

    # Initialize cache
    cache_dir = Path.home() / ".cache" / "youtube-music"
    cache = AudioCache(cache_dir, max_size_gb=5)

    # Initialize downloader
    downloader = YouTubeDownloader(cache_dir)

    # Initialize auth manager
    auth_manager = AuthManager()

    # Initialize recommendation engine
    recommendation_engine = RecommendationEngine(db)

    # Initialize YouTube API
    api_key = os.getenv('YOUTUBE_API_KEY')
    youtube_api = YouTubeAPI(api_key=api_key)

    logger.info("Services initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    if db:
        await db.close()
    logger.info("Services shutdown")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "YouTube Music Proxy API is running"}

@app.get("/auth/login")
async def login():
    """Initiate OAuth2 login flow"""
    if not auth_manager:
        raise HTTPException(status_code=500, detail="Auth manager not initialized")

    auth_url = auth_manager.get_auth_url()
    return {"auth_url": auth_url}

@app.get("/callback")
async def oauth_callback(code: str, state: str):
    """Handle OAuth2 callback"""
    if not auth_manager:
        raise HTTPException(status_code=500, detail="Auth manager not initialized")

    try:
        session_data = await auth_manager.handle_callback(code, state)
        return {"message": "Authentication successful", "session": session_data}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/auth/logout")
async def logout():
    """Logout user"""
    if not auth_manager:
        raise HTTPException(status_code=500, detail="Auth manager not initialized")

    auth_manager.clear_session()
    return {"message": "Logged out successfully"}

@app.get("/auth/status")
async def auth_status():
    """Check authentication status"""
    if not auth_manager:
        raise HTTPException(status_code=500, detail="Auth manager not initialized")

    is_authenticated = auth_manager.is_authenticated()
    return {"authenticated": is_authenticated}

@app.get("/api/search")
async def search_videos(query: str, max_results: int = 10):
    """Search YouTube videos"""
    global youtube_api, auth_manager

    # Try to use YouTube API if authenticated
    if youtube_api and auth_manager and auth_manager.is_authenticated():
        try:
            # Refresh access token if needed
            access_token = auth_manager.get_access_token()
            if access_token:
                youtube_api.access_token = access_token
                youtube_api._initialize_service()

            results = await youtube_api.search_videos(query, max_results)
            return SearchResult(results=[VideoInfo(**result) for result in results])
        except Exception as e:
            logger.warning(f"YouTube API search failed, falling back to yt-dlp: {e}")

    # Fallback to yt-dlp search
    try:
        results = await downloader.search(query, max_results)
        return SearchResult(results=[VideoInfo(**result) for result in results])
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/download")
async def download_audio(request: DownloadRequest, background_tasks: BackgroundTasks):
    """Download audio from YouTube video"""
    try:
        # Check if already cached
        cached_path = cache.get_cached_file(request.video_id, request.quality)
        if cached_path and cached_path.exists():
            return DownloadResponse(
                status="cached",
                video_id=request.video_id,
                quality=request.quality,
                path=str(cached_path.relative_to(cache.cache_dir))
            )

        # Start download in background
        background_tasks.add_task(
            downloader.download_audio,
            request.video_id,
            request.quality
        )

        return DownloadResponse(
            status="started",
            video_id=request.video_id,
            quality=request.quality
        )
    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stream/{video_id}")
async def stream_audio(video_id: str, quality: str = "192k"):
    """Stream audio file"""
    try:
        file_path = cache.get_cached_file(video_id, quality)
        if not file_path or not file_path.exists():
            raise HTTPException(status_code=404, detail="Audio not found")

        return FileResponse(
            file_path,
            media_type="audio/mpeg",
            headers={
                "Accept-Ranges": "bytes",
                "Content-Length": str(file_path.stat().st_size)
            }
        )
    except Exception as e:
        logger.error(f"Streaming failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Playlist endpoints
@app.get("/api/playlists", response_model=List[Playlist])
async def get_playlists():
    """Get all playlists"""
    try:
        playlists = await db.get_playlists()
        return [Playlist(**playlist) for playlist in playlists]
    except Exception as e:
        logger.error(f"Failed to get playlists: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/playlists", response_model=Playlist)
async def create_playlist(request: PlaylistCreateRequest):
    """Create new playlist"""
    try:
        playlist_id = await db.create_playlist(request.name)
        # Get the created playlist
        playlists = await db.get_playlists()
        created_playlist = next((p for p in playlists if p['id'] == playlist_id), None)
        if created_playlist:
            return Playlist(**created_playlist)
        raise HTTPException(status_code=500, detail="Failed to retrieve created playlist")
    except Exception as e:
        logger.error(f"Failed to create playlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/playlists/{playlist_id}", response_model=List[PlaylistItem])
async def get_playlist_items(playlist_id: int):
    """Get items in playlist"""
    try:
        items = await db.get_playlist_items(playlist_id)
        return [PlaylistItem(**item) for item in items]
    except Exception as e:
        logger.error(f"Failed to get playlist items: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/playlists/{playlist_id}/items", response_model=bool)
async def add_to_playlist(playlist_id: int, request: PlaylistItemCreateRequest):
    """Add video to playlist"""
    try:
        result = await db.add_to_playlist(
            playlist_id,
            request.video_id,
            request.title,
            request.duration
        )
        return result
    except Exception as e:
        logger.error(f"Failed to add to playlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Recently played endpoints
@app.get("/api/recently-played", response_model=List[RecentlyPlayedItem])
async def get_recently_played(limit: int = 20):
    """Get recently played items"""
    try:
        items = await db.get_recently_played(limit)
        return [RecentlyPlayedItem(**item) for item in items]
    except Exception as e:
        logger.error(f"Failed to get recently played: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recently-played", response_model=bool)
async def add_recently_played(request: PlaylistItemCreateRequest):
    """Add to recently played"""
    try:
        result = await db.add_recently_played(request.video_id, request.title)
        return result
    except Exception as e:
        logger.error(f"Failed to add recently played: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Authentication endpoints
@app.get("/api/auth/url")
async def get_auth_url():
    """Get YouTube OAuth2 authorization URL"""
    try:
        auth_url = auth_manager.get_auth_url()
        return {"auth_url": auth_url}
    except Exception as e:
        logger.error(f"Failed to generate auth URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/auth/callback")
async def auth_callback(code: str, state: str):
    """Handle OAuth2 callback"""
    try:
        success = auth_manager.handle_callback(code, state)
        if success:
            return {"message": "Authentication successful"}
        else:
            raise HTTPException(status_code=400, detail="Authentication failed")
    except Exception as e:
        logger.error(f"Auth callback failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/auth/status")
async def auth_status():
    """Check authentication status"""
    try:
        is_authenticated = auth_manager.is_authenticated()
        return {"authenticated": is_authenticated}
    except Exception as e:
        logger.error(f"Failed to check auth status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Recommendation endpoints
@app.get("/api/recommendations", response_model=List[VideoInfo])
async def get_recommendations(limit: int = 20):
    """Get personalized recommendations"""
    try:
        recommendations = await recommendation_engine.get_recommendations(limit)
        return [VideoInfo(**rec) for rec in recommendations]
    except Exception as e:
        logger.error(f"Failed to get recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recommendations/discovery", response_model=List[VideoInfo])
async def get_discovery_recommendations(limit: int = 10):
    """Get music discovery recommendations"""
    try:
        recommendations = await recommendation_engine.get_discovery_recommendations(limit)
        return [VideoInfo(**rec) for rec in recommendations]
    except Exception as e:
        logger.error(f"Failed to get discovery recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Cache management endpoints
@app.get("/api/cache/stats", response_model=CacheStats)
async def get_cache_stats():
    """Get cache statistics"""
    try:
        stats = cache.get_cache_stats()
        return CacheStats(**stats)
    except Exception as e:
        logger.error(f"Failed to get cache stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cache/cleanup", response_model=int)
async def cleanup_cache():
    """Clean up old cache files"""
    try:
        deleted_count = cache.cleanup_old_files()
        return deleted_count
    except Exception as e:
        logger.error(f"Cache cleanup failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cache/clear", response_model=bool)
async def clear_cache():
    """Clear entire cache"""
    try:
        result = cache.clear_cache()
        return result
    except Exception as e:
        logger.error(f"Failed to clear cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# YouTube API endpoints
@app.get("/api/youtube/playlists")
async def get_youtube_playlists():
    """Get user's YouTube playlists"""
    global youtube_api, auth_manager

    if not youtube_api or not auth_manager:
        raise HTTPException(status_code=500, detail="Services not initialized")

    if not auth_manager.is_authenticated():
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        # Refresh access token if needed
        access_token = auth_manager.get_access_token()
        if access_token:
            youtube_api.access_token = access_token
            youtube_api._initialize_service()

        playlists = await youtube_api.get_user_playlists()
        return playlists
    except Exception as e:
        logger.error(f"Failed to get YouTube playlists: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/youtube/playlists/{playlist_id}/items")
async def get_youtube_playlist_items(playlist_id: str):
    """Get items in a YouTube playlist"""
    global youtube_api, auth_manager

    if not youtube_api or not auth_manager:
        raise HTTPException(status_code=500, detail="Services not initialized")

    if not auth_manager.is_authenticated():
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        # Refresh access token if needed
        access_token = auth_manager.get_access_token()
        if access_token:
            youtube_api.access_token = access_token
            youtube_api._initialize_service()

        items = await youtube_api.get_playlist_items(playlist_id)
        return items
    except Exception as e:
        logger.error(f"Failed to get YouTube playlist items: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/youtube/liked-videos")
async def get_youtube_liked_videos():
    """Get user's liked videos"""
    global youtube_api, auth_manager

    if not youtube_api or not auth_manager:
        raise HTTPException(status_code=500, detail="Services not initialized")

    if not auth_manager.is_authenticated():
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        # Refresh access token if needed
        access_token = auth_manager.get_access_token()
        if access_token:
            youtube_api.access_token = access_token
            youtube_api._initialize_service()

        videos = await youtube_api.get_user_liked_videos()
        return videos
    except Exception as e:
        logger.error(f"Failed to get YouTube liked videos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )