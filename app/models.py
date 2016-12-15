from app import db, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

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
    reg_time = db.Column(db.DateTime, nullable=False)
    fcm_token = db.Column(db.Text, nullable=True, default='abc')
    sosCount = db.Column(db.Integer, nullable=True, default=0)

    groups = db.relationship('Group', secondary='group_user',
                             backref=db.backref('g_users', lazy='dynamic'),
                             lazy='dynamic')

    def verify_password(self, password_hash):
        return password_hash == self.password

    def generate_auth_token(self, expiration=None):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def confirm (token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt=None)
        except SignatureExpired:
            return TokenStatus.EXPIRED
        except BadSignature:
            return TokenStatus.INVALID
        req_user = User.query.filter_by(id = data['id']).first_or_404()
        req_id = req_user.id
        if data['id'] == req_id:
            req_user.isVerified = True
            db.session.add(req_user)
            db.session.commit()
            return True
        else:
            return False


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    adminId = db.Column(db.Integer, nullable=False,unique=False)
    adminName = db.Column(db.String,nullable=False)
    name = db.Column(db.String(64), nullable=False)
    photo = db.Column(db.String, nullable=True)
    userlist = db.Column(db.String,nullable=False)


class TokenStatus:
    INVALID = 0
    EXPIRED = 1


def is_user_unique(email, phone):
    user = User.query.filter((User.email == email) | (User.phone == phone)).first()
    if not user:
        return True
    else:
        return False


def is_user_verified(email):
    user = User.query.filter_by(email = email).first()
    return user.isVerified
