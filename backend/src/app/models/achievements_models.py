from uuid import UUID
from typing import Annotated
from typing_extensions import TypedDict

from pydantic import BaseModel, StringConstraints, Field


class Description(TypedDict):
    ru : Annotated[str, StringConstraints(max_length=256)]
    en : Annotated[str, StringConstraints(max_length=256)]


class TunedModel(BaseModel):
    class Config:

        from_attributes = True


class ShowAchievement(TunedModel):
    name: str
    value: int
    description: Description 


class AchievementCreate(BaseModel):
    name: Annotated[str, Field(min_length=4, max_length=128)]
    value: Annotated[int, Field(ge=0)]
    description: Annotated[Description, Field(
        min_length=2, 
        max_length=2, 
        description="the description must be written in both Russian and English, up to 256 characters each"
        )
    ]





