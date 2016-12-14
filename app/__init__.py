from flask.ext.restful import Api,Resource
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
api = Api(app)
import config

db = SQLAlchemy(app)
from models import User,Group
db.create_all()
import views
import user