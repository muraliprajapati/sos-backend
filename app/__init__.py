import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

import config



db = SQLAlchemy(app)

from models import User,Group
db.create_all()
import views