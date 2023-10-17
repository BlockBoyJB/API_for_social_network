from http import HTTPStatus

import matplotlib.pyplot as plt
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.users.models import User

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("/graph")
async def graph_leaderboard(session: AsyncSession = Depends(get_async_session)):
    query = select(User.username, User.total_reactions).order_by(
        desc(User.total_reactions)
    )
    db_info = await session.execute(query)

    usernames = []
    total_reactions = []
    for username, num_reactions in db_info.fetchall():
        usernames.append(username)
        total_reactions.append(num_reactions)

    plt.bar(usernames, total_reactions)
    plt.title("Leadeboard")
    plt.xlabel("Users")
    plt.ylabel("Total reactions")

    plt.savefig("static/leaderboard.png")

    return FileResponse(path="static/leaderboard.png")


@router.get("/list")
async def list_leaderboard(
    sort: str, session: AsyncSession = Depends(get_async_session)
):
    if sort == "desc":
        query = select(User.username, User.total_reactions).order_by(
            desc(User.total_reactions)
        )

    else:
        query = select(User.username, User.total_reactions).order_by(
            User.total_reactions
        )

    db_info = await session.execute(query)

    users = db_info.fetchall()
    result = []
    for i in range(len(users)):
        result.append(
            {
                "place": i + 1,
                "username": users[i][0],
                "total_reactions": users[i][1],
            }
        )

    return JSONResponse(
        content={
            f"leaderboard sort type {'asc' if sort == 'asc' else 'desc'}": result,
        },
        status_code=HTTPStatus.OK,
    )
