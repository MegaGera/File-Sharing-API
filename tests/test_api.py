"""Tests for the file-sharing API using FastAPI TestClient."""
import json
import pytest
from fastapi.testclient import TestClient
import shutil
from datetime import datetime

from app.main import app

# Create a test client
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch, tmp_path):
    """Set up test environment with temporary storage."""
    # Create temporary directories
    test_storage = tmp_path / "storage" / "files"
    test_storage.mkdir(parents=True)
    test_metadata = tmp_path / "storage" / "metadata.json"
    
    # Patch the config paths in app.storage_service
    monkeypatch.setattr("app.storage_service.STORAGE_PATH", test_storage)
    monkeypatch.setattr("app.storage_service.METADATA_FILE", test_metadata)
    
    # Reinitialize storage service with new paths
    from app.storage_service import StorageService
    import app.main
    app.main.storage_service = StorageService()
    
    yield
    
    # Cleanup
    if test_storage.exists():
        shutil.rmtree(test_storage.parent)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_upload_file_success():
    """Test successful file upload."""
    # Create a test file
    test_content = b"Test file content"
    files = {"file": ("test.txt", test_content, "text/plain")}
    
    response = client.post("/files", files=files)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["file_name"] == "test.txt"
    assert data["size"] == len(test_content)
    assert "timestamp" in data


def test_upload_file_no_file():
    """Test upload without file."""
    response = client.post("/files")
    assert response.status_code == 422  # FastAPI validation error


def test_upload_file_too_large():
    """Test upload of file exceeding size limit."""
    # Create a file larger than 20MB
    large_content = b"x" * (21 * 1024 * 1024)  # 21MB
    files = {"file": ("large.txt", large_content, "text/plain")}
    
    response = client.post("/files", files=files)
    assert response.status_code == 413


def test_list_files_empty():
    """Test listing files when no files exist."""
    response = client.get("/files")
    assert response.status_code == 200
    assert response.json() == []


def test_list_files_with_uploads():
    """Test listing files after uploads."""
    # Upload a file
    test_content = b"Test content"
    files = {"file": ("test.txt", test_content, "text/plain")}
    upload_response = client.post("/files", files=files)
    assert upload_response.status_code == 201
    file_id = upload_response.json()["id"]
    
    # List files
    response = client.get("/files")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == file_id
    assert data[0]["file_name"] == "test.txt"


def test_download_file_success():
    """Test successful file download."""
    # Upload a file
    test_content = b"Download test content"
    files = {"file": ("download.txt", test_content, "text/plain")}
    upload_response = client.post("/files", files=files)
    assert upload_response.status_code == 201
    file_id = upload_response.json()["id"]
    
    # Download the file
    response = client.get(f"/files/{file_id}")
    assert response.status_code == 200
    assert response.content == test_content


def test_download_file_not_found():
    """Test download of non-existent file."""
    response = client.get("/files/non-existent-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_files_with_invalid_metadata():
    """Test listing files when metadata contains invalid entries."""
    import app.storage_service
    
    # Write invalid metadata directly to the file
    invalid_metadata = [
        {
            "id": "valid-id-1",
            "file_name": "valid.txt",
            "size": 100,
            "timestamp": datetime.now().isoformat()
        },
        {
            "id": "invalid-id-1",
            # Missing required fields
            "file_name": "invalid.txt"
        },
        {
            "id": "invalid-id-2",
            "file_name": "invalid2.txt",
            "size": "not-a-number",  # Wrong type
            "timestamp": datetime.now().isoformat()
        },
        {
            "id": "valid-id-2",
            "file_name": "valid2.txt",
            "size": 200,
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    with open(app.storage_service.METADATA_FILE, 'w') as f:
        json.dump(invalid_metadata, f, indent=2)
    
    # List files - should only return valid entries
    response = client.get("/files")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Only valid entries
    assert data[0]["id"] == "valid-id-1"
    assert data[1]["id"] == "valid-id-2"


def test_get_file_metadata_with_invalid_entry():
    """Test getting file metadata when the entry is invalid."""
    import app.storage_service
    
    # Write invalid metadata for a specific file (using the patched path from fixture)
    invalid_metadata = [
        {
            "id": "invalid-file-id",
            "file_name": "invalid.txt",
            # Missing required 'size' and 'timestamp' fields
        }
    ]
    
    with open(app.storage_service.METADATA_FILE, 'w') as f:
        json.dump(invalid_metadata, f, indent=2)
    
    # Try to download the file - should return 404 because metadata is invalid
    response = client.get("/files/invalid-file-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_files_mixed_valid_invalid_metadata():
    """Test that valid entries are returned even when some entries are invalid."""
    import app.storage_service
    
    # Upload a valid file first
    test_content = b"Valid file content"
    files = {"file": ("valid.txt", test_content, "text/plain")}
    upload_response = client.post("/files", files=files)
    assert upload_response.status_code == 201
    valid_file_id = upload_response.json()["id"]
    
    # Read current metadata and add invalid entries (using the patched path from fixture)
    with open(app.storage_service.METADATA_FILE, 'r') as f:
        metadata_list = json.load(f)
    
    # Add invalid entries
    metadata_list.extend([
        {
            "id": "invalid-1",
            # Missing required fields
        },
        {
            "id": "invalid-2",
            "file_name": "bad.txt",
            "size": "not-a-number",
            "timestamp": "not-a-date"
        }
    ])
    
    with open(app.storage_service.METADATA_FILE, 'w') as f:
        json.dump(metadata_list, f, indent=2)
    
    # List files - should only return the valid entry
    response = client.get("/files")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == valid_file_id
    assert data[0]["file_name"] == "valid.txt"

