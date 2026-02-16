"""
Vercel Serverless API Handler
Entry point for YouTube Music Proxy backend on Vercel
"""

import sys
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add backend/src to path  
backend_path = os.path.join(os.path.dirname(__file__), 'backend', 'src')
if os.path.exists(backend_path) and backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import the simplified FastAPI app
try:
    from main import app
    logger.info("Successfully imported main app")
except Exception as e:
    logger.error(f"Failed to import main: {e}")
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {"error": str(e), "status": "error"}
    
    @app.get("/api/search")
    async def search():
        return {"results": [], "error": "Backend not loaded"}
