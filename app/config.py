"""Configuration constants for the file-sharing API."""
from pathlib import Path

# Base directory for the app
BASE_DIR = Path(__file__).parent

# Storage configuration
STORAGE_PATH = BASE_DIR / "storage" / "files"
METADATA_FILE = BASE_DIR / "storage" / "metadata.json"

# File size constraints
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB in bytes

# Ensure storage directories exist
STORAGE_PATH.mkdir(parents=True, exist_ok=True)
METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)

