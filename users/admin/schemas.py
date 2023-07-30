from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
# from sqlalchemy.sql import func
from datetime import datetime, time, timedelta
from uuid import UUID


# func.now()


class BaseUser(BaseModel):
    email: EmailStr
    name: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "example@gmail.com",
                "name": "John Doe",
                "password": "Qwerty123"
            }
        }


class UserOut (BaseModel):
    id: int
    email: EmailStr
    name: str
    role: int
    created_at: datetime
