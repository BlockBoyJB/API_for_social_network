from flask import Flask

app = Flask(__name__)


from src.modules import routes
from src.modules import classes
from src.modules import email_checker