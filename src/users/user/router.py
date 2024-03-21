from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from auth.models import User
from src.users.user.services import get_my_profile, get_user_profile, update_my_profile
from auth.schemas import UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.get("/me", status_code=200)
async def get_me(session: AsyncSession = Depends(get_async_session),
                 user: User = Depends(current_active_user)):
    return await get_my_profile(session, user)


@router.patch("/update-profile", status_code=201)
async def update_profile(profile: UserUpdate, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    return await update_my_profile(profile, session, user)


@router.get("/{user_id}", status_code=200)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_active_user)):
    return await get_user_profile(user_id, session, user)
