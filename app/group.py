from app import push_notification
from response import user_response, group_response
from models import Group, User
from flask.ext.restful import abort, marshal, Resource
from app import api, request, db


class CreateGroup(Resource):
    def post(self):
        # send Notification to every member
        group_json = request.get_json()
        if not group_json: abort(400)
        group_name = group_json['name']
        group_photo = group_json['photo']
        group_admin = group_json['adminId']
        group_users_list = group_json['userlist']
        group_users_list = group_users_list + "," + str(group_admin)
        member_id_list = group_users_list.split(',')
        member_id_list = map(int,member_id_list)
        if not member_id_list: abort(400)
        # delimiter = ','
        # group_users_list = delimiter.join(member_id_list)
        admin = User.query.filter_by(id=group_admin).first()
        group = Group(name=group_name, photo='xyzabc', adminId=group_admin,
                      adminName=admin.name, userlist=group_users_list)
        db.session.add(group)
        db.session.flush()
        db.session.refresh(group)
        db.session.commit()

        members = []
        for id in member_id_list:
            print id
            user = User.query.filter_by(id=id).first()
            if user:
                group.g_users.append(user)
                if user.id != group_admin:
                    push_notification.send_group_subscription_message(user.fcm_token,group.id)
                op = marshal(user, user_response)
                members.append(op)
        db.session.commit()
        op1 = marshal(group, group_response)

        return {
            'code': 200,
            'description': 'OK',
            'group': op1,
            'member': members
        }


class EditGroup(Resource):
    def put(self, id):
        # send notification to new added and removed members
        group = Group.query.filter_by(id=id).first()
        group_json = request.get_json()
        if not group_json: abort(400)
        group.name = group_json['name']
        group.photo = group_json['photo']
        group.adminId = group_json['adminId']
        group.userlist = group_json['userlist']
        member_id_list = group_json['userlist'].split(',')
        member_id_list = map(int, member_id_list)

        if not member_id_list: abort(400)
        db.session.commit()

        old_members = group.g_users
        removed_members = []
        members = []
        for u in old_members:
            # print u.name
            if u.id not in member_id_list:
                print u.id
                group.g_users.remove(u)
                removed_members.append(u)
        db.session.commit()
        for u in removed_members:
            print u.name

        for uid in member_id_list:
            print uid

            user = User.query.filter_by(id=uid).first()
            if user and user not in old_members:
                group.g_users.append(user)
            op = marshal(user, user_response)
            members.append(op)
        db.session.commit()
        op1 = marshal(group, group_response)

        return {
            'code': 200,
            'description': 'OK',
            'group': op1,
            'member': members
        }

    def get(self, id):
        group = Group.query.filter_by(id = id).first()
        group_members = group.g_users
        op1 = marshal(group,group_response)
        members = []
        for user in group_members:
            if user:
                op = marshal(user, user_response)
                members.append(op)
        return {
            'code': 200,
            'description': 'OK',
            'group': op1,
            'member': members
        }


api.add_resource(CreateGroup, '/group')
api.add_resource(EditGroup, '/group/<int:id>')
