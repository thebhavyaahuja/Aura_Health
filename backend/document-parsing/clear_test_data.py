#!/usr/bin/env python3
"""
Script to clear test data from the parsing database
"""
import os
from pathlib import Path

# Add the app directory to Python path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from app.models.database import SessionLocal, ParsingResult

def clear_test_data():
    """Clear test data from database"""
    db = SessionLocal()
    try:
        # Delete all parsing results
        db.query(ParsingResult).delete()
        db.commit()
        print("✅ Cleared all parsing results from database")
        
        # Clear parsed files
        parsed_dir = Path("storage/parsed")
        if parsed_dir.exists():
            for file in parsed_dir.glob("*.md"):
                file.unlink()
            print("✅ Cleared all parsed files")
        
    except Exception as e:
        print(f"❌ Error clearing data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🧹 Clearing test data...")
    clear_test_data()
    print("🎉 Done!")
