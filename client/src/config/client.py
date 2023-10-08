import os

if os.environ.get("is_docker"):
    backend_url = "http://server:8080"
else:
    backend_url = "http://localhost:8080"
