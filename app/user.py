import datetime
from flask.ext.restful import abort, fields, marshal
from app import Resource, api, request, db, models
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
    inserted_id = user.id
    db.session.commit()
    return inserted_id

class LoginRegister(Resource):
    def get(self):
        email = request.authorization.username
        password = request.authorization.password
        print email,password
        user = User.query.filter_by(email=email).first()
        if not user: abort(404,message='user not found')
        if user.verify_password(password):
            op = marshal(user, data)
            return {
                       'code': 200,
                       'data': op
                   }, 200

        else:
            abort(401)

    def post(self):
        auth_header = request.authorization
        email = auth_header.username
        password = auth_header.password
        user_json = request.get_json()

        if not auth_header or not user_json:
            abort(400)

        if models.is_user_unique(email, user_json['phone']):
            id = add_user_to_db(email, password, user_json)
            return {'id':id},200
        else:
            abort(400,message='user already exists')

    def put(self):
        pass


api.add_resource(LoginRegister, '/login')
