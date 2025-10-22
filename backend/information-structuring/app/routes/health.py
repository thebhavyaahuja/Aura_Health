"""
Health check routes for Information Structuring Service
"""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import HealthResponse
from app.config import GEMINI_API_KEY

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    
    # Check database connectivity
    try:
        db.execute("SELECT 1")
        database_status = "healthy"
    except Exception:
        database_status = "unhealthy"
    
    # Check Gemini API key
    if GEMINI_API_KEY:
        gemini_api_status = "configured"
    else:
        gemini_api_status = "not_configured"
    
    # Overall status
    overall_status = "healthy" if database_status == "healthy" else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow(),
        database=database_status,
        gemini_api=gemini_api_status
    )

@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    return {"status": "ready", "timestamp": datetime.utcnow()}

@router.get("/live")
async def liveness_check():
    """Liveness check endpoint"""
    return {"status": "alive", "timestamp": datetime.utcnow()}
