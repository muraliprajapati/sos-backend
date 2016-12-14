from flask_sqlalchemy import SQLAlchemy
from app import app
import os
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SECRET_KEY'] = 'Bruce Wayne is the JOKER'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'socialmurali@gmail.com'
app.config['MAIL_PASSWORD'] = 'shree@301'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True