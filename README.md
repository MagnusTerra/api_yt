# Social Media Video Downloader API

A FastAPI-based service for downloading videos from various social media platforms.

## Features

- Download videos from multiple platforms (YouTube, Instagram, TikTok, Twitter, Facebook)
- User authentication with JWT tokens
- Rate limiting to prevent abuse
- Asynchronous downloads for better performance
- Support for different video qualities

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- FFmpeg (for some video processing)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd api_yt
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your configuration:
   ```
   SECRET_KEY=your-secret-key-here
   ```

## Running the Application

1. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```

2. The API will be available at `http://127.0.0.1:8000`

3. Access the interactive API documentation at:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Authentication

- `POST /auth/login` - Login and get access token
- `POST /auth/signup` - Create a new user account

### Download

- `POST /api/v1/download` - Download a video from a URL
- `GET /api/v1/supported-platforms` - List supported platforms

## Usage Example

1. First, get an access token:
   ```bash
   curl -X 'POST' \
     'http://127.0.0.1:8000/auth/login' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'username=testuser&password=secret'
   ```

2. Use the access token to download a video:
   ```bash
   curl -X 'POST' \
     'http://127.0.0.1:8000/api/v1/download' \
     -H 'accept: application/json' \
     -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
     -H 'Content-Type: application/json' \
     -d '{
       "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
       "platform": "youtube",
       "quality": "720p"
     }'
   ```

## Rate Limiting

The API is rate limited to 10 requests per minute by default. This can be configured in `core/config.py`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
