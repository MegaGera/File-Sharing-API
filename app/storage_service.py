"""Service for handling file storage and metadata operations."""
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from fastapi import HTTPException, UploadFile
from pydantic import ValidationError

from app.config import STORAGE_PATH, METADATA_FILE, MAX_FILE_SIZE
from app.models import FileMetadata


class StorageService:
    """Service class for file storage operations."""
    
    def __init__(self):
        """Initialize the storage service."""
        self._ensure_metadata_file_exists()
    
    def _ensure_metadata_file_exists(self):
        """Ensure metadata.json file exists with empty list."""
        if not METADATA_FILE.exists():
            self._write_metadata([])
    
    def _read_metadata(self) -> List[dict]:
        """Read metadata from JSON file."""
        try:
            with open(METADATA_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _write_metadata(self, metadata_list: List[dict]):
        """Write metadata to JSON file."""
        with open(METADATA_FILE, 'w') as f:
            json.dump(metadata_list, f, indent=2, default=str)
    
    def upload_file(self, file: UploadFile) -> FileMetadata:
        """Upload a file and save its metadata.
        
        Args:
            file: The uploaded file (validated by FastAPI)
            
        Returns:
            FileMetadata object with file information
            
        Raises:
            HTTPException: If file is missing or too large
        """        
        # Read file content to check size
        content = file.file.read()
        file_size = len(content)
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024 * 1024)}MB"
            )
        
        # Generate unique ID
        file_id = str(uuid.uuid4())
        
        # Save file to disk
        # Save name as generated ID
        file_path = STORAGE_PATH / file_id
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Create metadata
        metadata = FileMetadata(
            id=file_id,
            file_name=file.filename,
            size=file_size,
            timestamp=datetime.now()
        )
        
        # Save metadata
        metadata_list = self._read_metadata()
        metadata_list.append(metadata.model_dump(mode='json'))
        self._write_metadata(metadata_list)
        
        return metadata
    
    def get_file(self, file_id: str) -> Optional[Path]:
        """Get file path by ID.
        
        Args:
            file_id: The file ID
            
        Returns:
            Path to the file if exists, None otherwise
        """
        file_path = STORAGE_PATH / file_id
        if file_path.exists():
            return file_path
        return None
    
    def get_all_metadata(self) -> List[FileMetadata]:
        """Get metadata for all files.
        
        Returns:
            List of FileMetadata objects (invalid entries are skipped)
        """
        metadata_list = self._read_metadata()
        valid_metadata = []
        for item in metadata_list:
            try:
                valid_metadata.append(FileMetadata(**item))
            except ValidationError:
                # Skip invalid metadata entries silently
                continue
        return valid_metadata
    
    def get_file_metadata(self, file_id: str) -> Optional[FileMetadata]:
        """Get metadata for a specific file.
        
        Args:
            file_id: The file ID
            
        Returns:
            FileMetadata if found and valid, None otherwise
        """
        metadata_list = self._read_metadata()
        for item in metadata_list:
            if item.get('id') == file_id:
                try:
                    return FileMetadata(**item)
                except ValidationError:
                    # Return None for invalid metadata entries
                    return None
        return None

