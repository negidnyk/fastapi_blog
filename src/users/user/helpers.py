from sqlalchemy import select
from src.posts.models import Post
from auth.models import User
from src.files.models import File
from src.files.schemas import MediaOut
from auth.schemas import UserGetsUser
from src.files.minio_config import client, bucket


async def get_avatar(user_id, session):
    query = select(File).join(User, onclause=File.id == User.avatar_id).where(User.id == user_id)
    post_media = await session.execute(query)
    response = post_media.scalar_one_or_none()

    if response is None:
        return None
    else:
        get_url = client.get_presigned_url("GET", bucket_name=bucket, object_name=response.file)
        return MediaOut(id=response.id, file=get_url)


async def get_creator_by_post(post_id, session):
    query = select(User).join(Post, onclause=User.id == Post.creator_id).where(Post.id == post_id)
    creator = await session.execute(query)
    response = creator.scalars().first()

    return UserGetsUser(id=response.id,
                        email=response.email,
                        username=response.username,
                        bio=response.bio,
                        avatar=await get_avatar(response.id, session))


async def get_creator_by_id(user_id, session):

    query = select(User).where(User.id == user_id)
    creator = await session.execute(query)
    response = creator.scalars().first()

    return UserGetsUser(id=response.id,
                        email=response.email,
                        username=response.username,
                        bio=response.bio,
                        avatar=await get_avatar(response.id, session))
