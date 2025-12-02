# Prompt 1 - ChatGPT: Ensure Analysis and Design

After analysis I made this question to ChatGPT to ensure the design:

```
For a Software task assignment I need to develop a minimal and lightweight file-sharing API that supports uploads and downloads, storesfiles on disk, read metadata list of files, and makes it easy to retrieve shared files via a simple HTTP endpoint. I'm going to share with you my initial analysis, I would like you to help me to finish the desing before I start to build it. Let me know if the approach is correct, highlight any weaknesses and suggest improvements to ensure the code and design are clean, scalable and maintainable.

Initial analysis:

- Framework: FastAPI - Python

- Endpoints:
    - POST: upload_file (multipart/form-data) returning an ID
         - 200 Ok
         - 400 No File
         - 413 Too Large
    - GET: download_file (multipart/form-data) with ID
         - 200 Ok
         - 400 No ID
         - 404 No File Found
    - GET: list_metadata (json)
         - 200 Ok
         - 400 No ID
         - 404 No File Found

- File Metadata as Pydantic Model:
   - ID
   - file_name
   - size in bytes
   - upload timestamp

- Constraints: 
   - Max 20MB of files

- Testing with TestClient of FastAPI

- Development server with uvicorn

- Deploy with Docker

- File-sharing service to handle logic

- Config file for:
   - STORAGE_PATH
   - METADATA_FILE
   - MAX_FILE_SIZE
```

# Prompt 2 - Cursor: Build basic structure of the project

Build the project files structure after design phase is finished:

```
This file @initial_analysis_and_design.md contains the  initial analysis and design I did for a Software task assignment I need to develop a minimal and lightweight file-sharing API that supports uploads and downloads, storesfiles on disk, read metadata list of files, and makes it easy to retrieve shared files via a simple HTTP endpoint.

Can you help me to build the basic structure of the project based on the content of the file?
```

# Prompt 3 - Cursor: Update README.md

Update README.md after build phase 2:

```
Can you update the @README.md file with:

- Testing part with the actual tests I have implemented.
- Create a section about the Makefile.
- Add a Phase 2 in the Building Process of what I did in this phase.
```