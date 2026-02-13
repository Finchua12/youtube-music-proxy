"""
Data Models for YouTube Music Proxy API
Pydantic models for request/response validation
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DownloadRequest(BaseModel):
    """Request model for downloading audio"""
    video_id: str
    quality: str = "192k"

class SearchRequest(BaseModel):
    """Request model for searching videos"""
    query: str
    max_results: int = 10

class VideoInfo(BaseModel):
    """Model for YouTube video information"""
    id: str
    title: str
    duration: Optional[int] = None
    uploader: Optional[str] = None
    thumbnail: Optional[str] = None
    view_count: Optional[int] = None
    upload_date: Optional[str] = None
    description: Optional[str] = None

class SearchResult(BaseModel):
    """Model for search results"""
    results: List[VideoInfo]

class DownloadResponse(BaseModel):
    """Response model for download requests"""
    status: str
    video_id: str
    quality: str
    path: Optional[str] = None

class PlaylistCreateRequest(BaseModel):
    """Request model for creating playlists"""
    name: str

class PlaylistItemCreateRequest(BaseModel):
    """Request model for adding items to playlist"""
    video_id: str
    title: str
    duration: Optional[int] = None

class PlaylistItem(BaseModel):
    """Model for playlist items"""
    id: int
    playlist_id: int
    video_id: str
    title: str
    duration: Optional[int] = None
    added_at: datetime

class Playlist(BaseModel):
    """Model for playlists"""
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    item_count: Optional[int] = 0

class RecentlyPlayedItem(BaseModel):
    """Model for recently played items"""
    id: int
    video_id: str
    title: str
    played_at: datetime

class CacheStats(BaseModel):
    """Model for cache statistics"""
    size_bytes: int
    size_gb: float
    max_size_gb: float
    file_count: int
    directory: str