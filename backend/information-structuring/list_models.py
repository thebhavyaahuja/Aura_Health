#!/usr/bin/env python3
"""
List available Gemini models
"""
import os
import httpx
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def list_models():
    """List available Gemini models"""
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return
    
    print(f"🔑 API Key: {api_key[:10]}...")
    
    # List models endpoint
    url = "https://generativelanguage.googleapis.com/v1beta/models"
    
    print(f"\n🧪 Listing available models")
    print(f"   URL: {url}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                params={"key": api_key},
                timeout=10.0
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if "models" in result:
                    print(f"   ✅ Found {len(result['models'])} models:")
                    for model in result["models"]:
                        name = model.get("name", "unknown")
                        display_name = model.get("displayName", "unknown")
                        supported_methods = model.get("supportedGenerationMethods", [])
                        print(f"      - {name}")
                        print(f"        Display: {display_name}")
                        print(f"        Methods: {supported_methods}")
                        print()
                else:
                    print(f"   ❌ No models in response")
                    print(f"   Response: {result}")
            else:
                print(f"   ❌ Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")

if __name__ == "__main__":
    asyncio.run(list_models())
