from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func, distinct
from auth.models import User
from auth.schemas import UserRead, GetUser


async def get_my_profile(session, user):

    query = select(User).where(User.id == user.id)
    my_profile = await session.execute(query)
    result_list = my_profile.scalars().one()

    return GetUser(id=result_list.id, email=result_list.email, username=result_list.username)


async def get_user_profile(user_id, session, user):

    query = select(User).where(User.id == user_id)
    user_profile = await session.execute(query)

    if user_profile.scalar_one_or_none() == None:
        raise HTTPException(status_code=404, detail="User not found")

    else:
        query = select(User).where(User.id == user_id)
        user_profile = await session.execute(query)
        result_list = user_profile.scalars().one()

        return GetUser(id=result_list.id, email=result_list.email, username=result_list.username)
