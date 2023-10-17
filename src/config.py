import os

from dotenv import load_dotenv
from polog import config as cfg
from polog import file_writer

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

EMAIL_SEND_LOGIN = os.environ.get("EMAIL_SEND_LOGIN")
EMAIL_SEND_PASS = os.environ.get("EMAIL_SEND_PASS")

cfg.add_handlers(file_writer("logfile.log"))
