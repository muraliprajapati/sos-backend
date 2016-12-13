from app import db

group_user = db.Table('group_user',
                      db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                      db.Column('group_id', db.Integer, db.ForeignKey('groups.id')))


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(10), nullable=False, unique=True)
    city = db.Column(db.String(64), nullable=False)
    photo = db.Column(db.String, nullable=True)
    isVerified = db.Column(db.Boolean, default=False, nullable=False)
    reg_time = db.Column(db.BigInteger, nullable=False)
    fcm_token = db.Column(db.Text)

    groups = db.relationship('Group', secondary='group_user',
                             backref=db.backref('g_users', lazy='dynamic'),
                             lazy='dynamic')


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    photo = db.Column(db.String, nullable=True)

