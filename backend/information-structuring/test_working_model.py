#!/usr/bin/env python3
"""
Test the working Gemini model
"""
import os
import httpx
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_working_model():
    """Test the working Gemini model"""
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return
    
    print(f"🔑 API Key: {api_key[:10]}...")
    
    # Use the working model
    model = "gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    test_prompt = "Extract the following information from this text and return as JSON: 'Patient: John Doe, Age: 45, Diagnosis: Healthy'. Return only JSON."
    
    print(f"\n🧪 Testing {model}")
    print(f"   URL: {url}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                params={"key": api_key},
                json={
                    "contents": [{
                        "parts": [{"text": test_prompt}]
                    }],
                    "generationConfig": {
                        "temperature": 0.1,
                        "topK": 1,
                        "topP": 0.8,
                        "maxOutputTokens": 2048,
                    }
                },
                timeout=30.0
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and result["candidates"]:
                    content = result["candidates"][0]["content"]["parts"][0]["text"]
                    print(f"   ✅ SUCCESS! Response: {content}")
                    print(f"   🎉 Model {model} is working!")
                    return True
                else:
                    print(f"   ❌ No candidates in response")
            else:
                print(f"   ❌ Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
    
    return False

if __name__ == "__main__":
    success = asyncio.run(test_working_model())
    if success:
        print(f"\n✅ Model is working! You can now test the pipeline.")
    else:
        print(f"\n❌ Model test failed.")
