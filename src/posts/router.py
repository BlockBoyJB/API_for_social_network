from uuid import uuid4
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from http import HTTPStatus

from polog import log

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.posts.schemas import PostCreate
from src.users.models import User
from src.posts.models import Post

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


# TODO: также при создании проверять, что у текущего пользователя не существует поста с таким же заголовком
@router.post("/post/create")
@log
async def add_post(new_post: PostCreate, session: AsyncSession = Depends(get_async_session)):
    query = select(User.user_uuid, User.is_verified).where(User.username == new_post.author_username)
    result = await session.execute(query)
    user_uuid, status = result.all()[0]
    if status is False:
        return JSONResponse(content={"message": "user is not confirmed"}, status_code=HTTPStatus.FORBIDDEN)

    sqmt = insert(Post).values(
        title=new_post.title,
        username=new_post.author_username,
        post_text=new_post.post_text,
        user_uuid=user_uuid,
        post_uuid=str(uuid4()),
    )

    await session.execute(sqmt)
    await session.commit()
    return JSONResponse(content={
        "title": new_post.title,
        "username": new_post.author_username,
        "text": new_post.post_text,
    }, status_code=HTTPStatus.CREATED)


@router.get("/post")
@log
async def get_post(title: str, username: str, session: AsyncSession = Depends(get_async_session)):
    query = select(Post).where(Post.title == title and Post.username == username)
    user_info = await session.execute(query)
    result: Post = user_info.fetchone()[0]
    data = {
        "title": result.title,
        "author_username": result.username,
        "text": result.post_text,
        "post_uuid": result.post_uuid,
        "reactions": [] if result.reactions is None else result.reactions,
    }
    return JSONResponse(content=data, status_code=HTTPStatus.OK)
