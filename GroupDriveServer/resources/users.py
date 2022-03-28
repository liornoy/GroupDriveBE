from flask_restful import Resource

class onLogin(Resource):
    def post(self):
        print("onLogin")

class onEditUser(Resource):
    def post(self, user_id):
        print("onEditUser")
