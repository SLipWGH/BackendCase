from fastapi import APIRouter

from app.api.achievements_api import achievements_router
from app.api.user_api import user_router
from app.api.statistics_api import statistics_router


api_router = APIRouter(
    prefix="/api"
)


api_router.include_router(user_router)
api_router.include_router(achievements_router)
api_router.include_router(statistics_router)