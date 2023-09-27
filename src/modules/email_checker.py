"""
The logic of sending a confirmation email to the user
"""
# you need to create a file at the specified path, which will contain the login and password from gmail,
# from which confirmation emails will be sent
from src.modules.verification_email import LOGIN, PASSWORD
from src.database.db import add_verification_db
import uuid
import smtplib


def _generate_code(username):
    code = str(uuid.uuid4())
    add_verification_db(username=username, code=code)
    return code


def send_verification_msg(email, username):
    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()
    server.login(user=LOGIN, password=PASSWORD)

    subject = "Verification message"

    text = (f"Your verification code is:\n"
            f"{_generate_code(username=username)}\n"
            f"Please, send POST request to /users/user/verify\n"
            f"Dont forget add json with username and code in request")

    server.sendmail(from_addr=LOGIN, to_addrs=email, msg=f'Subject: {subject}\n{text}')
    server.quit()
