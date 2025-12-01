"""Pydantic models for file metadata."""
from datetime import datetime
from pydantic import BaseModel


class FileMetadata(BaseModel):    
    id: str
    file_name: str
    size: int  # in bytes
    timestamp: datetime

