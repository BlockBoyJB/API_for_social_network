from smtplib import SMTP

from email_validate import validate

from src.config import EMAIL_SEND_LOGIN, EMAIL_SEND_PASS


class EmailCfg:

    @classmethod
    def send_email(cls, uuid: str, email: str):
        server = SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user=EMAIL_SEND_LOGIN, password=EMAIL_SEND_PASS)
        subject = "Verification message"

        text = (f"Your verification code is:\n"
                f"{uuid}\n"
                f"Please, send POST request to /users/user/verify\n"
                f"Dont forget add json with username and code in request")

        server.sendmail(from_addr="apiinterface166@gmail.com", to_addrs=email, msg=f'Subject: {subject}\n{text}')
        server.quit()

    @classmethod
    async def check_email(cls, email: str):
        result = validate(
            email_address=email,
            check_format=True,
            check_blacklist=True,
            check_dns=True,
            dns_timeout=10,
            check_smtp=True,
            smtp_debug=False)
        return result
