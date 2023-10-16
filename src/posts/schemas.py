from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    author_username: str
    post_text: str


class PostDelete(BaseModel):
    title: str
    username: str
    password: str
