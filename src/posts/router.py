from uuid import uuid4
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from http import HTTPStatus

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.posts.schemas import PostCreate
from src.users.models import user
from src.posts.models import post

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


# TODO: также при создании проверять, что у текущего пользователя не существует поста с таким же заголовком
@router.post("/post/create")
async def add_post(new_post: PostCreate, session: AsyncSession = Depends(get_async_session)):
    title, author_username, text = new_post.title, new_post.author_username, new_post.post_text
    query = select(user.c.user_uuid, user.c.is_verified).where(user.c.username == author_username)
    result = await session.execute(query)
    user_uuid, status = result.all()[0]
    if status is False:
        return JSONResponse(content={"message": "user is not confirmed"}, status_code=HTTPStatus.FORBIDDEN)

    sqmt = insert(post).values(
        title=title,
        username=author_username,
        post_text=text,
        user_uuid=user_uuid,
        post_uuid=str(uuid4()),
    )

    await session.execute(sqmt)
    await session.commit()
    return JSONResponse(content={"status": "done"}, status_code=HTTPStatus.CREATED)


@router.get("/post")
async def get_post(title: str, username: str, session: AsyncSession = Depends(get_async_session)):
    query = select(post).where(post.c.title == title and post.c.username == username)
    user_info = await session.execute(query)
    result = user_info.all()[0]
    data = {
        "title": result[1],
        "author_username": result[2],
        "text": result[3],
        "post_uuid": result[5],
        "reactions": [] if result[6] is None else result[6],
    }
    return JSONResponse(content=data, status_code=HTTPStatus.OK)
