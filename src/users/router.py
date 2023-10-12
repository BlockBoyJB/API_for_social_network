from uuid import uuid4
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from http import HTTPStatus

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.users.schemas import UserCreate
from src.users.models import user


router = APIRouter(
    prefix="/users",
    tags=["User"]
)


@router.post("/user/create")
async def add_user(new_user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    username, first_name, last_name, email = new_user.username, new_user.first_name, new_user.last_name, new_user.email
    user_uuid: str = str(uuid4())

    sqmt = insert(user).values(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        user_uuid=user_uuid,
    )
    await session.execute(sqmt)
    await session.commit()
    return {"status": "done"}  # TODO: прописать возвращение важных пунктов


@router.get("/user")
async def get_user(username: str, session: AsyncSession = Depends(get_async_session)):
    query = select(user).where(user.c.username == username)
    user_info = await session.execute(query)
    result = user_info.all()[0]
    data = {
        "username": result[1],
        "first_name": result[2],
        "last_name": result[3],
        "email": result[4],
        "total_reactions": result[5],
        "user_status": result[6],
        "user_uuid": result[7],
    }
    return JSONResponse(content=data, status_code=HTTPStatus.OK)
