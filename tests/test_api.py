"""Tests for the file-sharing API using FastAPI TestClient."""
import pytest
from fastapi.testclient import TestClient
import shutil

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

