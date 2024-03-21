from pydantic import BaseModel
from typing import Optional
from enum import Enum


# class UploadVideo(BaseModel):
#     title: str
#     description: str
#
#
# class FileOut(BaseModel):
#     id: int
#
#
# class MediaOut(BaseModel):
#     id: int
#     file: str


class SortingOptions(str, Enum):
    registered_at = "created_at"
    id = "_id"


class FilteringOptions(str, Enum):
    video = "video"
    image = "image"
    all = "all"


class SortingDirections(str, Enum):
    asc = 1
    desc = -1
