"""
File validation utilities
"""
import magic
from pathlib import Path
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException
from app.config import MAX_FILE_SIZE, ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES

def validate_file_size(file: UploadFile) -> None:
    """Validate file size"""
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size allowed: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
        )

def validate_file_extension(filename: str) -> None:
    """Validate file extension"""
    file_path = Path(filename)
    extension = file_path.suffix.lower()
    
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

def validate_file_content(file: UploadFile) -> Tuple[str, str]:
    """Validate file content using magic numbers"""
    # Read first 1024 bytes for magic number detection
    content = file.file.read(1024)
    file.file.seek(0)  # Reset file pointer
    
    # Detect MIME type
    mime_type = magic.from_buffer(content, mime=True)
    
    if mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File content not allowed. Detected type: {mime_type}"
        )
    
    return mime_type, content

def validate_upload_file(file: UploadFile) -> Tuple[str, str]:
    """
    Comprehensive file validation
    Returns: (mime_type, content_preview)
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Validate file size
    validate_file_size(file)
    
    # Validate file extension
    validate_file_extension(file.filename)
    
    # Validate file content
    mime_type, content_preview = validate_file_content(file)
    
    return mime_type, content_preview

def get_file_size(file: UploadFile) -> int:
    """Get file size in bytes"""
    if file.size:
        return file.size
    
    # If size is not available, read the file to get size
    current_pos = file.file.tell()
    file.file.seek(0, 2)  # Seek to end
    size = file.file.tell()
    file.file.seek(current_pos)  # Reset position
    return size
