"""
Document service for handling document operations
"""
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.database import Document, ProcessingStatus
from app.models.schemas import UploadMetadata, FileInfo
from app.utils.storage import generate_file_path, save_uploaded_file, get_file_info
from app.utils.validation import validate_upload_file, get_file_size

class DocumentService:
    """Service for document operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def upload_document(
        self, 
        file_content: bytes, 
        filename: str, 
        content_type: str,
        metadata: UploadMetadata
    ) -> Document:
        """Upload and store a document"""
        
        # Generate file path
        file_path, unique_filename = generate_file_path(filename)
        
        # Save file to storage
        save_uploaded_file(file_content, file_path)
        
        # Get file size
        file_size = len(file_content)
        
        # Create document record
        document = Document(
            filename=unique_filename,
            original_filename=filename,
            file_path=str(file_path),
            file_size=file_size,
            content_type=content_type,
            uploader_id=metadata.uploader_id,
            patient_id=metadata.patient_id,
            status="uploaded"
        )
        
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        # Create initial processing status
        processing_status = ProcessingStatus(
            document_id=document.id,
            service_name="document_ingestion",
            status="completed"
        )
        self.db.add(processing_status)
        self.db.commit()
        
        return document
    
    def get_document(self, document_id: str) -> Optional[Document]:
        """Get document by ID"""
        return self.db.query(Document).filter(Document.id == document_id).first()
    
    def get_documents(
        self, 
        page: int = 1, 
        limit: int = 10, 
        status: Optional[str] = None
    ) -> tuple[List[Document], int]:
        """Get paginated list of documents"""
        query = self.db.query(Document)
        
        if status:
            query = query.filter(Document.status == status)
        
        total = query.count()
        documents = query.offset((page - 1) * limit).limit(limit).all()
        
        return documents, total
    
    def update_document_status(self, document_id: str, status: str) -> bool:
        """Update document status"""
        document = self.get_document(document_id)
        if not document:
            return False
        
        document.status = status
        document.updated_at = datetime.utcnow()
        self.db.commit()
        return True
    
    def delete_document(self, document_id: str) -> bool:
        """Delete document and its file"""
        document = self.get_document(document_id)
        if not document:
            return False
        
        # Delete file from storage
        file_path = Path(document.file_path)
        if file_path.exists():
            file_path.unlink()
        
        # Delete from database
        self.db.delete(document)
        self.db.commit()
        return True
    
    def get_processing_statuses(self, document_id: str) -> List[ProcessingStatus]:
        """Get processing statuses for a document"""
        return self.db.query(ProcessingStatus).filter(
            ProcessingStatus.document_id == document_id
        ).all()
    
    def add_processing_status(
        self, 
        document_id: str, 
        service_name: str, 
        status: str, 
        error_message: Optional[str] = None
    ) -> ProcessingStatus:
        """Add processing status for a document"""
        processing_status = ProcessingStatus(
            document_id=document_id,
            service_name=service_name,
            status=status,
            error_message=error_message
        )
        self.db.add(processing_status)
        self.db.commit()
        self.db.refresh(processing_status)
        return processing_status
