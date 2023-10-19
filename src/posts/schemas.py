from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    username: str
    post_text: str


class PostDelete(BaseModel):
    username: str
    post_uuid: str
    password: str
