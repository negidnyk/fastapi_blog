from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from posts.schemas import CreatePost
from database import get_async_session
from auth.base_config import fastapi_users
from auth.models import User

from comments.schemas import CreateComment
from comments.services import create_a_comment, get_post_comments, update_a_comment, delete_comment


router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.get("/{post_id}", status_code=200)
async def get_comments_of_post(post_id: int, skip: int = 0, limit: int = 10,  session: AsyncSession = Depends(get_async_session),
                               user: User = Depends(current_active_user)):
    return await get_post_comments(skip, limit, post_id, session, user)


@router.post("/", status_code=201)
async def create_comment(post_id: int, new_comment: CreateComment, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):
    return await create_a_comment(post_id, new_comment, session, user)


@router.put("/{comment_id}", status_code=201)
async def update_comment(comment_id: int, updated_comment: CreateComment,
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    return await update_a_comment(comment_id, updated_comment, session, user)


@router.delete("/{post_id}", status_code=204)
async def delete_single_comment(comment_id: int, session: AsyncSession = Depends(get_async_session),
                                user: User = Depends(current_active_user)):
    return await delete_comment(comment_id, session, user)
