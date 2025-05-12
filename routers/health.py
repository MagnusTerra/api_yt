from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import test_db_connection, get_db

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        if not test_db_connection():
            raise HTTPException(status_code=503, detail="Database connection failed")
            
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
