from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func, distinct
from posts.models import Post, PostLikes, UserPost
from auth.base_config import fastapi_users
from auth.models import User


async def is_liked(post_id, user_id, session):
    query = select(PostLikes).where(PostLikes.post_id == post_id, PostLikes.user_id == user_id)
    postLikes = await session.execute(query)
    if postLikes.scalar_one_or_none() is None:
        return False
    else:
        return True


async def likes_count(post_id, session):
    query = select(func.count(distinct(PostLikes.id))).filter(PostLikes.post_id == post_id)
    likes_count = await session.execute(query)
    result = likes_count.scalar_one()
    return result


async def get_creator(post_id, session):
    query = select(User).join(UserPost).where(UserPost.post_id == post_id)
    creator = await session.execute(query)
    response = creator.scalars().all()
    result = {
        "id": response[0].id,
        "name": response[0].username
    }
    return result

