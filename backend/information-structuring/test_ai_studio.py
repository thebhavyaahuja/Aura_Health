#!/usr/bin/env python3
"""
Test Google AI Studio API (different from Google Cloud)
"""
import os
import httpx
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_ai_studio():
    """Test Google AI Studio API"""
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return
    
    print(f"🔑 API Key: {api_key[:10]}...")
    
    # Google AI Studio uses different endpoint
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    test_prompt = "Hello, how are you?"
    
    print(f"\n🧪 Testing Google AI Studio API")
    print(f"   URL: {url}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                params={"key": api_key},
                json={
                    "contents": [{
                        "parts": [{"text": test_prompt}]
                    }]
                },
                timeout=10.0
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and result["candidates"]:
                    content = result["candidates"][0]["content"]["parts"][0]["text"]
                    print(f"   ✅ SUCCESS! Response: {content[:50]}...")
                    print(f"   🎉 Use: gemini-pro with v1beta")
                    return "gemini-pro"
                else:
                    print(f"   ❌ No candidates in response")
            else:
                print(f"   ❌ Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
    
    return None

if __name__ == "__main__":
    result = asyncio.run(test_ai_studio())
    if result:
        print(f"\n✅ Working model found: {result}")
    else:
        print(f"\n❌ No working model found")
