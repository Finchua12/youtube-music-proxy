"""
Recommendation Engine
Generates music recommendations based on user listening history
"""

import logging
import random
from typing import List, Dict, Set
from collections import Counter
import asyncio

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """Generates personalized music recommendations"""

    def __init__(self, db):
        self.db = db
        self.user_history = []

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
        for item in self.user_history[:20]:  # Look at last 20 played
            # In a real implementation, you would extract artist from title
            # For now, we'll simulate this
            if 'queen' in item['title'].lower():
                artists.append('Queen')
            elif 'led zeppelin' in item['title'].lower():
                artists.append('Led Zeppelin')
            elif 'pink floyd' in item['title'].lower():
                artists.append('Pink Floyd')
            elif 'beatles' in item['title'].lower():
                artists.append('The Beatles')

        if not artists:
            return []

        # Count artist frequencies
        artist_counts = Counter(artists)
        top_artists = [artist for artist, count in artist_counts.most_common(3)]

        # Simulate getting similar tracks (in real implementation, use YouTube API)
        similar_tracks = []
        for artist in top_artists:
            similar_tracks.extend(await self._get_similar_tracks_by_artist(artist, limit // 3))

        return similar_tracks

    async def _get_similar_tracks_by_artist(self, artist: str, limit: int) -> List[Dict]:
        """Get tracks similar to a specific artist"""
        # This is a simulation - in real implementation, you would use YouTube API
        # or a music recommendation service

        artist_tracks = {
            'Queen': [
                {'id': 'fJ9rUzIMcZQ', 'title': 'Bohemian Rhapsody', 'artist': 'Queen'},
                {'id': '2Z4m4lnjxkY', 'title': 'Somebody to Love', 'artist': 'Queen'},
                {'id': '1wZoGFF_oi4', 'title': 'Don\'t Stop Me Now', 'artist': 'Queen'}
            ],
            'Led Zeppelin': [
                {'id': 'QkF3oxziUI4', 'title': 'Stairway to Heaven', 'artist': 'Led Zeppelin'},
                {'id': 'ET4btO2Na6I', 'title': 'Whole Lotta Love', 'artist': 'Led Zeppelin'},
                {'id': 'fqJOlDUzC5M', 'title': 'Black Dog', 'artist': 'Led Zeppelin'}
            ],
            'Pink Floyd': [
                {'id': 'HrxX9TBj2zY', 'title': 'Wish You Were Here', 'artist': 'Pink Floyd'},
                {'id': '8zWfDfoV2Fs', 'title': 'Comfortably Numb', 'artist': 'Pink Floyd'},
                {'id': 'P9qBe9-V_qg', 'title': 'Money', 'artist': 'Pink Floyd'}
            ],
            'The Beatles': [
                {'id': 'A_MjCqQoLLA', 'title': 'Hey Jude', 'artist': 'The Beatles'},
                {'id': 'dQw4w9WgXcQ', 'title': 'Yesterday', 'artist': 'The Beatles'},
                {'id': 'oKsxPW6i3pM', 'title': 'Come Together', 'artist': 'The Beatles'}
            ]
        }

        tracks = artist_tracks.get(artist, [])
        return tracks[:limit]

    async def _get_pattern_based_recommendations(self, limit: int) -> List[Dict]:
        """Get recommendations based on listening patterns"""
        if not self.user_history:
            return []

        # Analyze listening time patterns (morning, afternoon, evening, night)
        time_patterns = self._analyze_time_patterns()

        # Analyze genre preferences (simulated)
        genre_preferences = self._analyze_genre_preferences()

        # Get tracks based on patterns
        pattern_tracks = []

        # Morning energy tracks
        if 'morning' in time_patterns:
            pattern_tracks.extend(await self._get_energy_tracks('high', limit // 2))

        # Evening relaxing tracks
        if 'evening' in time_patterns:
            pattern_tracks.extend(await self._get_energy_tracks('low', limit // 2))

        # Genre-based tracks
        for genre in genre_preferences[:2]:
            pattern_tracks.extend(await self._get_genre_tracks(genre, limit // 4))

        return pattern_tracks

    def _analyze_time_patterns(self) -> Set[str]:
        """Analyze when user typically listens to music"""
        patterns = set()

        # In a real implementation, you would analyze actual timestamps
        # For now, we'll simulate common patterns
        patterns.add('evening')
        patterns.add('night')

        return patterns

    def _analyze_genre_preferences(self) -> List[str]:
        """Analyze user's genre preferences"""
        # In a real implementation, you would categorize tracks by genre
        # For now, we'll simulate common genres
        return ['rock', 'classic rock', 'progressive rock', 'psychedelic rock']

    async def _get_energy_tracks(self, energy_level: str, limit: int) -> List[Dict]:
        """Get tracks based on energy level"""
        # This is a simulation - in real implementation, use audio features
        high_energy_tracks = [
            {'id': 'fJ9rUzIMcZQ', 'title': 'Bohemian Rhapsody', 'artist': 'Queen', 'energy': 'high'},
            {'id': '1wZoGFF_oi4', 'title': 'Don\'t Stop Me Now', 'artist': 'Queen', 'energy': 'high'},
            {'id': 'n4RjJKxsamQ', 'title': 'We Will Rock You', 'artist': 'Queen', 'energy': 'high'}
        ]

        low_energy_tracks = [
            {'id': 'HrxX9TBj2zY', 'title': 'Wish You Were Here', 'artist': 'Pink Floyd', 'energy': 'low'},
            {'id': '6h9cAJpU5R4', 'title': 'Breathe', 'artist': 'Pink Floyd', 'energy': 'low'},
            {'id': 'PCzEJeoGNUA', 'title': 'Wish You Were Here (Live)', 'artist': 'Pink Floyd', 'energy': 'low'}
        ]

        if energy_level == 'high':
            return high_energy_tracks[:limit]
        else:
            return low_energy_tracks[:limit]

    async def _get_genre_tracks(self, genre: str, limit: int) -> List[Dict]:
        """Get tracks from a specific genre"""
        # This is a simulation - in real implementation, use genre classification
        genre_tracks = {
            'rock': [
                {'id': 'fJ9rUzIMcZQ', 'title': 'Bohemian Rhapsody', 'artist': 'Queen', 'genre': 'rock'},
                {'id': 'QkF3oxziUI4', 'title': 'Stairway to Heaven', 'artist': 'Led Zeppelin', 'genre': 'rock'}
            ],
            'classic rock': [
                {'id': 'ET4btO2Na6I', 'title': 'Whole Lotta Love', 'artist': 'Led Zeppelin', 'genre': 'classic rock'},
                {'id': 'A_MjCqQoLLA', 'title': 'Hey Jude', 'artist': 'The Beatles', 'genre': 'classic rock'}
            ]
        }

        return genre_tracks.get(genre, [])[:limit]

    async def get_popular_tracks(self, limit: int) -> List[Dict]:
        """Get popular tracks (fallback recommendations)"""
        # This is a simulation - in real implementation, use chart data or trending
        popular_tracks = [
            {'id': 'fJ9rUzIMcZQ', 'title': 'Bohemian Rhapsody', 'artist': 'Queen'},
            {'id': 'QkF3oxziUI4', 'title': 'Stairway to Heaven', 'artist': 'Led Zeppelin'},
            {'id': 'A_MjCqQoLLA', 'title': 'Hey Jude', 'artist': 'The Beatles'},
            {'id': 'HrxX9TBj2zY', 'title': 'Wish You Were Here', 'artist': 'Pink Floyd'},
            {'id': '2Z4m4lnjxkY', 'title': 'Somebody to Love', 'artist': 'Queen'},
            {'id': '1wZoGFF_oi4', 'title': 'Don\'t Stop Me Now', 'artist': 'Queen'},
            {'id': 'ET4btO2Na6I', 'title': 'Whole Lotta Love', 'artist': 'Led Zeppelin'},
            {'id': '8zWfDfoV2Fs', 'title': 'Comfortably Numb', 'artist': 'Pink Floyd'}
        ]

        return popular_tracks[:limit]

    def _remove_duplicates(self, tracks: List[Dict]) -> List[Dict]:
        """Remove duplicate tracks based on video ID"""
        seen_ids = set()
        unique_tracks = []

        for track in tracks:
            if track['id'] not in seen_ids:
                seen_ids.add(track['id'])
                unique_tracks.append(track)

        return unique_tracks

    async def get_discovery_recommendations(self, limit: int = 10) -> List[Dict]:
        """Get tracks for music discovery (less familiar artists)"""
        # Simulate discovery recommendations
        discovery_tracks = [
            {'id': '5E5YFvwb2GY', 'title': 'Roundabout', 'artist': 'Yes'},
            {'id': '7Qux17e7R00', 'title': 'Owner of a Lonely Heart', 'artist': 'Yes'},
            {'id': '7keTU3j8ucI', 'title': 'Tom Sawyer', 'artist': 'Rush'},
            {'id': 'auGALZzdmqY', 'title': 'Limelight', 'artist': 'Rush'},
            {'id': 'OykvVOWa1Nc', 'title': 'Mr. Roboto', 'artist': 'Styx'},
            {'id': 'l9VBsT9Ds4Y', 'title': 'Renegade', 'artist': 'Styx'}
        ]

        random.shuffle(discovery_tracks)
        return discovery_tracks[:limit]