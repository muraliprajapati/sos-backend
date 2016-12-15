from app.user import data
from models import Group, User
from flask.ext.restful import abort, fields, marshal, Resource
from app import api, request, db, mail, Message

group_response = {
    'id': fields.Integer,
    'name': fields.String,
    'photo': fields.String,
    'adminId': fields.Integer,
    'adminName': fields.String,
    'userlist': fields.String
}


class CreateGroup(Resource):
    def post(self):
        # send Notification to every member
        group_json = request.get_json()
        if not group_json: abort(400)
        group_name = group_json['name']
        group_photo = group_json['photo']
        group_admin = group_json['adminId']
        group_users_list = group_json['userlist']
        admin = User.query.filter_by(id=group_admin).first()
        group = Group(name=group_name, photo=group_photo, adminId=group_admin,
                      adminName=admin.name, userlist=group_users_list)
        db.session.add(group)
        db.session.flush()
        db.session.refresh(group)
        db.session.commit()
        member_id_list = group_users_list.split(',')


        members = []
        for id in member_id_list:
            print id
            user = User.query.filter_by(id=id).first()
            if user:
                group.g_users.append(user)
                op = marshal(user, data)
                members.append(op)
        db.session.commit()
        op1 = marshal(group, group_response)

        return {
            'code': 200,
            'description': 'OK',
            'group': op1,
            'member': members
        }



api.add_resource(CreateGroup, '/group')
