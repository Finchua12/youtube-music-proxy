"""
Authentication Module
Handles YouTube OAuth2 authentication and user sessions
"""

import os
import logging
import secrets
import time
import json
from typing import Optional, Dict
from pathlib import Path
import httpx

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

        # Load client credentials
        self.client_id = os.getenv('YOUTUBE_CLIENT_ID', 'YOUR_CLIENT_ID')
        self.client_secret = os.getenv('YOUTUBE_CLIENT_SECRET', 'YOUR_CLIENT_SECRET')
        self.redirect_uri = os.getenv('YOUTUBE_REDIRECT_URI', 'http://localhost:8000/callback')

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

        return time.time() < expires_at

    def get_auth_url(self) -> str:
        """Get YouTube OAuth2 authorization URL"""
        state_token = self.generate_state_token()

        # Save state token for verification later
        self.save_session({'state_token': state_token})

        # Google OAuth2 authorization URL
        auth_url = (
            f"https://accounts.google.com/o/oauth2/auth?"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.redirect_uri}&"
            f"scope=https://www.googleapis.com/auth/youtube.readonly "
            f"https://www.googleapis.com/auth/youtubepartner&"
            f"response_type=code&"
            f"state={state_token}&"
            f"access_type=offline&"
            f"prompt=consent"
        )

        return auth_url

    async def handle_callback(self, code: str, state: str) -> Dict:
        """Handle OAuth2 callback and exchange code for tokens"""
        # Verify state token
        session = self.load_session()
        if not session or session.get('state_token') != state:
            logger.error("Invalid state token")
            raise ValueError("Invalid state token")

        # Exchange code for tokens
        try:
            token_url = "https://oauth2.googleapis.com/token"

            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=data)
                response.raise_for_status()
                token_data = response.json()

            # Save credentials
            credentials = {
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            self.save_credentials(credentials)

            # Save session with tokens
            session_data = {
                'access_token': token_data['access_token'],
                'refresh_token': token_data.get('refresh_token'),
                'expires_at': time.time() + token_data['expires_in'],
                'token_type': token_data['token_type']
            }
            self.save_session(session_data)

            logger.info("Authentication successful")
            return session_data

        except httpx.HTTPStatusError as e:
            logger.error(f"Authentication failed with HTTP error: {e}")
            raise ValueError(f"Authentication failed: {e.response.text}")
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise ValueError(f"Authentication failed: {str(e)}")

    async def refresh_access_token(self) -> Optional[Dict]:
        """Refresh access token using refresh token"""
        session = self.load_session()
        if not session:
            return None

        refresh_token = session.get('refresh_token')
        if not refresh_token:
            return None

        try:
            token_url = "https://oauth2.googleapis.com/token"

            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=data)
                response.raise_for_status()
                token_data = response.json()

            # Update session with new access token
            session_data = {
                'access_token': token_data['access_token'],
                'refresh_token': refresh_token,  # Keep the same refresh token
                'expires_at': time.time() + token_data['expires_in'],
                'token_type': token_data['token_type']
            }
            self.save_session(session_data)

            logger.info("Access token refreshed successfully")
            return session_data

        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            return None

    def get_access_token(self) -> Optional[str]:
        """Get current access token if available and valid"""
        if self.is_authenticated():
            session = self.load_session()
            return session.get('access_token') if session else None
        return None