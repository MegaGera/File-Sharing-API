# Variables
APP_NAME=file-sharing-api
IMAGE_NAME=file-sharing-api
PORT=8000
STORAGE_PATH=$(shell pwd)/app/storage

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the container with persistent storage
run:
	docker run --name $(APP_NAME) -p $(PORT):8000 -v $(STORAGE_PATH):/app/app/storage $(IMAGE_NAME)

# Run in background (detached) with persistent storage
run-d:
	docker run -d --name $(APP_NAME) -p $(PORT):8000 -v $(STORAGE_PATH):/app/app/storage $(IMAGE_NAME)

# Stop and remove the container
stop:
	docker stop $(APP_NAME) || true
	docker rm $(APP_NAME) || true

# Rebuild from scratch
rebuild: stop
	docker build --no-cache -t $(IMAGE_NAME) .

# Run tests locally (not in Docker)
test:
	pytest -v

# Clean __pycache__, pytest cache etc
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .pytest_cache