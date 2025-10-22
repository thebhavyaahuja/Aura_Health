#!/usr/bin/env python3
"""
Debug environment variable loading
"""
import os
from pathlib import Path

def debug_env():
    """Debug environment variable loading"""
    print("🔍 Environment Variable Debug")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    print(f"📁 .env file exists: {env_file.exists()}")
    
    if env_file.exists():
        print(f"📄 .env file contents:")
        with open(env_file, 'r') as f:
            content = f.read()
            print(content)
    
    # Check environment variables
    print(f"\n🔑 Environment Variables:")
    print(f"GEMINI_API_KEY from os.getenv(): {os.getenv('GEMINI_API_KEY', 'NOT_SET')}")
    print(f"GEMINI_API_KEY length: {len(os.getenv('GEMINI_API_KEY', ''))}")
    
    # Try loading with python-dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print(f"\n🔄 After load_dotenv():")
        print(f"GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY', 'NOT_SET')}")
        print(f"GEMINI_API_KEY length: {len(os.getenv('GEMINI_API_KEY', ''))}")
    except ImportError:
        print("❌ python-dotenv not installed")
    
    # Check app config
    try:
        from app.config import GEMINI_API_KEY
        print(f"\n⚙️  From app.config:")
        print(f"GEMINI_API_KEY: {GEMINI_API_KEY}")
        print(f"GEMINI_API_KEY length: {len(GEMINI_API_KEY) if GEMINI_API_KEY else 0}")
    except Exception as e:
        print(f"❌ Error importing app.config: {e}")

if __name__ == "__main__":
    debug_env()
