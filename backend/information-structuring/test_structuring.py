#!/usr/bin/env python3
"""
Test suite for Information Structuring Service
"""
import requests
import uuid
import json
from pathlib import Path

# Service configuration
STRUCTURING_URL = "http://localhost:8003"
API_KEY = "demo-api-key-123"

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    
    try:
        response = requests.get(f"{STRUCTURING_URL}/health/")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed")
            print(f"   Status: {health_data['status']}")
            print(f"   Database: {health_data['database']}")
            print(f"   Gemini API: {health_data['gemini_api']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_structuring_with_sample_text():
    """Test structuring with sample mammography report text"""
    print("\n🔍 Testing document structuring...")
    
    # Sample mammography report text
    sample_text = """
    MAMMOGRAPHY REPORT
    
    Patient Information:
    Name: Jane Smith
    DOB: 01/15/1975
    Patient ID: 12345
    
    Exam Information:
    Date: 2024-01-15
    Indication: Routine screening mammography
    Technique: Digital mammography, bilateral CC and MLO views
    
    Clinical History:
    Patient presents for routine screening mammography.
    No breast symptoms or concerns.
    
    Findings:
    BREAST COMPOSITION: The breasts are heterogeneously dense, which may
    obscure small masses.
    
    RIGHT BREAST: No suspicious masses, architectural distortion, or
    suspicious calcifications identified.
    
    LEFT BREAST: No suspicious masses, architectural distortion, or
    suspicious calcifications identified.
    
    Assessment:
    BI-RADS Category 2: Benign findings
    
    Recommendation:
    Routine screening mammography in 12 months.
    
    Radiologist: Dr. Smith
    Date: 2024-01-15
    """
    
    # Generate unique document ID
    document_id = f"test-structuring-{uuid.uuid4().hex[:8]}"
    
    try:
        # Test structuring request
        payload = {
            "document_id": document_id,
            "extracted_text": sample_text
        }
        
        print(f"📤 Sending structuring request...")
        print(f"Document ID: {document_id}")
        
        response = requests.post(
            f"{STRUCTURING_URL}/structuring/structure",
            json=payload,
            params={"api_key": API_KEY}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Structuring successful!")
            print(f"Structuring ID: {result['structuring_id']}")
            print(f"Status: {result['status']}")
            print(f"Message: {result['message']}")
            
            # Get the full result
            print("\n📋 Getting full structuring result...")
            result_response = requests.get(
                f"{STRUCTURING_URL}/structuring/result/{result['structuring_id']}",
                params={"api_key": API_KEY}
            )
            
            if result_response.status_code == 200:
                full_result = result_response.json()
                print("✅ Full result retrieved!")
                print(f"Status: {full_result['status']}")
                print(f"Confidence Score: {full_result['confidence_score']}")
                print(f"Model Used: {full_result['model_used']}")
                print(f"Processing Time: {full_result['processing_time']}s")
                
                # Display structured data
                structured_data = full_result['structured_data']
                print("\n📄 Structured Data:")
                print("-" * 50)
                for key, value in structured_data.items():
                    if value != "unknown":
                        print(f"{key}: {value}")
                print("-" * 50)
                
                return True
            else:
                print(f"❌ Failed to get full result: {result_response.status_code}")
                print(result_response.text)
                return False
        else:
            print(f"❌ Structuring failed: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_structuring_with_minimal_text():
    """Test structuring with minimal text"""
    print("\n🔍 Testing structuring with minimal text...")
    
    minimal_text = """
    Mammography Report
    Patient: Test Patient
    BI-RADS: 2
    Recommendation: Routine follow-up
    """
    
    document_id = f"test-minimal-{uuid.uuid4().hex[:8]}"
    
    try:
        payload = {
            "document_id": document_id,
            "extracted_text": minimal_text
        }
        
        response = requests.post(
            f"{STRUCTURING_URL}/structuring/structure",
            json=payload,
            params={"api_key": API_KEY}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Minimal text structuring successful!")
            
            # Get result by document ID
            doc_response = requests.get(
                f"{STRUCTURING_URL}/structuring/result/document/{document_id}",
                params={"api_key": API_KEY}
            )
            
            if doc_response.status_code == 200:
                full_result = doc_response.json()
                print(f"✅ Retrieved by document ID")
                print(f"Confidence Score: {full_result['confidence_score']}")
                return True
            else:
                print(f"❌ Failed to get result by document ID: {doc_response.status_code}")
                return False
        else:
            print(f"❌ Minimal text structuring failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_error_handling():
    """Test error handling"""
    print("\n🔍 Testing error handling...")
    
    # Test with invalid API key
    try:
        response = requests.post(
            f"{STRUCTURING_URL}/structuring/structure",
            json={"document_id": "test", "extracted_text": "test"},
            params={"api_key": "invalid-key"}
        )
        
        if response.status_code == 401:
            print("✅ Invalid API key properly rejected")
        else:
            print(f"❌ Expected 401, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing invalid API key: {str(e)}")
        return False
    
    # Test with missing fields
    try:
        response = requests.post(
            f"{STRUCTURING_URL}/structuring/structure",
            json={"document_id": "test"},  # Missing extracted_text
            params={"api_key": API_KEY}
        )
        
        if response.status_code == 422:  # Validation error
            print("✅ Missing fields properly validated")
        else:
            print(f"❌ Expected 422, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing missing fields: {str(e)}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Information Structuring Service Test Suite")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Document Structuring", test_structuring_with_sample_text),
        ("Minimal Text Structuring", test_structuring_with_minimal_text),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        print("-" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
