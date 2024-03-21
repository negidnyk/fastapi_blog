from sqlalchemy import select, insert, delete
from src.posts.models import PostLikes
from src.users.user.helpers import get_creator_by_id
from src.postLikes.schemas import LikesListOut
from src.users.user.validations import is_user


async def like_or_unlike_post(post_id, session, user):

    is_user(user.role_id)

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

    is_user(user.role_id)

    query = select(PostLikes).where(PostLikes.post_id == post_id)
    likes_list = await session.execute(query)
    result_list = likes_list.scalars().all()
    return [LikesListOut(
        like_id=like.id,
        creator=await get_creator_by_id(like.user_id, session),
    ) for like in result_list]


