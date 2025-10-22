#!/usr/bin/env python3
"""
Test runner for Document Ingestion Service
"""
import subprocess
import sys
from pathlib import Path

def run_tests():
    """Run all tests"""
    print("🧪 Running Document Ingestion Service Tests")
    print("=" * 50)
    
    # Change to the service directory
    service_dir = Path(__file__).parent
    
    try:
        # Run pytest
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short"
        ], cwd=service_dir, capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")

if __name__ == "__main__":
    run_tests()
