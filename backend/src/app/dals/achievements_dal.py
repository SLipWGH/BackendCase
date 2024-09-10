from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.achievements_models import ShowAchievement
from app.tables import Achievement

class AchievementDAL:
    '''Data Access Layer for operating achievement info'''

    def __init__(
        self,
        db_session : AsyncSession
    )-> None:
        self.db_session = db_session
    
    async def create_achievement(
        self,
        name : str,
        value : int,
        description: dict[str]
    )-> Achievement:
        new_achievement = Achievement(
            name=name, 
            value=value,
            description=description
        )
        self.db_session.add(new_achievement)
        await self.db_session.flush()
        return new_achievement

    async def get_all_achievements(
        self
    )-> List[Achievement]:
        query = select(Achievement)
        result = await self.db_session.execute(query)
        return result.scalars().all()
