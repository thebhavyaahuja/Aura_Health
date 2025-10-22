#!/usr/bin/env python3
"""
Quick configuration check for Information Structuring Service
"""
import os
from pathlib import Path

def check_config():
    """Check if the service is properly configured"""
    print("🔍 Information Structuring Service Configuration Check")
    print("=" * 60)
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
        
        # Read .env file
        with open(env_file, 'r') as f:
            env_content = f.read()
        
        # Check for GEMINI_API_KEY
        if "GEMINI_API_KEY" in env_content:
            lines = env_content.split('\n')
            for line in lines:
                if line.startswith("GEMINI_API_KEY"):
                    if "your_gemini_api_key_here" in line or line.split('=')[1].strip() == "":
                        print("❌ GEMINI_API_KEY is not set (still has placeholder)")
                        print("   💡 Please set your actual Gemini API key in .env file")
                        return False
                    else:
                        print("✅ GEMINI_API_KEY is configured")
                        return True
        else:
            print("❌ GEMINI_API_KEY not found in .env file")
            print("   💡 Please add GEMINI_API_KEY=your_actual_key to .env file")
            return False
    else:
        print("❌ .env file not found")
        print("   💡 Please create .env file with GEMINI_API_KEY")
        return False

def show_setup_instructions():
    """Show setup instructions"""
    print("\n📋 Setup Instructions:")
    print("1. Get Gemini API key from: https://makersuite.google.com/app/apikey")
    print("2. Create .env file in backend/information-structuring/")
    print("3. Add: GEMINI_API_KEY=your_actual_api_key_here")
    print("4. Run: python3 test_pipeline.py")

if __name__ == "__main__":
    is_configured = check_config()
    
    if not is_configured:
        show_setup_instructions()
    else:
        print("\n🎉 Configuration looks good!")
        print("You can now run: python3 test_pipeline.py")
