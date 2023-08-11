from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func, distinct
from posts.models import Post, PostLikes
from auth.base_config import fastapi_users
from auth.models import User
from comments.models import Comment
from comments.schemas import CommentCreator, PostCommentsOut
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func, distinct
from auth.models import User
from comments.models import Comment

async def get_creator(comment_id, session):
    query = select(User).join(Comment).where(Comment.id == comment_id)
    creator = await session.execute(query)
    response = creator.scalars().first()
    return CommentCreator(id=response.id, name=response.username)


async def comments_count(post_id, session):
    query = select(func.count(distinct(Comment.id))).filter(Comment.post_id == post_id)
    comments_count = await session.execute(query)
    result = comments_count.scalar_one()
    return result


# async def get_latest_comments(post_id, session):
#     query = select(Comment).where(Comment.post_id == post_id)
#     latest_comments = await session.execute(query)
#     result = latest_comments.scalars().all()
#     print(result)
#     return [PostCommentsOut(id=comment.id, user=await get_creator(result.id, session), text=result.text,
#                             created_at=comment.created_at) for comment in result]
