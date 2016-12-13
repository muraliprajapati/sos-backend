from app import app, db
from models import User


@app.route('/')
def index():

    murali = User(name='mp', email='mup@g.com', phone='2000123654',
                  city='surat', password='asdf', reg_time=1515151,
                  fcm_token='dadasdw', photo='adadad', isVerified=True)
    db.session.add(murali)
    db.session.commit()
    return 'Hello SOS'
