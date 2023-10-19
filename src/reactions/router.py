from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from polog import log
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.posts.models import Post
from src.reactions.models import Reaction
from src.reactions.schemas import ReactionCreate
from src.users.models import User

router = APIRouter(prefix="/posts/reactions", tags=["Reaction"])


@router.post("/reaction")
@log
async def add_reaction(new_reaction: ReactionCreate):
    session = await get_async_session()
    await session["post"].update_one(
        {"post_uuid": new_reaction.post_uuid},
        {"$push": {"reactions": new_reaction.reaction}}
    )
    await session["user"].update_one(
        {"username": new_reaction.username},
        {"$inc": {"total_reactions": 1}}
    )
    return HTTPStatus.CREATED
