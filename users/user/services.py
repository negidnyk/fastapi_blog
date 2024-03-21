from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func, distinct
from auth.models import User
from auth.schemas import UserRead, UserGetsUser
from users.user.helpers import get_avatar
from files.helpers import get_media, validate_media, file_exist
from files.models import File
from users.user.validations import is_user


async def get_my_profile(session, user):

    is_user(user.role_id)

    query = select(User).where(User.id == user.id)
    my_profile = await session.execute(query)
    result_list = my_profile.scalars().one()

    return UserGetsUser(id=result_list.id,
                        email=result_list.email,
                        username=result_list.username,
                        bio=result_list.bio,
                        avatar=await get_avatar(user.id, session))


async def update_my_profile(profile, session, user):

    # if user.role_id != 2:
    #     raise HTTPException(status_code=403, detail="This option is for users only")
    is_user(user.role_id)

    if profile.avatar_id:

        is_file_exist = await file_exist(profile.avatar_id, session)

        if is_file_exist:
            raise HTTPException(status_code=404, detail="File not found!")

        media_validation = await validate_media(profile.avatar_id, session)

        if media_validation:
            raise HTTPException(status_code=400, detail="File is already used!")

    payload = {}

    if profile.username is not None:
        payload["username"] = profile.username

    if profile.bio is not None:
        payload["bio"] = profile.bio

    if profile.avatar_id is not None:
        payload["avatar_id"] = profile.avatar_id

    stmt = update(User).where(User.id == user.id).values(**payload)
    await session.execute(stmt)
    await session.commit()

    stmt2 = update(File).where(File.id == profile.avatar_id).values(is_used=True)
    await session.execute(stmt2)
    await session.commit()

    query = select(User).where(User.id == user.id)
    my_profile = await session.execute(query)
    result_list = my_profile.scalars().one()

    return UserGetsUser(id=result_list.id,
                        email=result_list.email,
                        username=result_list.username,
                        bio=result_list.bio,
                        avatar=await get_avatar(user.id, session))


async def get_user_profile(user_id, session, user):

    # if user.role_id != 2:
    #     raise HTTPException(status_code=403, detail="This option is for users only")
    is_user(user.role_id)

    query = select(User).where(User.id == user_id)
    user_profile = await session.execute(query)
    profile = user_profile.scalar_one_or_none()

    if profile == None or profile.role_id != 2:
        raise HTTPException(status_code=404, detail="User not found")

    else:
        query = select(User).where(User.id == user_id)
        user_profile = await session.execute(query)
        result_list = user_profile.scalars().one()

        return UserGetsUser(id=result_list.id,
                            email=result_list.email,
                            username=result_list.username,
                            bio=result_list.bio,
                            avatar=await get_avatar(user.id, session))
