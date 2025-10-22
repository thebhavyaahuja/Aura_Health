"""
Structuring routes for document processing
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import (
    StructureRequest, 
    StructureResponse, 
    StructuringResult, 
    StructuredData,
    ErrorResponse
)
from app.services.structuring_service import InformationStructuringService
from app.config import API_KEY

router = APIRouter(prefix="/structuring", tags=["structuring"])

def verify_api_key(api_key: str = Query(..., description="API Key for authentication")):
    """Simple API key verification"""
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@router.post("/structure", response_model=StructureResponse)
async def structure_document(
    request: StructureRequest,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Structure a mammography report using Gemini API"""
    
    try:
        structuring_service = InformationStructuringService(db)
        result = await structuring_service.structure_document(
            document_id=request.document_id,
            extracted_text=request.extracted_text
        )
        
        return StructureResponse(
            structuring_id=result.id,
            document_id=result.document_id,
            status=result.status,
            message="Document structured successfully" if result.status == "completed" else f"Structuring failed: {result.error_message}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Structuring failed: {str(e)}")

@router.get("/result/{structuring_id}", response_model=StructuringResult)
async def get_structuring_result(
    structuring_id: str,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Get structuring result by structuring ID"""
    
    structuring_service = InformationStructuringService(db)
    result = structuring_service.get_structuring_result_by_id(structuring_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Structuring result not found")
    
    return StructuringResult(
        structuring_id=result.id,
        document_id=result.document_id,
        structured_data=StructuredData(**result.structured_data),
        confidence_score=result.confidence_score,
        model_used=result.model_used,
        processing_time=result.processing_time,
        status=result.status,
        created_at=result.created_at
    )

@router.get("/result/document/{document_id}", response_model=StructuringResult)
async def get_structuring_result_by_document(
    document_id: str,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Get structuring result by document ID"""
    
    structuring_service = InformationStructuringService(db)
    result = structuring_service.get_structuring_result(document_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Structuring result not found")
    
    return StructuringResult(
        structuring_id=result.id,
        document_id=result.document_id,
        structured_data=StructuredData(**result.structured_data),
        confidence_score=result.confidence_score,
        model_used=result.model_used,
        processing_time=result.processing_time,
        status=result.status,
        created_at=result.created_at
    )
