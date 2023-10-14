from fastapi import APIRouter, Depends

from http import HTTPStatus

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from polog import log

from src.reactions.schemas import ReactionCreate
from src.posts.models import Post
from src.users.models import User


router = APIRouter(
    prefix="/posts/reactions",
    tags=["Reaction"]
)


@router.post("/reaction")
@log
async def add_reaction(new_reaction: ReactionCreate, session: AsyncSession = Depends(get_async_session)):

    query = select(Post.reactions).where(
        Post.username == new_reaction.username and Post.title == new_reaction.title
    )
    db_info = await session.execute(query)
    post_reactions: list = db_info.fetchone()[0]
    if post_reactions is None:
        post_reactions = []

    post_reactions.append(new_reaction.reaction)

    stmt = update(User).where(User.username == new_reaction.username).values(
        total_reactions=User.total_reactions + 1
    )
    await session.execute(stmt)
    await session.commit()

    stmt = update(Post).where(
        Post.username == new_reaction.username and Post.title == new_reaction.title
    ).values(
        reactions=post_reactions,
    )
    await session.execute(stmt)
    await session.commit()

    return HTTPStatus.CREATED
