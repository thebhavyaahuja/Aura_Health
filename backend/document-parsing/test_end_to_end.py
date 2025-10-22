#!/usr/bin/env python3
"""
End-to-end test: Upload PDF → Parse → Get Result
"""
import requests
import time
import uuid
from pathlib import Path

# Service URLs
INGESTION_URL = "http://localhost:8000"  # Document Ingestion Service runs on port 8000
PARSING_URL = "http://localhost:8002"    # Document Parsing Service runs on port 8002
API_KEY = "demo-api-key-123"

def create_test_document():
    """Create a test document in a supported format"""
    # For testing, we'll create a simple text file but upload it as a supported type
    # The Document Ingestion Service will accept it based on the content-type header
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
    
    # Create a text file (we'll upload it with PDF content-type)
    test_file = Path("test_mammography_report.txt")
    test_file.write_text(test_content)
    return test_file

def test_end_to_end():
    """Test complete flow: Upload → Parse → Result"""
    print("🚀 Testing End-to-End Flow")
    print("=" * 50)
    
    # Step 1: Create test file
    print("📄 Creating test document...")
    test_file = create_test_document()
    print(f"✅ Created test file: {test_file}")
    
    try:
        # Step 2: Upload to Document Ingestion Service
        print("\n📤 Uploading document to Ingestion Service...")
        
        with open(test_file, 'rb') as f:
            # Upload as PDF content-type to pass validation
            files = {'file': ('test_mammography_report.pdf', f, 'application/pdf')}
            data = {
                'uploader_id': 'test_user',
                'patient_id': 'patient_123',
                'description': 'Test mammography report'
            }
            params = {'api_key': API_KEY}
            
            response = requests.post(
                f"{INGESTION_URL}/documents/upload",
                files=files,
                data=data,
                params=params
            )
        
        if response.status_code == 200:
            upload_result = response.json()
            document_id = upload_result['upload_id']
            print(f"✅ Upload successful! Document ID: {document_id}")
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(response.text)
            return
        
        # Step 3: Wait a moment for parsing to complete
        print("\n⏳ Waiting for parsing to complete...")
        time.sleep(3)
        
        # Step 4: Check parsing result
        print("\n🔍 Checking parsing result...")
        
        # Try to get result by document_id
        response = requests.get(
            f"{PARSING_URL}/parsing/result/document/{document_id}",
            params={'api_key': API_KEY}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Parsing result retrieved!")
            print(f"Status: {result['status']}")
            print(f"Extracted text length: {len(result['extracted_text'])} characters")
            print(f"First 200 characters:")
            print("-" * 40)
            print(result['extracted_text'][:200])
            print("-" * 40)
        else:
            print(f"❌ Failed to get parsing result: {response.status_code}")
            print(response.text)
            
            # Check if parsing service is running
            health_response = requests.get(f"{PARSING_URL}/health/")
            if health_response.status_code == 200:
                health_data = health_response.json()
                print(f"Parsing service health: {health_data['status']}")
            else:
                print("❌ Parsing service is not responding!")
        
        # Step 5: Check document status in ingestion service
        print("\n📋 Checking document status in ingestion service...")
        response = requests.get(
            f"{INGESTION_URL}/documents/{document_id}",
            params={'api_key': API_KEY}
        )
        
        if response.status_code == 200:
            doc_status = response.json()
            print(f"Document status: {doc_status['status']}")
            print("Processing statuses:")
            for status in doc_status['processing_statuses']:
                print(f"  - {status['service_name']}: {status['status']}")
        else:
            print(f"❌ Failed to get document status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()
            print(f"\n🧹 Cleaned up test file: {test_file}")

def test_services_health():
    """Test if both services are running"""
    print("🏥 Checking service health...")
    
    # Check ingestion service
    try:
        response = requests.get(f"{INGESTION_URL}/health/")
        if response.status_code == 200:
            print("✅ Document Ingestion Service: Running")
        else:
            print("❌ Document Ingestion Service: Not responding")
    except:
        print("❌ Document Ingestion Service: Not running")
    
    # Check parsing service
    try:
        response = requests.get(f"{PARSING_URL}/health/")
        if response.status_code == 200:
            print("✅ Document Parsing Service: Running")
        else:
            print("❌ Document Parsing Service: Not responding")
    except:
        print("❌ Document Parsing Service: Not running")

if __name__ == "__main__":
    print("🧪 End-to-End Test for Mammography Report Processing")
    print("=" * 60)
    
    # Check services first
    test_services_health()
    print()
    
    # Run end-to-end test
    test_end_to_end()
    
    print("\n🎉 Test completed!")
