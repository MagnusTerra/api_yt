from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional, List
import os
import tempfile

from services.download_service import download_video
from schemas.download import DownloadRequest, Platform
from core.deps import get_current_user
from core.config import settings

router = APIRouter()

@router.post("/download")
async def download_video_endpoint(
    download_req: DownloadRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Download video from a given URL
    """
    try:
        # Create a temporary directory to store the downloaded file
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = await download_video(
                url=download_req.url,
                platform=download_req.platform,
                output_dir=temp_dir,
                quality=download_req.quality
            )
            
            if not file_path or not os.path.exists(file_path):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to download video"
                )
            
            # Return the file for download
            return FileResponse(
                path=file_path,
                media_type='application/octet-stream',
                filename=os.path.basename(file_path)
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/supported-platforms", response_model=List[str])
async def get_supported_platforms():
    """
    Get list of supported platforms
    """
    return [platform.value for platform in Platform]
