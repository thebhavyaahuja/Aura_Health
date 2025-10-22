#!/usr/bin/env python3
"""
Run script for Information Structuring Service
"""
import os
import uvicorn
from app.config import HOST, PORT

if __name__ == "__main__":
    print("🚀 Starting Information Structuring Service...")
    print(f"   Host: {HOST}")
    print(f"   Port: {PORT}")
    print(f"   Gemini API Key: {'✅ Configured' if os.getenv('GEMINI_API_KEY') else '❌ Not configured'}")
    
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )
