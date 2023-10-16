from pydantic import BaseModel


class ReactionCreate(BaseModel):
    title: str
    username: str
    reaction: str

