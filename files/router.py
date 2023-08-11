from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func, distinct
from posts.schemas import CreatePost
from database import get_async_session
from posts.models import Post, PostLikes
from typing import List, Dict
from auth.base_config import fastapi_users
from auth.models import User
import shutil
import aiofiles
from files.schemas import UploadVideo
from files.models import File
from files.schemas import FileOut
from files.services import upload_an_image


router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

current_active_user = fastapi_users.current_user(active=True)


@router.post("/image")
async def upload_image(file: UploadFile, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_active_user)):
    # if file.content_type not in ["image/jpeg", "image/png"]:
    #     raise HTTPException(status_code=418, detail="Only .png and .jpeg images are allowed")
    # else:
    #     if file.content_type == "image/jpeg":
    #         file_name = f'media/{user.id}_{uuid4()}.jpeg'
    #         await write_video(file_name, file)
    #     else:
    #         file_name = f'media/{user.id}_{uuid4()}.png'
    #         await write_video(file_name, file)
    #
    # details = {
    #     "file": file_name,
    #     "user_id": user.id
    # }
    # stmt = insert(File).values(**details)
    # await session.execute(stmt)
    # await session.commit()
    #
    # query = select(File).order_by(File.created_at.desc())
    # last_created_file = await session.execute(query)
    # result = last_created_file.scalars().first()
    # return FileOut(id=result.id)
    return await upload_an_image(file, session, user)
