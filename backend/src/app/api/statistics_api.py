
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.user_models import ShowUser
from app.dals.statistics_dal import StatisticsDAL

statistics_router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)


@statistics_router.get("/get-max-achievements-count-user")
async def get_max_achievements_count_user(
    session: AsyncSession = Depends(get_async_session)
)-> ShowUser:
    return await _get_user_with_max_achievements_count(session)


@statistics_router.get("/get-max-achievements-value-user")
async def get_max_achievements_value_user(
    session: AsyncSession = Depends(get_async_session)
)-> ShowUser:
    return await _get_user_with_max_achievements_value_summ(session)


@statistics_router.get("/get-max-difference-achievements-value-users")
async def get_max_difference_achievements_value_users(
    session: AsyncSession = Depends(get_async_session)
)-> tuple[ShowUser, ShowUser]:
    return await _get_user_with_max_achievements_value_summ(session)


@statistics_router.get("/get-min-difference-achivements-value-users")
async def get_min_difference_achivements_value_users(
    session: AsyncSession = Depends(get_async_session)
)-> tuple[ShowUser, ShowUser]:
    return await _get_users_with_min_achievements_value_difference(session)


@statistics_router.get("/get-week-achievement-streak-users")
async def get_week_achievement_streak_users(
    session: AsyncSession = Depends(get_async_session)
)-> list[ShowUser]:
    return await _get_week_achievement_streak_users(session)


async def _get_user_with_max_achievements_count(
    session: AsyncSession
)-> ShowUser:
    async with session:
        async with session.begin():
            statistics_dal = StatisticsDAL(session)
            user = await statistics_dal.get_max_achievements_user()
            return ShowUser(
                user_id=user.id,
                username=user.username,
                prefered_language=user.prefered_language
            )
        

async def _get_user_with_max_achievements_value_summ(
    session: AsyncSession
)-> ShowUser:
    async with session:
        async with session.begin():
            statistics_dal = StatisticsDAL(session)
            user = await statistics_dal.get_max_achievements_value_sum_user()
            return ShowUser(
                user_id=user.id,
                username=user.username,
                prefered_language=user.prefered_language
            )


async def _get_users_with_min_achievements_value_difference(
    session: AsyncSession
)-> tuple[ShowUser, ShowUser]:
    async with session:
        async with session.begin():
            statistics_dal = StatisticsDAL(session)
            user1, user2 = await statistics_dal.users_with_min_achievements_value_difference()
            return (
                ShowUser(
                    user_id=user1.id,
                    username=user1.username,
                    prefered_language=user1.prefered_language
                ),
                ShowUser(
                    user_id=user2.id,
                    username=user2.username,
                    prefered_language=user2.prefered_language
                )
            )


async def _get_week_achievement_streak_users(
    session: AsyncSession
)-> list[ShowUser]:
    async with session:
        async with session.begin():
            statistics_dal = StatisticsDAL(session)
            result = await statistics_dal.get_week_achievement_streak_users()
            users = []
            for user in result:
                users.append(ShowUser(
                    user_id=user.user_id,
                    username=user.username,
                    prefered_language=user.prefered_language
                ))

            return users

