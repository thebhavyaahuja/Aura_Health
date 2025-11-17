"""
Migration script to add progress column to parsing_results table
"""
import sqlite3
from pathlib import Path

def migrate():
    db_path = Path(__file__).parent / "parsing.db"
    
    if not db_path.exists():
        print("❌ Database not found. Nothing to migrate.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(parsing_results)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if "progress" in columns:
            print("✅ progress column already exists. No migration needed.")
            return
        
        # Add the column
        print("🔧 Adding progress column to parsing_results table...")
        cursor.execute("ALTER TABLE parsing_results ADD COLUMN progress INTEGER DEFAULT 0")
        conn.commit()
        print("✅ Successfully added progress column!")
        
        # Update existing records to 100% (completed)
        print("🔧 Updating existing records...")
        cursor.execute("UPDATE parsing_results SET progress = 100 WHERE status = 'completed'")
        conn.commit()
        print("✅ Updated existing records!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
