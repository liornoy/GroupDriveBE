from flask_restful import Resource
from flask import Response
from database.models import User, Trip, UserLiveGPSCoordinate 

class onLogin(Resource):
    def post(self):
        print("onLogin")

class onEditUser(Resource):
    def post(self, user_id):
        print("onEditUser")

class onShowUsers(Resource):
    def get(self):
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)