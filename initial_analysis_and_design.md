# API Initial Analysis And Design - 1h

## Analysis

After a careful reading of the requirements, I decided to proceed with the Task using python due to the technical requeriment of the position. I decided to use the framework FastAPI because I already have worked with it and is a very good option to build APIs. 

Then I started to work on the analysis of the solution to build, reading the [FastAPI documentation](https://fastapi.tiangolo.com/reference/) and thinking in how I should develop the API ensuring mainly clean code, maintanibility and scalabity.

After doing the initial analysis, I asked to ChatGPT what it thought about it, you can see the prompt in the file [first_chatGPT_question.md](first_chatGPT_question.md). After review the answer, I came with the final design presented in the next sections.

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

## Prompt to start building the task

After came with the final design I asked the next prompt tu Cursor, the code editor which I usually use, to start building the task assignment.

```
This file @initial_analysis_and_design.md contains the  initial analysis and design I did for a Software task assignment I need to develop a minimal and lightweight file-sharing API that supports uploads and downloads, storesfiles on disk, read metadata list of files, and makes it easy to retrieve shared files via a simple HTTP endpoint.

Can you help me to build the basic structure of the project based on the content of the file?
```

Then I carefully reviewed all the created files and code, ensuring that everything met my requirements. After do a first test and see that the endpoints where working, I do the initial commit.