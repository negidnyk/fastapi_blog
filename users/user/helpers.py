from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func, distinct
from posts.models import Post, PostLikes
from auth.models import User
from posts.schemas import PostCreator
from files.models import File
from files.schemas import MediaOut
from auth.schemas import UserGetsUser


async def get_avatar(user_id, session):
    query = select(File).join(User, onclause=File.id == User.avatar_id).where(User.id == user_id)
    post_media = await session.execute(query)
    response = post_media.scalar_one_or_none()
    if response is None:
        return None
    else:
        return MediaOut(id=response.id, file=response.file)


async def get_creator_by_post(post_id, session):
    query = select(User).join(Post, onclause=User.id == Post.creator_id).where(Post.id == post_id)
    creator = await session.execute(query)
    response = creator.scalars().first()

    return UserGetsUser(id=response.id,
                        email=response.email,
                        username=response.username,
                        bio=response.bio,
                        avatar=await get_avatar(response.id, session))