from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func, distinct
from posts.models import Post, PostLikes, UserPost, PostFiles
from auth.base_config import fastapi_users
from auth.models import User
from posts.schemas import PostCreator, MediaOut
from files.models import File


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
    response = creator.scalars().first()
    return PostCreator(id=response.id, name=response.username)


async def get_media(post_id, session):
    query = select(File).join(PostFiles).where(PostFiles.post_id == post_id)
    post_media = await session.execute(query)
    response = post_media.scalars().first()
    return MediaOut(id=response.id, file=response.file)