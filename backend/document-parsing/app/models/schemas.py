"""
Pydantic schemas for Document Parsing Service
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ParseRequest(BaseModel):
    """Request model for document parsing"""
    document_id: str = Field(..., description="Document ID from ingestion service")
    file_path: str = Field(..., description="Path to the file to parse")

class ParseResponse(BaseModel):
    """Response model for parsing request"""
    parsing_id: str
    document_id: str
    status: str
    message: str

class ParsingResult(BaseModel):
    """Parsing result model"""
    parsing_id: str
    document_id: str
    extracted_text: str
    status: str
    progress: int = 0  # Progress percentage (0-100)
    created_at: datetime

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    status_code: int

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    version: str = "1.0.0"
    database: str
