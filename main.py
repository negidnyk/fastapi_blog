from fastapi import FastAPI

from src.auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from src.posts.router import router as router_post
from src.users.admin.router import router as router_admin
from src.users.user.router import router as router_users
from src.postLikes.router import router as router_likes
from src.files.router import router as router_files
from comments.router import router as router_comments
from src.uploading_files.router import router as router_upload_files


app = FastAPI(
    title="Pet blog"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


current_user = fastapi_users.current_user()

app.include_router(router_post)
app.include_router(router_admin)
app.include_router(router_users)
app.include_router(router_likes)
app.include_router(router_files)
app.include_router(router_comments)
app.include_router(router_upload_files)
