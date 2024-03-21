from src.comments.schemas import CommentCreator
from sqlalchemy import select, func, distinct
from src.auth.models import User
from src.comments.models import Comment

async def get_creator(comment_id, session):
    query = select(User).join(Comment).where(Comment.id == comment_id)
    creator = await session.execute(query)
    response = creator.scalars().first()
    return CommentCreator(id=response.id, name=response.username)


async def comments_count(post_id, session):
    query = select(func.count(distinct(Comment.id))).filter(Comment.post_id == post_id)
    comments_count = await session.execute(query)
    result = comments_count.scalar_one()
    return result


# async def get_latest_comments(post_id, session):
#     query = select(Comment).where(Comment.post_id == post_id)
#     latest_comments = await session.execute(query)
#     result = latest_comments.scalars().all()
#     print(result)
#     return [PostCommentsOut(id=comment.id, user=await get_creator(result.id, session), text=result.text,
#                             created_at=comment.created_at) for comment in result]
