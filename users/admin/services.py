from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from posts.schemas import CreatePost
from auth.schemas import UserRead, GetUser
from posts.models import Post
from posts.schemas import CreatePost
from database import get_async_session
from typing import List
from auth.base_config import fastapi_users
from auth.models import User


async def get_all_users(skip, limit, session, user):

    if user.role_id == 1:
        query = select(User).limit(limit).offset(skip)
        users_list = await session.execute(query)
        return users_list.scalars().all()
    else:
        raise HTTPException(status_code=403, detail="This option is for admins only!")


async def delete_single_user(user_id, session, user):

    if user.role_id != 1:
        raise HTTPException(status_code=403, detail="This option is for admins only!")
    else:
        query = select(User).filter(User.id == user_id)
        user_to_delete = await session.execute(query)
        if user_to_delete.scalar_one_or_none() == None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            stmt0 = delete(Post).where(Post.creator_id == user_id)
            await session.execute(stmt0)
            await session.commit()
            stmt = delete(User).where(User.id == user_id)
            await session.execute(stmt)
            await session.commit()
            return user_id