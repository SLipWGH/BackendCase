import datetime
import uuid
from typing import Annotated, Literal


from sqlalchemy import func, String, JSON, UUID, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


PreferedLanguage = Literal['Русский', 'English']

timestamp = Annotated[
    datetime.datetime,
    mapped_column(
        nullable=False, 
        server_default=func.CURRENT_TIMESTAMP()
    )
]

pkuuid = Annotated[
    uuid.UUID,
    mapped_column(
        UUID(), 
        primary_key=True, 
        default=uuid.uuid4, 
        nullable=False
    )
]

class Base(DeclarativeBase):
    type_annotation_map = {
        dict[PreferedLanguage, str]: JSON,
    }

    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self,col)}")
        return f"<{self.__class__.__name__} {','.join(cols)}"


class User(Base):
    __tablename__ = "users_table"

    id : Mapped[pkuuid]
    username : Mapped[str] = mapped_column(String(64), nullable = False, unique=True)
    prefered_language : Mapped[PreferedLanguage] = mapped_column(nullable=False)


class Achievement(Base):
    __tablename__ = 'achievements_table'

    name : Mapped[str] = mapped_column(String(128), primary_key=True, nullable=False)
    value : Mapped[int]
    description : Mapped[dict[PreferedLanguage, str]] 


class UsersAchievements(Base):
    __tablename__ = 'users_achievements_table'

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users_table.id", 
            ondelete="CASCADE", 
            onupdate="CASCADE"
        ), 
        nullable=False,
        primary_key=True
    )
    achievement_name: Mapped[str] = mapped_column(
        String(64), 
        ForeignKey(
            "achievements_table.name", 
            ondelete="CASCADE", 
            onupdate="CASCADE"
        ), 
        nullable=False,
        primary_key=True
    )
    date: Mapped[timestamp]




