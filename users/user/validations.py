from fastapi import HTTPException
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