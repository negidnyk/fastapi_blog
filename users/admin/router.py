from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from posts.schemas import CreatePost
from auth.schemas import UserRead, GetUser
from posts.models import Post
from posts.schemas import CreatePost
from database import get_async_session
from typing import List
from auth.base_config import fastapi_users
from auth.models import User
from users.admin.services import get_all_users, delete_single_user


router = APIRouter(
    prefix="/admin-users",
    tags=["Admin-Users"]
)

current_active_user = fastapi_users.current_user(active=True)


@router.get("/", status_code=200, response_model=List[UserRead])
async def get_users(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_active_user)):

    return await get_all_users(skip, limit, session, user)


@router.delete("/delete", status_code=204)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):

    return await delete_single_user(user_id, session, user)
