from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy import select, insert, update, delete, func, distinct
from files.models import File
from files.schemas import FileOut
from files.helpers import write_file


async def upload_an_image(file, session, user):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=418, detail="Only .png and .jpeg images are allowed")
    else:
        if file.content_type == "image/jpeg":
            file_name = f'media/{user.id}_{uuid4()}.jpeg'
            await write_file(file_name, file)
        else:
            file_name = f'media/{user.id}_{uuid4()}.png'
            await write_file(file_name, file)

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
    return FileOut(id=result.id)

