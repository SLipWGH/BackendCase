from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.tables import User, Achievement, UsersAchievements

class UserDAL:
    '''Data Access Layer for operating user info'''

    def __init__(
        self,
        db_session : AsyncSession
    ) -> None:
        self.db_session = db_session
    
    async def create_user(
        self,
        username : str,
        prefered_language : str
    ) -> User:
        new_user = User(
            username=username, 
            prefered_language=prefered_language
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
    
    async def add_user_achievement_(
        self,
        user_id: UUID,
        achievement_name: str
    )-> None:
        new_user_achievement = UsersAchievements(
            user_id=user_id,
            achievement_name=achievement_name
        )
        self.db_session.add(new_user_achievement)
        await self.db_session.flush()
    

    async def get_user_by_id(
        self, 
        user_id: UUID
    )-> User:
        return await self.db_session.get(User, user_id)


    async def get_user_achievements_list(
        self,
        user_id: UUID
    )-> tuple[list[tuple], str]:
        
        # query = (
        #     select(Achievement)
        #     .options(selectinload(Achievement.users_with_achievement))
        #     .where(User.id == user_id)
        # )
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        # result = await self.db_session.execute(query)
        
        
        query = (
            select(UsersAchievements.date, Achievement)
            .join(Achievement, UsersAchievements.achievement_name == Achievement.name)
            .where(UsersAchievements.user_id == user_id)
        )
        result = await self.db_session.execute(query)
        
        lang = await self.db_session.execute(
            select(User.prefered_language)
            .select_from(User)
            .where(User.id == user_id)
        )

        return (result, lang.scalar_one())