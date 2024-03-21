from uuid import uuid4
from fastapi import HTTPException, File
from sqlalchemy import select, insert
from src.files.models import File
from src.files.schemas import MediaOut
from src.files.minio_config import client, bucket
import os
import tempfile
from src.users.user.validations import is_user


async def upload_an_image(file, session, user):

    is_user(user.role_id)

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=418, detail="Only .png and .jpeg images are allowed")
    else:
        file_extension = "jpeg" if file.content_type == "image/jpeg" else "png"
        file_name = f'media/{user.id}_{uuid4()}.{file_extension}'

        # Create a temporary file to save the uploaded content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            file_content = await file.read()
            temp_file.write(file_content)

        # Upload the temporary file to MinIO
        client.fput_object(bucket_name=bucket, object_name=file_name, file_path=temp_path,
                           content_type=file.content_type)

        # Remove the temporary file
        os.remove(temp_path)

    get_url = client.get_presigned_url("GET", bucket_name=bucket, object_name=file_name)

    details = {
        "file": file_name,
        "user_id": user.id
    }
    stmt = insert(File).values(**details)
    await session.execute(stmt)
    await session.commit()

    query = select(File).order_by(File.created_at.desc())
    last_created_file = await session.execute(query)
    result = last_created_file.scalars().first()

    return MediaOut(id=result.id, file=get_url)

