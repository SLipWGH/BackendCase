from uuid import uuid4
from typing import Annotated
from enum import Enum

from sqlalchemy import ForeignKey, String, Integer, JSON, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class PreferedLanguage(Enum):
    RUSSIAN = 'ru'
    ENGLISH = 'en'


class Base(DeclarativeBase):
    type_annotation_map = {
        dict[PreferedLanguage, str]: JSON
    }


class User(Base):
    __tablename__ = "users_table"


    id : Mapped[uuid4] = mapped_column(Uuid(), primary_key=True)
    username : Mapped[str] = mapped_column(String(64))
    prefered_language : Mapped[PreferedLanguage]


class Achievements(Base):
    __tablename__ = 'achievements_table'

    name : Mapped[str] = mapped_column(String(256), primary_key=True)
    value : Mapped[int]
    desctiprion : Mapped[dict[PreferedLanguage, str]]

