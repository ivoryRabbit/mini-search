from fastapi import APIRouter

from api.router import ping, search

router = APIRouter()

router.include_router(router=ping.router, prefix="", tags=["ping"])

router.include_router(router=search.router, prefix="/search", tags=["search"])

