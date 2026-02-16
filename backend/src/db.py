"""
Database Module
PostgreSQL database for storing playlists and user data (Neon)
"""

import asyncpg
import logging
from typing import List, Dict, Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_url: Optional[str] = None):
        if db_url is None:
            db_url = os.getenv('DATABASE_URL')
            if not db_url:
                # Default local SQLite for development
                import sqlite3
                from pathlib import Path
                db_path = Path.home() / ".local" / "share" / "youtube-music" / "database.db"
                db_path.parent.mkdir(parents=True, exist_ok=True)
                self.db_url = f"sqlite:///{db_path}"
                self.use_sqlite = True
            else:
                # Neon PostgreSQL
                if db_url.startswith('postgres://'):
                    db_url = db_url.replace('postgres://', 'postgresql://', 1)
                self.db_url = db_url
                self.use_sqlite = False
        else:
            self.db_url = db_url
            self.use_sqlite = 'sqlite' in db_url.lower()
        
        self.pool = None
        self.sqlite_conn = None

    async def init(self):
        """Initialize database connection and tables"""
        try:
            if self.use_sqlite:
                import sqlite3
                self.sqlite_conn = sqlite3.connect(self.db_url.replace('sqlite:///', ''))
                self.sqlite_conn.row_factory = sqlite3.Row
                self._create_sqlite_tables()
                logger.info("SQLite database initialized")
            else:
                self.pool = await asyncpg.create_pool(self.db_url, min_size=1, max_size=10)
                await self._create_postgres_tables()
                logger.info("PostgreSQL database initialized")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def _create_sqlite_tables(self):
        """Create SQLite tables"""
        cursor = self.sqlite_conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
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
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recently_played (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                title TEXT,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                title TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(video_id)
            )
        """)
        
        self.sqlite_conn.commit()

    async def _create_postgres_tables(self):
        """Create PostgreSQL tables"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS playlists (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS playlist_items (
                    id SERIAL PRIMARY KEY,
                    playlist_id INTEGER NOT NULL REFERENCES playlists(id) ON DELETE CASCADE,
                    video_id TEXT NOT NULL,
                    title TEXT,
                    duration INTEGER,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS recently_played (
                    id SERIAL PRIMARY KEY,
                    video_id TEXT NOT NULL,
                    title TEXT,
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id SERIAL PRIMARY KEY,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS likes (
                    id SERIAL PRIMARY KEY,
                    video_id TEXT NOT NULL UNIQUE,
                    title TEXT,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for better performance
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_playlist_items_playlist_id 
                ON playlist_items(playlist_id)
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_recently_played_played_at 
                ON recently_played(played_at DESC)
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_likes_video_id 
                ON likes(video_id)
            """)

    async def close(self):
        """Close database connection"""
        if self.use_sqlite:
            if self.sqlite_conn:
                self.sqlite_conn.close()
                logger.info("SQLite connection closed")
        else:
            if self.pool:
                await self.pool.close()
                logger.info("PostgreSQL pool closed")

    async def create_playlist(self, name: str) -> int:
        """Create new playlist"""
        if self.use_sqlite:
            cursor = self.sqlite_conn.cursor()
            cursor.execute("INSERT INTO playlists (name) VALUES (?)", (name,))
            self.sqlite_conn.commit()
            return cursor.lastrowid
        else:
            async with self.pool.acquire() as conn:
                return await conn.fetchval(
                    "INSERT INTO playlists (name) VALUES ($1) RETURNING id",
                    name
                )

    async def get_playlists(self) -> List[Dict]:
        """Get all playlists"""
        if self.use_sqlite:
            cursor = self.sqlite_conn.cursor()
            cursor.execute("""
                SELECT p.*, COUNT(pi.id) as item_count
                FROM playlists p
                LEFT JOIN playlist_items pi ON p.id = pi.playlist_id
                GROUP BY p.id
                ORDER BY p.created_at DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
        else:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT p.*, COUNT(pi.id) as item_count
                    FROM playlists p
                    LEFT JOIN playlist_items pi ON p.id = pi.playlist_id
                    GROUP BY p.id
                    ORDER BY p.created_at DESC
                """)
                return [dict(row) for row in rows]

    async def delete_playlist(self, playlist_id: int) -> bool:
        """Delete playlist"""
        if self.use_sqlite:
            cursor = self.sqlite_conn.cursor()
            cursor.execute("DELETE FROM playlists WHERE id = ?", (playlist_id,))
            self.sqlite_conn.commit()
            return cursor.rowcount > 0
        else:
            async with self.pool.acquire() as conn:
                result = await conn.execute("DELETE FROM playlists WHERE id = $1", playlist_id)
                return result == 'DELETE 1'

    async def add_to_playlist(self, playlist_id: int, video_id: str, title: str, duration: int = 0) -> bool:
        """Add video to playlist"""
        try:
            if self.use_sqlite:
                cursor = self.sqlite_conn.cursor()
                cursor.execute("""
                    INSERT INTO playlist_items (playlist_id, video_id, title, duration)
                    VALUES (?, ?, ?, ?)
                """, (playlist_id, video_id, title, duration))
                cursor.execute("""
                    UPDATE playlists SET updated_at = CURRENT_TIMESTAMP WHERE id = ?
                """, (playlist_id,))
                self.sqlite_conn.commit()
                return True
            else:
                async with self.pool.acquire() as conn:
                    await conn.execute("""
                        INSERT INTO playlist_items (playlist_id, video_id, title, duration)
                        VALUES ($1, $2, $3, $4)
                    """, playlist_id, video_id, title, duration)
                    await conn.execute("""
                        UPDATE playlists SET updated_at = CURRENT_TIMESTAMP WHERE id = $1
                    """, playlist_id)
                    return True
        except Exception as e:
            logger.error(f"Failed to add to playlist: {e}")
            return False

    async def remove_from_playlist(self, playlist_id: int, video_id: str) -> bool:
        """Remove video from playlist"""
        try:
            if self.use_sqlite:
                cursor = self.sqlite_conn.cursor()
                cursor.execute("""
                    DELETE FROM playlist_items WHERE playlist_id = ? AND video_id = ?
                """, (playlist_id, video_id))
                cursor.execute("""
                    UPDATE playlists SET updated_at = CURRENT_TIMESTAMP WHERE id = ?
                """, (playlist_id,))
                self.sqlite_conn.commit()
                return cursor.rowcount > 0
            else:
                async with self.pool.acquire() as conn:
                    await conn.execute("""
                        DELETE FROM playlist_items WHERE playlist_id = $1 AND video_id = $2
                    """, playlist_id, video_id)
                    await conn.execute("""
                        UPDATE playlists SET updated_at = CURRENT_TIMESTAMP WHERE id = $1
                    """, playlist_id)
                    return True
        except Exception as e:
            logger.error(f"Failed to remove from playlist: {e}")
            return False

    async def get_playlist_items(self, playlist_id: int) -> List[Dict]:
        """Get items in playlist"""
        if self.use_sqlite:
            cursor = self.sqlite_conn.cursor()
            cursor.execute("""
                SELECT * FROM playlist_items WHERE playlist_id = ? ORDER BY added_at ASC
            """, (playlist_id,))
            return [dict(row) for row in cursor.fetchall()]
        else:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT * FROM playlist_items WHERE playlist_id = $1 ORDER BY added_at ASC
                """, playlist_id)
                return [dict(row) for row in rows]

    async def add_recently_played(self, video_id: str, title: str) -> bool:
        """Add to recently played"""
        try:
            if self.use_sqlite:
                cursor = self.sqlite_conn.cursor()
                # Remove old entries (keep last 100)
                cursor.execute("""
                    DELETE FROM recently_played
                    WHERE id IN (
                        SELECT id FROM recently_played
                        ORDER BY played_at DESC
                        LIMIT -1 OFFSET 100
                    )
                """)
                cursor.execute("""
                    INSERT INTO recently_played (video_id, title) VALUES (?, ?)
                """, (video_id, title))
                self.sqlite_conn.commit()
                return True
            else:
                async with self.pool.acquire() as conn:
                    # Remove old entries (keep last 100)
                    await conn.execute("""
                        DELETE FROM recently_played
                        WHERE id NOT IN (
                            SELECT id FROM recently_played
                            ORDER BY played_at DESC
                            LIMIT 100
                        )
                    """)
                    await conn.execute("""
                        INSERT INTO recently_played (video_id, title) VALUES ($1, $2)
                    """, video_id, title)
                    return True
        except Exception as e:
            logger.error(f"Failed to add recently played: {e}")
            return False

    async def get_recently_played(self, limit: int = 20) -> List[Dict]:
        """Get recently played items"""
        if self.use_sqlite:
            cursor = self.sqlite_conn.cursor()
            cursor.execute("""
                SELECT * FROM recently_played ORDER BY played_at DESC LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
        else:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT * FROM recently_played ORDER BY played_at DESC LIMIT $1
                """, limit)
                return [dict(row) for row in rows]

    async def add_like(self, video_id: str, title: str) -> bool:
        """Add video to likes/favorites"""
        try:
            if self.use_sqlite:
                cursor = self.sqlite_conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO likes (video_id, title) VALUES (?, ?)
                """, (video_id, title))
                self.sqlite_conn.commit()
                return cursor.rowcount > 0
            else:
                async with self.pool.acquire() as conn:
                    await conn.execute("""
                        INSERT INTO likes (video_id, title) VALUES ($1, $2)
                        ON CONFLICT (video_id) DO NOTHING
                    """, video_id, title)
                    return True
        except Exception as e:
            logger.error(f"Failed to add like: {e}")
            return False

    async def remove_like(self, video_id: str) -> bool:
        """Remove video from likes/favorites"""
        try:
            if self.use_sqlite:
                cursor = self.sqlite_conn.cursor()
                cursor.execute("DELETE FROM likes WHERE video_id = ?", (video_id,))
                self.sqlite_conn.commit()
                return cursor.rowcount > 0
            else:
                async with self.pool.acquire() as conn:
                    await conn.execute("DELETE FROM likes WHERE video_id = $1", video_id)
                    return True
        except Exception as e:
            logger.error(f"Failed to remove like: {e}")
            return False

    async def get_likes(self, limit: int = 100) -> List[Dict]:
        """Get liked videos"""
        if self.use_sqlite:
            cursor = self.sqlite_conn.cursor()
            cursor.execute("""
                SELECT * FROM likes ORDER BY added_at DESC LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
        else:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT * FROM likes ORDER BY added_at DESC LIMIT $1
                """, limit)
                return [dict(row) for row in rows]

    async def is_liked(self, video_id: str) -> bool:
        """Check if video is liked"""
        if self.use_sqlite:
            cursor = self.sqlite_conn.cursor()
            cursor.execute("SELECT 1 FROM likes WHERE video_id = ?", (video_id,))
            return cursor.fetchone() is not None
        else:
            async with self.pool.acquire() as conn:
                result = await conn.fetchval("SELECT 1 FROM likes WHERE video_id = $1", video_id)
                return result is not None

    async def set_preference(self, key: str, value: str) -> bool:
        """Set user preference"""
        try:
            if self.use_sqlite:
                cursor = self.sqlite_conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO user_preferences (key, value, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (key, value))
                self.sqlite_conn.commit()
                return True
            else:
                async with self.pool.acquire() as conn:
                    await conn.execute("""
                        INSERT INTO user_preferences (key, value, updated_at)
                        VALUES ($1, $2, CURRENT_TIMESTAMP)
                        ON CONFLICT (key) DO UPDATE SET value = $2, updated_at = CURRENT_TIMESTAMP
                    """, key, value)
                    return True
        except Exception as e:
            logger.error(f"Failed to set preference: {e}")
            return False

    async def get_preference(self, key: str) -> Optional[str]:
        """Get user preference"""
        if self.use_sqlite:
            cursor = self.sqlite_conn.cursor()
            cursor.execute("SELECT value FROM user_preferences WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row['value'] if row else None
        else:
            async with self.pool.acquire() as conn:
                return await conn.fetchval("SELECT value FROM user_preferences WHERE key = $1", key)

    async def get_all_preferences(self) -> Dict[str, str]:
        """Get all user preferences"""
        if self.use_sqlite:
            cursor = self.sqlite_conn.cursor()
            cursor.execute("SELECT key, value FROM user_preferences")
            return {row['key']: row['value'] for row in cursor.fetchall()}
        else:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch("SELECT key, value FROM user_preferences")
                return {row['key']: row['value'] for row in rows}
