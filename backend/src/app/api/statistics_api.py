from fastapi import APIRouter

statistics_router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)


@statistics_router.get("/get-max-achievements-count-user")
async def get_max_achievements_count_user(
    session
):
    pass


@statistics_router.get("/get-max-achievements-value-user")
async def get_max_achievements_value_user(
    session
):
    pass


@statistics_router.get("/get-max-difference-achievements-value-users")
async def get_max_difference_achievements_value_users(
    session
):
    pass


@statistics_router.get("/get-min-diggerence-achivements-value-users")
async def get_min_diggerence_achivements_value_users(
    session
):
    pass


@statistics_router.get("/get-week-achievement-streak-users")
async def get_week_achievement_streak_users(
    session
):
    pass