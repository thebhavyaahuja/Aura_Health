"""
Health check routes for Document Parsing Service
"""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    
    # Check database connectivity
    try:
        db.execute("SELECT 1")
        database_status = "healthy"
    except Exception as e:
        print(f"Database error: {e}")  # Debug info
        database_status = "unhealthy"
    
    # Overall status
    overall_status = "healthy" if database_status == "healthy" else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow(),
        database=database_status
    )

@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    return {"status": "ready", "timestamp": datetime.utcnow()}

@router.get("/live")
async def liveness_check():
    """Liveness check endpoint"""
    return {"status": "alive", "timestamp": datetime.utcnow()}
