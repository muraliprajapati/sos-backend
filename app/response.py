from flask.ext.restful import fields

user_response = {
    'id': fields.Integer,
    'name': fields.String,
    'city': fields.String,
    'phone': fields.String,
    'photo': fields.String,
    'sosCount': fields.Integer
}

group_response = {
    'id': fields.Integer,
    'name': fields.String,
    'photo': fields.String,
    'adminId': fields.Integer,
    'adminName': fields.String,
    'userlist': fields.String
}
