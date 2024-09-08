from fastapi import APIRouter

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@user_router.post("/add-user")
async def add_new_user(
    user,
    session
)-> None:
    pass


@user_router.post("/add-user-achievement")
async def add_user_achievement(
    user,
    achievement,
    session,
)-> None:
    pass


@user_router.get("/get-user-data")
async def get_user_data(
    user,
    session
):
    pass


@user_router.get("/get-user-achievements-data")
async def get_user_achievements_data(
    user,
    session
):
    pass