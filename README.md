# File Sharing API

A RESTful file-sharing API built with FastAPI that allows users to upload, download, and list files. Files are stored locally with metadata tracking.

## Building process

### Phase 1: Initial Analysis and Design

#### Analysis

After a careful reading of the requirements, I decided to proceed with the Task using python due to the technical requeriments of the position. I decided to use the framework FastAPI because I already have worked with it and is a very good option to build APIs. 

Then I started to work on the analysis of the solution to build, reading the [FastAPI documentation](https://fastapi.tiangolo.com/reference/) and thinking in how I should develop the API ensuring mainly clean code, maintanibility and scalabity.

After doing the initial analysis, I asked to ChatGPT what it thought about it, you can see the prompt #1 in the file [AI_tools_prompts.md](AI_tools_prompts.md#prompt-1---chatgpt-ensure-analysis-and-design). After review the answer, I came with the final design presented in the next sections.

Initial Analysis and Design documentation available in the file [initial_analysis_and_design.md](initial_analysis_and_design.md)

#### Prompt to start building the task

After came with the final design I asked the next prompt tu Cursor, the code editor which I usually use, to start building the task assignment.

You can see the prompt #2 in the file [AI_tools_prompts.md](AI_tools_prompts.md#prompt-2---cursor-build-basic-structure-of-the-project)

Then I carefully reviewed all the created files and code, ensuring that everything met my requirements. After do a first test and see that the endpoints where working correctly, I did the first commit.

### Phase 2: Testing, Volume and Makefile

In this phase, comprehensive testing infrastructure was implemented along with Docker volume support and a Makefile for streamlined development and deployment workflows.

**Testing**: A complete test suite was developed using pytest and FastAPI's TestClient (`tests/test_api.py`). The tests cover all API endpoints with comprehensive scenarios including:
- Successful operations (file upload, download, listing)
- Error handling (422 validation errors, 413 file size limits, 404 not found)
- Edge cases (empty file lists, missing files)
- Test isolation using pytest fixtures with temporary storage directories to ensure tests don't interfere with each other

**Docker Volume**: Persistent storage support was added to ensure data persistence across container restarts. The storage directory (`app/storage`) is configured as a Docker volume in both the Dockerfile and Makefile, allowing uploaded files and metadata to persist even when containers are stopped and restarted.

**Makefile**: A comprehensive Makefile was created to simplify common development and deployment tasks:
- Docker operations: `build`, `run`, `run-d`, `stop`, `rebuild`
- Development commands: `test` (run pytest), `clean` (remove cache files)
- Configurable variables for container name, image name, port, and storage path

Then, I updated this README.md file using Cursor AI tool with the prompt #3 in the file [AI_tools_prompts.md](AI_tools_prompts.md#prompt-3---cursor-update-readmemd)

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
    - `422`: No file provided # FastAPI validation
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

FileMetadata model used when retrieve the list of files or when a new file is upload:

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

## Makefile Commands

The project includes a Makefile for convenient Docker operations, testing, and cleanup. All commands can be run with `make <command>`.

### Docker Commands

- **`make build`**: Build the Docker image
  ```bash
  make build
  ```

- **`make run`**: Run the container in foreground with persistent storage volume
  ```bash
  make run
  ```
  The storage directory (`app/storage`) is mounted as a volume to persist data between container restarts.

- **`make run-d`**: Run the container in background (detached mode) with persistent storage volume
  ```bash
  make run-d
  ```

- **`make stop`**: Stop and remove the running container
  ```bash
  make stop
  ```

- **`make rebuild`**: Rebuild the Docker image from scratch (no cache) and stop existing container
  ```bash
  make rebuild
  ```

### Development Commands

- **`make test`**: Run all tests locally using pytest with verbose output
  ```bash
  make test
  ```

- **`make clean`**: Clean up Python cache files (`__pycache__` directories) and pytest cache
  ```bash
  make clean
  ```

### Makefile Variables

The Makefile uses the following default variables (can be overridden):
- `APP_NAME`: `file-sharing-api` (container name)
- `IMAGE_NAME`: `file-sharing-api` (Docker image name)
- `PORT`: `8000` (host port mapping)
- `STORAGE_PATH`: `$(pwd)/app/storage` (persistent storage path)

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

The project includes comprehensive test coverage using pytest and FastAPI's TestClient. Tests use temporary storage directories to ensure isolation between test runs.

### Running Tests

Run all tests with Makefile:
```bash
make test
```

Run all tests with pytest:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

### Test Coverage

The test suite (`tests/test_api.py`) includes the following test cases:

#### Root Endpoint Tests
- **test_root_endpoint**: Verifies the root endpoint returns a 200 status code with message and version information

#### File Upload Tests
- **test_upload_file_success**: Tests successful file upload with proper metadata generation (ID, filename, size, timestamp)
- **test_upload_file_no_file**: Tests upload endpoint validation when no file is provided (422 status)
- **test_upload_file_too_large**: Tests file size validation for files exceeding the 20MB limit (413 status)

#### File Listing Tests
- **test_list_files_empty**: Tests listing files when no files have been uploaded (returns empty array)
- **test_list_files_with_uploads**: Tests listing files after successful uploads, verifying correct metadata is returned

#### File Download Tests
- **test_download_file_success**: Tests successful file download by file ID, verifying file content matches uploaded content
- **test_download_file_not_found**: Tests download endpoint error handling for non-existent file IDs (404 status)

All tests use pytest fixtures to set up isolated temporary storage directories, ensuring tests don't interfere with each other or the actual application storage.

