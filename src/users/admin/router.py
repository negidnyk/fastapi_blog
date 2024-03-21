from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from src.auth.models import User
from src.users.admin.services import get_all_users, delete_single_user, get_all_admins, delete_single_admin


router = APIRouter(
    prefix="/admin-users",
    tags=["Admin-Users"]
)

current_active_user = fastapi_users.current_user(active=True)


@router.get("/", status_code=200)
async def get_users(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_active_user)):

    return await get_all_users(skip, limit, session, user)


@router.delete("/", status_code=204)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):

    return await delete_single_user(user_id, session, user)


@router.get("/admins", status_code=200)
async def get_admins(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_active_user)):

    return await get_all_admins(skip, limit, session, user)


@router.delete("/admins", status_code=204)
async def delete_admin(user_id: int, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):

    return await delete_single_admin(user_id, session, user)