"""
Health check routes
"""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pathlib import Path

from app.models.database import get_db
from app.models.schemas import HealthResponse
from app.config import STORAGE_DIR

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
    
    # Check storage availability
    try:
        storage_path = Path(STORAGE_DIR)
        if storage_path.exists() and storage_path.is_dir():
            storage_status = "healthy"
        else:
            storage_status = "unhealthy"
    except Exception:
        storage_status = "unhealthy"
    
    # Overall status
    overall_status = "healthy" if database_status == "healthy" and storage_status == "healthy" else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow(),
        database=database_status,
        storage=storage_status
    )

@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    return {"status": "ready", "timestamp": datetime.utcnow()}

@router.get("/live")
async def liveness_check():
    """Liveness check endpoint"""
    return {"status": "alive", "timestamp": datetime.utcnow()}
