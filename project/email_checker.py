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
