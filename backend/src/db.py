"""
Database Module
SQLite database for storing playlists and user data
"""

import sqlite3
import logging
import asyncio
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = Path.home() / ".local" / "share" / "youtube-music" / "database.db"

        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None

    async def init(self):
        """Initialize database connection and tables"""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row

            # Create tables
            self._create_tables()

            logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def _create_tables(self):
        """Create database tables"""
        cursor = self.connection.cursor()

        # Playlists table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Playlist items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlist_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                playlist_id INTEGER NOT NULL,
                video_id TEXT NOT NULL,
                title TEXT,
                duration INTEGER,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE
            )
        """)

        # Recently played
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recently_played (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                title TEXT,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # User preferences
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Likes/Favorites
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                title TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(video_id)
            )
        """)

        self.connection.commit()

    async def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

    async def create_playlist(self, name: str) -> int:
        """Create new playlist"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO playlists (name) VALUES (?)",
                (name,)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to create playlist: {e}")
            raise

    async def get_playlists(self) -> List[Dict]:
        """Get all playlists"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT p.*, COUNT(pi.id) as item_count
                FROM playlists p
                LEFT JOIN playlist_items pi ON p.id = pi.playlist_id
                GROUP BY p.id
                ORDER BY p.created_at DESC
            """)

            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get playlists: {e}")
            return []

    async def delete_playlist(self, playlist_id: int) -> bool:
        """Delete playlist"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM playlists WHERE id = ?", (playlist_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to delete playlist: {e}")
            return False

    async def add_to_playlist(self, playlist_id: int, video_id: str, title: str, duration: int) -> bool:
        """Add video to playlist"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO playlist_items (playlist_id, video_id, title, duration)
                VALUES (?, ?, ?, ?)
            """, (playlist_id, video_id, title, duration))

            # Update playlist timestamp
            cursor.execute("""
                UPDATE playlists SET updated_at = CURRENT_TIMESTAMP WHERE id = ?
            """, (playlist_id,))

            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add to playlist: {e}")
            return False

    async def remove_from_playlist(self, playlist_id: int, video_id: str) -> bool:
        """Remove video from playlist"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                DELETE FROM playlist_items
                WHERE playlist_id = ? AND video_id = ?
            """, (playlist_id, video_id))

            # Update playlist timestamp
            cursor.execute("""
                UPDATE playlists SET updated_at = CURRENT_TIMESTAMP WHERE id = ?
            """, (playlist_id,))

            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to remove from playlist: {e}")
            return False

    async def get_playlist_items(self, playlist_id: int) -> List[Dict]:
        """Get items in playlist"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM playlist_items
                WHERE playlist_id = ?
                ORDER BY added_at ASC
            """, (playlist_id,))

            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get playlist items: {e}")
            return []

    async def add_recently_played(self, video_id: str, title: str) -> bool:
        """Add to recently played"""
        try:
            cursor = self.connection.cursor()

            # Remove old entries (keep last 100)
            cursor.execute("""
                DELETE FROM recently_played
                WHERE id IN (
                    SELECT id FROM recently_played
                    ORDER BY played_at DESC
                    LIMIT -1 OFFSET 100
                )
            """)

            # Add new entry
            cursor.execute("""
                INSERT INTO recently_played (video_id, title)
                VALUES (?, ?)
            """, (video_id, title))

            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add recently played: {e}")
            return False

    async def get_recently_played(self, limit: int = 20) -> List[Dict]:
        """Get recently played items"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM recently_played
                ORDER BY played_at DESC
                LIMIT ?
            """, (limit,))

            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get recently played: {e}")
            return []

    async def add_like(self, video_id: str, title: str) -> bool:
        """Add video to likes/favorites"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO likes (video_id, title)
                VALUES (?, ?)
            """, (video_id, title))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to add like: {e}")
            return False

    async def remove_like(self, video_id: str) -> bool:
        """Remove video from likes/favorites"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM likes WHERE video_id = ?", (video_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to remove like: {e}")
            return False

    async def get_likes(self, limit: int = 100) -> List[Dict]:
        """Get liked videos"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM likes
                ORDER BY added_at DESC
                LIMIT ?
            """, (limit,))

            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get likes: {e}")
            return []

    async def is_liked(self, video_id: str) -> bool:
        """Check if video is liked"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1 FROM likes WHERE video_id = ?", (video_id,))
            return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Failed to check if liked: {e}")
            return False

    async def set_preference(self, key: str, value: str) -> bool:
        """Set user preference"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO user_preferences (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (key, value))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to set preference: {e}")
            return False

    async def get_preference(self, key: str) -> Optional[str]:
        """Get user preference"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT value FROM user_preferences WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row['value'] if row else None
        except Exception as e:
            logger.error(f"Failed to get preference: {e}")
            return None

    async def get_all_preferences(self) -> Dict[str, str]:
        """Get all user preferences"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT key, value FROM user_preferences")
            return {row['key']: row['value'] for row in cursor.fetchall()}
        except Exception as e:
            logger.error(f"Failed to get preferences: {e}")
            return {}