"""
Vercel Serverless API Handler
Entry point for YouTube Music Proxy backend on Vercel
"""

import sys
import os

# Add backend/src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))

# Import FastAPI app
from main import app

# Export the app for Vercel
# Vercel expects an 'app' variable for ASGI applications
