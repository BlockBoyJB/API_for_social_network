from email_validate import validate
from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

    @classmethod
    async def validate_username(cls, username: str):
        correct_symbols = "abcdefghijklmnopqrstuvwxyz0123456789_"
        if len(username) < 3 or len(username) > 15:
            return False
        if len(username.split()) == 1 and username[0] == "@":
            for sym in username[1:]:
                if sym not in correct_symbols:
                    return False
            return True
        return False

    @classmethod
    async def validate_email(cls, email: str):
        result = validate(
            email_address=email,
            check_format=True,
            check_blacklist=True,
            check_dns=True,
            dns_timeout=10,
            check_smtp=True,
            smtp_debug=False,
        )
        return result


class UserVerify(BaseModel):
    username: str
    verification_code: str


class UserDelete(BaseModel):
    username: str
    password: str
