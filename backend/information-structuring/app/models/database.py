"""
Database models and setup for Information Structuring Service
"""
import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# Create database engine
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class StructuringResult(Base):
    """Structuring result model"""
    __tablename__ = "structuring_results"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, nullable=False, unique=True)
    extracted_text = Column(Text, nullable=False)
    structured_data = Column(JSON, nullable=False)
    confidence_score = Column(Float, nullable=True)
    model_used = Column(String(100), default="gemini")
    processing_time = Column(Integer, nullable=True)  # in seconds
    status = Column(String(50), default="completed")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

def create_tables():
    """Create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
