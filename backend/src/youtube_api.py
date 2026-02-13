"""
YouTube Data API Integration
Handles interaction with YouTube Data API v3 for enhanced features
"""

import logging
import asyncio
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

class YouTubeAPI:
    """Wrapper for YouTube Data API v3"""

    def __init__(self, api_key: Optional[str] = None, access_token: Optional[str] = None):
        self.api_key = api_key
        self.access_token = access_token
        self.service = None

        # Initialize YouTube API client
        if api_key or access_token:
            self._initialize_service()

    def _initialize_service(self):
        """Initialize YouTube API service"""
        try:
            credentials = None
            if self.access_token:
                # Create credentials from access token
                from google.auth.transport.requests import Request
                from google.oauth2.credentials import Credentials
                credentials = Credentials(token=self.access_token)

            self.service = build('youtube', 'v3',
                               developerKey=self.api_key,
                               credentials=credentials if self.access_token else None)
            logger.info("YouTube API service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize YouTube API service: {e}")

    async def search_videos(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search for videos using YouTube Data API"""
        if not self.service:
            logger.warning("YouTube API service not initialized")
            return []

        try:
            request = self.service.search().list(
                q=query,
                part='snippet',
                type='video',
                maxResults=max_results,
                videoCategoryId='10'  # Music category
            )
            response = request.execute()

            videos = []
            for item in response.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']

                # Get detailed video statistics
                video_details = await self.get_video_details(video_id)

                videos.append({
                    'id': video_id,
                    'title': snippet['title'],
                    'description': snippet.get('description', ''),
                    'channel_title': snippet['channelTitle'],
                    'published_at': snippet['publishedAt'],
                    'thumbnail': snippet['thumbnails'].get('high', {}).get('url'),
                    'duration': video_details.get('duration'),
                    'view_count': video_details.get('view_count'),
                    'like_count': video_details.get('like_count')
                })

            return videos

        except HttpError as e:
            logger.error(f"YouTube API search error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            return []

    async def get_video_details(self, video_id: str) -> Dict:
        """Get detailed video information"""
        if not self.service:
            return {}

        try:
            request = self.service.videos().list(
                part='contentDetails,statistics',
                id=video_id
            )
            response = request.execute()

            if response.get('items'):
                item = response['items'][0]
                content_details = item.get('contentDetails', {})
                statistics = item.get('statistics', {})

                return {
                    'duration': content_details.get('duration'),
                    'dimension': content_details.get('dimension'),
                    'definition': content_details.get('definition'),
                    'caption': content_details.get('caption'),
                    'licensed_content': content_details.get('licensedContent'),
                    'view_count': statistics.get('viewCount'),
                    'like_count': statistics.get('likeCount'),
                    'dislike_count': statistics.get('dislikeCount'),
                    'favorite_count': statistics.get('favoriteCount'),
                    'comment_count': statistics.get('commentCount')
                }

            return {}

        except HttpError as e:
            logger.error(f"YouTube API video details error: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error getting video details: {e}")
            return {}

    async def get_user_playlists(self) -> List[Dict]:
        """Get user's playlists from YouTube account"""
        if not self.service or not self.access_token:
            logger.warning("YouTube API service not initialized or no access token")
            return []

        try:
            request = self.service.playlists().list(
                part='snippet,contentDetails',
                mine=True,
                maxResults=50
            )
            response = request.execute()

            playlists = []
            for item in response.get('items', []):
                playlists.append({
                    'id': item['id'],
                    'title': item['snippet']['title'],
                    'description': item['snippet'].get('description', ''),
                    'published_at': item['snippet']['publishedAt'],
                    'item_count': item['contentDetails'].get('itemCount', 0),
                    'thumbnail': item['snippet']['thumbnails'].get('default', {}).get('url')
                })

            return playlists

        except HttpError as e:
            logger.error(f"YouTube API playlists error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error getting playlists: {e}")
            return []

    async def get_playlist_items(self, playlist_id: str, max_results: int = 50) -> List[Dict]:
        """Get items in a playlist"""
        if not self.service:
            return []

        try:
            request = self.service.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=playlist_id,
                maxResults=max_results
            )
            response = request.execute()

            items = []
            for item in response.get('items', []):
                snippet = item['snippet']
                content_details = item['contentDetails']

                items.append({
                    'id': item['id'],
                    'video_id': content_details['videoId'],
                    'title': snippet['title'],
                    'description': snippet.get('description', ''),
                    'channel_title': snippet['channelTitle'],
                    'published_at': snippet['publishedAt'],
                    'thumbnail': snippet['thumbnails'].get('default', {}).get('url'),
                    'position': snippet['position']
                })

            return items

        except HttpError as e:
            logger.error(f"YouTube API playlist items error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error getting playlist items: {e}")
            return []

    async def get_user_liked_videos(self) -> List[Dict]:
        """Get user's liked videos"""
        if not self.service or not self.access_token:
            logger.warning("YouTube API service not initialized or no access token")
            return []

        try:
            request = self.service.videos().list(
                part='snippet,contentDetails',
                myRating='like',
                maxResults=50
            )
            response = request.execute()

            videos = []
            for item in response.get('items', []):
                snippet = item['snippet']
                content_details = item['contentDetails']

                videos.append({
                    'id': item['id'],
                    'title': snippet['title'],
                    'description': snippet.get('description', ''),
                    'channel_title': snippet['channelTitle'],
                    'published_at': snippet['publishedAt'],
                    'thumbnail': snippet['thumbnails'].get('default', {}).get('url'),
                    'duration': content_details.get('duration'),
                    'dimension': content_details.get('dimension'),
                    'definition': content_details.get('definition')
                })

            return videos

        except HttpError as e:
            logger.error(f"YouTube API liked videos error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error getting liked videos: {e}")
            return []