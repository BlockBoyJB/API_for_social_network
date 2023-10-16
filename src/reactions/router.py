from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from http import HTTPStatus

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from polog import log

from src.reactions.schemas import ReactionCreate
from src.posts.models import Post
from src.users.models import User
from src.reactions.models import Reaction

router = APIRouter(
    prefix="/posts/reactions",
    tags=["Reaction"]
)


@router.post("/reaction")
@log
async def add_reaction(new_reaction: ReactionCreate, session: AsyncSession = Depends(get_async_session)):
    query = select(Post.post_uuid).where(
        Post.username == new_reaction.username, Post.title == new_reaction.title
    )
    db_info = await session.execute(query)

    post = db_info.fetchone()
    if post is None:
        return JSONResponse(content={
            "error": f"post with title {new_reaction.title} or username {new_reaction.username} does not exists"
        }, status_code=HTTPStatus.BAD_REQUEST)

    post_uuid: list = post[0]

    stmt = update(User).where(User.username == new_reaction.username).values(
        total_reactions=User.total_reactions + 1
    )
    await session.execute(stmt)
    await session.commit()

    stmt = update(Post).where(
        Post.title == new_reaction.title, Post.username == new_reaction.username
    ).values(
        post_reactions=Post.post_reactions + 1
    )
    await session.execute(stmt)
    await session.commit()

    stmt = insert(Reaction).values(
        reaction=new_reaction.reaction,
        post_uuid=post_uuid,
    )
    await session.execute(stmt)
    await session.commit()

    return HTTPStatus.CREATED
