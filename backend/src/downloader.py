"""
YouTube Downloader Module
Handles downloading and searching YouTube videos using yt-dlp
"""

import asyncio
import logging
from typing import List, Dict, Optional
from pathlib import Path
import yt_dlp

logger = logging.getLogger(__name__)

class YouTubeDownloader:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    async def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search YouTube videos"""
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'extract_flat': 'in_playlist',
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_query = f"ytsearch{max_results}:{query}"
                result = ydl.extract_info(search_query, download=False)

                if 'entries' in result:
                    videos = []
                    for entry in result['entries']:
                        if entry and '_type' not in entry:
                            videos.append({
                                'id': entry.get('id'),
                                'title': entry.get('title'),
                                'duration': entry.get('duration'),
                                'uploader': entry.get('uploader'),
                                'thumbnail': entry.get('thumbnail'),
                                'view_count': entry.get('view_count'),
                                'upload_date': entry.get('upload_date'),
                            })
                    return videos

                return []
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    async def download_audio(self, video_id: str, quality: str = "192k") -> Optional[Path]:
        """Download audio from YouTube video"""
        try:
            output_path = self.cache_dir / f"{video_id}_{quality}.mp3"

            if output_path.exists():
                logger.info(f"Audio already downloaded: {video_id}")
                return output_path

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(output_path.with_suffix('')),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality.replace('k', ''),
                }],
                'postprocessor_args': [
                    '-ar', '44100'
                ],
                'prefer_ffmpeg': True,
                'keepvideo': False,
                'quiet': True,
                'no_warnings': True,
            }

            url = f"https://www.youtube.com/watch?v={video_id}"

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if output_path.exists():
                logger.info(f"Downloaded audio: {video_id}")
                return output_path
            else:
                logger.error(f"Failed to download audio: {video_id}")
                return None

        except Exception as e:
            logger.error(f"Download failed for {video_id}: {e}")
            return None

    async def get_video_info(self, video_id: str) -> Optional[Dict]:
        """Get detailed video information"""
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
            }

            url = f"https://www.youtube.com/watch?v={video_id}"

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'id': info.get('id'),
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader'),
                    'thumbnail': info.get('thumbnail'),
                    'view_count': info.get('view_count'),
                    'upload_date': info.get('upload_date'),
                    'description': info.get('description'),
                }
        except Exception as e:
            logger.error(f"Failed to get video info for {video_id}: {e}")
            return None