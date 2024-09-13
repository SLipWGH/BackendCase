from datetime import datetime
from enum import Enum
from uuid import UUID
from typing import List, TypedDict, Annotated

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator, StringConstraints


class PreferedLanguage(Enum):
    RUSSIAN = 'Русский'
    ENGLISH = 'English'

class TunedModel(BaseModel):
    class Config:

        from_attributes = True


class ShowUser(TunedModel):
    user_id: UUID
    username: str
    prefered_language: PreferedLanguage 


class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=64, description="username length must be between 3 and 64 characters")]
    prefered_language: Annotated[PreferedLanguage, Field(description="language must be 'ru' or 'en'")]



class AddUserAchievement(BaseModel):
    user_id: UUID
    achievement_name: Annotated[str, Field(min_length=4, max_length=128)]


class UserAchievement(TunedModel):
    achievement_name: str
    achievement_value: int
    achievement_description: str
    achievement_date: datetime


class ShowUserAchievements(TunedModel):
    user_achievements: list[UserAchievement]
