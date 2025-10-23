"""
Authentication Service - Main FastAPI Application
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import LOG_LEVEL, LOG_FORMAT, CORS_ORIGINS
from app.models.database import create_tables, get_db, User
from app.routes import auth
from app.utils.auth import get_password_hash

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Authentication Service...")
    create_tables()
    
    # Create default users if they don't exist
    db = next(get_db())
    try:
        # Check if admin user exists
        admin_user = db.query(User).filter(User.email == "admin@gmail.com").first()
        if not admin_user:
            admin = User(
                email="admin@gmail.com",
                full_name="Admin User",
                organization="City Imaging Center",
                hashed_password=get_password_hash("pw"),
                role="clinic_admin",
                is_active=True
            )
            db.add(admin)
            logger.info("Created default admin user: admin@gmail.com")
        
        # Check if coordinator user exists
        coord_user = db.query(User).filter(User.email == "coord@gmail.com").first()
        if not coord_user:
            coordinator = User(
                email="coord@gmail.com",
                full_name="Krish Jalan",
                organization="GCF Program",
                hashed_password=get_password_hash("pw"),
                role="gcf_coordinator",
                is_active=True
            )
            db.add(coordinator)
            logger.info("Created default coordinator user: coord@gmail.com")
        
        db.commit()
        logger.info("Database initialization completed")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()
    
    yield
    # Shutdown
    logger.info("Shutting down Authentication Service...")

# Create FastAPI application
app = FastAPI(
    title="Authentication Service",
    description="Microservice for user authentication and authorization",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)

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
        "service": "Authentication Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "login": "/auth/login",
            "register": "/auth/register",
            "refresh": "/auth/refresh",
            "logout": "/auth/logout",
            "me": "/auth/me",
            "docs": "/docs"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "authentication"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8010,
        reload=True,
        log_level="info"
    )
