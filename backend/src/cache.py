"""
Audio Cache Management
Handles caching and cleanup of downloaded audio files
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class AudioCache:
    def __init__(self, cache_dir: Path, max_size_gb: float = 5.0):
        self.cache_dir = cache_dir
        self.max_size_bytes = int(max_size_gb * 1024 * 1024 * 1024)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_cached_file(self, video_id: str, quality: str) -> Optional[Path]:
        """Get path to cached audio file"""
        filename = f"{video_id}_{quality}.mp3"
        file_path = self.cache_dir / filename

        if file_path.exists():
            return file_path
        return None

    def get_cache_size(self) -> int:
        """Get total cache size in bytes"""
        total_size = 0
        for file_path in self.cache_dir.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size

    def cleanup_old_files(self) -> int:
        """Clean up old files to maintain size limit"""
        try:
            cache_size = self.get_cache_size()

            if cache_size <= self.max_size_bytes:
                return 0

            # Get all files with their modification times
            files = []
            for file_path in self.cache_dir.rglob("*"):
                if file_path.is_file():
                    files.append((file_path, file_path.stat().st_mtime))

            # Sort by oldest first
            files.sort(key=lambda x: x[1])

            # Delete oldest files until under limit
            deleted_count = 0
            for file_path, _ in files:
                if self.get_cache_size() <= self.max_size_bytes:
                    break

                try:
                    file_path.unlink()
                    deleted_count += 1
                    logger.info(f"Deleted old cache file: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to delete {file_path}: {e}")

            return deleted_count

        except Exception as e:
            logger.error(f"Cache cleanup failed: {e}")
            return 0

    def clear_cache(self) -> bool:
        """Clear entire cache"""
        try:
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
                self.cache_dir.mkdir(parents=True, exist_ok=True)
                logger.info("Cache cleared")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
            return False

    def get_cache_stats(self) -> Dict[str, any]:
        """Get cache statistics"""
        try:
            cache_size = self.get_cache_size()
            file_count = len(list(self.cache_dir.rglob("*")))

            return {
                "size_bytes": cache_size,
                "size_gb": round(cache_size / (1024**3), 2),
                "max_size_gb": self.max_size_bytes / (1024**3),
                "file_count": file_count,
                "directory": str(self.cache_dir)
            }
        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            return {}