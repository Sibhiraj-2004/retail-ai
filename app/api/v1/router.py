from fastapi import APIRouter
from app.api.v1.endpoints import upload, query

router = APIRouter()
router.include_router(upload.router, prefix="/api/v1")
router.include_router(query.router, prefix="/api/v1")
