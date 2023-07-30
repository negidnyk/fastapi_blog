# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy import select, insert, update, delete, func, distinct
# from posts.schemas import PostOut, CreatePost
# from posts.models import Post, PostLikes, UserPost
# from posts.helpers import is_liked, likes_count, get_creator
# from posts.schemas import CreatePost
# from uuid import uuid4
# from files.models import File
#
#
#
#
#
#
# async def save_video(file, session, user):
#
#     details = {
#         "file": file,
#         "user_id": user.id
#     }
#     # post_details = CreatePost(title=new_post.title, description=new_post.description, creator_id=user.id)
#
#     stmt = insert(File).values(**details)
#     await session.execute(stmt)
#     await session.commit()
#
#
#
#
#
#     file_name = f'media/{user.id}_{uuid4()}.mp4'
#     if file.content_type == 'video/mp4':
#         # back_tasks.add_task(write_video, file_name, file)
#         await write_video(file_name, file)
#     else:
#         raise HTTPException(status_code=418, detail="It isn't mp4")
#     info = UploadVideo(title=title, description=description)
#     return await Video.objects.create(file=file_name, user=user.dict(), **info.dict())
#
#
# async def write_video(file_name: str, file: UploadFile):
#     async with aiofiles.open(file_name, "wb") as buffer:
#         data = await file.read()
#         await buffer.write(data)
#     with open(file_name, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)