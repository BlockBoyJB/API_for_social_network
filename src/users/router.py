from uuid import uuid4
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from http import HTTPStatus

from polog import log

from sqlalchemy import select, insert, update, delete, func, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.posts.models import Post

from src.users.schemas import UserCreate, UserVerify
from src.users.models import User, UserVerifyingCode
from src.users.utilst import send_email

router = APIRouter(
    prefix="/users",
    tags=["User"]
)


@router.post("/user/create")
@log
async def add_user(new_user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    user_uuid: str = str(uuid4())

    try:

        sqmt = insert(User).values(
            username=new_user.username,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            email=new_user.email,
            user_uuid=user_uuid,
        )
        await session.execute(sqmt)
        await session.commit()

    except IntegrityError:
        return JSONResponse(content={
            "message": "current username or email is busy. Please, enter another one"
        }, status_code=HTTPStatus.BAD_REQUEST)

    sqmt = insert(UserVerifyingCode).values(
        username=new_user.username,
        verifying_uuid=user_uuid,
    )
    await session.execute(sqmt)
    await session.commit()

    # Warning! This function does not work async, so it may slow down the work add_user
    send_email(uuid=user_uuid, email=new_user.email)

    return JSONResponse(content={
        "username": new_user.username,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "user_uuid": user_uuid,
        "status": "unconfirmed",
        "message": "check email",
    }, status_code=HTTPStatus.CREATED)


@router.get("/user")
@log
async def get_user(username: str, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.username == username)
    user_info = await session.execute(query)
    result: User = user_info.fetchone()[0]
    data = {
        "username": result.username,
        "first_name": result.first_name,
        "last_name": result.last_name,
        "email": result.email,
        "total_reactions": result.total_reactions,
        "user_status": "unconfirmed" if result.is_verified is False else "confirmed",
        "user_uuid": result.user_uuid,
    }
    return JSONResponse(content=data, status_code=HTTPStatus.OK)


@router.post("/user/verify")
@log
async def verify_user(user_info: UserVerify, session: AsyncSession = Depends(get_async_session)):
    query = select(UserVerifyingCode.verifying_uuid).where(UserVerifyingCode.username == user_info.username)
    db_info = await session.execute(query)
    correct_uuid = db_info.fetchone()[0]

    if correct_uuid == user_info.verification_code:
        stmt = update(User).where(UserVerifyingCode.username == user_info.username).values(
            is_verified=True
        )
        await session.execute(stmt)
        await session.commit()

        query = delete(UserVerifyingCode).where(UserVerifyingCode.username == user_info.username)
        await session.execute(query)
        await session.commit()

        return JSONResponse(content={
            "message": f"user with username {user_info.username} successfully confirmed",
        }, status_code=HTTPStatus.OK)

    return JSONResponse(content={
        "message": "verification code is incorrect",
    }, status_code=HTTPStatus.UNAUTHORIZED)


@router.get("/user/posts")
@log
async def get_user_posts(username: str, sort: str, session: AsyncSession = Depends(get_async_session)):
    if sort == "asc":
        query = select(Post).where(Post.username == username).order_by(desc(func.cardinality(Post.reactions)))

    else:
        query = select(Post).where(Post.username == username).order_by(func.cardinality(Post.reactions))

    db_info = await session.execute(query)

    posts = db_info.all()
    result = []
    for post in posts:
        curr_post: Post = post[0]
        result.append({
            "title": curr_post.title,
            "author_username": curr_post.username,
            "post_uuid": curr_post.post_uuid,
            "text": curr_post.post_text,
            "reactions": curr_post.reactions,
        })

    return JSONResponse(content={f"posts {username}": result}, status_code=HTTPStatus.OK)
