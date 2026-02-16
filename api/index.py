"""
Vercel Serverless API Handler
Entry point for YouTube Music Proxy backend on Vercel
"""

import sys
import os

# Add backend/src to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'src')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import the simplified FastAPI app
from main import app

# For Vercel serverless functions
from mangum import Mangum

# Create handler for Vercel
handler = Mangum(app, lifespan="off")

# Export for Vercel
app = app
