#!/usr/bin/env python3
"""
Test Risk Prediction Service
Tests that the model is working correctly
"""
import requests
import json

BASE_URL = "http://localhost:8004"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    return response.status_code == 200

def test_model_loaded():
    """Test if model is loaded"""
    print("\n🤖 Testing model status...")
    try:
        response = requests.get(f"{BASE_URL}/model/status")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
            return True
    except Exception as e:
        print(f"   ⚠️  Endpoint might not exist: {e}")
    return False

def test_prediction():
    """Test prediction with sample data"""
    print("\n🔮 Testing prediction...")
    
    # Sample structured data (mammography report)
    test_data = {
        "document_id": "test-doc-123",
        "structured_data": {
            "age": "45",
            "reason": "Screening mammography",
            "observations": "Dense fibroglandular tissue. A 12mm irregular mass noted in the upper outer quadrant with associated microcalcifications. Suspicious findings present.",
            "conclusion": "Highly suggestive of malignancy. BI-RADS 5.",
            "recommendations": "Tissue diagnosis recommended. Biopsy advised.",
            "family_history": "Mother diagnosed with breast cancer at age 52",
            "hormonal_therapy": "None",
            "children": "2",
            "lmp": "unknown"
        }
    }
    
    # Note: This endpoint likely requires authentication
    # You may need to add authentication headers
    print(f"   Sending request to: {BASE_URL}/predictions/predict-internal")
    print(f"   Document ID: {test_data['document_id']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/predictions/predict-internal",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Prediction successful!")
            print(f"   Prediction ID: {result.get('prediction_id')}")
            print(f"   Status: {result.get('status')}")
            print(f"   Message: {result.get('message')}")
            
            # Get the full prediction details
            print("\n📊 Getting prediction details...")
            print(f"   (Note: Regular GET endpoint requires authentication)")
            print(f"   Prediction created successfully with ID: {result.get('prediction_id')}")
            
            # Try to get details (will likely fail without auth, but that's ok)
            pred_response = requests.get(
                f"{BASE_URL}/predictions/document/{test_data['document_id']}"
            )
            
            if pred_response.status_code == 200:
                details = pred_response.json()
                print(f"   BI-RADS Score: {details.get('predicted_birads')}")
                print(f"   Confidence: {details.get('confidence_score', 0):.3f}")
                print(f"   Risk Level: {details.get('risk_level')}")
                print(f"   Probabilities:")
                for birads, prob in details.get('probabilities', {}).items():
                    print(f"      BI-RADS {birads}: {prob:.3f}")
            else:
                print(f"   ⚠️  Cannot get details without authentication (expected)")
            
            return True
        else:
            print(f"   ❌ Prediction failed!")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  🧪 Risk Prediction Service Test")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Run tests
    health_ok = test_health()
    model_ok = test_model_loaded()
    prediction_ok = test_prediction()
    
    # Summary
    print("\n" + "━" * 60)
    print("📋 Test Summary:")
    print(f"   Health Check: {'✅' if health_ok else '❌'}")
    print(f"   Model Status: {'✅' if model_ok else '⚠️  (endpoint may not exist)'}")
    print(f"   Prediction: {'✅' if prediction_ok else '❌'}")
    print("━" * 60)
    
    if health_ok and prediction_ok:
        print("\n✅ All critical tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed. Check the logs for details.")
        return 1

if __name__ == "__main__":
    exit(main())
