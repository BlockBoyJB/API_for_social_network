from pydantic import BaseModel


class ReactionCreate(BaseModel):
    post_uuid: str
    username: str
    reaction: str
