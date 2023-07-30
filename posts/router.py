from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from posts.schemas import CreatePost
from database import get_async_session
from auth.base_config import fastapi_users
from auth.models import User
from posts.services import get_posts_list, get_my_posts_list, get_post_by_id, get_posts_of_user, create_a_post,\
    update_a_post, delete_post


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.get("/", status_code=200)
async def get_posts(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_active_user)):
    return await get_posts_list(limit, skip, session, user)


@router.get("/my", status_code=200)
async def get_my_posts(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_active_user)):
    return await get_my_posts_list(limit, skip, session, user)


@router.get("/{post_id}", status_code=200)
async def get_single_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_active_user)):
    return await get_post_by_id(post_id, session, user)


@router.get("-user/{user_id}", status_code=200)
async def get_users_posts(user_id: int, skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_active_user)):
    return await get_posts_of_user(user_id, skip, limit, session, user)


@router.post("/", status_code=201)
async def create_post(new_post: CreatePost, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):
    return {"status": "success", "post_details": await create_a_post(new_post, session, user)}


@router.put("/{post_id}", status_code=201)
async def update_post(post_id: int, post: CreatePost, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):
    return await update_a_post(post_id, post, session, user)


@router.delete("/{post_id}", status_code=204)
async def delete_single_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_active_user)):
    return await delete_post(post_id, session, user)
