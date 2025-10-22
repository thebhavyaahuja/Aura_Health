"""
Parsing routes for document processing
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import ParseRequest, ParseResponse, ParsingResult, ErrorResponse
from app.services.parsing_service import DocumentParsingService
from app.config import API_KEY

router = APIRouter(prefix="/parsing", tags=["parsing"])

def verify_api_key(api_key: str = Query(..., description="API Key for authentication")):
    """Simple API key verification"""
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@router.post("/parse", response_model=ParseResponse)
async def parse_document(
    request: ParseRequest,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Parse a document using docling"""
    
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
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Get parsing result by parsing ID"""
    
    parsing_service = DocumentParsingService(db)
    result = parsing_service.get_parsing_result_by_id(parsing_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Parsing result not found")
    
    return ParsingResult(
        parsing_id=result.id,
        document_id=result.document_id,
        extracted_text=result.extracted_text,
        status=result.status,
        created_at=result.created_at
    )

@router.get("/result/document/{document_id}", response_model=ParsingResult)
async def get_parsing_result_by_document(
    document_id: str,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Get parsing result by document ID"""
    
    parsing_service = DocumentParsingService(db)
    result = parsing_service.get_parsing_result(document_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Parsing result not found")
    
    return ParsingResult(
        parsing_id=result.id,
        document_id=result.document_id,
        extracted_text=result.extracted_text,
        status=result.status,
        created_at=result.created_at
    )
