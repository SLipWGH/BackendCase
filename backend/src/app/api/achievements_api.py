
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.database import get_async_session
from app.dals.achievements_dal import AchievementDAL
from app.models.achievements_models import AchievementCreate, ShowAchievement


achievements_router = APIRouter(
    prefix="/achievements",
    tags=["Achievements"]
)


@achievements_router.post("/")
async def create_achievement(
    body: AchievementCreate,
    session = Depends(get_async_session)
)-> ShowAchievement:
    return await _create_new_achievement(body, session)


@achievements_router.get("/")
async def get_achievements(
    session = Depends(get_async_session)
)-> List[ShowAchievement]:
    return await _get_all_achievements(session)


async def _create_new_achievement(
    body: AchievementCreate,
    session: AsyncSession
)-> ShowAchievement:
    async with session:
        async with session.begin():
            achievement_dal = AchievementDAL(session)
            achievement = await achievement_dal.create_achievement(
                name=body.name,
                value=body.value,
                description=body.description
            )
            return ShowAchievement(
                name=achievement.name,
                value=achievement.value,
                description=achievement.description
            )
        

async def _get_all_achievements(
    session: AsyncSession
)-> List[ShowAchievement]:
    async with session:
        async with session.begin():
            achievement_dal = AchievementDAL(session)
            result_orm = await achievement_dal.get_all_achievements()
            achievement_list = [
                ShowAchievement.model_validate(
                row, 
                from_attributes=True
            ) 
            for row in result_orm
        ]
        return achievement_list
