from pydantic import BaseModel


class UploadVideo(BaseModel):
    title: str
    description: str


class FileOut(BaseModel):
    id: int