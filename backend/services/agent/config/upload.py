import os
import time
from pathlib import Path

from fastapi import UploadFile

# Mirror of config/multer.js: disk storage in ./temp, image/pdf only, 20MB cap.
UPLOAD_DIR = Path("./temp").resolve()
print("uploadDir", UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 20 * 1024 * 1024


async def save_upload(upload: UploadFile):
    """Save an uploaded file the way multer does; returns the req.file shape."""
    mimetype = upload.content_type or ""
    if not (mimetype.startswith("image/") or mimetype == "application/pdf"):
        raise Exception("Only pdf and image files are allowed")
    data = await upload.read()
    if len(data) > MAX_FILE_SIZE:
        raise Exception("File too large")
    path = UPLOAD_DIR / f"{int(time.time() * 1000)}-{upload.filename}"
    path.write_bytes(data)
    return {
        "path": str(path),
        "mimetype": mimetype,
        "originalname": upload.filename,
    }
