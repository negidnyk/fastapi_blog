from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func, distinct
from posts.models import Post, PostLikes
from auth.base_config import fastapi_users
from auth.models import User
from posts.schemas import PostCreator, MediaOut
from files.models import File
from comments.models import Comment
from auth.schemas import UserGetsUser
from users.user.helpers import get_avatar


