from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str


class UserVerify(BaseModel):
    username: str
    verification_code: str
