import uvicorn
from fastapi import FastAPI

from posts.router import router as posts_router
from users.router import router as users_router

app = FastAPI(
    title="API for Social Network"
)

app.include_router(users_router)

app.include_router(posts_router)

if __name__ == "__main__":
    uvicorn.run(app)
