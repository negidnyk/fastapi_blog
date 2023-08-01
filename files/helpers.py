from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
import aiofiles


async def write_file(file_name: str, file: UploadFile):
    async with aiofiles.open(file_name, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)
