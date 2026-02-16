"""
Vercel Serverless API Handler
Entry point for YouTube Music Proxy backend on Vercel
"""

import sys
import os

# Add backend/src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))

from main import app

# Vercel handler
from fastapi import Request
from fastapi.responses import JSONResponse

async def handler(request: Request):
    """Handle Vercel serverless requests"""
    try:
        # Process the request through FastAPI
        response = await app(request.scope, request.receive, request.send)
        return response
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

# For Vercel Python runtime
def vercel_handler(request, context):
    """Vercel serverless function handler"""
    import asyncio
    return asyncio.run(handler(request))
