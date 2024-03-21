from fastapi import HTTPException
from sqlalchemy import select
from src.posts.models import Post


# from posts.helpers import get_creator


def is_user(role_id):
    if role_id != 2:
        raise HTTPException(status_code=403, detail="This option is for users only")


async def is_post_creator(post_id, creator_id, session):

    query = select(Post.creator_id).filter(Post.id == post_id)
    get_user_id = await session.execute(query)

    if get_user_id.scalar_one_or_none() != creator_id:
        raise HTTPException(status_code=403, detail="You are not creator of this post!")



def is_comment_creator(comment_id, creator_id, session):
    pass