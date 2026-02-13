"""
Authentication Module
Handles YouTube OAuth2 authentication and user sessions
"""

import os
import logging
import secrets
from typing import Optional, Dict
from pathlib import Path
import json

logger = logging.getLogger(__name__)

class AuthManager:
    """Manages user authentication and sessions"""

    def __init__(self, config_dir: Optional[Path] = None):
        if config_dir is None:
            config_dir = Path.home() / ".config" / "youtube-music"

        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.session_file = self.config_dir / "session.json"
        self.credentials_file = self.config_dir / "credentials.json"

    def generate_state_token(self) -> str:
        """Generate a secure state token for OAuth2 flow"""
        return secrets.token_urlsafe(32)

    def save_session(self, session_data: Dict) -> bool:
        """Save user session data"""
        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            logger.info("Session saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
            return False

    def load_session(self) -> Optional[Dict]:
        """Load user session data"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            return None

    def clear_session(self) -> bool:
        """Clear user session data"""
        try:
            if self.session_file.exists():
                self.session_file.unlink()
                logger.info("Session cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear session: {e}")
            return False

    def save_credentials(self, credentials: Dict) -> bool:
        """Save OAuth2 credentials"""
        try:
            with open(self.credentials_file, 'w') as f:
                json.dump(credentials, f, indent=2)
            logger.info("Credentials saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save credentials: {e}")
            return False

    def load_credentials(self) -> Optional[Dict]:
        """Load OAuth2 credentials"""
        try:
            if self.credentials_file.exists():
                with open(self.credentials_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Failed to load credentials: {e}")
            return None

    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        session = self.load_session()
        if not session:
            return False

        # Check if access token exists and is not expired
        access_token = session.get('access_token')
        expires_at = session.get('expires_at')

        if not access_token or not expires_at:
            return False

        import time
        return time.time() < expires_at

    def get_auth_url(self) -> str:
        """Get YouTube OAuth2 authorization URL"""
        # This is a placeholder - in a real implementation, you would integrate
        # with Google's OAuth2 API
        state_token = self.generate_state_token()

        # Save state token for verification later
        self.save_session({'state_token': state_token})

        # Placeholder URL - in real implementation, use Google's OAuth2 endpoint
        auth_url = (
            f"https://accounts.google.com/o/oauth2/auth?"
            f"client_id=YOUR_CLIENT_ID&"
            f"redirect_uri=http://localhost:8000/callback&"
            f"scope=https://www.googleapis.com/auth/youtube.readonly&"
            f"response_type=code&"
            f"state={state_token}&"
            f"access_type=offline"
        )

        return auth_url

    def handle_callback(self, code: str, state: str) -> bool:
        """Handle OAuth2 callback and exchange code for tokens"""
        # Verify state token
        session = self.load_session()
        if not session or session.get('state_token') != state:
            logger.error("Invalid state token")
            return False

        # Exchange code for tokens (placeholder)
        # In real implementation, you would make a POST request to Google's token endpoint
        try:
            # Placeholder for token exchange
            access_token = "placeholder_access_token"
            refresh_token = "placeholder_refresh_token"

            # Save credentials
            credentials = {
                'client_id': 'YOUR_CLIENT_ID',
                'client_secret': 'YOUR_CLIENT_SECRET'
            }
            self.save_credentials(credentials)

            # Save session with tokens
            import time
            session_data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_at': time.time() + 3600,  # 1 hour
                'token_type': 'Bearer'
            }
            self.save_session(session_data)

            logger.info("Authentication successful")
            return True

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False