from verification_email import login, password
import uuid
import smtplib


class EmailVerification:
    def __init__(self):
        self.__verification_codes: dict = {}

    def __generate_code(self, username):
        code = uuid.uuid4()
        self.__verification_codes[username] = str(code)
        return code

    def get_codes(self):
        return self.__verification_codes

    def send_verification_msg(self, email, username):
        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()
        server.login(user=login, password=password)

        subject = "Verification message"

        text = (f"Your verification code is:\n"
                f"{self.__generate_code(username=username)}\n"
                f"Please, send POST request to /users/{username}/verify\n"
                f"Dont forget add json with code in request")

        server.sendmail(from_addr=login, to_addrs=email, msg=f'Subject: {subject}\n{text}')
        server.quit()
