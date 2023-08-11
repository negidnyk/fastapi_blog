from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing import List, Tuple, Optional
from datetime import datetime, time, timedelta
from uuid import UUID
from auth.schemas import UserRead
# from sqlalchemy.sql import func
from files.schemas import MediaOut
from auth.schemas import UserGetsUser


# func.now()


class CreatePost(BaseModel):
    file_id: int = None
    title: str = Field(max_length=1500, example="My awesome post!")
    description: str = Field(max_length=1500, example="Some text to be attached to the post")


class PostCreator(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BasePost(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    is_liked: bool
    likes_count: int
    comments_count: int

    class Config:
        orm_mode = True


class PostOut(BasePost):
    creator: UserGetsUser
    media: MediaOut
    # media: MediaOut

    class Config:
        orm_mode = True


