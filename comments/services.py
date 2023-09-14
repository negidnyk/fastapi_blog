from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from posts.schemas import CreatePost
from database import get_async_session
from auth.base_config import fastapi_users
from auth.models import User

from comments.schemas import CreateComment
from comments.models import Comment
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func, distinct
from comments.schemas import PostCommentsOut
from users.user.helpers import get_creator_by_post, get_creator_by_id


async def create_a_comment(post_id, new_comment, session, user):

    if user.role_id != 2:
        raise HTTPException(status_code=403, detail="This option is for users only")

    comment_details = {
        "user_id": user.id,
        "post_id": post_id,
        "text": new_comment.text
    }
    stmt = insert(Comment).values(**comment_details)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success!", "comment_details": comment_details}


async def get_post_comments(skip, limit, post_id, session, user):

    if user.role_id != 2:
        raise HTTPException(status_code=403, detail="This option is for users only")

    query = select(Comment).where(Comment.post_id == post_id).limit(limit).offset(skip).order_by(Comment.created_at.desc())
    comments_list = await session.execute(query)
    result_list = comments_list.scalars().all()
    return[PostCommentsOut(id=comment.id, user=await get_creator_by_id(comment.user_id, session), text=comment.text,
                           created_at=comment.created_at) for comment in result_list]


async def update_a_comment(comment_id, updated_comment, session, user):

    if user.role_id != 2:
        raise HTTPException(status_code=403, detail="This option is for users only")

    query = select(Comment.user_id).filter(Comment.id == comment_id)
    comment_creator = await session.execute(query)
    result = comment_creator.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    if result != user.id:
        raise HTTPException(status_code=403, detail="You are not creator of this comment!")

    stmt = update(Comment).where(Comment.id == comment_id, Comment.user_id == user.id).values(**updated_comment.dict())
    await session.execute(stmt)
    await session.commit()

    query2 = select(Comment).where(Comment.id == comment_id, Comment.user_id == user.id)
    comment = await session.execute(query2)
    result2 = comment.scalars().one()

    return PostCommentsOut(id=result2.id,
                           user=await get_creator_by_post(result2.post_id, session),
                           text=result2.text,
                           created_at=result2.created_at)


async def delete_comment(comment_id, session, user):

    query = select(Comment).filter(Comment.id == comment_id)
    comment_to_delete = await session.execute(query)

    if comment_to_delete.scalar_one_or_none() == None:
        raise HTTPException(status_code=404, detail="Comment not found!")

    else:

        query = select(Comment.user_id).filter(Comment.id == comment_id)
        get_user_id = await session.execute(query)

        if get_user_id.scalar_one_or_none() != user.id:

            raise HTTPException(status_code=403, detail="You are not creator of this comment!")

        else:
            stmt = delete(Comment).where(Comment.id == comment_id)
            await session.execute(stmt)
            await session.commit()
