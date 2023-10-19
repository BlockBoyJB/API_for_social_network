from http import HTTPStatus

import matplotlib.pyplot as plt
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from polog import log

from src.database import get_async_session
from src.users.models import User

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("/graph")
@log
async def graph_leaderboard():
    session = await get_async_session()
    usernames = []
    total_reactions = []
    users = (
        await session["user"]
        .find({}, {"username": 1, "total_reactions": 2})
        .sort("total_reactions", -1)
        .to_list(length=None)
    )
    for user in users:
        del user["_id"]
        usernames.append(user["username"])
        total_reactions.append(user["total_reactions"])

    plt.bar(usernames, total_reactions)
    plt.title("Leadeboard")
    plt.xlabel("Users")
    plt.ylabel("Total reactions")

    plt.savefig("static/leaderboard.png")

    return FileResponse(path="static/leaderboard.png")


@router.get("/list")
@log
async def list_leaderboard(sort: str):
    session = await get_async_session()
    users = (
        await session["user"]
        .find({}, {"username": 1, "total_reactions": 2})
        .sort("total_reactions", (-1 if sort == "desc" else 1))
        .to_list(length=None)
    )
    all_users = []
    for user in users:
        del user["_id"]
        all_users.append(user)

    return JSONResponse(
        content={
            f"leaderboard sort type {'desc' if sort == 'desc' else 'asc'}": all_users
        },
        status_code=HTTPStatus.OK,
    )
