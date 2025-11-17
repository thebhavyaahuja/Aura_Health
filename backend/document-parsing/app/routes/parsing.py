"""
Parsing routes for document processing
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import ParseRequest, ParseResponse, ParsingResult, ErrorResponse
from app.services.parsing_service import DocumentParsingService
from app.utils.auth_middleware import get_any_user

router = APIRouter(prefix="/parsing", tags=["parsing"])

@router.post("/parse", response_model=ParseResponse)
async def parse_document(
    request: ParseRequest,
    current_user: dict = Depends(get_any_user),
    db: Session = Depends(get_db)
):
    """Parse a document using docling (authenticated users)"""
    
    try:
        parsing_service = DocumentParsingService(db)
        result = await parsing_service.parse_document(
            document_id=request.document_id,
            file_path=request.file_path
        )
        
        return ParseResponse(
            parsing_id=result.id,
            document_id=result.document_id,
            status=result.status,
            message="Document parsed successfully"
        )
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")

@router.get("/result/{parsing_id}", response_model=ParsingResult)
async def get_parsing_result(
    parsing_id: str,
    current_user: dict = Depends(get_any_user),
    db: Session = Depends(get_db)
):
    """Get parsing result by parsing ID (authenticated users) with progress tracking"""
    
    parsing_service = DocumentParsingService(db)
    result = parsing_service.get_parsing_result_by_id(parsing_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Parsing result not found")
    
    return ParsingResult(
        parsing_id=result.id,
        document_id=result.document_id,
        extracted_text=result.extracted_text,
        status=result.status,
        progress=result.progress if hasattr(result, 'progress') else 100,
        created_at=result.created_at
    )

@router.get("/result/document/{document_id}", response_model=ParsingResult)
async def get_parsing_result_by_document(
    document_id: str,
    current_user: dict = Depends(get_any_user),
    db: Session = Depends(get_db)
):
    """Get parsing result by document ID (authenticated users) with progress tracking"""
    
    parsing_service = DocumentParsingService(db)
    result = parsing_service.get_parsing_result(document_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Parsing result not found")
    
    return ParsingResult(
        parsing_id=result.id,
        document_id=result.document_id,
        extracted_text=result.extracted_text,
        status=result.status,
        progress=result.progress if hasattr(result, 'progress') else 100,
        created_at=result.created_at
    )

@router.get("/progress/{document_id}")
async def get_parsing_progress(
    document_id: str,
    current_user: dict = Depends(get_any_user),
    db: Session = Depends(get_db)
):
    """Get current parsing progress for a document (lightweight endpoint for polling)"""
    
    parsing_service = DocumentParsingService(db)
    result = parsing_service.get_parsing_result(document_id)
    
    if not result:
        # Return initial state if not started yet
        return {
            "document_id": document_id,
            "status": "pending",
            "progress": 0,
            "message": "Waiting to start parsing"
        }
    
    # Return progress info
    return {
        "document_id": document_id,
        "status": result.status,
        "progress": result.progress if hasattr(result, 'progress') else 100,
        "message": get_progress_message(result.status, result.progress if hasattr(result, 'progress') else 100),
        "error_message": result.error_message if hasattr(result, 'error_message') else None
    }

def get_progress_message(status: str, progress: int) -> str:
    """Get human-readable progress message"""
    if status == "failed":
        return "Parsing failed"
    elif status == "completed":
        return "Parsing completed successfully"
    elif progress < 20:
        return "Initializing parser..."
    elif progress < 40:
        return "Loading document..."
    elif progress < 70:
        return "Extracting text from PDF..."
    elif progress < 90:
        return "Processing extracted content..."
    else:
        return "Finalizing..."

@router.post("/parse-internal", response_model=ParseResponse, include_in_schema=False)
async def parse_document_internal(
    request: ParseRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Internal endpoint for service-to-service communication (no auth required)"""
    print(f"📥 Received parse request for document: {request.document_id}")
    print(f"   File path: {request.file_path}")
    
    try:
        # Check if file exists before queuing
        import os
        if not os.path.exists(request.file_path):
            raise FileNotFoundError(f"File not found: {request.file_path}")
        
        # Add parsing task to background
        background_tasks.add_task(
            process_document_async,
            request.document_id,
            request.file_path
        )
        
        print(f"   ⏳ Parsing queued for background processing")
        return ParseResponse(
            parsing_id=request.document_id,  # Use document_id as temp parsing_id
            document_id=request.document_id,
            status="processing",
            message="Document parsing started in background"
        )
        
    except FileNotFoundError as e:
        print(f"   ❌ File not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"   ❌ Parsing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")

async def process_document_async(document_id: str, file_path: str):
    """Background task to process document"""
    from app.models.database import SessionLocal
    db = SessionLocal()
    
    try:
        print(f"   🔄 Starting background parsing for: {document_id}")
        parsing_service = DocumentParsingService(db)
        result = await parsing_service.parse_document(
            document_id=document_id,
            file_path=file_path
        )
        print(f"   ✅ Parsing completed successfully")
    except Exception as e:
        print(f"   ❌ Background parsing failed: {str(e)}")
    finally:
        db.close()

@router.delete("/{document_id}/delete-internal", include_in_schema=False)
async def delete_parsing_result_internal(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Internal endpoint to delete parsing result (no auth required)"""
    
    try:
        from pathlib import Path
        from app.config import PARSED_DIR
        
        # Delete from database
        from app.models.database import ParsingResult
        result = db.query(ParsingResult).filter(ParsingResult.document_id == document_id).first()
        if result:
            db.delete(result)
            db.commit()
        
        # Delete parsed file if exists
        parsed_file = PARSED_DIR / f"{document_id}.md"
        if parsed_file.exists():
            parsed_file.unlink()
        
        return {"message": "Parsing result deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
