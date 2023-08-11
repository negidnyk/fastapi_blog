from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from posts.schemas import CreatePost
from database import get_async_session
from auth.base_config import fastapi_users
from auth.models import User

from comments.schemas import CreateComment
from comments.models import Comment
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func, distinct
from comments.schemas import PostCommentsOut
from users.user.helpers import get_creator_by_post


async def get_post_comments(post_id, session, user):
    pass


async def create_a_comment(post_id, new_comment, session, user):

    comment_details = {
        "user_id": user.id,
        "post_id": post_id,
        "text": new_comment.text
    }
    stmt = insert(Comment).values(**comment_details)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success!", "comment_details": comment_details}


async def get_post_comments(skip, limit, post_id, session, user):
    query = select(Comment).where(Comment.post_id == post_id).limit(limit).offset(skip).order_by(Comment.created_at.desc())
    comments_list = await session.execute(query)
    result_list = comments_list.scalars().all()
    return[PostCommentsOut(id=comment.id, user=await get_creator_by_post(comment.post_id, session), text=comment.text,
                           created_at=comment.created_at) for comment in result_list]
