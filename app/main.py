"""FastAPI application with file-sharing endpoints."""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import List

from app.models import FileMetadata
from app.storage_service import StorageService

title = "File Sharing API"
version = "0.1.0"

app = FastAPI(title=title, version=version)

# Initialize storage service
storage_service = StorageService()

@app.post("/files", response_model=FileMetadata, status_code=201)
async def upload_file(file: UploadFile = File(...)):
    """Upload a file.
    
    Returns:
        FileMetadata with file ID and information
        
    Raises:
        HTTPException: 400 if no file provided, 413 if file too large
    """
    try:
        metadata = storage_service.upload_file(file)
        return metadata
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@app.get("/files/{file_id}")
async def download_file(file_id: str):
    """Download a file by ID.
    
    Args:
        file_id: The unique file identifier
        
    Returns:
        FileResponse with the file content
        
    Raises:
        HTTPException: 404 if file not found
    """
    # Get file path by ID
    file_path = storage_service.get_file(file_id)
    
    # Get metadata to verify if file exists
    metadata = storage_service.get_file_metadata(file_id)
    
    # If file path or metadata is not found, raise 404 error
    if not file_path or not metadata:
        raise HTTPException(status_code=404, detail="File not found")

    # Get original filename from metadata
    filename = metadata.file_name
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type='application/octet-stream'
    )


@app.get("/files", response_model=List[FileMetadata])
async def list_files():
    """Get metadata for all uploaded files.
    
    Returns:
        List of FileMetadata objects
    """
    return storage_service.get_all_metadata()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": title, "version": version}

