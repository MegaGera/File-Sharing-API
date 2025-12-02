# API Initial Analysis And Design

## Framework
- FastAPI - Python

## Endpoints

### POST: /files (multipart/form-data)
- `201` Ok // return ID
- `400` No File
- `413` Too Large

### GET: /files/{file_id}
- `200` Ok // return file
- `404` No File Found

### GET: /files
- `200` Ok // return metadata json

### Exceptions
- Use class `HTTPException`

## File Metadata (Pydantic Model)
- ID // generated when uploaded
- file_name
- size // in bytes
- timestamp // upload timestamp

## Constraints
- Max 20MB of files
- Store files in disk
- Store metadata in json file

## Architecture
- Main file to init FastAPI and route
- File sharing service to handle logic

## Testing
- Testing with TestClient of FastAPI

## Development
- Development server with uvicorn

## Deployment
- Deploy with Docker

## Configuration
Config file for:
- STORAGE_PATH
- METADATA_FILE
- MAX_FILE_SIZE

## File Structure

```
file-sharing-api/
│
├── app/
│   ├── main.py                # FastAPI app + routes
│   ├── models.py              # Pydantic models
│   ├── config.py              # Constants
│   ├── storage_service.py     # Service that handles files logic
│   ├── storage/
│   │   ├── files/             # Uploaded files stored here
│   │   └── metadata.json      # Metadata stored here
│
├── tests/
│   └── test_api.py            # Tests using TestClient
│
├── Dockerfile                 # Docker image definition
└── requirements.txt           # Dependencies
```
