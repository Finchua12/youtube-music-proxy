"""
Database Module
Vercel KV (Redis) for storing playlists and user data
"""

import json
import logging
from typing import List, Dict, Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)

# Try to import upstash-redis for Vercel KV
try:
    from upstash_redis import Redis
    HAS_UPSTASH = True
except ImportError:
    HAS_UPSTASH = False
    try:
        import redis
        HAS_REDIS = True
    except ImportError:
        HAS_REDIS = False

class Database:
    def __init__(self):
        self.redis_client = None
        self.use_memory = False
        self.memory_store = {}  # Fallback for local development
        
    async def init(self):
        """Initialize database connection"""
        try:
            # Check for Vercel KV (Upstash) environment variables
            redis_url = os.getenv('KV_URL') or os.getenv('REDIS_URL')
            
            if redis_url:
                if HAS_UPSTASH:
                    self.redis_client = Redis.from_env()
                    logger.info("Connected to Vercel KV (Upstash)")
                elif HAS_REDIS:
                    self.redis_client = redis.from_url(redis_url, decode_responses=True)
                    logger.info("Connected to Redis")
                else:
                    logger.warning("Redis libraries not installed, using memory storage")
                    self.use_memory = True
            else:
                logger.info("No Redis URL found, using memory storage")
                self.use_memory = True
                
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            self.use_memory = True
            logger.info("Falling back to memory storage")

    async def close(self):
        """Close database connection"""
        if self.redis_client:
            try:
                if hasattr(self.redis_client, 'close'):
                    await self.redis_client.close()
                logger.info("Database connection closed")
            except:
                pass

    def _get_key(self, prefix: str, id: str) -> str:
        """Generate Redis key"""
        return f"{prefix}:{id}"

    async def _set(self, key: str, value: dict, expire: int = None):
        """Set value in storage"""
        data = json.dumps(value, default=str)
        if self.use_memory:
            self.memory_store[key] = data
        else:
            if HAS_UPSTASH:
                await self.redis_client.set(key, data)
            else:
                self.redis_client.set(key, data, ex=expire)

    async def _get(self, key: str) -> Optional[dict]:
        """Get value from storage"""
        try:
            if self.use_memory:
                data = self.memory_store.get(key)
            else:
                if HAS_UPSTASH:
                    data = await self.redis_client.get(key)
                else:
                    data = self.redis_client.get(key)
            
            if data:
                return json.loads(data) if isinstance(data, str) else data
            return None
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return None

    async def _delete(self, key: str):
        """Delete key from storage"""
        if self.use_memory:
            self.memory_store.pop(key, None)
        else:
            if HAS_UPSTASH:
                await self.redis_client.delete(key)
            else:
                self.redis_client.delete(key)

    async def _list_keys(self, pattern: str) -> List[str]:
        """List keys matching pattern"""
        if self.use_memory:
            return [k for k in self.memory_store.keys() if pattern.replace('*', '') in k]
        else:
            if HAS_UPSTASH:
                keys = []
                cursor = 0
                while True:
                    result = await self.redis_client.scan(cursor, match=pattern, count=100)
                    cursor = result[0]
                    keys.extend(result[1])
                    if cursor == 0:
                        break
                return keys
            else:
                return [k.decode() if isinstance(k, bytes) else k for k in self.redis_client.scan_iter(match=pattern)]

    # Playlist methods
    async def create_playlist(self, name: str) -> int:
        """Create new playlist"""
        import time
        playlist_id = int(time.time())
        playlist = {
            'id': playlist_id,
            'name': name,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'items': []
        }
        await self._set(self._get_key('playlist', str(playlist_id)), playlist)
        return playlist_id

    async def get_playlists(self) -> List[Dict]:
        """Get all playlists"""
        keys = await self._list_keys('playlist:*')
        playlists = []
        for key in keys:
            playlist = await self._get(key)
            if playlist:
                playlists.append({
                    'id': playlist['id'],
                    'name': playlist['name'],
                    'created_at': playlist['created_at'],
                    'updated_at': playlist['updated_at'],
                    'item_count': len(playlist.get('items', []))
                })
        return sorted(playlists, key=lambda x: x['created_at'], reverse=True)

    async def delete_playlist(self, playlist_id: int) -> bool:
        """Delete playlist"""
        key = self._get_key('playlist', str(playlist_id))
        await self._delete(key)
        return True

    async def add_to_playlist(self, playlist_id: int, video_id: str, title: str, duration: int = 0) -> bool:
        """Add video to playlist"""
        key = self._get_key('playlist', str(playlist_id))
        playlist = await self._get(key)
        
        if not playlist:
            return False
        
        item = {
            'video_id': video_id,
            'title': title,
            'duration': duration,
            'added_at': datetime.now().isoformat()
        }
        
        if 'items' not in playlist:
            playlist['items'] = []
        
        playlist['items'].append(item)
        playlist['updated_at'] = datetime.now().isoformat()
        
        await self._set(key, playlist)
        return True

    async def remove_from_playlist(self, playlist_id: int, video_id: str) -> bool:
        """Remove video from playlist"""
        key = self._get_key('playlist', str(playlist_id))
        playlist = await self._get(key)
        
        if not playlist:
            return False
        
        playlist['items'] = [item for item in playlist.get('items', []) if item['video_id'] != video_id]
        playlist['updated_at'] = datetime.now().isoformat()
        
        await self._set(key, playlist)
        return True

    async def get_playlist_items(self, playlist_id: int) -> List[Dict]:
        """Get items in playlist"""
        key = self._get_key('playlist', str(playlist_id))
        playlist = await self._get(key)
        
        if playlist:
            return playlist.get('items', [])
        return []

    # Recently played methods
    async def add_recently_played(self, video_id: str, title: str) -> bool:
        """Add to recently played"""
        items = await self.get_recently_played(100)
        
        # Remove if already exists
        items = [item for item in items if item['video_id'] != video_id]
        
        # Add new item at the beginning
        items.insert(0, {
            'video_id': video_id,
            'title': title,
            'played_at': datetime.now().isoformat()
        })
        
        # Keep only last 100
        items = items[:100]
        
        await self._set('recently_played', {'items': items})
        return True

    async def get_recently_played(self, limit: int = 20) -> List[Dict]:
        """Get recently played items"""
        data = await self._get('recently_played')
        if data:
            return data.get('items', [])[:limit]
        return []

    # Likes methods
    async def add_like(self, video_id: str, title: str) -> bool:
        """Add video to likes/favorites"""
        likes = await self.get_likes(1000)
        
        # Check if already liked
        if any(like['video_id'] == video_id for like in likes):
            return True
        
        likes.append({
            'video_id': video_id,
            'title': title,
            'added_at': datetime.now().isoformat()
        })
        
        await self._set('likes', {'items': likes})
        return True

    async def remove_like(self, video_id: str) -> bool:
        """Remove video from likes/favorites"""
        likes = await self.get_likes(1000)
        likes = [like for like in likes if like['video_id'] != video_id]
        await self._set('likes', {'items': likes})
        return True

    async def get_likes(self, limit: int = 100) -> List[Dict]:
        """Get liked videos"""
        data = await self._get('likes')
        if data:
            return data.get('items', [])[:limit]
        return []

    async def is_liked(self, video_id: str) -> bool:
        """Check if video is liked"""
        likes = await self.get_likes(1000)
        return any(like['video_id'] == video_id for like in likes)

    # Preferences methods
    async def set_preference(self, key: str, value: str) -> bool:
        """Set user preference"""
        prefs = await self.get_all_preferences()
        prefs[key] = value
        await self._set('preferences', prefs)
        return True

    async def get_preference(self, key: str) -> Optional[str]:
        """Get user preference"""
        prefs = await self.get_all_preferences()
        return prefs.get(key)

    async def get_all_preferences(self) -> Dict[str, str]:
        """Get all user preferences"""
        data = await self._get('preferences')
        return data if data else {}
