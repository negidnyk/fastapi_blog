from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from auth.models import User
from src.postLikes.services import like_or_unlike_post, get_likes_list


router = APIRouter(
    prefix="/like",
    tags=["Likes"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.put("/{post_id}", status_code=201)
async def like_or_unlilke_the_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_active_user)):
    return await like_or_unlike_post(post_id, session, user)


@router.get("/{post_id}", status_code=200)
async def get_post_likes(post_id: int, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    return await get_likes_list(post_id, session, user)



# @router.post("/{post_id}", status_code=201)
# async def like_post(post_id: int, session: AsyncSession = Depends(get_async_session),
#                     user: User = Depends(current_active_user)):
#     return await like_a_post(post_id, session, user)


# @router.delete("/{post_id}", status_code=204)
# async def unlike_post(post_id: int, session: AsyncSession = Depends(get_async_session),
#                       user: User = Depends(current_active_user)):
#     return await unlike_a_post(post_id, session, user)