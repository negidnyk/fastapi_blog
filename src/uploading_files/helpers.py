# from fastapi import UploadFile, File
# import aiofiles
# from sqlalchemy import select
# from posts.models import Post
# from posts.schemas import MediaOut
# from files.models import File
# from media.uploading_files.minio_config import client, bucket
#
#
# async def write_file(file_name: str, file: UploadFile):
#     async with aiofiles.open(file_name, "wb") as buffer:
#         data = await file.read()
#         await buffer.write(data)
#
#
# async def get_media(post_id, session):
#     query = select(File).join(Post).where(Post.id == post_id)
#     post_media = await session.execute(query)
#     response = post_media.scalars().first()
#
#     get_url = client.get_presigned_url("GET", bucket_name=bucket, object_name=response.file)
#
#     return MediaOut(id=response.id, file=get_url)
#
#
# async def validate_media(file_id, session):
#     query = select(File).where(File.id == file_id)
#     file = await session.execute(query)
#     response = file.scalars().first()
#     if response.is_used:
#         return True
#     else:
#         return False
#
#
# async def file_exist(file_id, session):
#     query = select(File).where(File.id == file_id)
#     file = await session.execute(query)
#     response = file.scalar_one_or_none()
#     if response is None:
#         return True
#     else:
#         return False
#
#
# # async def get_file_with_url(file_id, bucket, session):
# #
# #     query = select(File).where(File.id == file_id)
# #     file = await session.execute(query)
# #     result = file.scalars().first()
# #
# #     get_url = client.get_presigned_url("GET", bucket_name=bucket, object_name=result.file)
# #
# #     return MediaOut(id=result.id, file=get_url)
