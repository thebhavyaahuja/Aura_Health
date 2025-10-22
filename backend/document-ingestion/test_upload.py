#!/usr/bin/env python3
"""
Test script for uploading documents to the Document Ingestion Service
"""
import requests
import os
from pathlib import Path

# Service configuration
BASE_URL = "http://localhost:8000"
API_KEY = "demo-api-key-123"

def test_upload():
    """Test document upload"""
    
    # Create a test PDF file (simple text file for demo)
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
    
    try:
        # Prepare upload data
        files = {
            'file': ('test_document.txt', open(test_file_path, 'rb'), 'text/plain')
        }
        
        data = {
            'uploader_id': 'test_user_123',
            'patient_id': 'patient_456',
            'description': 'Test mammography report'
        }
        
        params = {
            'api_key': API_KEY
        }
        
        print("🚀 Uploading test document...")
        response = requests.post(
            f"{BASE_URL}/documents/upload",
            files=files,
            data=data,
            params=params
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload successful!")
            print(f"Upload ID: {result['upload_id']}")
            print(f"Status: {result['status']}")
            print(f"File: {result['file_info']['filename']}")
            print(f"Size: {result['file_info']['size']} bytes")
            
            # Test getting document status
            upload_id = result['upload_id']
            print(f"\n🔍 Getting document status for ID: {upload_id}")
            
            status_response = requests.get(
                f"{BASE_URL}/documents/{upload_id}",
                params={'api_key': API_KEY}
            )
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                print("✅ Status retrieved successfully!")
                print(f"Status: {status_data['status']}")
                print(f"Created: {status_data['created_at']}")
            else:
                print(f"❌ Failed to get status: {status_response.status_code}")
                print(status_response.text)
                
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        
    finally:
        # Clean up test file
        if test_file_path.exists():
            test_file_path.unlink()
            print("🧹 Test file cleaned up")

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
            print(f"Storage: {health_data['storage']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")

def test_list_documents():
    """Test listing documents"""
    try:
        print("📋 Testing document listing...")
        response = requests.get(
            f"{BASE_URL}/documents/",
            params={'api_key': API_KEY}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Document listing successful!")
            print(f"Total documents: {data['total']}")
            print(f"Page: {data['page']}")
            print(f"Limit: {data['limit']}")
            
            for doc in data['documents']:
                print(f"  - {doc['upload_id']}: {doc['file_info']['filename']} ({doc['status']})")
        else:
            print(f"❌ Document listing failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Document listing error: {str(e)}")

if __name__ == "__main__":
    print("🧪 Testing Document Ingestion Service")
    print("=" * 50)
    
    # Test health first
    test_health()
    print()
    
    # Test upload
    test_upload()
    print()
    
    # Test listing
    test_list_documents()
    
    print("\n🎉 Testing completed!")
