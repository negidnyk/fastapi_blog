from fastapi import APIRouter, Depends, UploadFile
from src.uploading_files.services import upload_a_file, get_files
from src.uploading_files.schemas import SortingOptions, FilteringOptions
from src.uploading_files.schemas import SortingDirections
from src.auth.base_config import fastapi_users
from auth.models import User


router = APIRouter(
    prefix="/media",
    tags=["Media"]
)

# current_active_user = fastapi_users.current_user(active=True)

# @router.post("/image")
# async def upload_image(file: UploadFile, session: AsyncSession = Depends(get_async_session),
#                        user: User = Depends(current_active_user)):

current_active_user = fastapi_users.current_user(active=True)


@router.post("/file", status_code=201)
async def upload_file(file: UploadFile, user: User = Depends(current_active_user)):
    return await upload_a_file(file, user)


@router.get("/files", status_code=200)
async def get_files_list(media_type: FilteringOptions, sort_by: SortingOptions, sorting_direction: SortingDirections,
                         skip: int = 0, limit: int = 10, user: User = Depends(current_active_user)):
    return await get_files(skip, limit, sort_by, sorting_direction, media_type, user)
