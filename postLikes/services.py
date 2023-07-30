from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func, distinct
from posts.schemas import CreatePost
from database import get_async_session
from posts.models import Post, PostLikes
from typing import List, Dict
from auth.base_config import fastapi_users
from auth.models import User


async def like_a_post(post_id, session, user):

    query = select(PostLikes).where(PostLikes.post_id == post_id, PostLikes.user_id == user.id)
    the_test = await session.execute(query)

    if the_test.scalar_one_or_none() == None:
        info_list = {
            "post_id": post_id,
            "user_id": user.id
        }
        stmt = insert(PostLikes).values(**info_list)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success!"}
    else:
        raise HTTPException(status_code=400, detail="Post already liked!")


async def unlike_a_post(post_id, session, user):

    query = select(PostLikes).where(PostLikes.post_id == post_id, PostLikes.user_id == user.id)
    the_test = await session.execute(query)

    if the_test.scalar_one_or_none() == None:
        raise HTTPException(status_code=400, detail="Post is not liked yet!")
    else:
        stmt = delete(PostLikes).where(PostLikes.post_id == post_id, PostLikes.user_id == user.id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success!"}
