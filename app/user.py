import datetime

import flask
from flask.ext.restful import abort, fields, marshal,Resource
from app import api, request, db, mail, Message, models
from models import User

data = {
    'id': fields.Integer,
    'name': fields.String,
    'city': fields.String,
    'phone': fields.String,
    'photo': fields.String,
    'sosCount': fields.Integer
}


def add_user_to_db(email, password, user_json):
    name = user_json['name']
    city = user_json['city']
    phone = user_json['phone']
    photo = user_json['photo']
    verified = False
    reg_time = datetime.datetime.now()
    user = User(email=email, password=password, name=name, city=city, phone=phone,
                photo=photo, isVerified=verified, reg_time=reg_time)
    db.session.add(user)
    db.session.flush()
    db.session.refresh(user)
    db.session.commit()
    return user


def send_verification_mail(user):
    token = user.generate_auth_token(expiration=60 * 60 * 24 * 2)
    print token
    link = 'http://127.0.0.1:5000/confirm/' + token
    message = Message(subject='SOS Confirmation Mail', recipients=[user.email],
                      sender='socialmurali@gmail.com')
    message.body = "please click on the link {0}".format(link)
    mail.send(message)
    print 'sent to ' + user.email
    return 'Sent'


class LoginRegister(Resource):
    def get(self):
        email = request.authorization.username
        password = request.authorization.password
        print email, password
        user = User.query.filter_by(email=email).first()
        if not user: abort(404, message='user not found')
        if models.is_user_verified(email):
            if user.verify_password(password):
                op = marshal(user, data)
                return {
                           'code': 200,
                           'data': op
                       }, 200
            else:
                abort(401)
        else:
            abort(403, message='Verify your account')

    def post(self):
        auth_header = request.authorization
        email = auth_header.username
        password = auth_header.password
        user_json = request.get_json()

        if not auth_header or not user_json:
            abort(400)

        if models.is_user_unique(email, user_json['phone']):
            added_user = add_user_to_db(email, password, user_json)
            id = added_user.id
            # send_verification_mail(added_user)
            op = {'id': id}
            return {'data': op}, 200
        else:
            abort(400, message='user already exists')

    def put(self):
        pass


class EmailVerification(Resource):
    def get(self, token):
        if User.confirm(token):
            msg = '<h1>You are now a verified user.</h1>'
            response = flask.make_response(msg)
            response.headers['content-type'] = 'text/html'
            return response
        else:
            msg = '<h1>Token expired.</h1>'
            response = flask.make_response(msg)
            response.headers['content-type'] = 'text/html'
            return response


class ContactRequest(Resource):
    def post(self):
        contact_json = request.get_json()
        contact_csv = contact_json['list']
        contact_list = contact_csv.split(',')
        response = []
        for phone in contact_list:
            print phone
            user = User.query.filter_by(phone=phone).first()
            if user:
                op = marshal(user, data)
                response.append(op)
        return {'data':response}


api.add_resource(LoginRegister, '/login')
api.add_resource(EmailVerification, '/confirm/<string:token>')
api.add_resource(ContactRequest, '/contacts')
