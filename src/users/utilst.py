from http import HTTPStatus
from smtplib import SMTP

from fastapi.responses import JSONResponse
from motor.core import AgnosticDatabase

from src.config import EMAIL_SEND_LOGIN, EMAIL_SEND_PASS


class EmailCfg:
    @classmethod
    async def send_email(cls, uuid: str, email: str):
        server = SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user=EMAIL_SEND_LOGIN, password=EMAIL_SEND_PASS)
        subject = "Verification message"

        text = (
            f"Your verification code is:\n"
            f"{uuid}\n"
            f"Please, send POST request to /users/user/verify\n"
            f"Dont forget add json with username and code in request"
        )

        server.sendmail(
            from_addr="apiinterface166@gmail.com",
            to_addrs=email,
            msg=f"Subject: {subject}\n{text}",
        )
        server.quit()


class DeleteCfg:
    @classmethod
    async def check_pass(cls, username: str, password: str, session: AgnosticDatabase):
        correct_pass = await session["user"].find_one(
            {"username": username}, {"password": 1}
        )
        if correct_pass is None:
            return JSONResponse(
                content={"error": f"user with username {username} does not exists"},
                status_code=HTTPStatus.BAD_REQUEST,
            )

        if password != correct_pass["password"]:
            return JSONResponse(
                content={"error": "incorrect password"},
                status_code=HTTPStatus.BAD_REQUEST,
            )
        return True
