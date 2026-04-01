from fastapi import APIRouter, UploadFile, File
import shutil
import os
from app.services.ingestion_service import ingest
import time

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        os.makedirs("data", exist_ok=True)
        timestamp = int(time.time())
        file_path = f"data/{timestamp}_{file.filename}"
    except Exception as e:
        print(e)
        return "building directory failed"
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        print(e)
        return "File writing failed."
    return ingest(file_path)
