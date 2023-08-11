from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing import List, Tuple
from datetime import datetime, time, timedelta
from uuid import UUID
from auth.schemas import UserRead
# from sqlalchemy.sql import func

# func.now()
from files.schemas import MediaOut


class CreateComment(BaseModel):
    text: str = Field(max_length=500, example="Some comment to be added")


class CommentCreator(BaseModel):
    id: int
    username: str
    avatar: MediaOut

    class Config:
        orm_mode = True

class PostCommentsOut(BaseModel):
    id: int
    user: CommentCreator
    text: str
    created_at: datetime


