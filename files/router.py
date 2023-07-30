from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func, distinct
from posts.schemas import CreatePost
from database import get_async_session
from posts.models import Post, PostLikes, UserPost
from typing import List, Dict
from auth.base_config import fastapi_users
from auth.models import User
import shutil
import aiofiles
from files.schemas import UploadVideo
from files.models import File


router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

current_active_user = fastapi_users.current_user(active=True)


# async def save_video(
#         user: User,
#         file: UploadFile,
#         title: str,
#         description: str,
#         back_tasks: BackgroundTasks
# ):
#     file_name = f'media/{user.id}_{uuid4()}.mp4'
#     if file.content_type == 'video/mp4':
#         # back_tasks.add_task(write_video, file_name, file)
#         await write_video(file_name, file)
#     else:
#         raise HTTPException(status_code=418, detail="It isn't mp4")
#     info = UploadVideo(title=title, description=description)
#     return await Video.objects.create(file=file_name, user=user.dict(), **info.dict())


async def write_video(file_name: str, file: UploadFile):
    async with aiofiles.open(file_name, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)
    # with open(file_name, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)



# @router.post("/", status_code=200)
# async def upload_file(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
#     info = UploadVideo(title=title, description=description)
#     with open(f'{file.filename}', "wb",) as buffer:
#         shutil.copyfileobj(file.file, buffer)
#
#     return {"file_name": file.filename, "info": info, "headers": file.headers}


@router.post("/image")
async def upload_image(file: UploadFile, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_active_user)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=418, detail="Only .png and .jpeg images are allowed")
    else:
        if file.content_type == "image/jpeg":
            file_name = f'media/{user.id}_{uuid4()}.jpeg'
            await write_video(file_name, file)
        else:
            file_name = f'media/{user.id}_{uuid4()}.png'
            await write_video(file_name, file)

    details = {
        "file": file_name,
        "user_id": user.id
    }
    stmt = insert(File).values(**details)
    await session.execute(stmt)
    await session.commit()


