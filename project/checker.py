from email_validate import validate
# взято из: https://docs-python.ru/packages/modul-validate-email-python/


def check_email(email):
    result = validate(
        email_address=email,
        check_format=True,
        check_blacklist=True,
        check_dns=True,
        dns_timeout=10,
        check_smtp=True,  # поставил True для более точной проверки
        smtp_debug=False)
    return result


"""
В следующих версиях здесь будет добавлена рассылка писем с кодом подтверждения. 
"""


def check_username(username: str):
    correct_symbols = "abcdefghijklmnopqrstuvwxyz0123456789_"
    if len(username.split()) == 1 and username[0] == "@" and username[1] != "_":
        for sym in username[1:]:
            if sym not in correct_symbols:
                return False
        return True
    return False
