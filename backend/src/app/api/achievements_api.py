from fastapi import APIRouter

achievements_router = APIRouter(
    prefix="/achievements",
    tags=["Achievements"]
)


@achievements_router.post("/add-achievement")
async def add_achievement(
    new_achievement,
    session
)-> None:
    pass


@achievements_router.get("/get-achievements-table")
async def get_achievements_table(
    session
):
    pass