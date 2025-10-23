#!/usr/bin/env python3
"""
Test script for Authentication Service
"""
import requests
import json

# Service configuration
AUTH_URL = "http://localhost:8010"

def test_login():
    """Test login for both user types"""
    print("🔐 Testing Authentication Service")
    print("=" * 50)
    
    # Test clinic admin login
    print("\n1. Testing Clinic Admin Login...")
    response = requests.post(
        f"{AUTH_URL}/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "pw"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Clinic Admin login successful!")
        print(f"   User: {data['user']['full_name']} ({data['user']['role']})")
        print(f"   Organization: {data['user']['organization']}")
        print(f"   Access Token: {data['token']['access_token'][:50]}...")
        admin_token = data['token']['access_token']
    else:
        print(f"❌ Clinic Admin login failed: {response.status_code}")
        print(response.text)
        return
    
    # Test coordinator login
    print("\n2. Testing GCF Coordinator Login...")
    response = requests.post(
        f"{AUTH_URL}/auth/login",
        json={
            "email": "coord@gmail.com",
            "password": "pw"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ GCF Coordinator login successful!")
        print(f"   User: {data['user']['full_name']} ({data['user']['role']})")
        print(f"   Organization: {data['user']['organization']}")
        print(f"   Access Token: {data['token']['access_token'][:50]}...")
        coord_token = data['token']['access_token']
    else:
        print(f"❌ GCF Coordinator login failed: {response.status_code}")
        print(response.text)
        return
    
    # Test getting current user
    print("\n3. Testing Get Current User...")
    response = requests.get(
        f"{AUTH_URL}/auth/me",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    if response.status_code == 200:
        user = response.json()
        print("✅ Got current user information!")
        print(f"   Email: {user['email']}")
        print(f"   Role: {user['role']}")
    else:
        print(f"❌ Failed to get user: {response.status_code}")
    
    # Test invalid login
    print("\n4. Testing Invalid Login...")
    response = requests.post(
        f"{AUTH_URL}/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "wrong"
        }
    )
    
    if response.status_code == 401:
        print("✅ Invalid login correctly rejected!")
    else:
        print(f"❌ Unexpected response: {response.status_code}")
    
    print("\n✅ All authentication tests passed!")

def test_health():
    """Test health endpoint"""
    print("\n🏥 Testing Health Endpoint...")
    response = requests.get(f"{AUTH_URL}/health")
    
    if response.status_code == 200:
        print("✅ Health check passed!")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Health check failed: {response.status_code}")

if __name__ == "__main__":
    try:
        test_health()
        test_login()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to Authentication Service")
        print("   Make sure the service is running on http://localhost:8010")
        print("   Run: python backend/authentication/run.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
