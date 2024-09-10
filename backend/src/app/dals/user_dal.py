from sqlalchemy.ext.asyncio import AsyncSession

from app.tables import User

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