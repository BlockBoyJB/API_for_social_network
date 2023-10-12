from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    author_username: str
    post_text: str
