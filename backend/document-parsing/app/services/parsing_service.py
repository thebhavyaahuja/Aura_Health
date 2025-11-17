"""
Document parsing service using docling
"""
import os
import httpx
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session
from docling.document_converter import DocumentConverter

from app.models.database import ParsingResult
from app.config import PARSED_DIR, INFORMATION_STRUCTURING_URL, DOCUMENT_INGESTION_URL

# Singleton instance of DocumentConverter to avoid reloading models
_converter_instance = None

def get_converter():
    """Get or create singleton DocumentConverter instance"""
    global _converter_instance
    if _converter_instance is None:
        print("🔧 Initializing DocumentConverter (one-time setup)...")
        _converter_instance = DocumentConverter()
        print("✅ DocumentConverter ready")
    return _converter_instance

class DocumentParsingService:
    """Service for parsing documents using docling"""
    
    def __init__(self, db: Session):
        self.db = db
        self.converter = get_converter()
    
    async def parse_document(self, document_id: str, file_path: str) -> ParsingResult:
        """Parse document using docling"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Handle different file types
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.txt':
                # For text files, just read the content directly
                with open(file_path, 'r', encoding='utf-8') as f:
                    extracted_text = f.read()
            else:
                # For other files (PDF, DOCX, images), use docling
                result = self.converter.convert(file_path)
                extracted_text = result.document.export_to_markdown()
            
            # Check if result already exists for this document_id
            existing_result = self.db.query(ParsingResult).filter(
                ParsingResult.document_id == document_id
            ).first()
            
            if existing_result:
                # Update existing result
                existing_result.extracted_text = extracted_text
                existing_result.status = "completed"
                existing_result.error_message = None
                self.db.commit()
                self.db.refresh(existing_result)
                parsing_result = existing_result
            else:
                # Create new result
                parsing_result = ParsingResult(
                    document_id=document_id,
                    extracted_text=extracted_text,
                    status="completed"
                )
                self.db.add(parsing_result)
                self.db.commit()
                self.db.refresh(parsing_result)
            
            # Save parsed text to file
            await self.save_parsed_text(document_id, extracted_text)
            
            # Update document-ingestion service about completion
            await self.update_document_status(document_id, "parsed", "completed")
            
            # Trigger information structuring service
            await self.trigger_structuring_service(document_id, extracted_text)
            
            return parsing_result
            
        except Exception as e:
            # Check if result already exists for this document_id
            existing_result = self.db.query(ParsingResult).filter(
                ParsingResult.document_id == document_id
            ).first()
            
            if existing_result:
                # Update existing result with error
                existing_result.extracted_text = ""
                existing_result.status = "failed"
                existing_result.error_message = str(e)
                self.db.commit()
                self.db.refresh(existing_result)
            else:
                # Create new error result
                error_result = ParsingResult(
                    document_id=document_id,
                    extracted_text="",
                    status="failed",
                    error_message=str(e)
                )
                self.db.add(error_result)
                self.db.commit()
                self.db.refresh(error_result)
            
            # Update document-ingestion service about failure
            await self.update_document_status(document_id, "uploaded", "failed", str(e))
            
            raise e
    
    async def save_parsed_text(self, document_id: str, text: str) -> None:
        """Save parsed text to file"""
        file_path = PARSED_DIR / f"{document_id}.md"
        file_path.write_text(text, encoding='utf-8')
    
    async def update_document_status(
        self, 
        document_id: str, 
        doc_status: str,
        processing_status: str,
        error_message: Optional[str] = None
    ) -> None:
        """Update document status in document-ingestion service"""
        try:
            payload = {
                "document_id": document_id,
                "service_name": "document_parsing",
                "status": processing_status,
                "error_message": error_message
            }
            
            async with httpx.AsyncClient() as client:
                # Update processing status
                await client.post(
                    f"{DOCUMENT_INGESTION_URL}/documents/update-status-internal",
                    json=payload,
                    timeout=10.0
                )
                
                # Update main document status
                if doc_status:
                    status_payload = {"status": doc_status}
                    await client.patch(
                        f"{DOCUMENT_INGESTION_URL}/documents/{document_id}/status-internal",
                        json=status_payload,
                        timeout=10.0
                    )
                    
        except Exception as e:
            print(f"Warning: Failed to update document status: {str(e)}")
    
    async def trigger_structuring_service(self, document_id: str, extracted_text: str) -> None:
        """Trigger information structuring service (internal service call, no auth needed)"""
        print(f"🔄 Triggering structuring service for document: {document_id}")
        print(f"   URL: {INFORMATION_STRUCTURING_URL}/structuring/structure-internal")
        print(f"   Text length: {len(extracted_text)} chars")
        
        try:
            payload = {
                "document_id": document_id,
                "extracted_text": extracted_text
            }
            
            async with httpx.AsyncClient() as client:
                # Internal service call - no authentication required
                response = await client.post(
                    f"{INFORMATION_STRUCTURING_URL}/structuring/structure-internal",
                    json=payload,
                    timeout=30.0
                )
                
                print(f"   Response status: {response.status_code}")
                if response.status_code != 200:
                    print(f"   ⚠️ Warning: Structuring service returned {response.status_code}")
                    print(f"   Response: {response.text}")
                else:
                    print(f"   ✅ Structuring triggered successfully")
                    
        except Exception as e:
            print(f"   ❌ Failed to trigger structuring service: {str(e)}")
    
    def get_parsing_result(self, document_id: str) -> Optional[ParsingResult]:
        """Get parsing result by document ID"""
        return self.db.query(ParsingResult).filter(
            ParsingResult.document_id == document_id
        ).first()
    
    def get_parsing_result_by_id(self, parsing_id: str) -> Optional[ParsingResult]:
        """Get parsing result by parsing ID"""
        return self.db.query(ParsingResult).filter(
            ParsingResult.id == parsing_id
        ).first()
