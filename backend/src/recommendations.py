"""
Recommendation Engine
Generates music recommendations based on user listening history
"""

import logging
import random
from typing import List, Dict, Set, Optional
from collections import Counter
import asyncio

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """Generates personalized music recommendations"""

    def __init__(self, db, youtube_api=None, downloader=None):
        self.db = db
        self.youtube_api = youtube_api
        self.downloader = downloader
        self.user_history = []
        self._popular_tracks_cache = None

    async def load_user_history(self):
        """Load user's listening history"""
        try:
            self.user_history = await self.db.get_recently_played(limit=100)
            logger.info(f"Loaded {len(self.user_history)} items from listening history")
        except Exception as e:
            logger.error(f"Failed to load user history: {e}")

    async def get_recommendations(self, limit: int = 20) -> List[Dict]:
        """Get personalized recommendations"""
        if not self.user_history:
            await self.load_user_history()

        if not self.user_history:
            return await self.get_popular_tracks(limit)

        # Combine different recommendation strategies
        recommendations = []

        # 1. Based on recently played artists
        artist_recs = await self._get_artist_based_recommendations(limit // 3)
        recommendations.extend(artist_recs)

        # 2. Based on listening patterns
        pattern_recs = await self._get_pattern_based_recommendations(limit // 3)
        recommendations.extend(pattern_recs)

        # 3. Popular tracks
        popular_recs = await self.get_popular_tracks(limit // 3)
        recommendations.extend(popular_recs)

        # Remove duplicates and shuffle
        unique_recommendations = self._remove_duplicates(recommendations)
        random.shuffle(unique_recommendations)

        return unique_recommendations[:limit]

    async def _get_artist_based_recommendations(self, limit: int) -> List[Dict]:
        """Get recommendations based on artists from listening history"""
        if not self.user_history:
            return []

        # Extract artists from recently played tracks
        artists = []
        for item in self.user_history[:20]:
            # Try to extract artist from title (usually "Artist - Title" format)
            title = item.get('title', '')
            if ' - ' in title:
                artist = title.split(' - ')[0].strip()
                if artist:
                    artists.append(artist)

        if not artists:
            return []

        # Count artist frequencies
        artist_counts = Counter(artists)
        top_artists = [artist for artist, count in artist_counts.most_common(3)]

        # Search for tracks by these artists using YouTube API or downloader
        similar_tracks = []
        for artist in top_artists:
            try:
                tracks = await self._search_tracks_by_artist(artist, limit // 3)
                similar_tracks.extend(tracks)
            except Exception as e:
                logger.warning(f"Failed to get tracks for artist {artist}: {e}")

        return similar_tracks

    async def _search_tracks_by_artist(self, artist: str, limit: int) -> List[Dict]:
        """Search for tracks by a specific artist using available API"""
        tracks = []
        
        try:
            # Try to use YouTube API if available
            if self.youtube_api:
                search_query = f"{artist} official music video"
                results = await self.youtube_api.search_videos(search_query, max_results=limit)
                tracks = [self._format_track(r) for r in results]
            # Fallback to downloader/yt-dlp
            elif self.downloader:
                search_query = f"{artist} music"
                results = await self.downloader.search(search_query, max_results=limit)
                tracks = [self._format_track(r) for r in results]
        except Exception as e:
            logger.error(f"Error searching tracks for {artist}: {e}")
        
        return tracks

    def _format_track(self, item: Dict) -> Dict:
        """Format track data consistently"""
        return {
            'id': item.get('id', ''),
            'title': item.get('title', 'Unknown'),
            'artist': item.get('artist', item.get('channel', 'Unknown')),
            'thumbnail': item.get('thumbnail', ''),
            'duration': item.get('duration', 0)
        }

    async def _get_pattern_based_recommendations(self, limit: int) -> List[Dict]:
        """Get recommendations based on listening patterns"""
        if not self.user_history:
            return []

        # Get a random sample from history and search similar
        sample_size = min(3, len(self.user_history))
        sample_tracks = random.sample(self.user_history, sample_size)
        
        pattern_tracks = []
        for track in sample_tracks:
            try:
                title = track.get('title', '')
                if title:
                    # Search for similar tracks
                    results = await self._search_similar_tracks(title, limit // sample_size)
                    pattern_tracks.extend(results)
            except Exception as e:
                logger.warning(f"Failed to get similar tracks for {track}: {e}")

        return pattern_tracks

    async def _search_similar_tracks(self, query: str, limit: int) -> List[Dict]:
        """Search for tracks similar to the query"""
        tracks = []
        
        try:
            # Try YouTube API first
            if self.youtube_api:
                results = await self.youtube_api.search_videos(query, max_results=limit)
                tracks = [self._format_track(r) for r in results]
            # Fallback to downloader
            elif self.downloader:
                results = await self.downloader.search(query, max_results=limit)
                tracks = [self._format_track(r) for r in results]
        except Exception as e:
            logger.error(f"Error searching similar tracks: {e}")
        
        return tracks

    async def get_popular_tracks(self, limit: int) -> List[Dict]:
        """Get popular tracks (fallback recommendations)"""
        # Cache popular tracks to avoid repeated searches
        if self._popular_tracks_cache is not None:
            return self._popular_tracks_cache[:limit]
        
        popular_queries = [
            "trending music",
            "popular songs 2024",
            "top hits",
            "viral music"
        ]
        
        all_tracks = []
        
        # Try to get trending tracks
        for query in popular_queries[:2]:  # Use first 2 queries
            try:
                if self.youtube_api:
                    results = await self.youtube_api.search_videos(query, max_results=limit // 2)
                    all_tracks.extend([self._format_track(r) for r in results])
                elif self.downloader:
                    results = await self.downloader.search(query, max_results=limit // 2)
                    all_tracks.extend([self._format_track(r) for r in results])
            except Exception as e:
                logger.warning(f"Failed to get popular tracks for query '{query}': {e}")
        
        # Cache results
        self._popular_tracks_cache = all_tracks
        
        return all_tracks[:limit]

    def _remove_duplicates(self, tracks: List[Dict]) -> List[Dict]:
        """Remove duplicate tracks based on video ID"""
        seen_ids = set()
        unique_tracks = []

        for track in tracks:
            track_id = track.get('id', '')
            if track_id and track_id not in seen_ids:
                seen_ids.add(track_id)
                unique_tracks.append(track)

        return unique_tracks

    async def get_discovery_recommendations(self, limit: int = 10) -> List[Dict]:
        """Get tracks for music discovery (less familiar artists)"""
        if not self.user_history:
            await self.load_user_history()
        
        # Get known artists from history
        known_artists = set()
        for item in self.user_history:
            title = item.get('title', '')
            if ' - ' in title:
                artist = title.split(' - ')[0].strip()
                known_artists.add(artist.lower())
        
        # Search for music from different genres
        discovery_queries = [
            "new music releases",
            "indie music",
            "alternative rock",
            "electronic music"
        ]
        
        discovery_tracks = []
        
        for query in discovery_queries:
            try:
                if self.youtube_api:
                    results = await self.youtube_api.search_videos(query, max_results=limit // len(discovery_queries))
                elif self.downloader:
                    results = await self.downloader.search(query, max_results=limit // len(discovery_queries))
                else:
                    continue
                
                for item in results:
                    track = self._format_track(item)
                    # Filter out tracks from known artists
                    artist = track.get('artist', '').lower()
                    if not any(known in artist or artist in known for known in known_artists):
                        discovery_tracks.append(track)
                        
            except Exception as e:
                logger.warning(f"Failed to get discovery tracks for '{query}': {e}")
        
        random.shuffle(discovery_tracks)
        return discovery_tracks[:limit]
