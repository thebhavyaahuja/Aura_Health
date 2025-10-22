#!/usr/bin/env python3
"""
Test script for Document Parsing Service
"""
import requests
import os
from pathlib import Path

# Service configuration
BASE_URL = "http://localhost:8002"
API_KEY = "demo-api-key-123"

def test_health():
    """Test health endpoint"""
    try:
        print("🏥 Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/health/")
        
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health check passed!")
            print(f"Status: {health_data['status']}")
            print(f"Database: {health_data['database']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")

def test_parse_document():
    """Test document parsing"""
    try:
        print("🔍 Testing document parsing...")
        
        # Create a test document (simple text file)
        test_file_path = Path("test_document.txt")
        test_content = """
        MAMMOGRAPHY REPORT
        
        Patient: Test Patient
        Date: 2024-01-15
        Indication: Routine screening
        
        Findings:
        - Dense glandular tissue
        - No suspicious masses
        - No calcifications
        
        Assessment: BIRADS 2
        Recommendation: Routine follow-up in 1 year
        """
        
        # Write test file
        test_file_path.write_text(test_content)
        
        # Test parsing request
        import uuid
        document_id = f"test-doc-{uuid.uuid4().hex[:8]}"
        payload = {
            "document_id": document_id,
            "file_path": str(test_file_path.absolute())
        }
        
        response = requests.post(
            f"{BASE_URL}/parsing/parse",
            json=payload,
            params={"api_key": API_KEY}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Document parsing successful!")
            print(f"Parsing ID: {result['parsing_id']}")
            print(f"Status: {result['status']}")
            print(f"Message: {result['message']}")
            
            # Test getting result
            parsing_id = result['parsing_id']
            print(f"\n📋 Getting parsing result for ID: {parsing_id}")
            
            result_response = requests.get(
                f"{BASE_URL}/parsing/result/{parsing_id}",
                params={"api_key": API_KEY}
            )
            
            if result_response.status_code == 200:
                result_data = result_response.json()
                print("✅ Result retrieved successfully!")
                print(f"Status: {result_data['status']}")
                print(f"Extracted text length: {len(result_data['extracted_text'])} characters")
                print(f"First 200 chars: {result_data['extracted_text'][:200]}...")
            else:
                print(f"❌ Failed to get result: {result_response.status_code}")
                print(result_response.text)
                
        else:
            print(f"❌ Parsing failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        
    finally:
        # Clean up test file
        if test_file_path.exists():
            test_file_path.unlink()
            print("🧹 Test file cleaned up")

def test_parse_nonexistent_file():
    """Test parsing with non-existent file"""
    try:
        print("🚫 Testing parsing with non-existent file...")
        
        import uuid
        document_id = f"test-doc-{uuid.uuid4().hex[:8]}"
        payload = {
            "document_id": document_id,
            "file_path": "/nonexistent/file.pdf"
        }
        
        response = requests.post(
            f"{BASE_URL}/parsing/parse",
            json=payload,
            params={"api_key": API_KEY}
        )
        
        if response.status_code == 404:
            print("✅ Correctly handled non-existent file!")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🧪 Testing Document Parsing Service")
    print("=" * 50)
    
    # Test health first
    test_health()
    print()
    
    # Test parsing
    test_parse_document()
    print()
    
    # Test error handling
    test_parse_nonexistent_file()
    
    print("\n🎉 Testing completed!")
