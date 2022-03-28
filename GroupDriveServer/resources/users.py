from flask import Resource, request

class onLogin(Resource):
    def post(self):
        print("onLogin")

class onEditUser(Resource):
    def post(self, user_id):
        print("onEditUser")
