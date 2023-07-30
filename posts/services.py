from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func, distinct
from posts.schemas import PostOut, CreatePost
from posts.models import Post, PostLikes, UserPost
from posts.helpers import is_liked, likes_count, get_creator
from posts.schemas import CreatePost


async def get_posts_list(limit, skip, session, user):
    query_post = select(Post).limit(limit).offset(skip).order_by(Post.created_at.desc())
    post_list = await session.execute(query_post)
    result_list = post_list.scalars().all()

    return [PostOut(id=post.id,
                    title=post.title,
                    description=post.description,
                    created_at=post.created_at,
                    creator=await get_creator(post.id, session),
                    is_liked=await is_liked(post.id, user.id, session),
                    likes_count=await likes_count(post.id, session),
                    ) for post in result_list]


async def get_my_posts_list(limit, skip, session, user):
    query = select(Post).where(Post.creator_id == user.id).limit(limit).offset(skip).order_by(Post.created_at.desc())
    my_posts = await session.execute(query)
    result_list = my_posts.scalars().all()

    return [PostOut(id=post.id,
                    title=post.title,
                    description=post.description,
                    created_at=post.created_at,
                    creator=await get_creator(post.id, session),
                    is_liked=await is_liked(post.id, user.id, session),
                    likes_count=await likes_count(post.id, session),
                    ) for post in result_list]


async def get_post_by_id(post_id, session, user):

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
                       created_at=result_list.created_at,
                       creator=await get_creator(result_list.id, session),
                       is_liked=await is_liked(result_list.id, user.id, session),
                       likes_count=await likes_count(result_list.id, session),)


async def get_posts_of_user(user_id, skip, limit, session, user):

    query = select(Post).where(Post.creator_id == user_id).limit(limit).offset(skip).order_by(Post.created_at.desc())
    user_posts = await session.execute(query)
    result_list = user_posts.scalars().all()

    return [PostOut(id=post.id,
                    title=post.title,
                    description=post.description,
                    created_at=post.created_at,
                    creator=await get_creator(post.id, session),
                    is_liked=await is_liked(post.id, user.id, session),
                    likes_count=await likes_count(post.id, session),
                    ) for post in result_list]


async def create_a_post(new_post, session, user):

    post_details = {
        "title": new_post.title,
        "description": new_post.description,
        "creator_id": user.id
    }
    # post_details = CreatePost(title=new_post.title, description=new_post.description, creator_id=user.id)

    stmt = insert(Post).values(**post_details)
    await session.execute(stmt)
    await session.commit()

    query = select(Post).where(Post.creator_id == user.id).order_by(Post.created_at.desc())
    last_created_post = await session.execute(query)
    last_post = last_created_post.scalars().first()
    user_post_info = {
        "post_id": last_post.id,
        "creator_id": user.id
    }

    stmt2 = insert(UserPost).values(**user_post_info)
    await session.execute(stmt2)
    await session.commit()
    return new_post


async def update_a_post(post_id, post, session, user):

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
            stmt = update(Post).where(Post.id == post_id).values(**post.dict())
            if stmt is not None:
                await session.execute(stmt)
                await session.commit()
                return {"status": "success!", "post": post}
            else:
                raise HTTPException(status_code=404, detail="Post not found")


async def delete_post(post_id, session, user):

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
            stmt0 = delete(UserPost).where(UserPost.post_id == post_id)
            await session.execute(stmt0)
            await session.commit()
            stmt = delete(Post).where(Post.id == post_id)
            await session.execute(stmt)
            await session.commit()
            return post_id
