from verification_email import login, password
import uuid
import smtplib


class EmailVerification:
    def __init__(self):
        self.__verification_codes: list = []

    def generate_code(self):
        code = uuid.uuid4()
        self.__verification_codes.append(code)
        return code

    def send_verification_msg(self, email):
        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()
        server.login(user=login, password=password)

        subject = "Verification message"

        text = (f"Your verification code is:\n"
                f"{self.generate_code()}\n"
                f"Please, send request to /users/verify/'ENTER YOUR VERIFICATION CODE'")

        server.sendmail(from_addr=login, to_addrs=email, msg=f'Subject: {subject}\n{text}')
        server.quit()
