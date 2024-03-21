from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from posts.models import Post
from auth.models import User
from auth.schemas import UserGetsUser, AdminGetsUser
from users.user.helpers import get_avatar
from users.admin.validations import is_admin_or_superadmin, is_superadmin


async def get_all_users(skip, limit, session, user):

    is_admin_or_superadmin(user.role_id)

    query = select(User).limit(limit).offset(skip).where(User.role_id == 2)
    users_list = await session.execute(query)
    result_list = users_list.scalars().all()

    return [AdminGetsUser(id=result.id,
                          email=result.email,
                          username=result.username,
                          bio=result.bio, role_id=result.role_id,
                          is_active=result.is_active,
                          is_superuser=result.is_superuser,
                          is_verified=result.is_verified,
                          avatar=await get_avatar(user.id, session)) for result in result_list]


async def get_all_admins(skip, limit, session, user):

    is_superadmin(user.role_id)

    query = select(User).limit(limit).offset(skip).where(User.role_id == 1)
    users_list = await session.execute(query)
    result_list = users_list.scalars().all()

    return [AdminGetsUser(id=result.id,
                          email=result.email,
                          username=result.username,
                          bio=result.bio,
                          role_id=result.role_id,
                          is_active=result.is_active,
                          is_superuser=result.is_superuser,
                          is_verified=result.is_verified,
                          avatar=await get_avatar(user.id, session)) for result in result_list]


async def delete_single_user(user_id, session, user):

    is_admin_or_superadmin(user.role_id)

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


async def delete_single_admin(user_id, session, user):

    is_superadmin(user.role_id)

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
