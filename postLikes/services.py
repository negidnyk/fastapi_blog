from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func, distinct
from posts.schemas import CreatePost
from database import get_async_session
from posts.models import Post, PostLikes
from typing import List, Dict
from auth.base_config import fastapi_users
from auth.models import User
from users.user.helpers import get_creator_by_id
from postLikes.schemas import LikesListOut


async def like_or_unlike_post(post_id, session, user):
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
        return {"status": "success!", "info": "Post is liked"}
    else:
        stmt1 = delete(PostLikes).where(PostLikes.post_id == post_id, PostLikes.user_id == user.id)
        await session.execute(stmt1)
        await session.commit()
        return {"status": "success!", "info": "Post is unliked"}


async def get_likes_list(post_id, session, user):
    query = select(PostLikes).where(PostLikes.post_id == post_id)
    likes_list = await session.execute(query)
    result_list = likes_list.scalars().all()
    return [LikesListOut(
        like_id=like.id,
        creator=await get_creator_by_id(like.user_id, session),
    ) for like in result_list]

# async def like_a_post(post_id, session, user):
#
#     query = select(PostLikes).where(PostLikes.post_id == post_id, PostLikes.user_id == user.id)
#     the_test = await session.execute(query)
#
#     if the_test.scalar_one_or_none() == None:
#         info_list = {
#             "post_id": post_id,
#             "user_id": user.id
#         }
#         stmt = insert(PostLikes).values(**info_list)
#         await session.execute(stmt)
#         await session.commit()
#         return {"status": "success!"}
#     else:
#         raise HTTPException(status_code=400, detail="Post already liked!")
#
#
# async def unlike_a_post(post_id, session, user):
#
#     query = select(PostLikes).where(PostLikes.post_id == post_id, PostLikes.user_id == user.id)
#     the_test = await session.execute(query)
#
#     if the_test.scalar_one_or_none() == None:
#         raise HTTPException(status_code=400, detail="Post is not liked yet!")
#     else:
#         stmt = delete(PostLikes).where(PostLikes.post_id == post_id, PostLikes.user_id == user.id)
#         await session.execute(stmt)
#         await session.commit()
#         return {"status": "success!"}
