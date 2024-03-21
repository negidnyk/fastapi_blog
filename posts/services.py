from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func, distinct
from posts.schemas import PostOut, CreatePost
from posts.models import Post, PostLikes
# from posts.helpers import get_creator
from posts.schemas import CreatePost
from files.models import File
from files.helpers import get_media, validate_media, file_exist
from postLikes.helpers import is_liked, likes_count
from comments.helpers import comments_count
from users.user.helpers import get_creator_by_post
from users.user.validations import is_user, is_post_creator


async def get_posts_list(limit, skip, session, user):

    is_user(user.role_id)

    query_post = select(Post).limit(limit).offset(skip).order_by(Post.created_at.desc())
    post_list = await session.execute(query_post)
    result_list = post_list.scalars().all()

    return [PostOut(id=post.id,
                    title=post.title,
                    description=post.description,
                    media=await get_media(post.id, session),
                    created_at=post.created_at,
                    creator=await get_creator_by_post(post.id, session),
                    is_liked=await is_liked(post.id, user.id, session),
                    likes_count=await likes_count(post.id, session),
                    comments_count=await comments_count(post.id, session)
                    ) for post in result_list]


async def get_my_posts_list(limit, skip, session, user):

    is_user(user.role_id)

    query = select(Post).where(Post.creator_id == user.id).limit(limit).offset(skip).order_by(Post.created_at.desc())
    my_posts = await session.execute(query)
    result_list = my_posts.scalars().all()

    return [PostOut(id=post.id,
                    title=post.title,
                    description=post.description,
                    media=await get_media(post.id, session),
                    created_at=post.created_at,
                    creator=await get_creator_by_post(post.id, session),
                    is_liked=await is_liked(post.id, user.id, session),
                    likes_count=await likes_count(post.id, session),
                    comments_count=await comments_count(post.id, session)
                    ) for post in result_list]


async def get_post_by_id(post_id, session, user):

    is_user(user.role_id)

    query = select(Post).filter(Post.id == post_id)
    post_to_exist = await session.execute(query)

    if post_to_exist.scalar_one_or_none() == None:
        raise HTTPException(status_code=404, detail="Post not found")

    else:
        query = select(Post).where(Post.id == post_id)
        post = await session.execute(query)
        result_list = post.scalars().one()

        return PostOut(id=result_list.id,
                       title=result_list.title,
                       description=result_list.description,
                       media=await get_media(result_list.id, session),
                       created_at=result_list.created_at,
                       creator=await get_creator_by_post(result_list.id, session),
                       is_liked=await is_liked(result_list.id, user.id, session),
                       likes_count=await likes_count(result_list.id, session),
                       comments_count=await comments_count(result_list.id, session))


async def get_posts_of_user(user_id, skip, limit, session, user):

    is_user(user.role_id)

    query = select(Post).where(Post.creator_id == user_id).limit(limit).offset(skip).order_by(Post.created_at.desc())
    user_posts = await session.execute(query)
    result_list = user_posts.scalars().all()

    return [PostOut(id=post.id,
                    title=post.title,
                    description=post.description,
                    media=await get_media(post.id, session),
                    created_at=post.created_at,
                    creator=await get_creator_by_post(post.id, session),
                    is_liked=await is_liked(post.id, user.id, session),
                    likes_count=await likes_count(post.id, session),
                    comments_count=await comments_count(post.id, session)
                    ) for post in result_list]


async def create_a_post(new_post, session, user):

    is_user(user.role_id)

    is_file_exist = await file_exist(new_post.file_id, session)

    if is_file_exist:
        raise HTTPException(status_code=404, detail="File not found!")

    media_validation = await validate_media(new_post.file_id, session)

    if media_validation:
        raise HTTPException(status_code=400, detail="File is already used!")

    else:
        stmt = insert(Post).values(**new_post.dict(), creator_id=user.id)
        await session.execute(stmt)
        await session.commit()

        stmt2 = update(File).where(File.id == new_post.file_id).values(is_used=True)
        await session.execute(stmt2)
        await session.commit()

        query = select(Post).limit(1).order_by(Post.created_at.desc())
        post = await session.execute(query)
        result_list = post.scalar_one_or_none()

        return PostOut(id=result_list.id,
                       title=result_list.title,
                       description=result_list.description,
                       media=await get_media(result_list.id, session),
                       created_at=result_list.created_at,
                       creator=await get_creator_by_post(result_list.id, session),
                       is_liked=await is_liked(result_list.id, user.id, session),
                       likes_count=await likes_count(result_list.id, session),
                       comments_count=await comments_count(result_list.id, session))


async def update_a_post(post_id, post, session, user):

    print(post)
    is_user(user.role_id)

    query = select(Post).filter(Post.id == post_id)
    post_to_find = await session.execute(query)

    if post_to_find.scalar_one_or_none() == None:
        raise HTTPException(status_code=404, detail="Post not found")

    # NEED TO UPDATE LOGIC TO GIVE THE USER AN OPPORTUNITY TO UPDATE POSTS WITH / WITHOUT FILES
    # is_file_exist = await file_exist(post.file_id, session)
    #
    # if is_file_exist:
    #     raise HTTPException(status_code=404, detail="File not found!")
    #
    # media_validation = await validate_media(post.file_id, session)
    #
    # if media_validation:
    #     raise HTTPException(status_code=400, detail="File is already used!")

    else:
        await is_post_creator(post_id, user.id, session)
        # query = select(Post.creator_id).filter(Post.id == post_id)
        # get_user_id = await session.execute(query)
        #
        # if get_user_id.scalar_one_or_none() != user.id:
        #     raise HTTPException(status_code=403, detail="You are not creator of this post!")
        # else:
        stmt = update(Post).where(Post.id == post_id).values(**post.dict())
        if stmt is not None:
            await session.execute(stmt)
            await session.commit()

            query = select(Post).where(Post.id == post_id)
            post = await session.execute(query)
            result_list = post.scalars().one()

            return PostOut(id=result_list.id,
                           title=result_list.title,
                           description=result_list.description,
                           media=await get_media(result_list.id, session),
                           created_at=result_list.created_at,
                           creator=await get_creator_by_post(result_list.id, session),
                           is_liked=await is_liked(result_list.id, user.id, session),
                           likes_count=await likes_count(result_list.id, session),
                           comments_count=await comments_count(result_list.id, session))
        else:
            raise HTTPException(status_code=400, detail="Sorry, something went wrong")


async def delete_post(post_id, session, user):

    is_user(user.role_id)

    query = select(Post).filter(Post.id == post_id)
    post_to_delete = await session.execute(query)

    if post_to_delete.scalar_one_or_none() == None:
        raise HTTPException(status_code=404, detail="Post not found")

    else:

        query = select(Post.creator_id).filter(Post.id == post_id)
        get_user_id = await session.execute(query)

        if get_user_id.scalar_one_or_none() != user.id:
            raise HTTPException(status_code=403, detail="You are not creator of this post!")
        else:
            file = await get_media(post_id, session)

            stmt = delete(Post).where(Post.id == post_id)
            await session.execute(stmt)
            await session.commit()

            stmt2 = delete(File).where(File.id == file.id)
            await session.execute(stmt2)
            await session.commit()

            return post_id
