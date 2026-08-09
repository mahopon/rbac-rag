import logging

from fastapi import APIRouter
from src.pdf import pdf_router
# from src.modules.auth.router import router as auth_router

logger = logging.getLogger(__name__)

router = APIRouter()

router.include_router(pdf_router)


@router.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}
# router.include_router(auth_router, prefix="/auth")
