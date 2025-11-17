"""
Configuration settings for Document Ingestion Service
"""
import os
from pathlib import Path
from typing import List

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Storage settings
STORAGE_DIR = BASE_DIR / "storage"
UPLOADS_DIR = STORAGE_DIR / "uploads"
TEMP_DIR = STORAGE_DIR / "temp"

# Database settings
DATABASE_URL = f"sqlite:///{BASE_DIR}/database.db"

# File upload settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".png", ".jpg", ".jpeg", ".tiff", ".tif"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/png",
    "image/jpeg",
    "image/tiff"
}

# API settings
API_V1_PREFIX = "/api/v1"
HOST = "0.0.0.0"
PORT = 8000

# Security settings
API_KEY = os.getenv("API_KEY", "demo-api-key-123")  # Simple API key for demo

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Service URLs (for inter-service communication)
DOCUMENT_PARSING_URL = os.getenv("DOCUMENT_PARSING_URL", "http://localhost:8002")
INFORMATION_STRUCTURING_URL = os.getenv("INFORMATION_STRUCTURING_URL", "http://localhost:8003")

# Create directories if they don't exist
def create_directories():
    """Create necessary directories"""
    STORAGE_DIR.mkdir(exist_ok=True)
    UPLOADS_DIR.mkdir(exist_ok=True)
    TEMP_DIR.mkdir(exist_ok=True)

# Initialize directories on import
create_directories()
