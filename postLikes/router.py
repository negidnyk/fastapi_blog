from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from auth.base_config import fastapi_users
from auth.models import User
from postLikes.services import like_a_post, unlike_a_post


router = APIRouter(
    prefix="/like",
    tags=["Likes"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.post("/{post_id}", status_code=201)
async def like_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_active_user)):
    return await like_a_post(post_id, session, user)


@router.delete("/{post_id}", status_code=204)
async def unlike_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):
    return await unlike_a_post(post_id, session, user)