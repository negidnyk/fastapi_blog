from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing import List, Tuple
from datetime import datetime, time, timedelta
from uuid import UUID
from auth.schemas import UserRead
# from sqlalchemy.sql import func

# func.now()


class CreatePost(BaseModel):
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

    class Config:
        orm_mode = True


class PostOut(BasePost):
    creator: PostCreator

    class Config:
        orm_mode = True


