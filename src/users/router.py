from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from polog import log
from sqlalchemy import delete, desc, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.posts.models import Post
from src.reactions.models import Reaction
from src.reactions.utils import get_all_reactions
from src.users.models import User, UserVerifyingCode
from src.users.schemas import UserCreate, UserDelete, UserVerify
from src.users.utilst import EmailCfg

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/user/create")
@log
async def add_user(new_user: UserCreate):
    session = await get_async_session()
    user_uuid: str = str(uuid4())

    if await new_user.validate_username(new_user.username) is False:
        return JSONResponse(
            content={
                "error": "entered username is incorrect. Enter another one. "
                "Username can consist only of lowercase Latin characters and numbers, and also have the _ "
                "symbol. The username must necessarily start with @. Maximum allowed length is 15 characters, "
                "minimun - 3"
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )

    if await new_user.validate_email(new_user.email) is False:
        return JSONResponse(
            content={
                "error": f"current email {new_user.email} is incorrect. Enter another one"
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )

    if await session["user"].find_one({"username": new_user.username}):
        return JSONResponse(
            content={"error": "current username is busy. Please, enter another one"},
            status_code=HTTPStatus.BAD_REQUEST,
        )

    if await session["user"].find_one({"email": new_user.email}):
        return JSONResponse(
            content={
                "error": "current email adress is busy. Please, enter another one"
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )

    data = new_user.dict()

    data["user_uuid"] = user_uuid
    data["is_verified"] = False
    data["putted_reactions"] = 0
    data["received_reactions"] = 0

    await session["user"].insert_one(data)

    verification_uuid = str(uuid4())
    await session["user_verification_code"].insert_one(
        {
            "username": new_user.username,
            "verification_code": verification_uuid,
        }
    )

    await EmailCfg.send_email(uuid=verification_uuid, email=new_user.email)

    return JSONResponse(
        content={
            "username": new_user.username,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "user_uuid": user_uuid,
            "status": "unconfirmed",
            "message": "check_email",
        },
        status_code=HTTPStatus.CREATED,
    )


@router.get("/user")
@log
async def get_user(username: str):
    session = await get_async_session()
    user: dict = await session["user"].find_one({"username": username})
    if user:
        del user["_id"]
        del user["password"]
        return JSONResponse(content=user, status_code=HTTPStatus.OK)

    return JSONResponse(
        content={"error": f"user with username {username} does not exists"},
        status_code=HTTPStatus.BAD_REQUEST,
    )


@router.post("/user/verify")
@log
async def verify_user(user_info: UserVerify):
    session = await get_async_session()
    correct_code = await session["user_verification_code"].find_one(
        {"username": user_info.username}, {"verification_code": 1}
    )
    if correct_code is None:
        return JSONResponse(
            content={
                "error": f"user with username {user_info.username} does not exists or user is already verified"
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )

    if user_info.verification_code != correct_code["verification_code"]:
        return JSONResponse(
            content={"error": "Current verification code is incorrect"},
            status_code=HTTPStatus.UNAUTHORIZED,
        )

    await session["user_verification_code"].delete_one({"username": user_info.username})
    await session["user"].update_one(
        {"username": user_info.username}, {"$set": {"is_verified": True}}
    )
    return JSONResponse(
        content={
            "message": f"user with username {user_info.username} successfully confirmed"
        },
        status_code=HTTPStatus.OK,
    )


@router.get("/user/posts")
@log
async def get_user_posts(
    username: str, sort: str, session: AsyncSession = Depends(get_async_session)
):
    if sort == "desc":
        query = (
            select(Post)
            .where(Post.username == username)
            .order_by(desc(Post.post_reactions))
        )

    else:
        query = (
            select(Post).where(Post.username == username).order_by(Post.post_reactions)
        )

    db_info = await session.execute(query)

    posts = db_info.all()

    result = []
    for post in posts:
        curr_post: Post = post[0]

        query = select(Reaction.reaction).where(
            Reaction.post_uuid == curr_post.post_uuid
        )

        db_info = await session.execute(query)

        curr_reactions = await get_all_reactions(db_info.fetchall())

        result.append(
            {
                "title": curr_post.title,
                "author_username": curr_post.username,
                "post_uuid": curr_post.post_uuid,
                "text": curr_post.post_text,
                "reactions": curr_reactions,
            }
        )

    return JSONResponse(
        content={
            f"posts {username}. Sort type {'desc' if sort == 'desc' else 'asc'}": result
        },
        status_code=HTTPStatus.OK,
    )


@router.delete("/user/delete")
@log
async def delete_user(user_info: UserDelete):
    session = await get_async_session()
    correct_pass = await session["user"].find_one(
        {"username": user_info.username}, {"password": 1}
    )
    if correct_pass is None:
        return JSONResponse(
            content={
                "error": f"user with username {user_info.username} does not exists"
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )

    if user_info.password != correct_pass["password"]:
        return JSONResponse(
            content={"error": "user password is incorrect"},
            status_code=HTTPStatus.BAD_REQUEST,
        )

    await session["user"].delete_one({"username": user_info.username})

    return JSONResponse(
        content={"message": "user successfully delete"},
        status_code=HTTPStatus.ACCEPTED,
    )