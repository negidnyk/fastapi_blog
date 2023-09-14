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

class LikesListOut(BaseModel):
    like_id: int
    creator: UserGetsUser
