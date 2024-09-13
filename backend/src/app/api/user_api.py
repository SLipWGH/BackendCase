from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.dals.user_dal import UserDAL
from app.models.user_models import UserCreate, ShowUser, AddUserAchievement, UserAchievement, ShowUserAchievements
from app.database import get_async_session
from pydantic import UUID4

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@user_router.post("/", response_model=ShowUser)
async def create_user(
    body: UserCreate,
    session: AsyncSession = Depends(get_async_session)
)-> ShowUser:
    return await _create_new_user(body, session)


@user_router.put("/achievements")
async def add_user_achievement(
    body: AddUserAchievement,
    session: AsyncSession = Depends(get_async_session),
)-> None:
    return await _add_user_achievement(body, session)


@user_router.get("/{user_id}")
async def get_user_data(
    user_id : UUID,
    session: AsyncSession = Depends(get_async_session)
):
    return await _get_user_data(user_id, session)


@user_router.get("/achievements/{user_id}")
async def get_user_achievements(
    user_id : str,
    session: AsyncSession = Depends(get_async_session)
):
    user_id = await validate_uuid(user_id)
    return await _get_user_achievements(user_id, session)


async def _create_new_user(
    body: UserCreate,
    session: AsyncSession
)-> ShowUser:
    async with session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                username=body.username,
                prefered_language=body.prefered_language.value
            )
            return ShowUser(
                user_id=user.id,
                username=user.username,
                prefered_language=user.prefered_language
            )
        

async def _add_user_achievement(
    body: AddUserAchievement,
    session: AsyncSession
)-> None:
    async with session:
        async with session.begin():
            user_dal = UserDAL(session)
            await user_dal.add_user_achievement_(
                user_id=body.user_id,
                achievement_name=body.achievement_name
            )


async def _get_user_data(
    user_id: UUID,
    session: AsyncSession
)-> ShowUser:
    async with session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(user_id)
            return ShowUser(
                user_id=user_id,
                username=user.username,
                prefered_language=user.prefered_language        
            )
            

async def _get_user_achievements(
    user_id: UUID,
    session: AsyncSession
)-> ShowUserAchievements:
    async with session:
        async with session.begin():
            user_dal = UserDAL(session)
            result, lang = await user_dal.get_user_achievements_list(user_id) 
            user_achievements = []
            for user_achievement in result:
                date, achievement = user_achievement
                user_achievements.append(
                    UserAchievement(
                        achievement_name=achievement.name,
                        achievement_value=achievement.value,
                        achievement_description=achievement.description[lang],
                        achievement_date=date
                    )
                )
            return ShowUserAchievements(user_achievements=user_achievements)


async def validate_uuid(
    uuid: str
)-> UUID:
    try:
        id_validated =  UUID(uuid)
    except ValueError as e:
            return JSONResponse(
            status_code=400,
            content={"message": f"Oops! your streem id is not a valid UUID..."},
        )
    return id_validated
    