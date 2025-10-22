"""
Document routes for file upload and management
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import (
    UploadResponse, 
    DocumentStatus, 
    DocumentListResponse, 
    FileInfo,
    ErrorResponse
)
from app.services.document_service import DocumentService
from app.utils.validation import validate_upload_file
from app.config import API_KEY

router = APIRouter(prefix="/documents", tags=["documents"])

def verify_api_key(api_key: str = Query(..., description="API Key for authentication")):
    """Simple API key verification"""
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(..., description="Document file to upload"),
    uploader_id: str = Form(..., description="ID of the person uploading the file"),
    patient_id: Optional[str] = Form(None, description="Patient ID (optional)"),
    description: Optional[str] = Form(None, description="Description of the document"),
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Upload a mammography report document"""
    
    try:
        # Validate file
        mime_type, _ = validate_upload_file(file)
        
        # Read file content
        file_content = await file.read()
        
        # Create metadata
        from app.models.schemas import UploadMetadata
        metadata = UploadMetadata(
            uploader_id=uploader_id,
            patient_id=patient_id,
            description=description
        )
        
        # Upload document
        document_service = DocumentService(db)
        document = await document_service.upload_document(
            file_content=file_content,
            filename=file.filename,
            content_type=mime_type,
            metadata=metadata
        )
        
        # Create response
        file_info = FileInfo(
            filename=document.original_filename,
            size=document.file_size,
            content_type=document.content_type
        )
        
        return UploadResponse(
            upload_id=document.id,
            status=document.status,
            file_info=file_info,
            created_at=document.created_at,
            message="Document uploaded successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/{document_id}", response_model=DocumentStatus)
async def get_document_status(
    document_id: str,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Get document status and information"""
    
    document_service = DocumentService(db)
    document = document_service.get_document(document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Get processing statuses
    processing_statuses = document_service.get_processing_statuses(document_id)
    
    file_info = FileInfo(
        filename=document.original_filename,
        size=document.file_size,
        content_type=document.content_type
    )
    
    return DocumentStatus(
        upload_id=document.id,
        status=document.status,
        file_info=file_info,
        created_at=document.created_at,
        updated_at=document.updated_at,
        processing_statuses=[
            {
                "service_name": ps.service_name,
                "status": ps.status,
                "error_message": ps.error_message,
                "created_at": ps.created_at
            }
            for ps in processing_statuses
        ]
    )

@router.get("/", response_model=DocumentListResponse)
async def list_documents(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """List all documents with pagination"""
    
    document_service = DocumentService(db)
    documents, total = document_service.get_documents(page, limit, status)
    
    document_list = []
    for doc in documents:
        file_info = FileInfo(
            filename=doc.original_filename,
            size=doc.file_size,
            content_type=doc.content_type
        )
        
        document_list.append(DocumentStatus(
            upload_id=doc.id,
            status=doc.status,
            file_info=file_info,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
            processing_statuses=[]
        ))
    
    return DocumentListResponse(
        documents=document_list,
        total=total,
        page=page,
        limit=limit
    )

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Delete a document"""
    
    document_service = DocumentService(db)
    success = document_service.delete_document(document_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {"message": "Document deleted successfully"}
