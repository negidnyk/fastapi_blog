from pydantic import BaseModel
# from sqlalchemy.sql import func
from src.auth.schemas import UserGetsUser


# func.now()

class LikesListOut(BaseModel):
    like_id: int
    creator: UserGetsUser
