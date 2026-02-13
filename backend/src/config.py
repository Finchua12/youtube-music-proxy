"""
Configuration Management
Handles application configuration and settings
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages application configuration"""

    def __init__(self, config_dir: Optional[Path] = None):
        if config_dir is None:
            config_dir = Path.home() / ".config" / "youtube-music"

        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "cache_dir": "~/.cache/youtube-music",
            "max_cache_size_gb": 5,
            "audio_quality": "192k",
            "auto_cleanup": True,
            "download_format": "mp3",
            "max_download_threads": 3,
            "proxy_enabled": False,
            "proxy_url": "",
            "theme": "dark",
            "language": "uk",
            "auto_update": True,
            "notifications": True,
            "minimize_to_tray": True,
            "start_minimized": False
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                    # Merge with default config to ensure all keys are present
                    default_config.update(file_config)
                    logger.info("Configuration loaded successfully")
                    return default_config
            except Exception as e:
                logger.error(f"Failed to load config file: {e}")
                return default_config
        else:
            # Create default config file
            self._save_config(default_config)
            return default_config

    def _save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            logger.info("Configuration saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save config file: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> bool:
        """Set configuration value"""
        self.config[key] = value
        return self._save_config(self.config)

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values"""
        return self.config.copy()

    def reset_to_default(self) -> bool:
        """Reset configuration to default values"""
        default_config = {
            "cache_dir": "~/.cache/youtube-music",
            "max_cache_size_gb": 5,
            "audio_quality": "192k",
            "auto_cleanup": True,
            "download_format": "mp3",
            "max_download_threads": 3,
            "proxy_enabled": False,
            "proxy_url": "",
            "theme": "dark",
            "language": "uk",
            "auto_update": True,
            "notifications": True,
            "minimize_to_tray": True,
            "start_minimized": False
        }

        self.config = default_config
        return self._save_config(default_config)

    def get_cache_dir(self) -> Path:
        """Get cache directory path"""
        cache_dir = self.config.get("cache_dir", "~/.cache/youtube-music")
        return Path(os.path.expanduser(cache_dir))

    def get_max_cache_size(self) -> int:
        """Get maximum cache size in bytes"""
        gb = self.config.get("max_cache_size_gb", 5)
        return int(gb * 1024 * 1024 * 1024)

    def get_audio_quality(self) -> str:
        """Get audio quality setting"""
        return self.config.get("audio_quality", "192k")

    def is_auto_cleanup_enabled(self) -> bool:
        """Check if auto cleanup is enabled"""
        return self.config.get("auto_cleanup", True)

    def get_download_format(self) -> str:
        """Get download format"""
        return self.config.get("download_format", "mp3")

    def get_max_download_threads(self) -> int:
        """Get maximum download threads"""
        return self.config.get("max_download_threads", 3)

    def is_proxy_enabled(self) -> bool:
        """Check if proxy is enabled"""
        return self.config.get("proxy_enabled", False)

    def get_proxy_url(self) -> str:
        """Get proxy URL"""
        return self.config.get("proxy_url", "")

    def get_theme(self) -> str:
        """Get theme setting"""
        return self.config.get("theme", "dark")

    def get_language(self) -> str:
        """Get language setting"""
        return self.config.get("language", "uk")

    def is_auto_update_enabled(self) -> bool:
        """Check if auto update is enabled"""
        return self.config.get("auto_update", True)

    def are_notifications_enabled(self) -> bool:
        """Check if notifications are enabled"""
        return self.config.get("notifications", True)

    def should_minimize_to_tray(self) -> bool:
        """Check if should minimize to tray"""
        return self.config.get("minimize_to_tray", True)

    def should_start_minimized(self) -> bool:
        """Check if should start minimized"""
        return self.config.get("start_minimized", False)