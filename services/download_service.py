import os
import re
import asyncio
from typing import Optional
from urllib.parse import urlparse
from pytube import YouTube
import yt_dlp

from schemas.download import Platform

# Suppress yt-dlp output
class SuppressOutput:
    def __enter__(self):
        self._original_stdout = os.dup(1)
        self._original_stderr = os.dup(2)
        self._devnull = open(os.devnull, 'w')
        os.dup2(self._devnull.fileno(), 1)
        os.dup2(self._devnull.fileno(), 2)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.dup2(self._original_stdout, 1)
        os.dup2(self._original_stderr, 2)
        self._devnull.close()

async def download_video(
    url: str,
    platform: Platform,
    output_dir: str,
    quality: str = "best"
) -> Optional[str]:
    """
    Download video from the given URL based on the platform
    
    Args:
        url: URL of the video to download
        platform: Platform the video is from
        output_dir: Directory to save the downloaded video
        quality: Preferred video quality (e.g., 'best', '720p', '1080p')
    
    Returns:
        Path to the downloaded file or None if download failed
    """
    try:
        if platform == Platform.YOUTUBE:
            return await _download_youtube_video(url, output_dir, quality)
        else:
            return await _download_with_ytdlp(url, output_dir, quality)
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None

async def _download_youtube_video(url: str, output_dir: str, quality: str) -> Optional[str]:
    """Download video from YouTube"""
    try:
        yt = YouTube(url)
        
        # Get the best quality stream
        if quality == "best":
            stream = yt.streams.get_highest_resolution()
        else:
            stream = yt.streams.filter(res=quality, progressive=True).first()
            if not stream:
                stream = yt.streams.get_highest_resolution()
        
        if not stream:
            raise Exception("No suitable video stream found")
        
        # Sanitize filename
        safe_title = "".join(c if c.isalnum() or c in ' -_' else '_' for c in yt.title)
        output_path = os.path.join(output_dir, f"{safe_title}.mp4")
        
        # Download the video
        stream.download(output_path=output_dir, filename=f"{safe_title}.mp4")
        
        return output_path
    except Exception as e:
        print(f"Error downloading YouTube video: {str(e)}")
        return None

async def _download_with_ytdlp(url: str, output_dir: str, quality: str) -> Optional[str]:
    """Download video using yt-dlp (supports multiple platforms)"""
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'merge_output_format': 'mp4',
    }
    
    if quality != "best":
        ydl_opts['format'] = f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best'
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            with SuppressOutput():
                info_dict = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: ydl.extract_info(url, download=True)
                )
                
            if not info_dict:
                raise Exception("Failed to extract video info")
                
            # Get the actual filename
            if 'entries' in info_dict:  # Playlist
                info_dict = info_dict['entries'][0]
                
            filename = ydl.prepare_filename(info_dict)
            return filename if os.path.exists(filename) else None
            
    except Exception as e:
        print(f"Error downloading with yt-dlp: {str(e)}")
        return None
