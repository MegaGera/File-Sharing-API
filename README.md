# File Sharing API

A RESTful file-sharing API built with FastAPI that allows users to upload, download, and list files. Files are stored locally with metadata tracking.

## Building process

### Phase 1: Initial Analysis and Design

Initial Analysis and Design documentation available in the file [initial_analysis_and_design.md](initial_analysis_and_design.md)

## Features

- **Upload Files**: Upload files with automatic metadata generation
- **Download Files**: Download files by unique ID
- **List Files**: Retrieve metadata for all uploaded files
- **File Size Validation**: Maximum file size limit of 20MB
- **Metadata Tracking**: Automatic tracking of file name, size, upload timestamp, and unique ID
- **Docker Support**: Containerized deployment ready

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.11**: Programming language
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server
- **Docker**: Containerization

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd file-sharing-api
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Root Endpoint
- **GET** `/`
  - Returns API name and version
  - Response: `{"message": name, "version": version}`

### Upload File
- **POST** `/files`
  - Upload a file to the server
  - **Request**: Multipart form data with file
  - **Response**: FileMetadata object (201 Created)
  - **Errors**:
    - `400`: No file provided
    - `413`: File too large (max 20MB)
    - `500`: Server error

### Download File
- **GET** `/files/{file_id}`
  - Download a file by its unique ID
  - **Parameters**: `file_id` (string) - Unique file identifier
  - **Response**: File content with original filename
  - **Errors**:
    - `404`: File not found

### List All Files
- **GET** `/files`
  - Get metadata for all uploaded files
  - **Response**: List of FileMetadata objects
  - **Response Model**: Array of `FileMetadata`

## API Documentation

Once the server is running, interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Data Models

### FileMetadata
```json
{
  "id": "string (UUID)",
  "file_name": "string",
  "size": "integer (bytes)",
  "timestamp": "datetime (ISO format)"
}
```

## Docker Deployment

### Build the Docker image:
```bash
docker build -t file-sharing-api .
```

### Run the container:
```bash
docker run -p 8000:8000 file-sharing-api
```

Or use the Makefile:
```bash
make build
make run        # Run in foreground
make run-d      # Run in background (detached)
```

The API will be available at `http://localhost:8000`

## Project Structure

```
file-sharing-api/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI application and routes
│   ├── models.py                   # Pydantic models
│   ├── storage_service.py          # File storage and metadata operations
│   ├── config.py                   # Configuration constants
│   └── storage/
│       ├── files/                  # Stored files directory
│       └── metadata.json           # File metadata storage
├── tests/
│   ├── __init__.py
│   └── test_api.py                 # API tests
├── Dockerfile                      # Docker configuration
├── requirements.txt                # Python dependencies
├── first_chatGPT_question.md       # Question asked to ChatGPT about the design
├── initial_analysis_and_design.md  # Initial Analysis and Design document
└── README.md                       # This file
```

## Configuration

Default configuration (in `app/config.py`):
- **Storage Path**: `app/storage/files`
- **Metadata File**: `app/storage/metadata.json`
- **Max File Size**: 20MB

## Testing

Run tests with pytest:
```bash
pytest
```

