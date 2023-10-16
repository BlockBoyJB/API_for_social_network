from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


class UserVerify(BaseModel):
    username: str
    verification_code: str


class UserDelete(BaseModel):
    username: str
    password: str
