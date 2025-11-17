"""
Document Parsing Service - Main FastAPI Application
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import LOG_LEVEL, LOG_FORMAT
from app.models.database import create_tables
from app.routes import parsing, health

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Document Parsing Service...")
    create_tables()
    logger.info("Database tables created successfully")
    
    # Preload DocumentConverter to avoid delay on first request
    logger.info("Preloading DocumentConverter...")
    from app.services.parsing_service import get_converter
    get_converter()
    logger.info("DocumentConverter preloaded successfully")
    
    yield
    # Shutdown
    logger.info("Shutting down Document Parsing Service...")

# Create FastAPI application
app = FastAPI(
    title="Document Parsing Service",
    description="Microservice for parsing mammography reports using docling",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(parsing.router)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Document Parsing Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health/",
            "parse": "/parsing/parse",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )
