from flask import Flask

app = Flask(__name__)

from src.modules import classes
from src.modules import checker
from src.modules import email_checker
from src.modules import new_routes
