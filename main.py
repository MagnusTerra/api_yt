from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
from core.database import Base, engine

from routers import download, auth, health
from core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Social Media Video Downloader API",
             description="API for downloading videos from various social media platforms",
             version="1.0.0")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(download.router, prefix="/api/v1", tags=["Download"])
app.include_router(health.router, tags=["Health"])

@app.get("/")
async def root():
    return {"message": "Welcome to Social Media Video Downloader API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
