from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
import aiofiles
from files.schemas import MediaOut
from posts.models import Post
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func, distinct
from posts.models import Post, PostLikes
from posts.schemas import PostCreator, MediaOut
from files.models import File


async def write_file(file_name: str, file: UploadFile):
    async with aiofiles.open(file_name, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)


async def get_media(post_id, session):
    query = select(File).join(Post).where(Post.id == post_id)
    post_media = await session.execute(query)
    response = post_media.scalars().first()
    return MediaOut(id=response.id, file=response.file)


async def validate_media(file_id, session):
    query = select(File).where(File.id == file_id)
    file = await session.execute(query)
    response = file.scalars().first()
    if response.is_used:
        return True
    else:
        return False


async def file_exist(file_id, session):
    query = select(File).where(File.id == file_id)
    file = await session.execute(query)
    response = file.scalar_one_or_none()
    if response is None:
        return True
    else:
        return False
