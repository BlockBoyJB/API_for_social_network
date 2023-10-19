from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from polog import log
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.posts.models import Post
from src.posts.schemas import PostCreate, PostDelete
from src.reactions.models import Reaction
from src.reactions.utils import get_all_reactions
from src.users.utilst import DeleteCfg

router = APIRouter(prefix="/posts", tags=["Post"])


@router.post("/post/create")
@log
async def add_post(new_post: PostCreate):
    session = await get_async_session()
    post_uuid = str(uuid4())
    user_info = await session["user"].find_one(
        {"username": new_post.username}, {"is_verified": 1, "user_uuid": 2}
    )
    if user_info is None:
        return JSONResponse(
            content={
                "error": f"user with username {new_post.username} does not exists"
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )

    if user_info["is_verified"] is False:
        return JSONResponse(
            content={"error": "user is not confirmed"},
            status_code=HTTPStatus.FORBIDDEN,
        )

    data = new_post.dict()
    data["post_uuid"] = post_uuid
    data["user_uuid"] = user_info["user_uuid"]
    data["reactions"] = []

    await session["post"].insert_one(data)

    return JSONResponse(
        content={
            "title": new_post.title,
            "username": new_post.username,
            "text": new_post.post_text,
        },
        status_code=HTTPStatus.CREATED,
    )


@router.get("/post")
@log
async def get_post(title: str, username: str):
    session = await get_async_session()
    all_posts = []

    db_info = (
        await session["post"]
        .find({"title": title, "username": username})
        .to_list(length=None)
    )
    if len(db_info) == 0:
        return JSONResponse(
            content={
                "error": f"posts with title '{title}' or author username {username} does not exists"
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )

    for post in db_info:
        del post["_id"]
        del post["user_uuid"]
        all_posts.append(post)

    return JSONResponse(
        content={f"post with title '{title}' user {username}": all_posts},
        status_code=HTTPStatus.OK,
    )


@router.delete("/post/delete")
@log
async def delete_post(post_info: PostDelete):
    session = await get_async_session()
    result = await DeleteCfg.check_pass(
        username=post_info.username,
        password=post_info.password,
        session=session,
    )
    if result is True:
        post = await session["post"].find_one(
            {"post_uuid": post_info.post_uuid}, {"post_uuid": 1}
        )
        if post is None:
            return JSONResponse(
                content={
                    "error": f"post with uuid '{post_info.post_uuid}' does not exists"
                },
                status_code=HTTPStatus.BAD_REQUEST,
            )

        await session["post"].delete_one({"post_uuid": post["post_uuid"]})

        return JSONResponse(
            content={"message": "post deleted successfully"},
            status_code=HTTPStatus.ACCEPTED,
        )
    return result
