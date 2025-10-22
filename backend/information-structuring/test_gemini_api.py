#!/usr/bin/env python3
"""
Test Gemini API directly to verify the correct endpoint
"""
import os
import httpx
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_gemini_api():
    """Test Gemini API with different model names"""
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return
    
    print(f"🔑 API Key: {api_key[:10]}...")
    
    # Test different API versions and model names
    api_versions = ["v1beta", "v1"]
    models_to_test = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-001", 
        "gemini-1.5-pro",
        "gemini-1.5-pro-001",
        "gemini-pro",
        "gemini-1.0-pro"
    ]
    
    test_prompt = "Hello, how are you?"
    
    async with httpx.AsyncClient() as client:
        for api_version in api_versions:
            for model in models_to_test:
                url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model}:generateContent"
            
                print(f"\n🧪 Testing {api_version} - {model}")
                print(f"   URL: {url}")
            
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
                            print(f"   🎉 Use this model: {model} with {api_version}")
                            return f"{api_version}/{model}"
                        else:
                            print(f"   ❌ No candidates in response")
                    else:
                        print(f"   ❌ Error: {response.text[:100]}...")
                        
                except Exception as e:
                    print(f"   ❌ Exception: {str(e)}")
    
    print("\n❌ No working model found")
    return None

if __name__ == "__main__":
    asyncio.run(test_gemini_api())
