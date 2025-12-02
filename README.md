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

### Phase 3: Metadata validation Testing

In this phase I added a metadata validation handling exception in case the metadata JSON is not correctly stored. In that case, when listing metadata it will skip the invalid objects and when getting a file with invalid metadata it will return a 404 error code (not found). I added 3 more tests to validate this behaviour:

- `test_list_files_with_invalid_metadata`: Verifies that invalid entries are skipped when listing files
- `test_get_file_metadata_with_invalid_entry`: Verifies that invalid metadata returns 404
- `test_list_files_mixed_valid_invalid_metadata`: Verifies that valid entries are still returned when mixed with invalid ones

I added this validation and the new tests asking Cursor with the prompt #4 in the file [AI_tools_prompts.md](AI_tools_prompts.md#prompt-4---cursor-metadata-validation-testing)

### Task Questions

#### What happens if something goes wrong during a request? How does the API communicate this to a client?

The API uses FastAPI's built-in error handling mechanism with `HTTPException` to communicate errors to clients. Errors are returned as JSON responses with appropriate HTTP status codes:

- **422 Unprocessable Entity**: Validation errors (e.g., no file provided in upload request). FastAPI automatically validates request parameters and returns detailed validation error messages.

- **413 Payload Too Large**: File size exceeds the 20MB limit. The error message includes details about the maximum allowed size.

- **404 Not Found**: Requested file ID doesn't exist or has invalid metadata. Returns a JSON response with a descriptive error message.

- **500 Internal Server Error**: Unexpected server errors during file operations. Includes error details in the response.

All error responses follow FastAPI's standard error format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

The API also handles edge cases gracefully:
- Invalid metadata entries are automatically skipped when listing files
- Missing or corrupted metadata files are handled without crashing the service
- File validation ensures data integrity before storing

#### How can you confirm the code works?

The codebase includes a comprehensive test suite using `pytest` and FastAPI's `TestClient`. To confirm the code works:

1. **Run all tests using Makefile**:
   ```bash
   make test
   ```

2. **Run tests directly with pytest**:
   ```bash
   pytest
   pytest -v  # for verbose output
   ```

The test suite (`tests/test_api.py`) covers:
- ✅ All API endpoints (root, upload, download, list)
- ✅ Success scenarios with proper data validation
- ✅ Error handling (422, 413, 404, 500)
- ✅ Edge cases (empty file lists, invalid metadata, missing files)
- ✅ Test isolation using temporary storage directories

All tests use pytest fixtures to ensure complete isolation - each test runs with its own temporary storage, preventing interference between test runs and with actual application data.

#### How can someone else run and test the API quickly?

There are multiple quick ways to run and test the API:

**Option 1: Docker with Makefile (Recommended - Fastest)**

```bash
# Build and run the container
make build
make run-d    # Runs in background

# Or run in foreground to see logs
make run
```

The API will be available at `http://localhost:8000`

**Option 2: Docker commands directly**

```bash
docker build -t file-sharing-api .
docker run -p 8000:8000 file-sharing-api
```

**Option 3: Local Python setup**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

**Testing the API:**

Once running, you can test it in several ways:

1. **Interactive API Documentation** (Swagger UI):
   - Visit `http://localhost:8000/docs` in your browser
   - Test all endpoints directly from the browser interface
   - Upload, download, and list files with a user-friendly UI

2. **Command line with curl**:
   ```bash
   # Upload a file
   curl -X POST "http://localhost:8000/files" \
        -F "file=@/path/to/your/file.txt"
   
   # List all files
   curl http://localhost:8000/files
   
   # Download a file (replace FILE_ID with actual ID)
   curl http://localhost:8000/files/FILE_ID --output downloaded_file.txt
   ```

3. **Run the test suite**:
   ```bash
   make test
   ```

### Notes, Considerations and Future Updates

- I chose to build the task with Python and FastAPI due to the technical requeriments of the position/offer
- I store the metadata in a simple JSON file because is enough for a minimal app like this task
- When storing the files I change the names in disk to be the new generated UUID. With this approach multiple files with the same name can be uploaded
- I chose Docker and Makefile to simplify development and deploying and improve scalability and maintainability

#### Future Updates

- Delete file
- Logging for all operations. New file/table with the logs
- Public/Private keys for authentication
- History of downloads of the files by different users
- Add metadata in a DB instead of simple JSON file. Run app and DB with docker-compose
- Serverless file to deploy in file with, for example AWS, S3 for file storage, DynamoDB for metadata storage, and API Gateway with Lambda for running the API and the file storage logic

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

#### Metadata Validation Tests
- **test_list_files_with_invalid_metadata**: Verifies that invalid metadata entries are skipped when listing files, ensuring only valid entries are returned
- **test_get_file_metadata_with_invalid_entry**: Verifies that files with invalid metadata return a 404 error (not found) when attempting to download
- **test_list_files_mixed_valid_invalid_metadata**: Verifies that valid metadata entries are still returned correctly when mixed with invalid entries in the metadata file

All tests use pytest fixtures to set up isolated temporary storage directories, ensuring tests don't interfere with each other or the actual application storage.

## Author

Gonzalo Berné - gonzalo.berne@gmail.com