from fastapi import FastAPI

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from posts.router import router as router_post
from users.admin.router import router as router_admin
from users.user.router import router as router_users
from postLikes.router import router as router_likes
from files.router import router as router_files
from comments.router import router as router_comments


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
