import uvicorn
from fastapi import FastAPI

from posts.router import router as posts_router
from users.router import router as users_router
from reactions.router import router as reactions_router
from leaderboard.router import router as leaderboard_router

app = FastAPI(
    title="API for Social Network"
)

app.include_router(users_router)

app.include_router(posts_router)

app.include_router(reactions_router)

app.include_router(leaderboard_router)

if __name__ == "__main__":
    uvicorn.run(app)
