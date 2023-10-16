from uuid import uuid4
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from http import HTTPStatus

from polog import log

from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.posts.schemas import PostCreate, PostDelete
from src.reactions.models import Reaction
from src.reactions.utils import get_all_reactions
from src.users.models import User
from src.posts.models import Post

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


@router.post("/post/create")
@log
async def add_post(new_post: PostCreate, session: AsyncSession = Depends(get_async_session)):
    query = select(User.user_uuid, User.is_verified).where(User.username == new_post.author_username)
    db_info = await session.execute(query)
    result = db_info.all()
    if len(result) == 0:
        return JSONResponse(content={
            "error": f"user with username {new_post.author_username} does not exists"
        }, status_code=HTTPStatus.BAD_REQUEST)
    user_uuid, status = result[0]

    if status is False:
        return JSONResponse(content={"message": "user is not confirmed"}, status_code=HTTPStatus.FORBIDDEN)

    query = select(Post.title).where(Post.title == new_post.title, Post.username == new_post.author_username)
    result = await session.execute(query)

    if result.fetchone() is not None:
        return JSONResponse(content={
            "message": f"post with title {new_post.title} is already exists in user posts. Please, enter another one"
        }, status_code=HTTPStatus.BAD_REQUEST)

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
    query = select(Post).where(Post.title == title, Post.username == username)
    user_info = await session.execute(query)

    post = user_info.fetchone()
    if post is None:
        return JSONResponse(content={
            "error": f"post with title {title} or username {username} does not exists"
        }, status_code=HTTPStatus.BAD_REQUEST)
    result: Post = post[0]

    query = select(Reaction.reaction).where(Reaction.post_uuid == result.post_uuid)

    db_info = await session.execute(query)

    reactions = await get_all_reactions(db_info.fetchall())

    data = {
        "title": result.title,
        "author_username": result.username,
        "text": result.post_text,
        "post_uuid": result.post_uuid,
        "reactions": reactions,
    }
    return JSONResponse(content=data, status_code=HTTPStatus.OK)


@router.delete("/post/delete")
@log
async def delete_post(post_info: PostDelete, session: AsyncSession = Depends(get_async_session)):
    query = select(User.password).where(User.username == post_info.username)
    db_info = await session.execute(query)
    password = db_info.fetchone()
    if password is None:
        return JSONResponse(content={
            "error": f"Post with author username {post_info.username} does not exists"
        }, status_code=HTTPStatus.BAD_REQUEST)

    if post_info.password != password[0]:
        return JSONResponse(content={"error": "password is incorrect"}, status_code=HTTPStatus.BAD_REQUEST)

    query = delete(Post).where(Post.title == post_info.title, Post.username == post_info.username)
    await session.execute(query)
    await session.commit()

    return JSONResponse(content={"message": "post successfully delete"}, status_code=HTTPStatus.ACCEPTED)
