from enum import Enum
from pydantic import BaseModel, HttpUrl
from typing import Optional

class Platform(str, Enum):
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    TWITTER = "twitter"
    FACEBOOK = "facebook"

class DownloadRequest(BaseModel):
    url: HttpUrl
    platform: Platform
    quality: Optional[str] = "best"  # best, 1080p, 720p, etc.

class DownloadResponse(BaseModel):
    status: str
    message: str
    download_url: Optional[str] = None
    file_path: Optional[str] = None
