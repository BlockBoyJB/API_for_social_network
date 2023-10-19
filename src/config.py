import os

from dotenv import load_dotenv
from polog import config as cfg
from polog import file_writer

load_dotenv()

EMAIL_SEND_LOGIN = os.environ.get("EMAIL_SEND_LOGIN")
EMAIL_SEND_PASS = os.environ.get("EMAIL_SEND_PASS")

cfg.add_handlers(file_writer("logfile.log"))
